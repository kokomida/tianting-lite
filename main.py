from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from contextlib import contextmanager

app = FastAPI(title="FastAPI Todo", version="1.0.0")

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@contextmanager
def get_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE
            )
        """)
        conn.commit()
        yield conn
    finally:
        conn.close()

db_connection = None

def init_db():
    global db_connection
    db_connection = sqlite3.connect(":memory:", check_same_thread=False)
    db_connection.row_factory = sqlite3.Row
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    db_connection.commit()

init_db()

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@app.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (todo.title, todo.description, todo.completed)
    )
    db_connection.commit()
    todo_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    return dict(row)

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return dict(row)

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.dict(exclude_unset=True)
    if update_data:
        set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
        values = list(update_data.values()) + [todo_id]
        cursor.execute(f"UPDATE todos SET {set_clause} WHERE id = ?", values)
        db_connection.commit()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    return dict(row)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db_connection.commit()
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
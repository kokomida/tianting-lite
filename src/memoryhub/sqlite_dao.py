"""
SQLite Data Access Object for MemoryHub Core Layer persistence
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List


class MemoryHubDAO:
    """Data Access Object for SQLite persistence of MemoryHub data"""

    def __init__(self, db_path: str = "memoryhub/data/memory.db"):
        """
        Initialize SQLite DAO

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        # Ensure directory exists (skip for in-memory database)
        if db_path != ":memory:":
            db_dir = os.path.dirname(db_path)
            if db_dir:  # Only create if directory path is not empty
                os.makedirs(db_dir, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    tags TEXT NOT NULL,  -- JSON array
                    context_path TEXT,
                    layer TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    recalled_count INTEGER DEFAULT 0,
                    updated_at TEXT
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS windows (
                    window_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    pid INTEGER,
                    state TEXT DEFAULT 'OPEN',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks (task_id)
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS review_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    agent TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    score REAL NOT NULL,
                    comments TEXT,
                    ts TEXT NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks (task_id)
                )
            """
            )

            # Create indices for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_layer ON tasks(layer)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_windows_task_id ON windows(task_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_review_logs_task_id ON review_logs(task_id)"
            )

            conn.commit()

    def store_memory(self, memory_record: Dict[str, Any]) -> bool:
        """
        Store a memory record in the tasks table

        Args:
            memory_record: Memory record dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Use memory ID as task_id for Core layer memories
                task_id = memory_record["id"]

                conn.execute(
                    """
                    INSERT OR REPLACE INTO tasks 
                    (task_id, content, tags, context_path, layer, created_at, recalled_count, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        task_id,
                        memory_record["content"],
                        json.dumps(memory_record["tags"]),
                        memory_record.get("context_path", ""),
                        memory_record["layer"],
                        memory_record["created_at"],
                        memory_record.get("recalled_count", 0),
                        datetime.now().isoformat(),
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing memory to SQLite: {e}")
            return False

    def load_memories(self, layer: str = "core") -> List[Dict[str, Any]]:
        """
        Load memories from specified layer

        Args:
            layer: Memory layer to load from

        Returns:
            List of memory records
        """
        memories = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    SELECT task_id, content, tags, context_path, layer, 
                           created_at, recalled_count, updated_at
                    FROM tasks 
                    WHERE layer = ?
                    ORDER BY created_at DESC
                """,
                    (layer,),
                )

                for row in cursor:
                    memory = {
                        "id": row["task_id"],
                        "content": row["content"],
                        "tags": json.loads(row["tags"]),
                        "context_path": row["context_path"],
                        "layer": row["layer"],
                        "created_at": row["created_at"],
                        "recalled_count": row["recalled_count"],
                        "updated_at": row["updated_at"],
                    }
                    memories.append(memory)
        except Exception as e:
            print(f"Error loading memories from SQLite: {e}")

        return memories

    def search_memories(
        self, query: str, layer: str = "core", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search memories in SQLite database

        Args:
            query: Search query
            layer: Layer to search in
            limit: Maximum results to return

        Returns:
            List of matching memory records
        """
        memories = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row

                # Simple text search in content and tags
                cursor = conn.execute(
                    """
                    SELECT task_id, content, tags, context_path, layer, 
                           created_at, recalled_count, updated_at
                    FROM tasks 
                    WHERE layer = ? AND (
                        content LIKE ? OR 
                        tags LIKE ? OR 
                        context_path LIKE ?
                    )
                    ORDER BY created_at DESC
                    LIMIT ?
                """,
                    (layer, f"%{query}%", f"%{query}%", f"%{query}%", limit),
                )

                for row in cursor:
                    memory = {
                        "id": row["task_id"],
                        "content": row["content"],
                        "tags": json.loads(row["tags"]),
                        "context_path": row["context_path"],
                        "layer": row["layer"],
                        "created_at": row["created_at"],
                        "recalled_count": row["recalled_count"],
                        "updated_at": row["updated_at"],
                    }
                    memories.append(memory)
        except Exception as e:
            print(f"Error searching memories in SQLite: {e}")

        return memories

    def update_recall_count(self, memory_id: str) -> bool:
        """
        Increment recall count for a memory

        Args:
            memory_id: Memory ID to update

        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    UPDATE tasks 
                    SET recalled_count = recalled_count + 1,
                        updated_at = ?
                    WHERE task_id = ?
                """,
                    (datetime.now().isoformat(), memory_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating recall count: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics

        Returns:
            Dictionary with statistics
        """
        stats = {"core_memory_count": 0, "total_recalls": 0, "tables": []}

        try:
            with sqlite3.connect(self.db_path) as conn:
                # Count memories by layer
                cursor = conn.execute(
                    "SELECT layer, COUNT(*) FROM tasks GROUP BY layer"
                )
                for layer, count in cursor:
                    stats[f"{layer}_memory_count"] = count

                # Total recalls
                cursor = conn.execute("SELECT SUM(recalled_count) FROM tasks")
                total_recalls = cursor.fetchone()[0]
                stats["total_recalls"] = total_recalls or 0

                # Table names
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                stats["tables"] = [row[0] for row in cursor]

        except Exception as e:
            print(f"Error getting stats: {e}")

        return stats

    def close(self):
        """Close database connection (no-op for sqlite3 context manager usage)"""
        pass

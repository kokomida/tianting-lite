"""
简化的天庭API服务器
避免复杂的导入问题
"""

import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="天庭API服务",
    description="天庭系统RESTful API服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok", 
        "service": "api",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "天庭API服务器",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/test")
async def test():
    """测试接口"""
    return {"message": "API服务正常运行"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
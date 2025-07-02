"""
Core服务FastAPI应用
为RequirementAnalyzer提供HTTP接口
"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requirement_analyzer import RequirementAnalyzer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="天庭Core服务",
    description="需求分析核心服务",
    version="1.0.0"
)

# 添加CORS中间件
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化分析器
analyzer = RequirementAnalyzer()

class RequirementRequest(BaseModel):
    text: str

class RequirementResponse(BaseModel):
    success: bool
    data: dict = None
    error: str = None

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "core"}

@app.post("/analyze", response_model=RequirementResponse)
async def analyze_requirement(request: RequirementRequest):
    """分析需求"""
    try:
        result = await analyzer.analyze_requirement(request.text)
        return RequirementResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"需求分析失败: {str(e)}")
        return RequirementResponse(success=False, error=str(e))

@app.get("/test")
async def test_analyzer():
    """测试分析器功能"""
    try:
        result = await analyzer.validate_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
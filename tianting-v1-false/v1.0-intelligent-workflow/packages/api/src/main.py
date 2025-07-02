"""
天庭API服务器主入口
FastAPI应用配置和启动
"""

import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

import structlog
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from config import settings
from database import database_manager
from middleware import (
    ErrorHandlerMiddleware,
    LoggingMiddleware,
    RateLimitMiddleware,
    RequestTracingMiddleware
)
from routers import health_router

# 配置结构化日志
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format=settings.log_format
)

logger = structlog.get_logger(__name__)

# Prometheus指标
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    logger.info("🚀 启动天庭API服务器...", version=settings.app_version)
    
    # 启动时初始化
    try:
        # 初始化数据库连接
        logger.info("🔌 正在连接数据库...")
        await database_manager.connect()
        logger.info("✅ 数据库连接成功")
        
        # 创建上传目录
        import os
        os.makedirs(settings.upload_dir, exist_ok=True)
        logger.info("📁 文件上传目录已准备", path=settings.upload_dir)
        
        logger.info("✅ 天庭API服务器启动完成", host=settings.host, port=settings.port)
        
    except Exception as e:
        logger.error("❌ 服务器启动失败", error=str(e))
        raise
    
    yield
    
    # 关闭时清理
    try:
        logger.info("🛑 正在关闭天庭API服务器...")
        await database_manager.disconnect()
        logger.info("✅ 数据库连接已关闭")
        logger.info("✅ 天庭API服务器已安全关闭")
    except Exception as e:
        logger.error("❌ 服务器关闭时出错", error=str(e))


def create_app() -> FastAPI:
    """创建FastAPI应用实例"""
    app = FastAPI(
        title=settings.app_name,
        description="天庭系统RESTful API - 为「言出法随」的开发体验而生",
        version=settings.app_version,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        openapi_url="/openapi.json" if settings.is_development else None,
        lifespan=lifespan
    )
    
    # 添加中间件（注意顺序很重要）
    
    # 1. 信任的主机中间件
    if not settings.is_development:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.allowed_hosts
        )
    
    # 2. CORS中间件
    app.add_middleware(
        CORSMiddleware,
        **settings.get_cors_config()
    )
    
    # 3. 请求追踪中间件
    app.add_middleware(RequestTracingMiddleware)
    
    # 4. 限流中间件
    app.add_middleware(
        RateLimitMiddleware,
        calls=settings.rate_limit_per_minute,
        period=60
    )
    
    # 5. 日志中间件
    app.add_middleware(LoggingMiddleware)
    
    # 6. 错误处理中间件
    app.add_middleware(ErrorHandlerMiddleware)
    
    # 指标收集中间件
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # 记录指标
        duration = time.time() - start_time
        endpoint = request.url.path
        method = request.method
        status_code = str(response.status_code)
        
        request_count.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code
        ).inc()
        
        request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
        
        return response
    
    # 注册路由
    app.include_router(health_router, prefix="/health", tags=["健康检查"])
    
    # 指标端点
    if settings.enable_metrics:
        @app.get(settings.metrics_path, include_in_schema=False)
        async def metrics():
            return Response(
                generate_latest(),
                media_type=CONTENT_TYPE_LATEST
            )
    
    # 根路径
    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "message": "天庭API服务器",
            "version": settings.app_version,
            "timestamp": datetime.utcnow().isoformat(),
            "docs_url": "/docs" if settings.is_development else None
        }
    
    return app


# 创建应用实例
app = create_app()


def main():
    """主函数 - 开发服务器入口"""
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
        access_log=settings.debug,
        workers=1 if settings.is_development else settings.workers
    )


if __name__ == "__main__":
    main()
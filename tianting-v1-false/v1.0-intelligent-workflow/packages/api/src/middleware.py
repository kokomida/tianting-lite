"""
天庭API中间件集合
包含日志、错误处理、限流、请求追踪等中间件
"""

import json
import time
import uuid
from typing import Callable, Dict, Any

import redis.asyncio as redis
import structlog
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from config import settings

logger = structlog.get_logger(__name__)


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """请求追踪中间件 - 为每个请求生成唯一ID"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # 添加到响应头
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件 - 记录请求和响应信息"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # 获取客户端信息
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        request_id = getattr(request.state, "request_id", "unknown")
        
        # 记录请求开始
        logger.info(
            "请求开始",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_ip=client_ip,
            user_agent=user_agent
        )
        
        try:
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录请求完成
            logger.info(
                "请求完成",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                process_time_ms=round(process_time * 1000, 2)
            )
            
            # 添加处理时间到响应头
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # 记录错误
            process_time = time.time() - start_time
            logger.error(
                "请求异常",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                error=str(e),
                process_time_ms=round(process_time * 1000, 2)
            )
            raise


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """错误处理中间件 - 统一处理异常和错误响应"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except HTTPException as e:
            # HTTP异常，返回标准格式
            return await self._create_error_response(
                request=request,
                status_code=e.status_code,
                error_code=f"HTTP_{e.status_code}",
                message=e.detail
            )
        except ValueError as e:
            # 参数错误
            return await self._create_error_response(
                request=request,
                status_code=400,
                error_code="INVALID_PARAMETER",
                message=f"参数错误: {str(e)}"
            )
        except ConnectionError as e:
            # 连接错误（数据库、Redis等）
            return await self._create_error_response(
                request=request,
                status_code=503,
                error_code="SERVICE_UNAVAILABLE",
                message="服务暂时不可用，请稍后重试"
            )
        except Exception as e:
            # 未知异常
            logger.exception(
                "未处理的异常",
                request_id=getattr(request.state, "request_id", "unknown"),
                error=str(e)
            )
            
            return await self._create_error_response(
                request=request,
                status_code=500,
                error_code="INTERNAL_SERVER_ERROR",
                message="服务器内部错误" if not settings.debug else str(e)
            )
    
    async def _create_error_response(
        self,
        request: Request,
        status_code: int,
        error_code: str,
        message: str,
        details: Any = None
    ) -> JSONResponse:
        """创建标准错误响应"""
        request_id = getattr(request.state, "request_id", None)
        
        error_response = {
            "success": False,
            "data": None,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
            "request_id": request_id,
            "error": {
                "code": error_code,
                "details": details
            }
        }
        
        return JSONResponse(
            status_code=status_code,
            content=error_response,
            headers={"X-Request-ID": request_id} if request_id else {}
        )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """限流中间件 - 基于Redis的API限流"""
    
    def __init__(self, app: ASGIApp, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.redis_client = None
    
    async def _get_redis_client(self):
        """获取Redis客户端（懒加载）"""
        if self.redis_client is None:
            try:
                self.redis_client = redis.from_url(
                    settings.redis_url,
                    max_connections=settings.redis_max_connections,
                    decode_responses=True
                )
                # 测试连接
                await self.redis_client.ping()
            except Exception as e:
                logger.warning("Redis连接失败，限流功能将被禁用", error=str(e))
                self.redis_client = False
        
        return self.redis_client if self.redis_client is not False else None
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 获取客户端标识
        client_id = self._get_client_id(request)
        
        # 检查限流
        if await self._is_rate_limited(client_id):
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "data": None,
                    "message": f"请求过于频繁，每{self.period}秒最多{self.calls}次请求",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
                    "request_id": getattr(request.state, "request_id", None),
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "details": {
                            "limit": self.calls,
                            "period_seconds": self.period
                        }
                    }
                },
                headers={"Retry-After": str(self.period)}
            )
        
        return await call_next(request)
    
    def _get_client_id(self, request: Request) -> str:
        """获取客户端标识"""
        # 优先使用用户ID（如果已认证）
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"
        
        # 使用客户端IP
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    async def _is_rate_limited(self, client_id: str) -> bool:
        """检查是否超过限流"""
        redis_client = await self._get_redis_client()
        if not redis_client:
            # Redis不可用，不进行限流
            return False
        
        try:
            # 使用滑动窗口算法
            key = f"rate_limit:{client_id}"
            current_time = int(time.time())
            window_start = current_time - self.period
            
            # 使用管道提高性能
            pipe = redis_client.pipeline()
            
            # 删除过期的记录
            pipe.zremrangebyscore(key, 0, window_start)
            
            # 添加当前请求
            pipe.zadd(key, {str(current_time): current_time})
            
            # 计算当前窗口内的请求数
            pipe.zcard(key)
            
            # 设置过期时间
            pipe.expire(key, self.period)
            
            results = await pipe.execute()
            
            # 检查是否超过限制
            current_requests = results[2]  # zcard的结果
            return current_requests > self.calls
            
        except Exception as e:
            logger.error("限流检查失败", client_id=client_id, error=str(e))
            # 出错时不限流，避免影响正常请求
            return False


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """安全头中间件 - 添加安全相关的HTTP头"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # 添加安全头
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        
        # 只在HTTPS环境下添加HSTS头
        if request.url.scheme == "https":
            security_headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        for header, value in security_headers.items():
            response.headers[header] = value
        
        return response


class CompressionMiddleware(BaseHTTPMiddleware):
    """压缩中间件 - 为大响应启用gzip压缩"""
    
    def __init__(self, app: ASGIApp, minimum_size: int = 1024):
        super().__init__(app)
        self.minimum_size = minimum_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # 检查是否需要压缩
        if (
            "gzip" in request.headers.get("accept-encoding", "")
            and response.headers.get("content-length")
            and int(response.headers["content-length"]) >= self.minimum_size
            and "content-encoding" not in response.headers
        ):
            # 这里可以添加gzip压缩逻辑
            # FastAPI默认支持，这里主要是示例
            pass
        
        return response
"""
健康检查和监控端点
提供系统状态、性能指标等信息
"""

import time
from typing import Dict, Any

import redis.asyncio as redis
import structlog
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import sys
sys.path.append('..')
from config import settings
from database import database_manager
sys.path.append('../schemas')
from base import create_success_response, HealthCheckResponse

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get(
    "/",
    response_model=dict,
    summary="基础健康检查",
    description="检查API服务器基础状态"
)
async def health_check(request: Request) -> dict:
    """基础健康检查端点"""
    request_id = getattr(request.state, "request_id", None)
    
    return create_success_response(
        data={
            "status": "healthy",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
            "version": settings.app_version,
            "environment": settings.environment
        },
        message="API服务器运行正常",
        request_id=request_id
    )


@router.get(
    "/detailed",
    response_model=dict,
    summary="详细健康检查",
    description="检查所有系统组件的详细状态"
)
async def detailed_health_check(request: Request) -> dict:
    """详细健康检查端点"""
    request_id = getattr(request.state, "request_id", None)
    
    # 检查各个组件状态
    database_health = await _check_database_health()
    redis_health = await _check_redis_health()
    external_services = await _check_external_services()
    
    # 确定整体状态
    overall_status = "healthy"
    if (
        database_health["status"] != "connected" or
        redis_health["status"] != "connected"
    ):
        overall_status = "unhealthy"
    
    health_data = {
        "status": overall_status,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "version": settings.app_version,
        "database": database_health,
        "redis": redis_health,
        "external_services": external_services
    }
    
    return create_success_response(
        data=health_data,
        message=f"系统状态: {overall_status}",
        request_id=request_id
    )


@router.get(
    "/readiness",
    summary="就绪检查",
    description="检查服务是否已准备好接收请求"
)
async def readiness_check(request: Request) -> JSONResponse:
    """就绪检查端点 - 用于Kubernetes等容器编排"""
    request_id = getattr(request.state, "request_id", None)
    
    # 检查关键依赖
    database_ready = await _is_database_ready()
    
    if database_ready:
        return JSONResponse(
            status_code=200,
            content=create_success_response(
                data={"ready": True},
                message="服务已就绪",
                request_id=request_id
            )
        )
    else:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "data": {"ready": False},
                "message": "服务未就绪",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
                "request_id": request_id
            }
        )


@router.get(
    "/liveness",
    summary="存活检查",
    description="检查服务是否存活"
)
async def liveness_check(request: Request) -> dict:
    """存活检查端点 - 用于Kubernetes等容器编排"""
    request_id = getattr(request.state, "request_id", None)
    
    return create_success_response(
        data={"alive": True},
        message="服务存活",
        request_id=request_id
    )


@router.get(
    "/metrics",
    summary="性能指标",
    description="获取服务性能指标"
)
async def metrics_check(request: Request) -> dict:
    """性能指标端点"""
    request_id = getattr(request.state, "request_id", None)
    
    # 收集性能指标
    metrics = await _collect_metrics()
    
    return create_success_response(
        data=metrics,
        message="性能指标收集完成",
        request_id=request_id
    )


# 内部辅助函数

async def _check_database_health() -> Dict[str, Any]:
    """检查数据库健康状态"""
    try:
        health_info = await database_manager.health_check()
        return health_info
    except Exception as e:
        logger.error("数据库健康检查失败", error=str(e))
        return {
            "status": "error",
            "latency_ms": None,
            "error": str(e)
        }


async def _check_redis_health() -> Dict[str, Any]:
    """检查Redis健康状态"""
    try:
        start_time = time.time()
        
        redis_client = redis.from_url(
            settings.redis_url,
            socket_timeout=settings.health_check_timeout,
            decode_responses=True
        )
        
        # 执行ping命令
        await redis_client.ping()
        
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        await redis_client.close()
        
        return {
            "status": "connected",
            "latency_ms": latency_ms
        }
    except Exception as e:
        logger.error("Redis健康检查失败", error=str(e))
        return {
            "status": "disconnected",
            "latency_ms": None,
            "error": str(e)
        }


async def _check_external_services() -> Dict[str, str]:
    """检查外部服务状态"""
    services = {}
    
    # 检查Core服务
    try:
        import httpx
        async with httpx.AsyncClient(timeout=settings.health_check_timeout) as client:
            response = await client.get(f"{settings.core_service_url}/health")
            if response.status_code == 200:
                services["core_service"] = "available"
            else:
                services["core_service"] = "unavailable"
    except Exception as e:
        logger.debug("Core服务检查失败", error=str(e))
        services["core_service"] = "unavailable"
    
    return services


async def _is_database_ready() -> bool:
    """检查数据库是否就绪"""
    try:
        if not database_manager.is_connected:
            return False
        
        health_info = await database_manager.health_check()
        return health_info["status"] == "connected"
    except Exception:
        return False


async def _collect_metrics() -> Dict[str, Any]:
    """收集性能指标"""
    import psutil
    import os
    
    try:
        # 系统指标
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 进程指标
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        process_cpu = process.cpu_percent()
        
        return {
            "system": {
                "cpu_percent": cpu_percent,
                "memory_total_mb": round(memory.total / 1024 / 1024, 2),
                "memory_used_mb": round(memory.used / 1024 / 1024, 2),
                "memory_percent": memory.percent,
                "disk_total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
                "disk_used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
                "disk_percent": round(disk.used / disk.total * 100, 2)
            },
            "process": {
                "pid": os.getpid(),
                "cpu_percent": process_cpu,
                "memory_rss_mb": round(process_memory.rss / 1024 / 1024, 2),
                "memory_vms_mb": round(process_memory.vms / 1024 / 1024, 2),
                "threads": process.num_threads()
            },
            "application": {
                "version": settings.app_version,
                "environment": settings.environment,
                "uptime_seconds": time.time() - psutil.boot_time()
            }
        }
    except Exception as e:
        logger.error("性能指标收集失败", error=str(e))
        return {
            "error": "指标收集失败",
            "details": str(e)
        }
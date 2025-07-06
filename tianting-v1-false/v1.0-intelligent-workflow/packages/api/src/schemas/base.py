"""
Pydantic基础Schema定义
严格遵循shared包API类型定义
"""

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field, ConfigDict

# 泛型类型变量
T = TypeVar('T')


class BaseSchema(BaseModel):
    """基础Schema类"""
    
    model_config = ConfigDict(
        # 启用属性验证
        validate_assignment=True,
        # 允许额外字段（向前兼容）
        extra='ignore',
        # 使用枚举值而不是名称
        use_enum_values=True,
        # 启用JSON编码器
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    )


class ApiResponse(BaseSchema, Generic[T]):
    """标准API响应格式"""
    
    success: bool = Field(description="请求是否成功")
    data: Optional[T] = Field(default=None, description="响应数据")
    message: str = Field(default="操作成功", description="响应消息")
    timestamp: str = Field(description="响应时间戳")
    request_id: Optional[str] = Field(default=None, description="请求ID")


class ErrorResponse(BaseSchema):
    """错误响应格式"""
    
    success: bool = Field(default=False, description="请求是否成功")
    data: None = Field(default=None, description="响应数据")
    message: str = Field(description="错误消息")
    timestamp: str = Field(description="响应时间戳")
    request_id: Optional[str] = Field(default=None, description="请求ID")
    error: "ErrorDetail" = Field(description="错误详情")


class ErrorDetail(BaseSchema):
    """错误详情"""
    
    code: str = Field(description="错误代码")
    details: Optional[Any] = Field(default=None, description="错误详细信息")


class PaginatedResponse(BaseSchema, Generic[T]):
    """分页响应格式"""
    
    success: bool = Field(default=True, description="请求是否成功")
    data: List[T] = Field(description="响应数据列表")
    message: str = Field(default="查询成功", description="响应消息")
    timestamp: str = Field(description="响应时间戳")
    request_id: Optional[str] = Field(default=None, description="请求ID")
    pagination: "PaginationInfo" = Field(description="分页信息")


class PaginationInfo(BaseSchema):
    """分页信息"""
    
    total_count: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页大小")
    total_pages: int = Field(description="总页数")


class HealthCheckData(BaseSchema):
    """健康检查数据"""
    
    status: str = Field(description="服务状态", pattern="^(healthy|unhealthy)$")
    timestamp: str = Field(description="检查时间")
    version: str = Field(description="服务版本")
    database: "DatabaseHealth" = Field(description="数据库状态")
    redis: "RedisHealth" = Field(description="Redis状态")
    external_services: dict[str, str] = Field(description="外部服务状态")


class DatabaseHealth(BaseSchema):
    """数据库健康状态"""
    
    status: str = Field(description="连接状态", pattern="^(connected|disconnected)$")
    latency_ms: Optional[float] = Field(default=None, description="延迟（毫秒）")


class RedisHealth(BaseSchema):
    """Redis健康状态"""
    
    status: str = Field(description="连接状态", pattern="^(connected|disconnected)$")
    latency_ms: Optional[float] = Field(default=None, description="延迟（毫秒）")


class HealthCheckResponse(ApiResponse[HealthCheckData]):
    """健康检查响应"""
    pass


# 通用请求Schema
class PaginationParams(BaseSchema):
    """分页参数"""
    
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")
    
    @property
    def offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.page_size


class SortParams(BaseSchema):
    """排序参数"""
    
    sort_by: Optional[str] = Field(default=None, description="排序字段")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$", description="排序方向")


class SearchParams(BaseSchema):
    """搜索参数"""
    
    keyword: Optional[str] = Field(default=None, description="搜索关键词")
    filters: Optional[dict] = Field(default=None, description="筛选条件")


# 响应工具函数
def create_success_response(
    data: T = None,
    message: str = "操作成功",
    request_id: Optional[str] = None
) -> dict:
    """创建成功响应"""
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id
    }


def create_error_response(
    message: str,
    error_code: str,
    details: Any = None,
    request_id: Optional[str] = None
) -> dict:
    """创建错误响应"""
    return {
        "success": False,
        "data": None,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "error": {
            "code": error_code,
            "details": details
        }
    }


def create_paginated_response(
    data: List[T],
    total_count: int,
    page: int,
    page_size: int,
    message: str = "查询成功",
    request_id: Optional[str] = None
) -> dict:
    """创建分页响应"""
    total_pages = (total_count + page_size - 1) // page_size
    
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "pagination": {
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    }
"""
天庭API服务器配置管理
支持环境变量和配置文件
"""

import os
from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置设置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # 应用基础配置
    app_name: str = Field(default="天庭API服务", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    environment: str = Field(default="development", description="运行环境")

    # 服务器配置
    host: str = Field(default="0.0.0.0", description="服务器地址")
    port: int = Field(default=8002, description="服务器端口")
    workers: int = Field(default=1, description="工作进程数")

    # 数据库配置
    database_url: str = Field(
        default="postgresql+asyncpg://tianting_dev:dev_password@localhost:5432/tianting_api_dev",
        description="数据库连接URL"
    )
    database_pool_size: int = Field(default=20, description="数据库连接池大小")
    database_max_overflow: int = Field(default=0, description="数据库连接池最大溢出")
    database_pool_timeout: int = Field(default=30, description="数据库连接超时时间")
    database_pool_recycle: int = Field(default=3600, description="数据库连接回收时间")

    # Redis配置
    redis_url: str = Field(
        default="redis://localhost:6379/2",
        description="Redis连接URL"
    )
    redis_password: Optional[str] = Field(default=None, description="Redis密码")
    redis_max_connections: int = Field(default=20, description="Redis最大连接数")

    # JWT配置
    jwt_secret_key: str = Field(
        default="dev_jwt_secret_for_api_package_change_in_production",
        description="JWT密钥"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT算法")
    jwt_expire_minutes: int = Field(default=1440, description="JWT过期时间（分钟）")

    # CORS配置
    cors_origins: List[str] = Field(
        default=["http://localhost:3001", "http://localhost:3000"],
        description="允许的跨域源"
    )
    cors_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="允许的HTTP方法"
    )
    cors_headers: List[str] = Field(
        default=["*"],
        description="允许的请求头"
    )

    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="日志格式"
    )
    log_file: Optional[str] = Field(default=None, description="日志文件路径")

    # API限流配置
    rate_limit_per_minute: int = Field(default=100, description="每分钟请求限制")
    rate_limit_per_hour: int = Field(default=1000, description="每小时请求限制")

    # 外部服务配置
    core_service_url: str = Field(
        default="http://localhost:8001",
        description="Core服务URL"
    )
    core_service_timeout: int = Field(default=30, description="Core服务超时时间")

    # 文件存储配置
    upload_dir: str = Field(default="./uploads", description="文件上传目录")
    max_file_size: int = Field(default=10 * 1024 * 1024, description="最大文件大小（字节）")

    # 安全配置
    allowed_hosts: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="允许的主机名"
    )
    trusted_proxies: List[str] = Field(
        default=["127.0.0.1"],
        description="信任的代理IP"
    )

    # 监控配置
    enable_metrics: bool = Field(default=True, description="启用指标收集")
    metrics_path: str = Field(default="/metrics", description="指标路径")

    # 健康检查配置
    health_check_timeout: int = Field(default=5, description="健康检查超时时间")

    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.environment.lower() in ("development", "dev")

    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.environment.lower() in ("production", "prod")

    @property
    def is_testing(self) -> bool:
        """是否为测试环境"""
        return self.environment.lower() in ("testing", "test")

    @property
    def database_engine_options(self) -> dict:
        """数据库引擎配置选项"""
        return {
            "pool_size": self.database_pool_size,
            "max_overflow": self.database_max_overflow,
            "pool_timeout": self.database_pool_timeout,
            "pool_recycle": self.database_pool_recycle,
            "pool_pre_ping": True,
            "echo": self.debug and self.is_development,
        }

    def get_cors_config(self) -> dict:
        """获取CORS配置"""
        return {
            "allow_origins": self.cors_origins,
            "allow_methods": self.cors_methods,
            "allow_headers": self.cors_headers,
            "allow_credentials": True,
        }


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置（缓存单例）"""
    return Settings()


# 全局配置实例
settings = get_settings()


def create_database_url(
    username: str,
    password: str,
    host: str,
    port: int,
    database: str,
    driver: str = "postgresql+asyncpg"
) -> str:
    """创建数据库连接URL"""
    return f"{driver}://{username}:{password}@{host}:{port}/{database}"


def create_redis_url(
    host: str,
    port: int,
    db: int = 0,
    password: Optional[str] = None
) -> str:
    """创建Redis连接URL"""
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"
"""
天庭API数据库连接和ORM基础
基于SQLAlchemy 2.0异步引擎
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import structlog
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from config import settings

logger = structlog.get_logger(__name__)


class Base(DeclarativeBase):
    """数据库模型基类"""
    pass


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        self._connected = False
    
    async def connect(self) -> None:
        """连接数据库"""
        if self._connected:
            logger.warning("数据库已经连接")
            return
        
        try:
            logger.info("🔌 创建数据库引擎...")
            
            # 创建异步引擎
            self.engine = create_async_engine(
                settings.database_url,
                **settings.database_engine_options
            )
            
            # 创建会话工厂
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True,
                autocommit=False
            )
            
            # 测试连接
            await self._test_connection()
            
            self._connected = True
            logger.info("✅ 数据库连接成功")
            
        except Exception as e:
            logger.error("❌ 数据库连接失败", error=str(e))
            raise
    
    async def disconnect(self) -> None:
        """断开数据库连接"""
        if not self._connected:
            return
        
        try:
            if self.engine:
                await self.engine.dispose()
                logger.info("✅ 数据库连接已关闭")
            
            self.engine = None
            self.session_factory = None
            self._connected = False
            
        except Exception as e:
            logger.error("❌ 关闭数据库连接时出错", error=str(e))
    
    async def _test_connection(self) -> None:
        """测试数据库连接"""
        if not self.engine:
            raise RuntimeError("数据库引擎未初始化")
        
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                result.scalar()
            logger.debug("数据库连接测试成功")
        except Exception as e:
            logger.error("数据库连接测试失败", error=str(e))
            raise
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话（上下文管理器）"""
        if not self._connected or not self.session_factory:
            raise RuntimeError("数据库未连接")
        
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error("数据库会话异常，已回滚", error=str(e))
            raise
        finally:
            await session.close()
    
    async def get_session_simple(self) -> AsyncSession:
        """获取数据库会话（简单方式）"""
        if not self._connected or not self.session_factory:
            raise RuntimeError("数据库未连接")
        
        return self.session_factory()
    
    async def create_tables(self) -> None:
        """创建数据库表"""
        if not self.engine:
            raise RuntimeError("数据库引擎未初始化")
        
        try:
            logger.info("📋 创建数据库表...")
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ 数据库表创建完成")
        except Exception as e:
            logger.error("❌ 创建数据库表失败", error=str(e))
            raise
    
    async def drop_tables(self) -> None:
        """删除数据库表"""
        if not self.engine:
            raise RuntimeError("数据库引擎未初始化")
        
        try:
            logger.warning("⚠️ 删除数据库表...")
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.info("✅ 数据库表删除完成")
        except Exception as e:
            logger.error("❌ 删除数据库表失败", error=str(e))
            raise
    
    async def health_check(self) -> dict:
        """数据库健康检查"""
        if not self._connected:
            return {
                "status": "disconnected",
                "latency_ms": None,
                "error": "数据库未连接"
            }
        
        try:
            import time
            start_time = time.time()
            
            await self._test_connection()
            
            latency_ms = round((time.time() - start_time) * 1000, 2)
            
            return {
                "status": "connected",
                "latency_ms": latency_ms
            }
        except Exception as e:
            return {
                "status": "error",
                "latency_ms": None,
                "error": str(e)
            }
    
    @property
    def is_connected(self) -> bool:
        """检查数据库是否已连接"""
        return self._connected


# 全局数据库管理器实例
database_manager = DatabaseManager()


# 依赖注入函数
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI依赖注入：获取数据库会话
    
    使用方式:
    @app.get("/")
    async def endpoint(db: AsyncSession = Depends(get_db_session)):
        # 使用db执行数据库操作
        pass
    """
    async with database_manager.get_session() as session:
        yield session


async def get_db() -> AsyncSession:
    """
    获取数据库会话（简单方式）
    注意：需要手动管理会话生命周期
    """
    return await database_manager.get_session_simple()


# 数据库操作基类
class BaseRepository:
    """数据库操作基类"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def commit(self) -> None:
        """提交事务"""
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("提交事务失败", error=str(e))
            raise
    
    async def rollback(self) -> None:
        """回滚事务"""
        await self.session.rollback()
    
    async def refresh(self, instance) -> None:
        """刷新实例"""
        await self.session.refresh(instance)
    
    async def close(self) -> None:
        """关闭会话"""
        await self.session.close()


# 数据库初始化函数
async def init_database() -> None:
    """初始化数据库"""
    logger.info("🏗️ 初始化数据库...")
    
    try:
        await database_manager.connect()
        await database_manager.create_tables()
        logger.info("✅ 数据库初始化完成")
    except Exception as e:
        logger.error("❌ 数据库初始化失败", error=str(e))
        raise


# 数据库清理函数
async def cleanup_database() -> None:
    """清理数据库"""
    logger.info("🧹 清理数据库...")
    
    try:
        await database_manager.disconnect()
        logger.info("✅ 数据库清理完成")
    except Exception as e:
        logger.error("❌ 数据库清理失败", error=str(e))
        raise
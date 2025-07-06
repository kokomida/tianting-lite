"""
数据库模型基类
提供通用字段和方法
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """数据库模型基类"""
    
    # 通用字段
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="创建时间"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新时间"
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """从字典更新属性"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        """字符串表示"""
        class_name = self.__class__.__name__
        attrs = []
        
        # 显示主键
        for column in self.__table__.columns:
            if column.primary_key:
                value = getattr(self, column.name, None)
                attrs.append(f"{column.name}={value}")
        
        return f"<{class_name}({', '.join(attrs)})>"
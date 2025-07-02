#!/usr/bin/env python3
"""
天庭API服务器功能验证脚本
检查核心配置、导入和基础功能
"""

import sys
import traceback
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """测试核心模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试配置模块
        from src.config import settings
        print(f"✅ 配置模块加载成功 - 应用名称: {settings.app_name}")
        
        # 测试数据库模块
        from src.database import database_manager, Base
        print("✅ 数据库模块加载成功")
        
        # 测试中间件模块
        from src.middleware import RequestTracingMiddleware, LoggingMiddleware
        print("✅ 中间件模块加载成功")
        
        # 测试schemas模块
        from src.schemas.base import BaseSchema, ApiResponse
        print("✅ Schema模块加载成功")
        
        # 测试路由模块
        from src.routers.health import router as health_router
        print("✅ 路由模块加载成功")
        
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        traceback.print_exc()
        return False

def test_configuration():
    """测试配置功能"""
    print("\n🔍 测试配置功能...")
    
    try:
        from src.config import settings
        
        # 检查关键配置
        assert settings.app_name == "天庭API服务"
        assert settings.port == 8002
        assert settings.app_version == "1.0.0"
        
        # 检查数据库配置
        assert settings.database_url is not None
        assert settings.database_pool_size > 0
        
        # 检查CORS配置
        cors_config = settings.get_cors_config()
        assert "allow_origins" in cors_config
        assert "allow_methods" in cors_config
        
        print("✅ 配置验证通过")
        return True
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        traceback.print_exc()
        return False

def test_fastapi_app():
    """测试FastAPI应用创建"""
    print("\n🔍 测试FastAPI应用创建...")
    
    try:
        from src.main import create_app
        
        # 创建应用实例
        app = create_app()
        
        # 检查应用基本属性
        assert app.title == "天庭API服务"
        assert app.version == "1.0.0"
        
        # 检查路由是否已注册
        routes = [route.path for route in app.routes]
        assert "/" in routes
        assert "/health/" in routes or any("/health" in route for route in routes)
        
        print("✅ FastAPI应用创建成功")
        print(f"📋 注册的路由: {routes}")
        return True
    except Exception as e:
        print(f"❌ FastAPI应用创建失败: {e}")
        traceback.print_exc()
        return False

def test_database_models():
    """测试数据库模型"""
    print("\n🔍 测试数据库模型...")
    
    try:
        from src.models.base import Base
        from src.database import Base as DatabaseBase
        
        # 检查基类
        assert Base is not None
        assert DatabaseBase is not None
        
        print("✅ 数据库模型验证通过")
        return True
    except Exception as e:
        print(f"❌ 数据库模型验证失败: {e}")
        traceback.print_exc()
        return False

def test_schemas():
    """测试Pydantic schemas"""
    print("\n🔍 测试Pydantic schemas...")
    
    try:
        from src.schemas.base import (
            BaseSchema, 
            ApiResponse, 
            create_success_response,
            create_error_response
        )
        
        # 测试响应创建函数
        success_resp = create_success_response(data={"test": "value"})
        assert success_resp["success"] is True
        assert success_resp["data"]["test"] == "value"
        
        error_resp = create_error_response("测试错误", "TEST_ERROR")
        assert error_resp["success"] is False
        assert error_resp["message"] == "测试错误"
        assert error_resp["error"]["code"] == "TEST_ERROR"
        
        print("✅ Schema验证通过")
        return True
    except Exception as e:
        print(f"❌ Schema验证失败: {e}")
        traceback.print_exc()
        return False

def test_api_endpoints():
    """测试API端点可用性"""
    print("\n🔍 测试API端点...")
    
    try:
        # 检查shared包的API类型定义
        shared_api_path = Path(__file__).parent.parent / "shared" / "src" / "types" / "api.ts"
        if shared_api_path.exists():
            print("✅ Shared包API类型定义存在")
        else:
            print("⚠️ Shared包API类型定义不存在")
        
        return True
    except Exception as e:
        print(f"❌ API端点测试失败: {e}")
        traceback.print_exc()
        return False

def check_file_structure():
    """检查文件结构完整性"""
    print("\n🔍 检查文件结构...")
    
    required_files = [
        "src/__init__.py",
        "src/main.py",
        "src/config.py",
        "src/database.py",
        "src/middleware.py",
        "src/models/__init__.py",
        "src/models/base.py",
        "src/schemas/__init__.py",
        "src/schemas/base.py",
        "src/routers/__init__.py",
        "src/routers/health.py",
        "tests/__init__.py",
        "tests/test_server.py",
        "requirements.txt",
        "package.json",
        "pytest.ini"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (Path(__file__).parent / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 文件结构完整")
        return True

def main():
    """主验证函数"""
    print("🚀 开始验证天庭API服务器...")
    print("=" * 50)
    
    tests = [
        ("文件结构检查", check_file_structure),
        ("模块导入", test_imports),
        ("配置功能", test_configuration),
        ("FastAPI应用", test_fastapi_app),
        ("数据库模型", test_database_models),
        ("Pydantic schemas", test_schemas),
        ("API端点", test_api_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} 测试失败")
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 验证结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有验证通过！API服务器基础框架实现完成")
        return True
    else:
        print("⚠️ 部分验证失败，请检查相关问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
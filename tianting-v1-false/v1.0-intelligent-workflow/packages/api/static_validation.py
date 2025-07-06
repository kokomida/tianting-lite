#!/usr/bin/env python3
"""
天庭API服务器静态验证脚本
检查代码结构、语法和文件完整性
"""

import ast
import sys
from pathlib import Path

def validate_python_syntax(file_path):
    """验证Python文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 解析AST检查语法
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, f"语法错误: {e}"
    except Exception as e:
        return False, f"读取错误: {e}"

def check_python_files():
    """检查所有Python文件的语法"""
    print("🔍 检查Python文件语法...")
    
    python_files = [
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
        "tests/test_server.py"
    ]
    
    all_valid = True
    for file_path in python_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            valid, error = validate_python_syntax(full_path)
            if valid:
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path}: {error}")
                all_valid = False
        else:
            print(f"⚠️ {file_path}: 文件不存在")
            all_valid = False
    
    return all_valid

def check_file_completeness():
    """检查文件完整性"""
    print("\n🔍 检查文件完整性...")
    
    required_files = {
        "src/main.py": "FastAPI应用入口",
        "src/config.py": "配置管理",
        "src/database.py": "数据库连接",
        "src/middleware.py": "中间件集合",
        "src/models/base.py": "数据库模型基类",
        "src/schemas/base.py": "Pydantic schemas",
        "src/routers/health.py": "健康检查路由",
        "tests/test_server.py": "服务器测试",
        "requirements.txt": "Python依赖",
        "package.json": "包配置",
        "pytest.ini": "测试配置"
    }
    
    all_complete = True
    for file_path, description in required_files.items():
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path} ({description}) - {size} bytes")
        else:
            print(f"❌ {file_path} ({description}) - 缺失")
            all_complete = False
    
    return all_complete

def check_code_structure():
    """检查代码结构完整性"""
    print("\n🔍 检查代码结构...")
    
    structure_checks = []
    
    # 检查main.py结构
    try:
        main_path = Path(__file__).parent / "src" / "main.py"
        with open(main_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        if "def create_app()" in main_content:
            structure_checks.append("✅ create_app函数存在")
        else:
            structure_checks.append("❌ create_app函数缺失")
        
        if "lifespan" in main_content:
            structure_checks.append("✅ 生命周期管理存在")
        else:
            structure_checks.append("❌ 生命周期管理缺失")
            
        if "CORSMiddleware" in main_content:
            structure_checks.append("✅ CORS中间件配置存在")
        else:
            structure_checks.append("❌ CORS中间件配置缺失")
            
    except Exception as e:
        structure_checks.append(f"❌ main.py检查失败: {e}")
    
    # 检查config.py结构
    try:
        config_path = Path(__file__).parent / "src" / "config.py"
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        if "class Settings" in config_content:
            structure_checks.append("✅ Settings类存在")
        else:
            structure_checks.append("❌ Settings类缺失")
            
        if "get_settings()" in config_content:
            structure_checks.append("✅ get_settings函数存在")
        else:
            structure_checks.append("❌ get_settings函数缺失")
            
    except Exception as e:
        structure_checks.append(f"❌ config.py检查失败: {e}")
    
    # 检查database.py结构
    try:
        db_path = Path(__file__).parent / "src" / "database.py"
        with open(db_path, 'r', encoding='utf-8') as f:
            db_content = f.read()
        
        if "class DatabaseManager" in db_content:
            structure_checks.append("✅ DatabaseManager类存在")
        else:
            structure_checks.append("❌ DatabaseManager类缺失")
            
        if "async def connect" in db_content:
            structure_checks.append("✅ 异步连接方法存在")
        else:
            structure_checks.append("❌ 异步连接方法缺失")
            
    except Exception as e:
        structure_checks.append(f"❌ database.py检查失败: {e}")
    
    for check in structure_checks:
        print(f"  {check}")
    
    return all("✅" in check for check in structure_checks)

def check_requirements():
    """检查requirements.txt内容"""
    print("\n🔍 检查依赖要求...")
    
    try:
        req_path = Path(__file__).parent / "requirements.txt"
        with open(req_path, 'r', encoding='utf-8') as f:
            requirements = f.read()
        
        required_packages = [
            "fastapi",
            "uvicorn", 
            "sqlalchemy",
            "asyncpg",
            "pydantic",
            "structlog",
            "prometheus-client",
            "redis",
            "httpx",
            "pytest"
        ]
        
        missing_packages = []
        for package in required_packages:
            if package.lower() not in requirements.lower():
                missing_packages.append(package)
        
        if not missing_packages:
            print("✅ 所有必需的依赖包都已列出")
            return True
        else:
            print(f"❌ 缺少依赖包: {missing_packages}")
            return False
            
    except Exception as e:
        print(f"❌ requirements.txt检查失败: {e}")
        return False

def check_shared_types():
    """检查shared包类型定义"""
    print("\n🔍 检查shared包类型定义...")
    
    try:
        shared_path = Path(__file__).parent.parent / "shared" / "src" / "types" / "api.ts"
        if shared_path.exists():
            with open(shared_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_types = [
                "ApiResponse",
                "RequirementParseRequest", 
                "RequirementParseResponse",
                "PlanningGenerateRequest",
                "PlanningGenerateResponse",
                "HealthCheckResponse"
            ]
            
            missing_types = []
            for type_name in required_types:
                if type_name not in content:
                    missing_types.append(type_name)
            
            if not missing_types:
                print("✅ 所有必需的API类型都已定义")
                return True
            else:
                print(f"❌ 缺少API类型: {missing_types}")
                return False
        else:
            print("❌ shared包API类型文件不存在")
            return False
            
    except Exception as e:
        print(f"❌ shared包类型检查失败: {e}")
        return False

def performance_check():
    """性能相关检查"""
    print("\n🔍 检查性能相关配置...")
    
    checks = []
    
    # 检查是否有连接池配置
    try:
        config_path = Path(__file__).parent / "src" / "config.py"
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        if "pool_size" in config_content:
            checks.append("✅ 数据库连接池配置存在")
        else:
            checks.append("❌ 数据库连接池配置缺失")
            
        if "rate_limit" in config_content:
            checks.append("✅ API限流配置存在")
        else:
            checks.append("❌ API限流配置缺失")
            
    except Exception as e:
        checks.append(f"❌ 性能配置检查失败: {e}")
    
    # 检查是否有监控指标
    try:
        main_path = Path(__file__).parent / "src" / "main.py"
        with open(main_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        if "prometheus_client" in main_content:
            checks.append("✅ Prometheus指标收集存在")
        else:
            checks.append("❌ Prometheus指标收集缺失")
            
    except Exception as e:
        checks.append(f"❌ 监控指标检查失败: {e}")
    
    for check in checks:
        print(f"  {check}")
    
    return all("✅" in check for check in checks)

def main():
    """主验证函数"""
    print("🚀 开始静态验证天庭API服务器...")
    print("=" * 60)
    
    tests = [
        ("文件完整性", check_file_completeness),
        ("Python语法", check_python_files),
        ("代码结构", check_code_structure),
        ("依赖要求", check_requirements),
        ("Shared类型", check_shared_types),
        ("性能配置", performance_check),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name} 验证通过")
            else:
                print(f"\n❌ {test_name} 验证失败")
        except Exception as e:
            print(f"\n❌ {test_name} 验证异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 静态验证结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有静态验证通过！API服务器基础框架符合规范")
        print("📝 建议：在部署前安装依赖包并运行完整测试")
        return True
    else:
        print("⚠️ 部分验证失败，请检查相关问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
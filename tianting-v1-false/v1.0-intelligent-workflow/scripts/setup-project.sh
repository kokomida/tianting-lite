#!/bin/bash
# scripts/setup-project.sh

set -e

echo "🚀 天庭系统项目初始化开始..."

# 检查必需工具
check_requirements() {
    echo "检查系统要求..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker 未安装，请先安装 Docker Desktop"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose 未安装"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js 未安装，请安装 Node.js 18+"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 未安装，请安装 Python 3.11+"
        exit 1
    fi
    
    echo "✅ 系统要求检查通过"
}

# 复制环境配置模板
setup_environment_config() {
    echo "设置环境配置..."
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "📝 请编辑 .env 文件，设置必要的环境变量（特别是 CLAUDE_API_KEY）"
    fi
    
    echo "✅ 环境配置完成"
}

# 初始化包依赖配置文件
setup_package_dependencies() {
    echo "初始化包依赖配置..."
    
    # 初始化shared包
    if [ ! -f packages/shared/package.json ]; then
        cat > packages/shared/package.json << 'EOF'
{
  "name": "@tianting/shared",
  "version": "1.0.0",
  "description": "天庭系统共享类型定义",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "watch": "tsc --watch",
    "test": "jest",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {},
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }
}
EOF
    fi
    
    # 初始化core包requirements.txt
    if [ ! -f packages/core/requirements.txt ]; then
        cat > packages/core/requirements.txt << 'EOF'
# 天庭Core包依赖
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
anthropic==0.7.8
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
EOF
    fi
    
    # 初始化api包requirements.txt
    if [ ! -f packages/api/requirements.txt ]; then
        cat > packages/api/requirements.txt << 'EOF'
# 天庭API包依赖
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
websockets==12.0
EOF
    fi
    
    echo "✅ 包依赖配置初始化完成"
}

# 启动基础服务
start_base_services() {
    echo "启动基础服务..."
    
    docker-compose up -d postgres redis
    
    # 等待服务启动
    echo "等待数据库启动..."
    sleep 15
    
    # 检查服务状态
    if docker-compose ps postgres | grep -q "Up"; then
        echo "✅ PostgreSQL 启动成功"
    else
        echo "❌ PostgreSQL 启动失败"
        exit 1
    fi
    
    if docker-compose ps redis | grep -q "Up"; then
        echo "✅ Redis 启动成功"
    else
        echo "❌ Redis 启动失败"
        exit 1
    fi
}

# 执行健康检查
run_health_check() {
    echo "执行系统健康检查..."
    
    ./scripts/health-check.sh
    
    if [ $? -eq 0 ]; then
        echo "✅ 系统健康检查通过"
    else
        echo "❌ 系统健康检查失败"
        exit 1
    fi
}

# 主执行流程
main() {
    check_requirements
    setup_environment_config
    setup_package_dependencies
    start_base_services
    run_health_check
    
    echo ""
    echo "🎉 天庭系统项目初始化完成！"
    echo ""
    echo "下一步："
    echo "1. 编辑 .env 文件，设置 CLAUDE_API_KEY"
    echo "2. 开始执行包级别的并发开发任务"
    echo ""
    echo "基础服务地址："
    echo "- PostgreSQL: localhost:5432"
    echo "- Redis: localhost:6379"
    echo ""
    echo "准备就绪，可以开始并发开发！"
}

main "$@"
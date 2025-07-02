# 🐳 天庭系统多包并发开发环境

## 🎯 环境隔离架构

每个包都有完全独立的开发环境，支持并发开发而无任何冲突。

```mermaid
graph TB
    subgraph "开发环境隔离"
        subgraph "Core Package Dev"
            C1[FastAPI:8001]
            C2[DB: tianting_core]
            C3[Redis: db1]
        end
        
        subgraph "API Package Dev"  
            A1[FastAPI:8002]
            A2[DB: tianting_api]
            A3[Redis: db2]
        end
        
        subgraph "Frontend Package Dev"
            F1[React:3001]
            F2[Mock API:3002]
        end
        
        subgraph "Shared Services"
            M1[MockServer:1080]
            M2[Redis Cluster]
            M3[Test DB Pool]
        end
    end
    
    F1 --> M1
    C1 --> C2
    A1 --> A2
    C1 --> C3
    A1 --> A3
```

## 📦 包级别环境配置

### Core Package环境 (Port: 8001)
```yaml
# packages/core/.env.dev
PACKAGE_NAME=core
SERVER_PORT=8001
DATABASE_URL=postgresql://user:pass@localhost:5432/tianting_core_dev
REDIS_URL=redis://localhost:6379/1
LOCAL_AI_ENDPOINT=http://localhost:8080
LOG_LEVEL=DEBUG
ENVIRONMENT=development

# 包特定配置
REQUIREMENT_PARSING_TIMEOUT=30
AI_MODEL_TYPE=local_ai_model
CACHE_TTL_SECONDS=3600
```

### API Package环境 (Port: 8002)  
```yaml
# packages/api/.env.dev
PACKAGE_NAME=api
SERVER_PORT=8002
DATABASE_URL=postgresql://user:pass@localhost:5432/tianting_api_dev
REDIS_URL=redis://localhost:6379/2
JWT_SECRET_KEY=dev_jwt_secret_for_api_package
CORS_ORIGINS=["http://localhost:3001"]
LOG_LEVEL=DEBUG
ENVIRONMENT=development

# API包特定配置
RATE_LIMIT_PER_MINUTE=100
SESSION_TIMEOUT_MINUTES=60
API_VERSION=v1
```

### Frontend Package环境 (Port: 3001)
```yaml
# packages/frontend/.env.dev
REACT_APP_PACKAGE_NAME=frontend
PORT=3001
REACT_APP_API_BASE_URL=http://localhost:1080/api
REACT_APP_MOCK_MODE=true
REACT_APP_LOG_LEVEL=debug
REACT_APP_ENVIRONMENT=development

# 前端特定配置
REACT_APP_ENABLE_DEVTOOLS=true
REACT_APP_AUTO_REFRESH=true
GENERATE_SOURCEMAP=true
```

### Shared Package环境
```yaml
# packages/shared/.env.dev
PACKAGE_NAME=shared
NODE_ENV=development
LOG_LEVEL=debug

# 共享包配置
TYPE_CHECK_INTERVAL=5000
WATCH_MODE=true
```

## 🐳 Docker Compose配置

### 主开发环境
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # 数据库服务
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: tianting_dev
      POSTGRES_PASSWORD: dev_password
      POSTGRES_MULTIPLE_DATABASES: tianting_core_dev,tianting_api_dev,tianting_shared_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./packages/common/environments/init-databases.sh:/docker-entrypoint-initdb.d/init-databases.sh

  # Redis服务
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --databases 16
    volumes:
      - redis_data:/data

  # Mock服务器
  mockserver:
    image: mockserver/mockserver:5.15.0
    ports:
      - "1080:1080"
    environment:
      MOCKSERVER_PROPERTY_FILE: /config/mockserver.properties
    volumes:
      - ./packages/common/mock-data:/config

  # Core包开发环境
  core-dev:
    build:
      context: ./packages/core
      dockerfile: Dockerfile.dev
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://tianting_dev:dev_password@postgres:5432/tianting_core_dev
      - REDIS_URL=redis://redis:6379/1
    volumes:
      - ./packages/core:/app
      - /app/node_modules
    depends_on:
      - postgres
      - redis
    command: npm run dev

  # API包开发环境
  api-dev:
    build:
      context: ./packages/api
      dockerfile: Dockerfile.dev
    ports:
      - "8002:8002"
    environment:
      - DATABASE_URL=postgresql://tianting_dev:dev_password@postgres:5432/tianting_api_dev
      - REDIS_URL=redis://redis:6379/2
    volumes:
      - ./packages/api:/app
      - /app/node_modules
    depends_on:
      - postgres
      - redis
    command: npm run dev

  # 前端包开发环境  
  frontend-dev:
    build:
      context: ./packages/frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3001:3001"
    environment:
      - REACT_APP_API_BASE_URL=http://mockserver:1080/api
    volumes:
      - ./packages/frontend:/app
      - /app/node_modules
    depends_on:
      - mockserver
    command: npm start

volumes:
  postgres_data:
  redis_data:
```

### 数据库初始化脚本
```bash
#!/bin/bash
# packages/common/environments/init-databases.sh

set -e
set -u

function create_user_and_database() {
    local database=$1
    echo "Creating user and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        create_user_and_database $db
    done
    echo "Multiple databases created"
fi
```

## 🚀 并发开发启动脚本

### 一键启动所有环境
```bash
#!/bin/bash
# scripts/start-concurrent-dev.sh

echo "🚀 启动天庭系统并发开发环境..."

# 启动基础服务
echo "📦 启动基础服务 (PostgreSQL, Redis, MockServer)..."
docker-compose -f docker-compose.dev.yml up -d postgres redis mockserver

# 等待服务就绪
echo "⏳ 等待服务启动..."
sleep 10

# 启动各包开发环境
echo "🔨 启动Core包开发环境 (Port: 8001)..."
cd packages/core && npm run dev &
CORE_PID=$!

echo "🔌 启动API包开发环境 (Port: 8002)..."  
cd packages/api && npm run dev &
API_PID=$!

echo "🎨 启动Frontend包开发环境 (Port: 3001)..."
cd packages/frontend && npm start &
FRONTEND_PID=$!

echo "📚 启动Shared包监控 (TypeScript编译)..."
cd packages/shared && npm run watch &
SHARED_PID=$!

# 保存进程ID
echo $CORE_PID > .dev-pids/core.pid
echo $API_PID > .dev-pids/api.pid
echo $FRONTEND_PID > .dev-pids/frontend.pid  
echo $SHARED_PID > .dev-pids/shared.pid

echo ""
echo "✅ 并发开发环境启动完成!"
echo ""
echo "📊 服务访问地址:"
echo "  - Core包开发:    http://localhost:8001"
echo "  - API包开发:     http://localhost:8002"  
echo "  - Frontend开发:  http://localhost:3001"
echo "  - Mock服务器:    http://localhost:1080"
echo ""
echo "🛠️  开发命令:"
echo "  - 停止所有服务:  npm run stop-dev"
echo "  - 查看日志:      npm run logs"
echo "  - 重启服务:      npm run restart-dev"
```

### 停止开发环境
```bash
#!/bin/bash
# scripts/stop-concurrent-dev.sh

echo "🛑 停止天庭系统并发开发环境..."

# 停止各包进程
if [ -f .dev-pids/core.pid ]; then
    kill $(cat .dev-pids/core.pid) 2>/dev/null || true
    rm .dev-pids/core.pid
fi

if [ -f .dev-pids/api.pid ]; then
    kill $(cat .dev-pids/api.pid) 2>/dev/null || true
    rm .dev-pids/api.pid
fi

if [ -f .dev-pids/frontend.pid ]; then
    kill $(cat .dev-pids/frontend.pid) 2>/dev/null || true
    rm .dev-pids/frontend.pid
fi

if [ -f .dev-pids/shared.pid ]; then
    kill $(cat .dev-pids/shared.pid) 2>/dev/null || true
    rm .dev-pids/shared.pid
fi

# 停止Docker服务
docker-compose -f docker-compose.dev.yml down

echo "✅ 所有开发服务已停止"
```

## 🔧 包级别开发工具

### Core包开发工具
```json
{
  "scripts": {
    "dev": "uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload",
    "test": "pytest tests/ -v",
    "test:watch": "pytest-watch tests/",
    "lint": "black src/ && isort src/ && flake8 src/",
    "type-check": "mypy src/"
  }
}
```

### API包开发工具  
```json
{
  "scripts": {
    "dev": "uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload",
    "test": "pytest tests/ -v",
    "test:integration": "pytest tests/integration/ -v",
    "db:migrate": "alembic upgrade head",
    "db:reset": "alembic downgrade base && alembic upgrade head"
  }
}
```

### Frontend包开发工具
```json
{
  "scripts": {
    "start": "PORT=3001 react-scripts start",
    "test": "react-scripts test --watchAll=false",
    "test:watch": "react-scripts test",
    "test:coverage": "react-scripts test --coverage --watchAll=false",
    "storybook": "start-storybook -p 6006"
  }
}
```

## 📊 健康检查和监控

### 环境健康检查
```bash
#!/bin/bash
# scripts/health-check.sh

echo "🔍 检查开发环境健康状态..."

# 检查PostgreSQL
if pg_isready -h localhost -p 5432 -U tianting_dev; then
    echo "✅ PostgreSQL: 正常"
else
    echo "❌ PostgreSQL: 异常"
fi

# 检查Redis
if redis-cli -h localhost -p 6379 ping | grep -q PONG; then
    echo "✅ Redis: 正常"
else
    echo "❌ Redis: 异常"  
fi

# 检查各包服务
for port in 8001 8002 3001 1080; do
    if curl -s http://localhost:$port/health > /dev/null; then
        echo "✅ Port $port: 正常"
    else
        echo "❌ Port $port: 异常"
    fi
done
```

### 性能监控
```javascript
// packages/common/monitoring/dev-metrics.js
const express = require('express');
const promClient = require('prom-client');

// 创建指标收集器
const developmentMetrics = {
    buildTime: new promClient.Histogram({
        name: 'dev_build_duration_seconds',
        help: 'Development build duration',
        labelNames: ['package']
    }),
    
    testDuration: new promClient.Histogram({
        name: 'dev_test_duration_seconds', 
        help: 'Test execution duration',
        labelNames: ['package', 'test_type']
    })
};

// 启动监控服务器
const app = express();
app.get('/metrics', (req, res) => {
    res.set('Content-Type', promClient.register.contentType);
    res.end(promClient.register.metrics());
});

app.listen(9090, () => {
    console.log('📊 开发环境监控: http://localhost:9090/metrics');
});
```

## 🎯 环境验证清单

### 启动验证
- [ ] PostgreSQL数据库连接成功，所有开发数据库已创建
- [ ] Redis连接成功，各包使用不同的数据库索引
- [ ] MockServer启动成功，API契约响应正常
- [ ] Core包服务启动 (Port: 8001)
- [ ] API包服务启动 (Port: 8002)  
- [ ] Frontend包启动 (Port: 3001)
- [ ] 所有包的健康检查端点响应正常

### 并发开发验证
- [ ] 多个开发者可以同时修改不同包的代码
- [ ] 包间无文件冲突，各包独立构建
- [ ] Mock API支持前端独立开发
- [ ] 热重载功能正常，代码变更自动生效
- [ ] 测试可以并发运行，互不干扰

### 性能验证
- [ ] 单包测试执行时间 < 30秒
- [ ] 代码热重载响应时间 < 3秒
- [ ] 前端页面加载时间 < 2秒
- [ ] Mock API响应时间 < 100ms

---

**🎯 通过完全隔离的开发环境，实现真正无冲突的并发开发！**
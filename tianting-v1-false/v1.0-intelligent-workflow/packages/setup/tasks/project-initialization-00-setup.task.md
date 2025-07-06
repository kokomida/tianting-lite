// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业系统架构师的思维模式思考，遵循DevOps原则，确保环境的可重复性、可移植性和架构一致性。我承诺：
- 以可重复、自动化的环境搭建为核心指导思想
- 先理解项目架构，再实现环境配置，通过验证确保环境可用
- 确保所有环境配置与天庭系统整体架构保持一致
- 严格遵循Docker容器化和环境隔离原则

## 执行承诺
我将遵循严格的执行流程，不偏离既定规范。我承诺：

**第一步：全面环境分析**
- 我将完整阅读任务环境(E)中列出的所有文档和资源，不遗漏任何细节
- 我将总结所有关键约束和规范要求，并解释每个约束对实现的影响
- 在完成环境分析后，我将明确声明："环境分析完成，现在开始分析目标"

**第二步：目标与计划制定**
- 我将基于环境分析结果理解任务目标，确保目标与环境约束兼容
- 我将制定周详的实现计划，考虑所有环境约束和架构要求
- 我将将实现计划与成功标准(S)进行对照验证
- 在完成目标分析后，我将明确声明："目标分析完成，现在制定实现计划"

**第三步：测试驱动实现**
- 我将严格按照测试优先级实现功能
- 每完成一个配置步骤，我将立即运行相关验证测试
- 遇到环境问题时，我将使用日志和系统性调试方法而非依赖猜测
- 我将确保环境配置满足所有验证要求，不妥协环境质量
- 我将确保环境配置符合业务需求，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：环境任务重点验证服务启动和连通性
- 自我验证：
  * 我将执行所有服务启动脚本确保环境正常运行
  * 我将执行连通性测试确保各服务间通信正常
  * 我将确认没有端口冲突和资源竞争
  * 在验证通过后，我将明确声明："自我验证完成，环境搭建成功，所有服务正常运行"

## 禁止事项（红线）
- 我绝不跳过环境验证步骤，确保每个组件都正常工作
- 我绝不使用硬编码的配置，而是使用环境变量和配置文件
- 我绝不依赖猜测解决环境问题，而是使用日志和系统性调试
- 如果我需要修改架构设计，我将明确说明修改理由并请求审批
- 我绝不在未理清环境全貌的情况下，直接开始配置

## 调试规范
- 遇到环境问题时，我将：
  * 首先检查Docker容器状态和日志
  * 分析端口占用和网络连接
  * 检查配置文件和环境变量
  * 验证数据库连接和权限设置
  * 追踪问题根源至具体配置
- 当我需要添加日志时，我将：
  * 在关键启动步骤记录状态信息
  * 在连接建立处记录连接参数
  * 在错误发生处记录详细错误信息
  * 在验证步骤处记录验证结果

## 权利
- 我有权利在环境配置本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让环境搭建更加稳定和高效

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 天庭系统项目初始化和环境搭建（前置任务）

**目标(O)**:
- **功能目标**:
  - 建立天庭系统的完整项目结构和开发环境
  - 配置所有必需的基础服务（数据库、缓存、消息队列等）
  - 建立包级别的环境隔离和并发开发基础
  - 为后续所有并发任务提供稳定的运行环境

- **执行任务**:
  - 创建文件:
    - `docker-compose.yml` - 主环境编排文件
    - `packages/shared/package.json` - 共享包配置
    - `packages/core/requirements.txt` - Python依赖
    - `packages/api/requirements.txt` - API服务依赖
    - `packages/frontend/package.json` - 前端依赖
    - `scripts/setup-project.sh` - 项目初始化脚本
    - `scripts/start-all-services.sh` - 启动所有服务脚本
    - `scripts/stop-all-services.sh` - 停止所有服务脚本
    - `scripts/reset-environment.sh` - 环境重置脚本
    - `scripts/health-check.sh` - 健康检查脚本
    - `.env.example` - 环境变量模板
    - `.gitignore` - Git忽略文件
    - `README.md` - 项目说明文档
  - 创建目录结构:
    - 完整的packages目录结构
    - logs、data、temp等运行时目录
    - 配置文件目录
  - 实现功能:
    - Docker容器编排和网络配置
    - 数据库初始化和权限设置
    - 包级别的依赖管理
    - 开发环境的启动和验证脚本
    - 健康检查和故障排查工具

- **任务边界**:
  - 包含完整的环境搭建，不包含业务逻辑实现
  - 包含所有基础服务配置，不包含具体的应用代码
  - 包含开发环境配置，不包含生产环境部署
  - 专注于环境基础设施，不涉及具体功能开发

**环境(E)**:
- **参考资源**:
  - `docs/requirements-analysis.md` - 了解系统需求和技术栈
  - `development/architecture/technical-architecture.md` - 技术架构设计
  - `planning/user-stories-breakdown.md` - 了解功能范围
  - `packages/common/guides/concurrent-development-framework.md` - 并发开发要求
  - `packages/common/environments/dev-environment-setup.md` - 环境配置细节

- **上下文信息**:
  - 任务定位：这是所有其他任务的前置依赖，必须最先完成
  - 并发要求：完成后，shared/core/api/frontend可以并发开发
  - 技术栈：Python 3.11+, Node.js 18+, PostgreSQL 15+, Redis 7+, Docker
  - 端口分配：
    - Core服务: 8001
    - API服务: 8002  
    - 前端服务: 3001
    - PostgreSQL: 5432
    - Redis: 6379
  - 数据库隔离：
    - tianting_shared (共享配置)
    - tianting_core_dev (Core包专用)
    - tianting_api_dev (API包专用)

- **规范索引**:
  - Docker Compose最佳实践
  - Python项目结构标准
  - Node.js项目配置规范
  - 数据库设计和权限管理标准

- **注意事项**:
  - 环境配置必须支持多平台（Windows、macOS、Linux）
  - 所有服务必须容器化，避免本地环境依赖
  - 端口分配必须避免冲突，支持同时运行
  - 数据持久化必须考虑开发环境的数据保护

**实现指导(I)**:
- **算法与流程**:
  - 项目初始化流程:
    ```
    创建目录结构 → 配置Docker环境 → 初始化数据库 → 配置包依赖 → 启动服务 → 验证连通性
    ```
  - 服务启动顺序:
    ```
    PostgreSQL → Redis → Core服务 → API服务 → 前端服务
    ```

- **技术选型**:
  - 容器编排：Docker Compose (开发环境)
  - 数据库：PostgreSQL 15 (主数据库)
  - 缓存：Redis 7 (缓存和会话)
  - Python环境：Python 3.11 + FastAPI + SQLAlchemy
  - Node.js环境：Node.js 18 + React 18 + TypeScript 5
  - 开发工具：VS Code + Docker Desktop

- **代码模式**:
  - Docker Compose配置:
    ```yaml
    version: '3.8'
    
    services:
      # PostgreSQL数据库
      postgres:
        image: postgres:15-alpine
        container_name: tianting-postgres
        ports:
          - "5432:5432"
        environment:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: tianting123
          POSTGRES_DB: postgres
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
        networks:
          - tianting-network
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U postgres"]
          interval: 10s
          timeout: 5s
          retries: 5
      
      # Redis缓存
      redis:
        image: redis:7-alpine
        container_name: tianting-redis
        ports:
          - "6379:6379"
        volumes:
          - redis_data:/data
        networks:
          - tianting-network
        healthcheck:
          test: ["CMD", "redis-cli", "ping"]
          interval: 10s
          timeout: 5s
          retries: 5
          
      # Core服务 (Business Logic)
      core-service:
        build: 
          context: ./packages/core
          dockerfile: Dockerfile
        container_name: tianting-core
        ports:
          - "8001:8001"
        environment:
          - DATABASE_URL=postgresql://postgres:tianting123@postgres:5432/tianting_core_dev
          - REDIS_URL=redis://redis:6379/0
          - LOCAL_AI_ENDPOINT=http://localhost:8080
        volumes:
          - ./packages/core:/app
          - ./packages/shared:/shared
        depends_on:
          postgres:
            condition: service_healthy
          redis:
            condition: service_healthy
        networks:
          - tianting-network
        restart: unless-stopped
        
      # API服务 (HTTP Interface)
      api-service:
        build:
          context: ./packages/api
          dockerfile: Dockerfile
        container_name: tianting-api
        ports:
          - "8002:8002"
        environment:
          - DATABASE_URL=postgresql://postgres:tianting123@postgres:5432/tianting_api_dev
          - REDIS_URL=redis://redis:6379/1
          - CORE_SERVICE_URL=http://core-service:8001
        volumes:
          - ./packages/api:/app
          - ./packages/shared:/shared
        depends_on:
          - postgres
          - redis
          - core-service
        networks:
          - tianting-network
        restart: unless-stopped
        
      # 前端服务 (React App)
      frontend-service:
        build:
          context: ./packages/frontend
          dockerfile: Dockerfile
        container_name: tianting-frontend
        ports:
          - "3001:3001"
        environment:
          - REACT_APP_API_URL=http://localhost:8002
          - REACT_APP_WS_URL=ws://localhost:8002
        volumes:
          - ./packages/frontend:/app
          - ./packages/shared:/shared
          - /app/node_modules
        depends_on:
          - api-service
        networks:
          - tianting-network
        restart: unless-stopped
    
    volumes:
      postgres_data:
      redis_data:
      
    networks:
      tianting-network:
        driver: bridge
    ```
  - 项目初始化脚本:
    ```bash
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
    
    # 创建项目目录结构
    create_directory_structure() {
        echo "创建项目目录结构..."
        
        mkdir -p packages/{shared,core,api,frontend,integration,validation,setup}/src
        mkdir -p packages/{shared,core,api,frontend,integration,validation,setup}/tests
        mkdir -p packages/{shared,core,api,frontend,integration,validation,setup}/tasks
        mkdir -p packages/common/{contracts,environments,guides}
        mkdir -p scripts
        mkdir -p logs
        mkdir -p data/{postgres,redis}
        mkdir -p temp
        mkdir -p docs
        mkdir -p development/{architecture,planning}
        mkdir -p resources
        
        echo "✅ 目录结构创建完成"
    }
    
    # 复制环境配置模板
    setup_environment_config() {
        echo "设置环境配置..."
        
        if [ ! -f .env ]; then
            cp .env.example .env
            echo "📝 请编辑 .env 文件，设置必要的环境变量（特别是 LOCAL_AI_ENDPOINT）"
        fi
        
        echo "✅ 环境配置完成"
    }
    
    # 初始化包依赖
    setup_package_dependencies() {
        echo "初始化包依赖..."
        
        # 初始化shared包
        if [ ! -f packages/shared/package.json ]; then
            cd packages/shared
            npm init -y
            npm install typescript @types/node --save-dev
            cd ../..
        fi
        
        # 初始化frontend包
        if [ ! -f packages/frontend/package.json ]; then
            cd packages/frontend
            npx create-react-app . --template typescript --skip-git
            cd ../..
        fi
        
        echo "✅ 包依赖初始化完成"
    }
    
    # 构建Docker镜像
    build_docker_images() {
        echo "构建Docker镜像..."
        
        docker-compose build
        
        echo "✅ Docker镜像构建完成"
    }
    
    # 启动基础服务
    start_base_services() {
        echo "启动基础服务..."
        
        docker-compose up -d postgres redis
        
        # 等待服务启动
        echo "等待数据库启动..."
        sleep 10
        
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
    
    # 初始化数据库
    initialize_databases() {
        echo "初始化数据库..."
        
        # 创建应用数据库
        docker exec tianting-postgres psql -U postgres -c "CREATE DATABASE tianting_shared;"
        docker exec tianting-postgres psql -U postgres -c "CREATE DATABASE tianting_core_dev;"
        docker exec tianting-postgres psql -U postgres -c "CREATE DATABASE tianting_api_dev;"
        
        echo "✅ 数据库初始化完成"
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
        create_directory_structure
        setup_environment_config
        setup_package_dependencies
        build_docker_images
        start_base_services
        initialize_databases
        run_health_check
        
        echo ""
        echo "🎉 天庭系统项目初始化完成！"
        echo ""
        echo "下一步："
        echo "1. 编辑 .env 文件，设置 LOCAL_AI_ENDPOINT"
        echo "2. 运行 ./scripts/start-all-services.sh 启动所有服务"
        echo "3. 开始执行包级别的并发开发任务"
        echo ""
        echo "服务地址："
        echo "- 前端: http://localhost:3001"
        echo "- API: http://localhost:8002"
        echo "- Core: http://localhost:8001"
        echo "- PostgreSQL: localhost:5432"
        echo "- Redis: localhost:6379"
    }
    
    main "$@"
    ```
  - 健康检查脚本:
    ```bash
    #!/bin/bash
    # scripts/health-check.sh
    
    echo "🔍 天庭系统健康检查..."
    
    # 检查Docker容器状态
    check_containers() {
        echo "检查容器状态..."
        
        containers=("tianting-postgres" "tianting-redis")
        
        for container in "${containers[@]}"; do
            if docker ps | grep -q "$container"; then
                echo "✅ $container 运行正常"
            else
                echo "❌ $container 未运行"
                return 1
            fi
        done
        
        return 0
    }
    
    # 检查数据库连接
    check_database() {
        echo "检查数据库连接..."
        
        if docker exec tianting-postgres pg_isready -U postgres > /dev/null 2>&1; then
            echo "✅ PostgreSQL 连接正常"
        else
            echo "❌ PostgreSQL 连接失败"
            return 1
        fi
        
        # 检查数据库是否存在
        databases=("tianting_shared" "tianting_core_dev" "tianting_api_dev")
        
        for db in "${databases[@]}"; do
            if docker exec tianting-postgres psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$db"; then
                echo "✅ 数据库 $db 存在"
            else
                echo "❌ 数据库 $db 不存在"
                return 1
            fi
        done
        
        return 0
    }
    
    # 检查Redis连接
    check_redis() {
        echo "检查Redis连接..."
        
        if docker exec tianting-redis redis-cli ping | grep -q "PONG"; then
            echo "✅ Redis 连接正常"
        else
            echo "❌ Redis 连接失败"
            return 1
        fi
        
        return 0
    }
    
    # 检查端口占用
    check_ports() {
        echo "检查端口占用..."
        
        ports=(3001 8001 8002 5432 6379)
        
        for port in "${ports[@]}"; do
            if lsof -i ":$port" > /dev/null 2>&1; then
                echo "✅ 端口 $port 正在使用"
            else
                echo "⚠️  端口 $port 未使用（可能服务未启动）"
            fi
        done
        
        return 0
    }
    
    # 检查文件系统
    check_filesystem() {
        echo "检查项目文件结构..."
        
        required_dirs=(
            "packages/shared"
            "packages/core" 
            "packages/api"
            "packages/frontend"
            "scripts"
            "logs"
            "data"
        )
        
        for dir in "${required_dirs[@]}"; do
            if [ -d "$dir" ]; then
                echo "✅ 目录 $dir 存在"
            else
                echo "❌ 目录 $dir 不存在"
                return 1
            fi
        done
        
        return 0
    }
    
    # 主健康检查流程
    main() {
        local overall_status=0
        
        check_filesystem || overall_status=1
        check_containers || overall_status=1
        check_database || overall_status=1
        check_redis || overall_status=1
        check_ports
        
        echo ""
        if [ $overall_status -eq 0 ]; then
            echo "🎉 系统健康检查通过"
            echo "环境已准备就绪，可以开始并发开发！"
        else
            echo "💥 系统健康检查失败"
            echo "请检查上述错误并重新运行初始化脚本"
        fi
        
        return $overall_status
    }
    
    main "$@"
    ```

- **实现策略**:
  1. 创建完整的项目目录结构
  2. 配置Docker Compose环境编排
  3. 设置包级别的依赖管理
  4. 实现服务启动和健康检查脚本
  5. 配置开发环境的数据持久化
  6. 验证所有服务的连通性和可用性

- **调试指南**:
  - 环境问题排查:
    ```bash
    # 检查容器状态
    docker-compose ps
    
    # 查看服务日志
    docker-compose logs postgres
    docker-compose logs redis
    
    # 重新构建镜像
    docker-compose build --no-cache
    
    # 重置环境
    ./scripts/reset-environment.sh
    
    # 检查端口占用
    lsof -i :5432
    lsof -i :6379
    
    # 检查网络连接
    docker network ls
    docker network inspect tianting-mvp_tianting-network
    ```

**成功标准(S)**:
- **基础达标**:
  - 项目目录结构完整创建，所有必需目录存在
  - Docker Compose环境正常启动，所有基础服务运行
  - PostgreSQL数据库连接正常，所有应用数据库创建成功
  - Redis缓存服务连接正常，可以正常读写
  - 所有端口分配正确，无冲突现象

- **预期品质**:
  - 健康检查脚本运行成功，所有检查项通过
  - 环境启动时间<2分钟，服务响应正常
  - 支持一键重置和重新初始化
  - 跨平台兼容性良好，支持Windows/macOS/Linux
  - 文档清晰完整，便于新开发者快速上手

- **卓越表现**:
  - 实现智能的环境检测和自动修复
  - 支持多环境配置和快速切换
  - 提供详细的监控和日志收集
  - 实现环境的版本管理和回滚
  - 集成开发工具的自动配置和优化
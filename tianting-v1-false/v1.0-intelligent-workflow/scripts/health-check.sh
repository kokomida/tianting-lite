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
    
    ports=(5432 6379)
    
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
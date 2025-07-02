#!/bin/bash

# 天庭系统快速启动脚本
# 一键启动所有服务，适合开发和测试

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
CORE_PORT=8011
API_PORT=8012
FRONTEND_PORT=3011
POSTGRES_PORT=5432
REDIS_PORT=6379

# PID文件目录
PID_DIR="./tmp/pids"
mkdir -p "$PID_DIR"

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查端口是否被占用
port_in_use() {
    netstat -tuln 2>/dev/null | grep -q ":$1 " || ss -tuln 2>/dev/null | grep -q ":$1 "
}

# 等待端口可用
wait_for_port() {
    local host=$1
    local port=$2
    local timeout=${3:-30}
    local count=0
    
    log_info "等待 $host:$port 服务启动..."
    
    while [ $count -lt $timeout ]; do
        if nc -z "$host" "$port" 2>/dev/null || (command_exists curl && curl -s "$host:$port" >/dev/null 2>&1); then
            return 0
        fi
        sleep 1
        count=$((count + 1))
    done
    
    return 1
}

# 检查服务状态
check_service_health() {
    local service_name=$1
    local port=$2
    local health_endpoint=$3
    
    if wait_for_port "localhost" "$port" 10; then
        if [ -n "$health_endpoint" ] && command_exists curl; then
            if curl -sf "$health_endpoint" >/dev/null 2>&1; then
                log_success "$service_name 服务健康检查通过"
                return 0
            else
                log_warning "$service_name 端口开放但健康检查失败"
                return 1
            fi
        else
            log_success "$service_name 服务启动成功 (端口:$port)"
            return 0
        fi
    else
        log_error "$service_name 服务启动失败"
        return 1
    fi
}

# 启动数据库服务
start_databases() {
    log_step "启动数据库服务..."
    
    if ! command_exists docker-compose && ! command_exists docker; then
        log_error "Docker未安装，无法启动数据库服务"
        return 1
    fi
    
    # 检查docker-compose.yml是否存在
    if [ ! -f "docker-compose.yml" ]; then
        log_error "未找到docker-compose.yml文件"
        return 1
    fi
    
    # 启动数据库容器
    log_info "启动PostgreSQL和Redis容器..."
    if command_exists docker-compose; then
        docker-compose up -d postgres redis
    else
        docker compose up -d postgres redis
    fi
    
    # 等待数据库就绪
    if wait_for_port "localhost" "$POSTGRES_PORT" 30; then
        log_success "PostgreSQL启动成功"
    else
        log_error "PostgreSQL启动失败"
        return 1
    fi
    
    if wait_for_port "localhost" "$REDIS_PORT" 15; then
        log_success "Redis启动成功"
    else
        log_error "Redis启动失败"
        return 1
    fi
}

# 启动Core服务
start_core_service() {
    log_step "启动Core服务..."
    
    if [ ! -d "packages/core" ]; then
        log_warning "Core包不存在，跳过"
        return 0
    fi
    
    # 检查端口是否被占用
    if port_in_use "$CORE_PORT"; then
        log_warning "端口$CORE_PORT已被占用，尝试关闭现有服务"
        pkill -f "uvicorn.*:$CORE_PORT" || true
        sleep 2
    fi
    
    # 启动服务  
    log_info "在端口$CORE_PORT启动Core服务..."
    cd packages/core
    
    # 后台启动 - 使用Core FastAPI应用
    nohup ../../tianting-env/bin/python -c "
import sys, os
sys.path.append('src')
os.chdir('src')
from app import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=$CORE_PORT, reload=False)
" > "../../logs/core.log" 2>&1 &
    CORE_PID=$!
    echo $CORE_PID > "../../$PID_DIR/core.pid"
    
    cd ../../
    
    # 健康检查
    if check_service_health "Core" "$CORE_PORT" "http://localhost:$CORE_PORT/health"; then
        log_info "Core服务日志: tail -f logs/core.log"
    else
        log_error "Core服务启动失败，检查日志: cat logs/core.log"
        return 1
    fi
}

# 启动API服务
start_api_service() {
    log_step "启动API服务..."
    
    if [ ! -d "packages/api" ]; then
        log_warning "API包不存在，跳过"
        return 0
    fi
    
    # 检查端口是否被占用
    if port_in_use "$API_PORT"; then
        log_warning "端口$API_PORT已被占用，尝试关闭现有服务"
        pkill -f "uvicorn.*:$API_PORT" || true
        sleep 2
    fi
    
    # 启动服务
    log_info "在端口$API_PORT启动API服务..."
    cd packages/api
    
    # 后台启动 - 使用实际的FastAPI应用
    nohup ../../tianting-env/bin/python -c "
import sys, os
sys.path.append('src')
os.chdir('src')
from simple_main import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=$API_PORT, reload=False)
" > "../../logs/api.log" 2>&1 &
    API_PID=$!
    echo $API_PID > "../../$PID_DIR/api.pid"
    
    cd ../../
    
    # 健康检查
    if check_service_health "API" "$API_PORT" "http://localhost:$API_PORT/health"; then
        log_success "API文档地址: http://localhost:$API_PORT/docs"
        log_info "API服务日志: tail -f logs/api.log"
    else
        log_error "API服务启动失败，检查日志: cat logs/api.log"
        return 1
    fi
}

# 启动前端服务
start_frontend_service() {
    log_step "启动前端服务..."
    
    if [ ! -d "packages/frontend" ]; then
        log_warning "Frontend包不存在，跳过"
        return 0
    fi
    
    if ! command_exists npm; then
        log_warning "npm未安装，跳过前端服务"
        return 0
    fi
    
    # 检查端口是否被占用
    if port_in_use "$FRONTEND_PORT"; then
        log_warning "端口$FRONTEND_PORT已被占用，尝试关闭现有服务"
        pkill -f "react-scripts.*start" || true
        sleep 2
    fi
    
    # 启动服务
    log_info "在端口$FRONTEND_PORT启动前端服务..."
    cd packages/frontend
    
    # 后台启动
    nohup npm start > "../../logs/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "../../$PID_DIR/frontend.pid"
    
    cd ../../
    
    # 等待前端启动（前端启动较慢）
    if wait_for_port "localhost" "$FRONTEND_PORT" 60; then
        log_success "前端服务启动成功"
        log_success "访问地址: http://localhost:$FRONTEND_PORT"
        log_info "前端服务日志: tail -f logs/frontend.log"
    else
        log_error "前端服务启动失败，检查日志: cat logs/frontend.log"
        return 1
    fi
}

# 停止所有服务
stop_all_services() {
    log_step "停止所有服务..."
    
    # 停止应用服务
    for service in core api frontend; do
        pid_file="$PID_DIR/$service.pid"
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                log_info "停止$service服务 (PID: $pid)"
                kill "$pid"
                rm -f "$pid_file"
            else
                log_info "$service服务已停止"
                rm -f "$pid_file"
            fi
        fi
    done
    
    # 强制关闭端口占用
    for port in $CORE_PORT $API_PORT $FRONTEND_PORT; do
        if port_in_use "$port"; then
            log_info "强制关闭端口$port"
            pkill -f ":$port" || true
        fi
    done
    
    # 停止数据库服务
    if [ -f "docker-compose.yml" ]; then
        log_info "停止数据库服务..."
        if command_exists docker-compose; then
            docker-compose down
        else
            docker compose down
        fi
    fi
    
    log_success "所有服务已停止"
}

# 检查服务状态
check_all_services() {
    log_step "检查服务状态..."
    
    echo -e "${CYAN}服务状态:${NC}"
    
    # 检查数据库
    if port_in_use "$POSTGRES_PORT"; then
        echo -e "  ${GREEN}✅${NC} PostgreSQL (端口:$POSTGRES_PORT)"
    else
        echo -e "  ${RED}❌${NC} PostgreSQL"
    fi
    
    if port_in_use "$REDIS_PORT"; then
        echo -e "  ${GREEN}✅${NC} Redis (端口:$REDIS_PORT)"
    else
        echo -e "  ${RED}❌${NC} Redis"
    fi
    
    # 检查应用服务
    if port_in_use "$CORE_PORT"; then
        echo -e "  ${GREEN}✅${NC} Core服务 (端口:$CORE_PORT)"
    else
        echo -e "  ${RED}❌${NC} Core服务"
    fi
    
    if port_in_use "$API_PORT"; then
        echo -e "  ${GREEN}✅${NC} API服务 (端口:$API_PORT) - http://localhost:$API_PORT/docs"
    else
        echo -e "  ${RED}❌${NC} API服务"
    fi
    
    if port_in_use "$FRONTEND_PORT"; then
        echo -e "  ${GREEN}✅${NC} 前端服务 (端口:$FRONTEND_PORT) - http://localhost:$FRONTEND_PORT"
    else
        echo -e "  ${RED}❌${NC} 前端服务"
    fi
}

# 显示使用帮助
show_help() {
    echo -e "${CYAN}天庭系统快速启动脚本${NC}"
    echo
    echo "用法: $0 [命令] [选项]"
    echo
    echo -e "${YELLOW}命令:${NC}"
    echo "  start     启动所有服务 (默认)"
    echo "  stop      停止所有服务"
    echo "  restart   重启所有服务"
    echo "  status    检查服务状态"
    echo "  logs      查看服务日志"
    echo "  help      显示此帮助"
    echo
    echo -e "${YELLOW}选项:${NC}"
    echo "  --no-db      跳过数据库启动"
    echo "  --no-frontend 跳过前端启动"
    echo "  --core-only  仅启动Core服务"
    echo "  --api-only   仅启动API服务"
    echo
    echo -e "${YELLOW}示例:${NC}"
    echo "  $0                    # 启动所有服务"
    echo "  $0 start --no-frontend # 启动除前端外的所有服务"
    echo "  $0 stop              # 停止所有服务"
    echo "  $0 status            # 查看服务状态"
    echo "  $0 logs              # 查看实时日志"
}

# 查看日志
show_logs() {
    log_step "显示服务日志..."
    
    if [ ! -d "logs" ]; then
        log_error "日志目录不存在"
        return 1
    fi
    
    echo -e "${YELLOW}可用日志文件:${NC}"
    ls -la logs/ 2>/dev/null || echo "无日志文件"
    echo
    
    echo -e "${YELLOW}实时查看日志 (Ctrl+C退出):${NC}"
    echo "  tail -f logs/core.log      # Core服务日志"
    echo "  tail -f logs/api.log       # API服务日志"  
    echo "  tail -f logs/frontend.log  # 前端服务日志"
    echo "  docker-compose logs -f     # 数据库日志"
    echo
    
    # 询问用户要查看哪个日志
    read -p "选择要查看的日志 [core/api/frontend/docker/all]: " choice
    case $choice in
        core)
            tail -f logs/core.log
            ;;
        api)
            tail -f logs/api.log
            ;;
        frontend)
            tail -f logs/frontend.log
            ;;
        docker)
            if command_exists docker-compose; then
                docker-compose logs -f
            else
                docker compose logs -f
            fi
            ;;
        all)
            tail -f logs/*.log
            ;;
        *)
            log_info "取消查看日志"
            ;;
    esac
}

# 主函数
main() {
    # 确保必要目录存在
    mkdir -p logs tmp/pids
    
    # 解析命令行参数
    COMMAND="start"
    SKIP_DB=false
    SKIP_FRONTEND=false
    CORE_ONLY=false
    API_ONLY=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            start|stop|restart|status|logs|help)
                COMMAND="$1"
                shift
                ;;
            --no-db)
                SKIP_DB=true
                shift
                ;;
            --no-frontend)
                SKIP_FRONTEND=true
                shift
                ;;
            --core-only)
                CORE_ONLY=true
                shift
                ;;
            --api-only)
                API_ONLY=true
                shift
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 执行命令
    case $COMMAND in
        start)
            echo -e "${PURPLE}🚀 启动天庭系统...${NC}"
            echo
            
            if [ "$SKIP_DB" = false ]; then
                start_databases
            fi
            
            if [ "$CORE_ONLY" = true ]; then
                start_core_service
            elif [ "$API_ONLY" = true ]; then
                start_api_service
            else
                start_core_service
                start_api_service
                
                if [ "$SKIP_FRONTEND" = false ]; then
                    start_frontend_service
                fi
            fi
            
            echo
            log_success "天庭系统启动完成！"
            echo
            check_all_services
            echo
            echo -e "${YELLOW}📚 常用地址:${NC}"
            echo -e "  ${CYAN}API文档:${NC} http://localhost:$API_PORT/docs"
            echo -e "  ${CYAN}前端应用:${NC} http://localhost:$FRONTEND_PORT"
            echo -e "  ${CYAN}健康检查:${NC} http://localhost:$API_PORT/health"
            echo
            echo -e "${YELLOW}🛠️ 管理命令:${NC}"
            echo -e "  ${CYAN}查看状态:${NC} $0 status"
            echo -e "  ${CYAN}查看日志:${NC} $0 logs"
            echo -e "  ${CYAN}停止服务:${NC} $0 stop"
            ;;
        stop)
            stop_all_services
            ;;
        restart)
            log_info "重启天庭系统..."
            stop_all_services
            sleep 3
            main start "$@"
            ;;
        status)
            check_all_services
            ;;
        logs)
            show_logs
            ;;
        help)
            show_help
            ;;
        *)
            log_error "未知命令: $COMMAND"
            show_help
            exit 1
            ;;
    esac
}

# 错误处理
trap 'log_error "脚本执行出错"; exit 1' ERR

# 信号处理
trap 'log_info "收到中断信号，正在清理..."; stop_all_services; exit 0' INT TERM

# 执行主函数
main "$@"
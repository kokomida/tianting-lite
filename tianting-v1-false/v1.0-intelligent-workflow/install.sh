#!/bin/bash

# 天庭系统一键安装脚本
# 自动检测环境并解决依赖冲突

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

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

# 检查Python版本
check_python_version() {
    log_step "检查Python版本..."
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_info "找到Python版本: $PYTHON_VERSION"
        
        # 检查版本是否>=3.8
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
            log_success "Python版本符合要求 (>=3.8)"
            PYTHON_CMD="python3"
        else
            log_error "Python版本过低，需要>=3.8，当前版本: $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "未找到Python3，请先安装Python 3.8+"
        exit 1
    fi
}

# 检查Node.js版本
check_node_version() {
    log_step "检查Node.js版本..."
    
    if command_exists node; then
        NODE_VERSION=$(node --version)
        log_info "找到Node.js版本: $NODE_VERSION"
        
        # 检查版本是否>=16
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
        if [ "$NODE_MAJOR" -ge 16 ]; then
            log_success "Node.js版本符合要求 (>=16)"
        else
            log_warning "Node.js版本建议升级到>=16，当前版本: $NODE_VERSION"
        fi
    else
        log_warning "未找到Node.js，前端功能将不可用"
        log_info "可运行: sudo apt install nodejs npm"
    fi
}

# 检测系统类型
detect_system() {
    log_step "检测系统环境..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if grep -q Microsoft /proc/version 2>/dev/null; then
            SYSTEM="WSL"
            log_info "检测到WSL环境"
        else
            SYSTEM="Linux"
            log_info "检测到Linux环境"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        SYSTEM="macOS"
        log_info "检测到macOS环境"
    else
        SYSTEM="Unknown"
        log_warning "未知系统类型: $OSTYPE"
    fi
}

# 安装Poetry
install_poetry() {
    log_step "检查Poetry安装状态..."
    
    if command_exists poetry; then
        POETRY_VERSION=$(poetry --version 2>/dev/null | awk '{print $3}' || echo "unknown")
        log_info "找到Poetry版本: $POETRY_VERSION"
        
        # 检查版本是否>=1.4
        if poetry --version | grep -q "Poetry (version 1\.[4-9]\|2\."; then
            log_success "Poetry版本符合要求"
        else
            log_warning "Poetry版本较低，建议升级"
            log_info "运行命令升级: poetry self update"
        fi
    else
        log_info "未找到Poetry，开始安装..."
        
        # 使用官方安装器
        if command_exists curl; then
            log_info "使用curl安装Poetry..."
            curl -sSL https://install.python-poetry.org | $PYTHON_CMD -
        else
            log_error "需要curl来安装Poetry，请先安装curl"
            exit 1
        fi
        
        # 添加到PATH
        export PATH="$HOME/.local/bin:$PATH"
        
        # 验证安装
        if command_exists poetry; then
            log_success "Poetry安装成功"
        else
            log_error "Poetry安装失败，请手动安装"
            log_info "安装命令: curl -sSL https://install.python-poetry.org | python3 -"
            exit 1
        fi
    fi
}

# 配置Poetry
configure_poetry() {
    log_step "配置Poetry环境..."
    
    # 配置在项目目录创建虚拟环境
    poetry config virtualenvs.in-project true
    log_info "配置Poetry在项目目录创建虚拟环境"
    
    # 配置包安装器
    poetry config installer.max-workers 10
    log_info "配置Poetry并行安装"
    
    # 显示当前配置
    log_info "Poetry配置:"
    poetry config --list | grep -E "(virtualenvs|installer)" || true
}

# 处理依赖冲突
handle_conflicts() {
    log_step "处理可能的依赖冲突..."
    
    # 检查是否有全局包可能冲突
    CONFLICT_PACKAGES=("fastapi" "uvicorn" "pydantic" "sqlalchemy")
    
    for pkg in "${CONFLICT_PACKAGES[@]}"; do
        if $PYTHON_CMD -c "import $pkg" 2>/dev/null; then
            log_warning "检测到全局安装的 $pkg，可能导致冲突"
            log_info "建议使用虚拟环境隔离依赖"
        fi
    done
}

# 安装Python依赖
install_python_deps() {
    log_step "安装Python依赖..."
    
    # 检查pyproject.toml是否存在
    if [ ! -f "pyproject.toml" ]; then
        log_error "未找到pyproject.toml文件"
        exit 1
    fi
    
    # 清理缓存（如果需要）
    if [ "$1" = "--clean" ]; then
        log_info "清理Poetry缓存..."
        poetry cache clear pypi --all -n || true
    fi
    
    # 安装依赖
    log_info "安装项目依赖（包括开发依赖）..."
    poetry install --with dev,test,docs
    
    log_success "Python依赖安装完成"
}

# 安装Node.js依赖
install_node_deps() {
    if command_exists npm; then
        log_step "安装Node.js依赖..."
        
        # Shared包
        if [ -d "packages/shared" ]; then
            log_info "安装Shared包依赖..."
            cd packages/shared
            npm install
            cd ../../
        fi
        
        # Frontend包
        if [ -d "packages/frontend" ]; then
            log_info "安装Frontend包依赖..."
            cd packages/frontend
            npm install
            cd ../../
        fi
        
        log_success "Node.js依赖安装完成"
    else
        log_warning "跳过Node.js依赖安装（npm未找到）"
    fi
}

# 验证安装
verify_installation() {
    log_step "验证安装..."
    
    # 检查Poetry环境
    if poetry env info >/dev/null 2>&1; then
        log_success "Poetry虚拟环境创建成功"
        VENV_PATH=$(poetry env info --path)
        log_info "虚拟环境路径: $VENV_PATH"
    else
        log_error "Poetry虚拟环境创建失败"
        exit 1
    fi
    
    # 测试关键包导入
    log_info "测试关键包导入..."
    poetry run python -c "
import pydantic
import fastapi
import uvicorn
import sqlalchemy
print('✅ 核心依赖导入成功')
" || {
        log_error "依赖包导入失败"
        exit 1
    }
    
    log_success "安装验证通过"
}

# 设置项目环境
setup_project_env() {
    log_step "设置项目环境..."
    
    # 复制环境变量模板
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        cp .env.example .env
        log_info "创建.env文件"
    fi
    
    # 确保必要目录存在
    mkdir -p logs data/uploads temp
    log_info "创建必要目录"
    
    # 设置权限
    chmod +x scripts/*.sh 2>/dev/null || true
    log_info "设置脚本执行权限"
}

# 显示安装结果
show_installation_summary() {
    echo
    echo -e "${GREEN}🎉 天庭系统安装完成！${NC}"
    echo -e "${CYAN}=====================${NC}"
    echo
    
    echo -e "${YELLOW}📋 安装摘要:${NC}"
    echo -e "  ${GREEN}✅${NC} Python: $($PYTHON_CMD --version)"
    if command_exists poetry; then
        echo -e "  ${GREEN}✅${NC} Poetry: $(poetry --version)"
    fi
    if command_exists node; then
        echo -e "  ${GREEN}✅${NC} Node.js: $(node --version)"
    fi
    echo
    
    echo -e "${YELLOW}🚀 快速启动:${NC}"
    echo -e "  ${CYAN}启动数据库:${NC} docker-compose up -d"
    echo -e "  ${CYAN}启动Core服务:${NC} poetry run start-core"
    echo -e "  ${CYAN}启动API服务:${NC} poetry run start-api"
    if command_exists npm; then
        echo -e "  ${CYAN}启动前端:${NC} poetry run start-frontend"
    fi
    echo
    
    echo -e "${YELLOW}🛠️ 开发工具:${NC}"
    echo -e "  ${CYAN}运行测试:${NC} poetry run test"
    echo -e "  ${CYAN}代码格式化:${NC} poetry run format"
    echo -e "  ${CYAN}代码检查:${NC} poetry run lint"
    echo -e "  ${CYAN}健康检查:${NC} poetry run health-check"
    echo
    
    echo -e "${YELLOW}📚 更多信息:${NC}"
    echo -e "  ${CYAN}查看文档:${NC} cat INSTALL.md"
    echo -e "  ${CYAN}项目状态:${NC} cat CURRENT-VERSION-STATUS.md"
    echo
}

# 主函数
main() {
    echo -e "${PURPLE}🌟 天庭智能工作流引擎安装器${NC}"
    echo -e "${CYAN}================================${NC}"
    echo
    
    # 解析命令行参数
    CLEAN_INSTALL=false
    SKIP_NODE=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --clean)
                CLEAN_INSTALL=true
                shift
                ;;
            --skip-node)
                SKIP_NODE=true
                shift
                ;;
            --help|-h)
                echo "用法: $0 [选项]"
                echo "选项:"
                echo "  --clean     清理缓存重新安装"
                echo "  --skip-node 跳过Node.js依赖安装"
                echo "  --help      显示此帮助"
                exit 0
                ;;
            *)
                log_error "未知选项: $1"
                exit 1
                ;;
        esac
    done
    
    # 执行安装步骤
    detect_system
    check_python_version
    check_node_version
    install_poetry
    configure_poetry
    handle_conflicts
    
    if [ "$CLEAN_INSTALL" = true ]; then
        install_python_deps --clean
    else
        install_python_deps
    fi
    
    if [ "$SKIP_NODE" = false ]; then
        install_node_deps
    fi
    
    verify_installation
    setup_project_env
    show_installation_summary
    
    log_success "安装流程完成！"
}

# 错误处理
trap 'log_error "安装过程中发生错误，请检查日志"; exit 1' ERR

# 执行主函数
main "$@"
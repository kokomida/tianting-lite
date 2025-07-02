#!/bin/bash

# 天庭系统环境设置脚本
# 解决每次都要设置PATH的问题

echo "🌟 设置天庭系统环境..."

# 设置Poetry PATH
export PATH="$HOME/.local/bin:$PATH"

# 进入项目目录（如果不在的话）
if [ ! -f "pyproject.toml" ]; then
    cd /mnt/d/kokovsc/koko/Python/promptX+/tianting/v1.0-intelligent-workflow
fi

# 验证环境
if command -v poetry >/dev/null 2>&1; then
    echo "✅ Poetry环境已设置"
    echo "📁 当前目录: $(pwd)"
    echo "🎯 可以使用以下命令："
    echo "   ./quick-start.sh     # 启动所有服务"
    echo "   ./quick-start.sh status  # 查看状态"
    echo "   poetry run test      # 运行测试"
else
    echo "❌ Poetry环境设置失败"
    echo "请检查是否已正确安装Poetry"
fi

# 创建便捷别名
alias tt-start="./quick-start.sh"
alias tt-stop="./quick-start.sh stop"
alias tt-status="./quick-start.sh status"
alias tt-logs="./quick-start.sh logs"

echo "🔗 便捷别名已创建："
echo "   tt-start    # 启动服务"
echo "   tt-stop     # 停止服务"
echo "   tt-status   # 查看状态"
echo "   tt-logs     # 查看日志"
echo ""
echo "💡 提示: 在新终端中运行 'source setup-env.sh' 来设置环境"
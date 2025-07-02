#!/bin/bash
# Claude Control Tower - 实时监控器
# 生成时间: 2025-06-30T09:55:57.853Z
# 作者: 鲁班

echo "📊 Claude Control Tower - 实时监控器"
echo "======================================"
echo "📝 监控 4 个任务的实时输出"
echo "🛑 按 Ctrl+C 停止监控"
echo ""

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 任务颜色数组
COLORS=("$RED" "$GREEN" "$YELLOW" "$BLUE" "$PURPLE" "$CYAN")

# 创建命名管道用于多文件监控
PIPE_DIR="/tmp/claude_monitor_$$"
mkdir -p "$PIPE_DIR"

# 清理函数
cleanup() {
    echo ""
    echo "🛑 停止监控..."
    # 杀死所有tail进程
    for pid in ${TAIL_PIDS[@]}; do
        kill $pid 2>/dev/null
    done
    # 清理临时文件
    rm -rf "$PIPE_DIR"
    echo "✅ 监控已停止"
    exit 0
}

# 设置信号处理
trap cleanup SIGINT SIGTERM

# 存储tail进程ID
TAIL_PIDS=()

# 为每个日志文件启动tail监控
# 监控任务 1
if [ -f "task_1.log" ]; then
    tail -f "task_1.log" | while read line; do
        echo -e "${COLORS[0]}[任务1]${NC} $line"
    done &
    TAIL_PIDS+=($!)
    echo "✅ 开始监控: task_1.log"
else
    echo "⚠️  日志文件不存在: task_1.log"
fi

# 监控任务 2
if [ -f "task_2.log" ]; then
    tail -f "task_2.log" | while read line; do
        echo -e "${COLORS[1]}[任务2]${NC} $line"
    done &
    TAIL_PIDS+=($!)
    echo "✅ 开始监控: task_2.log"
else
    echo "⚠️  日志文件不存在: task_2.log"
fi

# 监控任务 3
if [ -f "task_3.log" ]; then
    tail -f "task_3.log" | while read line; do
        echo -e "${COLORS[2]}[任务3]${NC} $line"
    done &
    TAIL_PIDS+=($!)
    echo "✅ 开始监控: task_3.log"
else
    echo "⚠️  日志文件不存在: task_3.log"
fi

# 监控任务 4
if [ -f "task_4.log" ]; then
    tail -f "task_4.log" | while read line; do
        echo -e "${COLORS[3]}[任务4]${NC} $line"
    done &
    TAIL_PIDS+=($!)
    echo "✅ 开始监控: task_4.log"
else
    echo "⚠️  日志文件不存在: task_4.log"
fi

echo ""
echo "🔄 实时监控中... (刷新间隔: 1500ms)"
echo "💡 提示: 不同颜色代表不同的任务"
echo ""

# 保持脚本运行
wait

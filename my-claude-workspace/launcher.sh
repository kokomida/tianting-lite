#!/bin/bash
# Claude Control Tower - 任务启动器
# 生成时间: 2025-06-30T09:55:57.849Z
# 作者: 鲁班

echo "🚀 Claude Control Tower - 任务启动器"
echo "======================================"

# 清理旧的日志文件
echo "🧹 清理旧日志文件..."
rm -f task_*.log

# 启动所有任务
echo "📋 启动任务 1: claude --project frontend --prompt "设计用户界面""
nohup bash -c 'claude --project frontend --prompt "设计用户界面"' > task_1.log 2>&1 &
echo "   📄 日志文件: task_1.log"
echo "   🆔 进程ID: $!"

echo "📋 启动任务 2: claude --project backend --prompt "开发API接口""
nohup bash -c 'claude --project backend --prompt "开发API接口"' > task_2.log 2>&1 &
echo "   📄 日志文件: task_2.log"
echo "   🆔 进程ID: $!"

echo "📋 启动任务 3: claude --project database --prompt "设计数据库""
nohup bash -c 'claude --project database --prompt "设计数据库"' > task_3.log 2>&1 &
echo "   📄 日志文件: task_3.log"
echo "   🆔 进程ID: $!"

echo "📋 启动任务 4: claude --project testing --prompt "编写测试""
nohup bash -c 'claude --project testing --prompt "编写测试"' > task_4.log 2>&1 &
echo "   📄 日志文件: task_4.log"
echo "   🆔 进程ID: $!"

echo ""
echo "✅ 所有任务已启动完毕！"
echo "📊 运行 './monitor.sh' 开始监控"
echo "🛑 要停止所有任务，运行: pkill -f 'claude'"
echo ""

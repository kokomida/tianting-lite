#!/bin/bash
# scripts/reset-environment.sh

echo "🔄 重置天庭系统环境..."

# 停止所有服务
docker-compose down

# 清理Docker卷（谨慎使用）
read -p "是否要清理数据库数据？这将删除所有数据 (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose down -v
    echo "✅ 数据卷已清理"
fi

# 重新启动
echo "重新启动基础服务..."
docker-compose up -d postgres redis

echo "✅ 环境重置完成"
#!/bin/bash
# scripts/stop-all-services.sh

echo "🛑 停止天庭系统所有服务..."

docker-compose down

echo "✅ 所有服务已停止"
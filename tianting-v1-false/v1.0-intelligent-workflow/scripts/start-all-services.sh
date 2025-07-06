#!/bin/bash
# scripts/start-all-services.sh

echo "🚀 启动天庭系统所有服务..."

# 启动基础服务
echo "启动基础服务..."
docker-compose up -d postgres redis

# 等待基础服务就绪
echo "等待基础服务启动..."
sleep 10

# 启动应用服务（当Dockerfile就绪时）
# echo "启动应用服务..."
# docker-compose up -d core-service api-service frontend-service

echo "✅ 基础服务启动完成"
echo ""
echo "服务状态："
docker-compose ps

echo ""
echo "服务地址："
echo "- PostgreSQL: localhost:5432" 
echo "- Redis: localhost:6379"
# echo "- Core服务: http://localhost:8001"
# echo "- API服务: http://localhost:8002"  
# echo "- 前端服务: http://localhost:3001"
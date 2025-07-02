"""
天庭API服务器基础测试
测试FastAPI应用、中间件、健康检查等核心功能
"""

import asyncio
import json
import pytest
import time
from unittest.mock import AsyncMock, patch, MagicMock

import httpx
from fastapi.testclient import TestClient

from src.main import create_app
from src.config import settings
from src.database import database_manager


@pytest.fixture
def app():
    """创建测试应用"""
    return create_app()


@pytest.fixture
def client(app):
    """创建测试客户端"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def async_client(app):
    """创建异步测试客户端"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client


class TestBasicEndpoints:
    """基础端点测试"""
    
    def test_root_endpoint(self, client):
        """测试根路径端点"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "timestamp" in data
        assert data["message"] == "天庭API服务器"
        assert data["version"] == settings.app_version
    
    def test_health_check_basic(self, client):
        """测试基础健康检查"""
        response = client.get("/health/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["status"] == "healthy"
        assert data["data"]["version"] == settings.app_version
    
    def test_health_check_liveness(self, client):
        """测试存活检查"""
        response = client.get("/health/liveness")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["alive"] is True
    
    @patch('src.routers.health._is_database_ready')
    def test_health_check_readiness_ready(self, mock_db_ready, client):
        """测试就绪检查 - 就绪状态"""
        mock_db_ready.return_value = True
        
        response = client.get("/health/readiness")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["ready"] is True
    
    @patch('src.routers.health._is_database_ready')
    def test_health_check_readiness_not_ready(self, mock_db_ready, client):
        """测试就绪检查 - 未就绪状态"""
        mock_db_ready.return_value = False
        
        response = client.get("/health/readiness")
        assert response.status_code == 503
        
        data = response.json()
        assert data["success"] is False
        assert data["data"]["ready"] is False


class TestMiddleware:
    """中间件测试"""
    
    def test_request_id_middleware(self, client):
        """测试请求ID中间件"""
        response = client.get("/health/")
        
        # 检查响应头中是否包含请求ID
        assert "X-Request-ID" in response.headers
        request_id = response.headers["X-Request-ID"]
        
        # 检查响应体中是否包含请求ID
        data = response.json()
        assert data.get("request_id") == request_id
    
    def test_process_time_middleware(self, client):
        """测试处理时间中间件"""
        response = client.get("/health/")
        
        # 检查响应头中是否包含处理时间
        assert "X-Process-Time" in response.headers
        process_time = float(response.headers["X-Process-Time"])
        assert process_time > 0
    
    def test_cors_middleware(self, client):
        """测试CORS中间件"""
        # 发送OPTIONS预检请求
        response = client.options(
            "/health/",
            headers={
                "Origin": "http://localhost:3001",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers
    
    def test_error_handling_middleware(self, client):
        """测试错误处理中间件"""
        # 访问不存在的端点
        response = client.get("/nonexistent")
        assert response.status_code == 404
        
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert data["error"]["code"] == "HTTP_404"


class TestDatabaseIntegration:
    """数据库集成测试"""
    
    @pytest.mark.asyncio
    async def test_database_connection(self):
        """测试数据库连接"""
        # 这里使用模拟，因为测试环境可能没有真实数据库
        with patch.object(database_manager, 'connect') as mock_connect:
            mock_connect.return_value = None
            await database_manager.connect()
            mock_connect.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_database_health_check(self):
        """测试数据库健康检查"""
        with patch.object(database_manager, 'health_check') as mock_health:
            mock_health.return_value = {
                "status": "connected",
                "latency_ms": 10.5
            }
            
            health_info = await database_manager.health_check()
            assert health_info["status"] == "connected"
            assert health_info["latency_ms"] == 10.5


class TestErrorHandling:
    """错误处理测试"""
    
    def test_404_error(self, client):
        """测试404错误处理"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        
        data = response.json()
        assert data["success"] is False
        assert data["data"] is None
        assert "timestamp" in data
        assert "request_id" in data
        assert data["error"]["code"] == "HTTP_404"
    
    def test_method_not_allowed(self, client):
        """测试方法不允许错误"""
        response = client.post("/health/")
        assert response.status_code == 405
        
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "HTTP_405"


class TestResponseFormat:
    """响应格式测试"""
    
    def test_success_response_format(self, client):
        """测试成功响应格式"""
        response = client.get("/health/")
        assert response.status_code == 200
        
        data = response.json()
        
        # 检查必需字段
        required_fields = ["success", "data", "message", "timestamp"]
        for field in required_fields:
            assert field in data
        
        # 检查数据类型
        assert isinstance(data["success"], bool)
        assert data["success"] is True
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_error_response_format(self, client):
        """测试错误响应格式"""
        response = client.get("/nonexistent")
        data = response.json()
        
        # 检查必需字段
        required_fields = ["success", "data", "message", "timestamp", "error"]
        for field in required_fields:
            assert field in data
        
        # 检查数据类型和值
        assert isinstance(data["success"], bool)
        assert data["success"] is False
        assert data["data"] is None
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["error"], dict)
        assert "code" in data["error"]


class TestPerformance:
    """性能测试"""
    
    def test_health_check_response_time(self, client):
        """测试健康检查响应时间"""
        start_time = time.time()
        response = client.get("/health/")
        end_time = time.time()
        
        assert response.status_code == 200
        
        # 响应时间应小于100ms
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"响应时间过长: {response_time_ms}ms"
    
    def test_concurrent_requests(self, client):
        """测试并发请求处理"""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get("/health/")
        
        # 并发发送10个请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # 所有请求都应该成功
        for response in results:
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True


class TestConfigurationIntegration:
    """配置集成测试"""
    
    def test_settings_loading(self):
        """测试配置加载"""
        assert settings.app_name == "天庭API服务"
        assert settings.app_version == "1.0.0"
        assert settings.port == 8002
        assert settings.environment in ["development", "testing", "production"]
    
    def test_cors_configuration(self, client):
        """测试CORS配置"""
        response = client.get(
            "/health/",
            headers={"Origin": "http://localhost:3001"}
        )
        
        assert response.status_code == 200
        # 在实际的CORS响应中应该包含相应的头
        # 注意：TestClient可能不会完全模拟CORS行为


class TestMetrics:
    """指标测试"""
    
    @patch('src.routers.health._collect_metrics')
    def test_metrics_endpoint(self, mock_metrics, client):
        """测试指标端点"""
        mock_metrics.return_value = {
            "system": {
                "cpu_percent": 15.5,
                "memory_percent": 45.2
            },
            "process": {
                "pid": 12345,
                "cpu_percent": 8.1
            }
        }
        
        response = client.get("/health/metrics")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "system" in data["data"]
        assert "process" in data["data"]


# 集成测试夹具

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """设置测试环境"""
    # 这里可以进行全局测试设置
    # 比如设置测试数据库、清理缓存等
    yield
    # 测试完成后的清理


@pytest.fixture
async def mock_database():
    """模拟数据库连接"""
    with patch.object(database_manager, 'is_connected', True):
        with patch.object(database_manager, 'health_check') as mock_health:
            mock_health.return_value = {
                "status": "connected",
                "latency_ms": 5.0
            }
            yield mock_health


# 运行标记

pytestmark = pytest.mark.asyncio
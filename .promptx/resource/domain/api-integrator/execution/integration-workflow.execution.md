<execution>
  <constraint>
    ## API集成限制条件
    - **性能约束**：API调用延迟必须在可接受范围内
    - **可靠性约束**：必须处理网络故障和服务不可用
    - **安全约束**：API密钥和敏感信息必须安全存储
    - **成本约束**：API调用成本必须在预算范围内
    - **合规约束**：必须遵循各服务提供商的使用条款
  </constraint>

  <rule>
    ## API集成强制规则
    - **错误处理**：所有API调用必须有完善的错误处理
    - **重试机制**：临时失败必须有指数退避重试
    - **超时控制**：所有API调用必须设置合理超时
    - **日志记录**：所有API调用必须详细记录
    - **权限验证**：API调用前必须验证权限和配额
  </rule>

  <guideline>
    ## API集成指导原则
    - **统一接口**：为不同API提供统一的调用接口
    - **异步优先**：优先使用异步调用提高性能
    - **缓存策略**：合理使用缓存减少API调用
    - **降级处理**：设计服务降级和熔断机制
    - **监控可观测**：提供完善的监控和调试信息
  </guideline>

  <process>
    ## 🌐 API集成工作流程

    ### API集成架构
    ```mermaid
    graph TD
        A[Augment Agent] --> B[API网关]
        B --> C[服务适配器]
        C --> D[外部服务]
        
        B --> B1[认证管理]
        B --> B2[限流控制]
        B --> B3[缓存层]
        B --> B4[监控日志]
        
        C --> C1[HTTP适配器]
        C --> C2[GraphQL适配器]
        C --> C3[WebSocket适配器]
        C --> C4[gRPC适配器]
        
        D --> D1[OpenAI API]
        D --> D2[GitHub API]
        D --> D3[数据库服务]
        D --> D4[第三方工具]
    ```

    ### 第一阶段：API发现与分析
    ```mermaid
    flowchart TD
        A[API需求分析] --> B[API调研]
        B --> C[接口设计]
        C --> D[认证方案]
        D --> E[测试验证]
        E --> F[文档编写]
        
        B --> B1[功能评估]
        B --> B2[性能评估]
        B --> B3[成本评估]
        B --> B4[可靠性评估]
        
        C --> C1[请求格式]
        C --> C2[响应格式]
        C --> C3[错误码定义]
        C --> C4[参数验证]
        
        D --> D1[API Key]
        D --> D2[OAuth 2.0]
        D --> D3[JWT Token]
        D --> D4[自定义认证]
    ```

    ### 第二阶段：集成开发与测试
    ```mermaid
    graph TD
        A[集成开发] --> B[适配器开发]
        B --> C[错误处理]
        C --> D[性能优化]
        D --> E[集成测试]
        E --> F[部署上线]
        
        B --> B1[请求封装]
        B --> B2[响应解析]
        B --> B3[数据转换]
        
        C --> C1[重试机制]
        C --> C2[熔断器]
        C --> C3[降级策略]
        
        D --> D1[连接池]
        D --> D2[缓存策略]
        D --> D3[批量处理]
        
        E --> E1[单元测试]
        E --> E2[集成测试]
        E --> E3[压力测试]
    ```

    ### 第三阶段：监控与维护
    ```mermaid
    flowchart LR
        A[运行监控] --> B[性能分析]
        B --> C[问题诊断]
        C --> D[优化改进]
        D --> E[版本升级]
        E --> A
        
        B --> B1[响应时间]
        B --> B2[成功率]
        B --> B3[错误分布]
        
        C --> C1[日志分析]
        C --> C2[链路追踪]
        C --> C3[异常告警]
        
        D --> D1[性能调优]
        D --> D2[架构优化]
        D --> D3[配置调整]
    ```

    ## 🛠️ API集成框架实现

    ### 通用API客户端
    ```python
    import asyncio
    import aiohttp
    import json
    import time
    from typing import Dict, Any, Optional, List
    from dataclasses import dataclass
    from enum import Enum
    import logging

    class AuthType(Enum):
        API_KEY = "api_key"
        BEARER_TOKEN = "bearer_token"
        OAUTH2 = "oauth2"
        BASIC_AUTH = "basic_auth"

    @dataclass
    class APIConfig:
        base_url: str
        auth_type: AuthType
        auth_credentials: Dict[str, str]
        timeout: int = 30
        max_retries: int = 3
        retry_delay: float = 1.0
        rate_limit: Optional[int] = None

    class APIClient:
        def __init__(self, config: APIConfig):
            self.config = config
            self.session = None
            self.logger = logging.getLogger(__name__)
            self._rate_limiter = RateLimiter(config.rate_limit) if config.rate_limit else None
        
        async def __aenter__(self):
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
                headers=self._get_auth_headers()
            )
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if self.session:
                await self.session.close()
        
        def _get_auth_headers(self) -> Dict[str, str]:
            """获取认证头"""
            headers = {"Content-Type": "application/json"}
            
            if self.config.auth_type == AuthType.API_KEY:
                headers["X-API-Key"] = self.config.auth_credentials["api_key"]
            elif self.config.auth_type == AuthType.BEARER_TOKEN:
                headers["Authorization"] = f"Bearer {self.config.auth_credentials['token']}"
            elif self.config.auth_type == AuthType.BASIC_AUTH:
                import base64
                credentials = f"{self.config.auth_credentials['username']}:{self.config.auth_credentials['password']}"
                encoded = base64.b64encode(credentials.encode()).decode()
                headers["Authorization"] = f"Basic {encoded}"
            
            return headers
        
        async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
            """通用请求方法"""
            url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            
            # 速率限制
            if self._rate_limiter:
                await self._rate_limiter.acquire()
            
            # 重试机制
            for attempt in range(self.config.max_retries + 1):
                try:
                    start_time = time.time()
                    
                    async with self.session.request(method, url, **kwargs) as response:
                        response_time = time.time() - start_time
                        
                        # 记录请求日志
                        self.logger.info(f"API Request: {method} {url} - {response.status} - {response_time:.3f}s")
                        
                        if response.status == 429:  # Rate limited
                            if attempt < self.config.max_retries:
                                delay = self.config.retry_delay * (2 ** attempt)
                                self.logger.warning(f"Rate limited, retrying in {delay}s")
                                await asyncio.sleep(delay)
                                continue
                        
                        response.raise_for_status()
                        
                        # 解析响应
                        if response.content_type == 'application/json':
                            return await response.json()
                        else:
                            return {"content": await response.text()}
                
                except aiohttp.ClientError as e:
                    if attempt < self.config.max_retries:
                        delay = self.config.retry_delay * (2 ** attempt)
                        self.logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {delay}s: {e}")
                        await asyncio.sleep(delay)
                    else:
                        self.logger.error(f"Request failed after {self.config.max_retries} retries: {e}")
                        raise
        
        async def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
            """GET请求"""
            return await self.request("GET", endpoint, params=params)
        
        async def post(self, endpoint: str, data: Dict = None, json_data: Dict = None) -> Dict[str, Any]:
            """POST请求"""
            kwargs = {}
            if data:
                kwargs["data"] = data
            if json_data:
                kwargs["json"] = json_data
            return await self.request("POST", endpoint, **kwargs)
        
        async def put(self, endpoint: str, data: Dict = None, json_data: Dict = None) -> Dict[str, Any]:
            """PUT请求"""
            kwargs = {}
            if data:
                kwargs["data"] = data
            if json_data:
                kwargs["json"] = json_data
            return await self.request("PUT", endpoint, **kwargs)
        
        async def delete(self, endpoint: str) -> Dict[str, Any]:
            """DELETE请求"""
            return await self.request("DELETE", endpoint)

    class RateLimiter:
        def __init__(self, max_calls_per_second: int):
            self.max_calls = max_calls_per_second
            self.calls = []
        
        async def acquire(self):
            """获取调用许可"""
            now = time.time()
            
            # 清理过期的调用记录
            self.calls = [call_time for call_time in self.calls if now - call_time < 1.0]
            
            # 检查是否超过限制
            if len(self.calls) >= self.max_calls:
                sleep_time = 1.0 - (now - self.calls[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            
            self.calls.append(now)
    ```

    ### 服务适配器模式
    ```python
    from abc import ABC, abstractmethod
    from typing import Any, Dict, List

    class ServiceAdapter(ABC):
        """服务适配器基类"""
        
        def __init__(self, config: APIConfig):
            self.config = config
            self.client = APIClient(config)
        
        @abstractmethod
        async def health_check(self) -> bool:
            """健康检查"""
            pass
        
        @abstractmethod
        async def get_service_info(self) -> Dict[str, Any]:
            """获取服务信息"""
            pass

    class OpenAIAdapter(ServiceAdapter):
        """OpenAI API适配器"""
        
        async def health_check(self) -> bool:
            """健康检查"""
            try:
                async with self.client as client:
                    response = await client.get("models")
                    return "data" in response
            except Exception:
                return False
        
        async def get_service_info(self) -> Dict[str, Any]:
            """获取服务信息"""
            async with self.client as client:
                models = await client.get("models")
                return {
                    "service": "OpenAI",
                    "available_models": [model["id"] for model in models.get("data", [])],
                    "status": "healthy" if await self.health_check() else "unhealthy"
                }
        
        async def chat_completion(self, messages: List[Dict], model: str = "gpt-3.5-turbo", **kwargs) -> Dict[str, Any]:
            """聊天完成"""
            async with self.client as client:
                payload = {
                    "model": model,
                    "messages": messages,
                    **kwargs
                }
                return await client.post("chat/completions", json_data=payload)
        
        async def create_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
            """创建嵌入"""
            async with self.client as client:
                payload = {
                    "model": model,
                    "input": text
                }
                response = await client.post("embeddings", json_data=payload)
                return response["data"][0]["embedding"]

    class GitHubAdapter(ServiceAdapter):
        """GitHub API适配器"""
        
        async def health_check(self) -> bool:
            """健康检查"""
            try:
                async with self.client as client:
                    response = await client.get("user")
                    return "login" in response
            except Exception:
                return False
        
        async def get_service_info(self) -> Dict[str, Any]:
            """获取服务信息"""
            async with self.client as client:
                user = await client.get("user")
                return {
                    "service": "GitHub",
                    "user": user.get("login"),
                    "status": "healthy" if await self.health_check() else "unhealthy"
                }
        
        async def get_repositories(self, username: str) -> List[Dict[str, Any]]:
            """获取用户仓库"""
            async with self.client as client:
                return await client.get(f"users/{username}/repos")
        
        async def create_issue(self, owner: str, repo: str, title: str, body: str) -> Dict[str, Any]:
            """创建Issue"""
            async with self.client as client:
                payload = {
                    "title": title,
                    "body": body
                }
                return await client.post(f"repos/{owner}/{repo}/issues", json_data=payload)
    ```

    ### 服务编排器
    ```python
    class ServiceOrchestrator:
        """服务编排器"""
        
        def __init__(self):
            self.adapters: Dict[str, ServiceAdapter] = {}
            self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        
        def register_adapter(self, name: str, adapter: ServiceAdapter):
            """注册服务适配器"""
            self.adapters[name] = adapter
            self.circuit_breakers[name] = CircuitBreaker(name)
        
        async def call_service(self, service_name: str, method_name: str, *args, **kwargs) -> Any:
            """调用服务方法"""
            if service_name not in self.adapters:
                raise ValueError(f"Service {service_name} not registered")
            
            adapter = self.adapters[service_name]
            circuit_breaker = self.circuit_breakers[service_name]
            
            # 熔断器检查
            if circuit_breaker.is_open():
                raise Exception(f"Circuit breaker is open for service {service_name}")
            
            try:
                method = getattr(adapter, method_name)
                result = await method(*args, **kwargs)
                circuit_breaker.record_success()
                return result
            
            except Exception as e:
                circuit_breaker.record_failure()
                raise
        
        async def health_check_all(self) -> Dict[str, bool]:
            """检查所有服务健康状态"""
            results = {}
            
            for name, adapter in self.adapters.items():
                try:
                    results[name] = await adapter.health_check()
                except Exception:
                    results[name] = False
            
            return results

    class CircuitBreaker:
        """熔断器"""
        
        def __init__(self, name: str, failure_threshold: int = 5, timeout: int = 60):
            self.name = name
            self.failure_threshold = failure_threshold
            self.timeout = timeout
            self.failure_count = 0
            self.last_failure_time = None
            self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        
        def is_open(self) -> bool:
            """检查熔断器是否打开"""
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "HALF_OPEN"
                    return False
                return True
            return False
        
        def record_success(self):
            """记录成功调用"""
            self.failure_count = 0
            self.state = "CLOSED"
        
        def record_failure(self):
            """记录失败调用"""
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
    ```

    ## 📊 API监控与分析

    ### API调用监控
    ```python
    class APIMonitor:
        def __init__(self):
            self.metrics = {}
        
        def record_api_call(self, service: str, method: str, success: bool, 
                          response_time: float, status_code: int = None):
            """记录API调用指标"""
            key = f"{service}.{method}"
            
            if key not in self.metrics:
                self.metrics[key] = {
                    "total_calls": 0,
                    "success_calls": 0,
                    "total_response_time": 0,
                    "max_response_time": 0,
                    "min_response_time": float('inf'),
                    "status_codes": {}
                }
            
            metrics = self.metrics[key]
            metrics["total_calls"] += 1
            
            if success:
                metrics["success_calls"] += 1
            
            metrics["total_response_time"] += response_time
            metrics["max_response_time"] = max(metrics["max_response_time"], response_time)
            metrics["min_response_time"] = min(metrics["min_response_time"], response_time)
            
            if status_code:
                metrics["status_codes"][status_code] = metrics["status_codes"].get(status_code, 0) + 1
        
        def get_metrics_report(self) -> Dict[str, Any]:
            """获取指标报告"""
            report = {}
            
            for key, metrics in self.metrics.items():
                success_rate = metrics["success_calls"] / metrics["total_calls"] if metrics["total_calls"] > 0 else 0
                avg_response_time = metrics["total_response_time"] / metrics["total_calls"] if metrics["total_calls"] > 0 else 0
                
                report[key] = {
                    "total_calls": metrics["total_calls"],
                    "success_rate": success_rate,
                    "avg_response_time_ms": avg_response_time * 1000,
                    "max_response_time_ms": metrics["max_response_time"] * 1000,
                    "min_response_time_ms": metrics["min_response_time"] * 1000,
                    "status_code_distribution": metrics["status_codes"]
                }
            
            return report
    ```

    ## 🔄 缓存策略

    ### 智能缓存管理
    ```python
    import hashlib
    from typing import Optional, Any
    import json
    import time

    class APICache:
        def __init__(self, default_ttl: int = 300):
            self.cache = {}
            self.default_ttl = default_ttl
        
        def _generate_key(self, service: str, method: str, args: tuple, kwargs: dict) -> str:
            """生成缓存键"""
            data = {
                "service": service,
                "method": method,
                "args": args,
                "kwargs": kwargs
            }
            content = json.dumps(data, sort_keys=True)
            return hashlib.md5(content.encode()).hexdigest()
        
        def get(self, service: str, method: str, args: tuple, kwargs: dict) -> Optional[Any]:
            """获取缓存"""
            key = self._generate_key(service, method, args, kwargs)
            
            if key in self.cache:
                value, expiry = self.cache[key]
                if time.time() < expiry:
                    return value
                else:
                    del self.cache[key]
            
            return None
        
        def set(self, service: str, method: str, args: tuple, kwargs: dict, 
               value: Any, ttl: Optional[int] = None):
            """设置缓存"""
            key = self._generate_key(service, method, args, kwargs)
            expiry = time.time() + (ttl or self.default_ttl)
            self.cache[key] = (value, expiry)
        
        def invalidate(self, pattern: str = None):
            """清理缓存"""
            if pattern:
                keys_to_remove = [k for k in self.cache.keys() if pattern in k]
                for key in keys_to_remove:
                    del self.cache[key]
            else:
                self.cache.clear()
    ```
  </process>

  <criteria>
    ## API集成评价标准

    ### 性能指标
    - ✅ API调用延迟 ≤ 2秒
    - ✅ 并发调用支持 ≥ 100 req/s
    - ✅ 缓存命中率 ≥ 70%
    - ✅ 重试成功率 ≥ 90%

    ### 可靠性指标
    - ✅ API调用成功率 ≥ 99%
    - ✅ 错误恢复时间 ≤ 30秒
    - ✅ 熔断器响应及时
    - ✅ 降级策略有效

    ### 安全性指标
    - ✅ 认证机制完善
    - ✅ 敏感信息加密存储
    - ✅ 访问日志完整
    - ✅ 权限控制严格

    ### 可维护性指标
    - ✅ 接口设计统一
    - ✅ 错误信息清晰
    - ✅ 监控指标完善
    - ✅ 文档详细准确
  </criteria>
</execution>

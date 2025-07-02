<execution>
  <constraint>
    ## MCP协议开发限制条件
    - **协议兼容性**：必须严格遵循MCP协议规范
    - **性能约束**：工具调用延迟必须在可接受范围内
    - **安全约束**：工具执行必须有安全边界和权限控制
    - **稳定性约束**：协议通信必须可靠，支持错误恢复
    - **扩展性约束**：架构必须支持新工具的动态添加
  </constraint>

  <rule>
    ## MCP协议强制规则
    - **标准遵循**：严格遵循MCP协议标准和最佳实践
    - **错误处理**：所有工具调用必须有完善的错误处理
    - **参数验证**：工具参数必须经过严格验证
    - **日志记录**：所有协议交互必须详细记录
    - **版本兼容**：支持MCP协议的向后兼容性
  </rule>

  <guideline>
    ## MCP协议指导原则
    - **简洁设计**：工具接口设计简洁明了
    - **高效通信**：优化协议通信效率
    - **安全第一**：确保工具执行的安全性
    - **用户友好**：提供清晰的工具描述和使用说明
    - **可观测性**：提供完善的调试和监控能力
  </guideline>

  <process>
    ## 🔌 MCP协议开发流程

    ### MCP服务器架构
    ```mermaid
    graph TD
        A[Augment Client] --> B[MCP Server]
        B --> C[Tool Registry]
        C --> D[Tool Executor]
        D --> E[Result Processor]
        E --> F[Response Builder]
        F --> A
        
        C --> C1[PromptX Tools]
        C --> C2[Memory Tools]
        C --> C3[Search Tools]
        C --> C4[Data Tools]
        
        D --> D1[Parameter Validation]
        D --> D2[Security Check]
        D --> D3[Tool Execution]
        D --> D4[Error Handling]
        
        E --> E1[Result Formatting]
        E --> E2[Error Mapping]
        E --> E3[Logging]
    ```

    ### 第一阶段：工具注册与发现
    ```mermaid
    flowchart TD
        A[MCP Server启动] --> B[工具扫描]
        B --> C[工具注册]
        C --> D[接口验证]
        D --> E[元数据生成]
        E --> F[服务发布]
        
        B --> B1[扫描工具目录]
        B --> B2[加载工具模块]
        B --> B3[解析工具定义]
        
        C --> C1[工具名称注册]
        C --> C2[参数模式注册]
        C --> C3[权限配置]
        
        D --> D1[接口完整性检查]
        D --> D2[参数类型验证]
        D --> D3[安全策略验证]
        
        E --> E1[生成工具描述]
        E --> E2[创建JSON Schema]
        E --> E3[构建帮助文档]
    ```

    ### 第二阶段：工具调用处理
    ```mermaid
    graph TD
        A[工具调用请求] --> B[请求解析]
        B --> C[参数验证]
        C --> D[权限检查]
        D --> E[工具执行]
        E --> F[结果处理]
        F --> G[响应构建]
        G --> H[响应返回]
        
        C --> C1[参数类型检查]
        C --> C2[必需参数检查]
        C --> C3[参数范围验证]
        
        D --> D1[用户权限验证]
        D --> D2[工具权限检查]
        D --> D3[资源访问控制]
        
        E --> E1[同步执行]
        E --> E2[异步执行]
        E --> E3[批量执行]
        
        F --> F1[成功结果处理]
        F --> F2[错误结果处理]
        F --> F3[部分成功处理]
    ```

    ### 第三阶段：错误处理与恢复
    ```mermaid
    flowchart LR
        A[错误发生] --> B[错误分类]
        B --> C[错误处理]
        C --> D[恢复策略]
        D --> E[结果返回]
        
        B --> B1[协议错误]
        B --> B2[参数错误]
        B --> B3[执行错误]
        B --> B4[系统错误]
        
        C --> C1[错误日志记录]
        C --> C2[错误信息格式化]
        C --> C3[用户友好提示]
        
        D --> D1[重试机制]
        D --> D2[降级处理]
        D --> D3[回滚操作]
    ```

    ## 🛠️ MCP服务器实现

    ### Python MCP服务器框架
    ```python
    import asyncio
    import json
    from typing import Dict, Any, List, Optional
    from dataclasses import dataclass
    from abc import ABC, abstractmethod
    
    @dataclass
    class ToolDefinition:
        name: str
        description: str
        parameters: Dict[str, Any]
        required: List[str]
        handler: callable
        permissions: List[str] = None
    
    class MCPTool(ABC):
        @abstractmethod
        async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
            pass
        
        @abstractmethod
        def get_definition(self) -> ToolDefinition:
            pass
    
    class MCPServer:
        def __init__(self):
            self.tools: Dict[str, MCPTool] = {}
            self.running = False
        
        def register_tool(self, tool: MCPTool):
            """注册工具"""
            definition = tool.get_definition()
            self.tools[definition.name] = tool
            print(f"Registered tool: {definition.name}")
        
        async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
            """处理MCP请求"""
            try:
                method = request.get('method')
                params = request.get('params', {})
                
                if method == 'tools/list':
                    return await self.list_tools()
                elif method == 'tools/call':
                    return await self.call_tool(params)
                else:
                    return self.error_response(f"Unknown method: {method}")
            
            except Exception as e:
                return self.error_response(str(e))
        
        async def list_tools(self) -> Dict[str, Any]:
            """列出所有可用工具"""
            tools = []
            for tool in self.tools.values():
                definition = tool.get_definition()
                tools.append({
                    'name': definition.name,
                    'description': definition.description,
                    'inputSchema': {
                        'type': 'object',
                        'properties': definition.parameters,
                        'required': definition.required
                    }
                })
            
            return {
                'tools': tools
            }
        
        async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """调用工具"""
            tool_name = params.get('name')
            arguments = params.get('arguments', {})
            
            if tool_name not in self.tools:
                return self.error_response(f"Tool not found: {tool_name}")
            
            tool = self.tools[tool_name]
            
            # 参数验证
            validation_error = self.validate_parameters(tool, arguments)
            if validation_error:
                return self.error_response(validation_error)
            
            # 执行工具
            try:
                result = await tool.execute(arguments)
                return {
                    'content': [
                        {
                            'type': 'text',
                            'text': json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            except Exception as e:
                return self.error_response(f"Tool execution failed: {str(e)}")
        
        def validate_parameters(self, tool: MCPTool, arguments: Dict[str, Any]) -> Optional[str]:
            """验证工具参数"""
            definition = tool.get_definition()
            
            # 检查必需参数
            for required_param in definition.required:
                if required_param not in arguments:
                    return f"Missing required parameter: {required_param}"
            
            # 检查参数类型（简化版本）
            for param_name, param_value in arguments.items():
                if param_name in definition.parameters:
                    expected_type = definition.parameters[param_name].get('type')
                    if expected_type and not self.check_type(param_value, expected_type):
                        return f"Invalid type for parameter {param_name}: expected {expected_type}"
            
            return None
        
        def check_type(self, value: Any, expected_type: str) -> bool:
            """检查参数类型"""
            type_mapping = {
                'string': str,
                'integer': int,
                'number': (int, float),
                'boolean': bool,
                'array': list,
                'object': dict
            }
            
            expected_python_type = type_mapping.get(expected_type)
            if expected_python_type:
                return isinstance(value, expected_python_type)
            
            return True
        
        def error_response(self, message: str) -> Dict[str, Any]:
            """构建错误响应"""
            return {
                'isError': True,
                'content': [
                    {
                        'type': 'text',
                        'text': f"Error: {message}"
                    }
                ]
            }
    ```

    ### PromptX集成工具示例
    ```python
    class PromptXActionTool(MCPTool):
        def __init__(self):
            self.promptx_client = None  # 初始化PromptX客户端
        
        async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
            role = parameters.get('role')
            
            try:
                # 调用PromptX激活角色
                result = await self.activate_role(role)
                return {
                    'success': True,
                    'role': role,
                    'message': f"Successfully activated role: {role}",
                    'result': result
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
        
        def get_definition(self) -> ToolDefinition:
            return ToolDefinition(
                name='promptx_action',
                description='Activate a PromptX role for specialized AI capabilities',
                parameters={
                    'role': {
                        'type': 'string',
                        'description': 'The role ID to activate (e.g., "data-cleaner", "memory-manager")'
                    }
                },
                required=['role'],
                handler=self.execute
            )
        
        async def activate_role(self, role: str):
            # 实际的PromptX角色激活逻辑
            # 这里需要集成实际的PromptX API
            return f"Role {role} activated successfully"
    
    class MemorySearchTool(MCPTool):
        def __init__(self, memory_manager):
            self.memory_manager = memory_manager
        
        async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
            query = parameters.get('query')
            limit = parameters.get('limit', 10)
            threshold = parameters.get('threshold', 0.7)
            
            try:
                results = self.memory_manager.retrieve_memories(query, limit, threshold)
                return {
                    'success': True,
                    'query': query,
                    'results': [
                        {
                            'id': r[0],
                            'content': r[1],
                            'similarity': r[2]
                        } for r in results
                    ]
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
        
        def get_definition(self) -> ToolDefinition:
            return ToolDefinition(
                name='memory_search',
                description='Search through stored memories using semantic similarity',
                parameters={
                    'query': {
                        'type': 'string',
                        'description': 'The search query text'
                    },
                    'limit': {
                        'type': 'integer',
                        'description': 'Maximum number of results to return',
                        'default': 10
                    },
                    'threshold': {
                        'type': 'number',
                        'description': 'Minimum similarity threshold (0.0-1.0)',
                        'default': 0.7
                    }
                },
                required=['query'],
                handler=self.execute
            )
    ```

    ## 📊 协议性能监控

    ### 性能指标收集
    ```python
    import time
    from collections import defaultdict
    
    class MCPMetrics:
        def __init__(self):
            self.call_counts = defaultdict(int)
            self.call_times = defaultdict(list)
            self.error_counts = defaultdict(int)
        
        def record_call(self, tool_name: str, duration: float, success: bool):
            self.call_counts[tool_name] += 1
            self.call_times[tool_name].append(duration)
            if not success:
                self.error_counts[tool_name] += 1
        
        def get_stats(self) -> Dict[str, Any]:
            stats = {}
            for tool_name in self.call_counts:
                times = self.call_times[tool_name]
                stats[tool_name] = {
                    'total_calls': self.call_counts[tool_name],
                    'error_count': self.error_counts[tool_name],
                    'error_rate': self.error_counts[tool_name] / self.call_counts[tool_name],
                    'avg_duration': sum(times) / len(times) if times else 0,
                    'max_duration': max(times) if times else 0,
                    'min_duration': min(times) if times else 0
                }
            return stats
    ```

    ## 🔄 协议优化策略

    ### 批量操作支持
    ```mermaid
    graph TD
        A[批量请求] --> B[请求分组]
        B --> C[并行执行]
        C --> D[结果聚合]
        D --> E[批量响应]
        
        B --> B1[相同工具分组]
        B --> B2[依赖关系分析]
        
        C --> C1[线程池执行]
        C --> C2[异步执行]
        
        D --> D1[成功结果合并]
        D --> D2[错误结果处理]
    ```

    ### 缓存机制
    ```python
    class MCPCache:
        def __init__(self, ttl=300):  # 5分钟TTL
            self.cache = {}
            self.ttl = ttl
        
        def get(self, key: str) -> Optional[Any]:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    return value
                else:
                    del self.cache[key]
            return None
        
        def set(self, key: str, value: Any):
            self.cache[key] = (value, time.time())
        
        def invalidate(self, pattern: str = None):
            if pattern:
                keys_to_remove = [k for k in self.cache.keys() if pattern in k]
                for key in keys_to_remove:
                    del self.cache[key]
            else:
                self.cache.clear()
    ```
  </process>

  <criteria>
    ## MCP协议评价标准

    ### 协议兼容性
    - ✅ 严格遵循MCP规范
    - ✅ 支持标准工具接口
    - ✅ 向后兼容性良好
    - ✅ 错误处理规范

    ### 性能指标
    - ✅ 工具调用延迟 ≤ 100ms
    - ✅ 并发处理能力 ≥ 100 req/s
    - ✅ 内存使用合理
    - ✅ CPU使用率 ≤ 80%

    ### 可靠性
    - ✅ 错误恢复能力强
    - ✅ 系统可用性 ≥ 99.5%
    - ✅ 数据一致性保证
    - ✅ 安全边界完善

    ### 可维护性
    - ✅ 代码结构清晰
    - ✅ 文档完整准确
    - ✅ 调试信息丰富
    - ✅ 监控指标完善
  </criteria>
</execution>

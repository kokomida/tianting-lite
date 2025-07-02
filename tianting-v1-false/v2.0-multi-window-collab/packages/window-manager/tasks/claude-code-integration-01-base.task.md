// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业分布式系统架构师的思维模式思考，遵循微服务设计原则，确保系统的可扩展性、可靠性和架构一致性。我承诺：
- 以可扩展、高可用的分布式架构为核心指导思想
- 先理解系统需求，再实现技术方案，通过测试验证系统稳定性
- 确保所有实现与天庭系统整体架构保持一致
- 严格遵循微服务最佳实践和进程管理规范

## 执行承诺
我将遵循严格的执行流程，不偏离既定规范。我承诺：

**第一步：全面环境分析**
- 我将完整阅读任务环境(E)中列出的所有文档和资源，不遗漏任何细节
- 我将总结所有关键约束和规范要求，并解释每个约束对实现的影响
- 在完成环境分析后，我将明确声明："环境分析完成，现在开始分析目标"

**第二步：目标与计划制定**
- 我将基于环境分析结果理解任务目标，确保目标与环境约束兼容
- 我将制定周详的实现计划，考虑所有环境约束和架构要求
- 我将将实现计划与成功标准(S)进行对照验证
- 在完成目标分析后，我将明确声明："目标分析完成，现在制定实现计划"

**第三步：测试驱动实现**
- 我将严格按照测试优先级实现功能
- 每完成一个功能点，我将立即运行相关测试验证
- 遇到测试失败时，我将使用日志和系统性调试方法而非依赖猜测
- 我将确保实现满足所有测试要求，不妥协代码质量
- 我将确保代码实现符合分布式系统设计原则，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：基础任务重点验证相关单元测试和系统集成
- 自我验证：
  * 我将执行完整的进程管理测试确保窗口稳定性
  * 我将执行负载测试确保系统可扩展性
  * 我将确认没有资源泄漏和内存泄漏
  * 在验证通过后，我将明确声明："自我验证完成，窗口管理系统稳定运行，集成测试通过"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合分布式系统设计原则的实现代码
- 我绝不依赖猜测解决问题，而是使用日志和系统性调试方法
- 如果我需要修改测试，我将明确说明修改理由并请求人类审批
- 我绝不在未理清系统架构全貌的情况下，直接开始编码

## 调试规范
- 遇到系统问题时，我将：
  * 首先检查进程状态和资源使用情况
  * 分析系统日志和错误堆栈
  * 检查进程间通信和状态同步
  * 验证API调用和网络连接
  * 追踪问题根源至具体组件
- 当我需要添加日志时，我将：
  * 在关键系统操作处记录详细状态
  * 在进程生命周期关键点记录事件
  * 在API调用处记录请求和响应
  * 在错误处理处记录完整上下文

## 权利
- 我有权利在设计本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让系统更加稳定和高效

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: Claude Code窗口集成管理系统（基础任务）

**目标(O)**:
- **功能目标**:
  - 建立稳定的Claude Code实例管理系统
  - 实现多窗口的生命周期管理和监控
  - 提供窗口池的动态分配和资源管理
  - 为多窗口协作奠定可靠的基础设施

- **执行任务**:
  - 创建文件:
    - `packages/window-manager/src/claude_client.py` - Claude Code API客户端
    - `packages/window-manager/src/window_manager.py` - 窗口管理器核心
    - `packages/window-manager/src/process_pool.py` - 进程池管理
    - `packages/window-manager/src/health_monitor.py` - 窗口健康监控
    - `packages/window-manager/src/resource_tracker.py` - 资源使用追踪
    - `packages/window-manager/src/config.py` - 配置管理
    - `packages/window-manager/src/exceptions.py` - 异常定义
    - `packages/window-manager/requirements.txt` - Python依赖
    - `packages/window-manager/tests/test_window_manager.py` - 单元测试
    - `packages/window-manager/tests/test_integration.py` - 集成测试
  - 修改文件:
    - 无（这是window-manager包的第一个任务）
  - 实现功能:
    - Claude Code API的安全认证和调用
    - 窗口实例的创建、启动、停止、销毁
    - 进程池的动态扩缩容管理
    - 窗口健康状态监控和自动恢复
    - 资源使用监控和泄漏检测

- **任务边界**:
  - 包含窗口管理基础设施，不包含任务分发逻辑
  - 包含Claude Code集成，不包含其他AI服务
  - 包含进程管理，不包含分布式集群管理
  - 专注于窗口生命周期，不涉及业务逻辑执行

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/window.ts` - 窗口相关类型定义
  - `packages/common/contracts/window-manager-api.md` - 窗口管理API规范
  - `MVP-0/packages/core/src/claude_client.py` - 参考已有Claude集成
  - `MVP-1/PREPARATION-GUIDE.md` - MVP-1技术架构和要求
  - `packages/common/environments/mvp1-environment-setup.md` - MVP-1环境配置

- **上下文信息**:
  - 包定位：window-manager是MVP-1的核心基础设施包
  - 技术要求：支持4个并发窗口，窗口存活率≥95%
  - 性能要求：窗口启动时间<5秒，故障恢复时间<10秒
  - 依赖关系：依赖shared包类型定义，为其他MVP-1包提供服务
  - 集成要求：与sync-system、task-engine、coordinator包协作

- **规范索引**:
  - Claude Code API官方文档和最佳实践
  - Python多进程编程规范
  - 微服务健康检查标准
  - 进程池管理最佳实践

- **注意事项**:
  - Claude Code API有调用频率和并发限制，需要合理管理
  - 窗口进程可能因为网络、资源等问题异常退出，需要自动恢复
  - 系统资源（内存、CPU、网络）需要监控和保护
  - 窗口间状态需要隔离，避免相互干扰

**实现指导(I)**:
- **算法与流程**:
  - 窗口生命周期管理:
    ```
    窗口请求 → 权限验证 → 实例创建 → 健康检查 → 任务执行 → 状态监控 → 实例回收
    ```
  - 故障恢复流程:
    ```
    故障检测 → 故障分类 → 恢复策略选择 → 实例重建 → 状态恢复 → 服务继续
    ```

- **技术选型**:
  - API客户端：httpx (异步HTTP客户端)
  - 进程管理：multiprocessing + concurrent.futures
  - 健康监控：定时任务 + 事件驱动
  - 资源监控：psutil (系统资源监控)
  - 配置管理：pydantic-settings (类型安全配置)
  - 日志系统：structlog (结构化日志)

- **代码模式**:
  - 窗口管理器核心:
    ```python
    import asyncio
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    from typing import Dict, List, Optional
    import structlog
    from pydantic import BaseModel
    
    logger = structlog.get_logger()
    
    class WindowInstance(BaseModel):
        window_id: str
        process_id: int
        status: str  # 'starting', 'running', 'stopping', 'stopped', 'error'
        created_at: datetime
        last_heartbeat: datetime
        resource_usage: dict
        
    class WindowManager:
        def __init__(self, max_windows: int = 4):
            self.max_windows = max_windows
            self.windows: Dict[str, WindowInstance] = {}
            self.process_pool = ProcessPoolExecutor(max_workers=max_windows)
            self.health_monitor = HealthMonitor()
            self.resource_tracker = ResourceTracker()
            
        async def create_window(self, window_config: dict) -> str:
            """创建新的Claude Code窗口实例"""
            if len(self.windows) >= self.max_windows:
                raise WindowPoolExhausted("窗口池已满")
                
            window_id = str(uuid.uuid4())
            
            try:
                # 1. 创建窗口进程
                future = self.process_pool.submit(
                    self._start_claude_code_process,
                    window_id,
                    window_config
                )
                
                process_id = future.result(timeout=30)  # 30秒超时
                
                # 2. 创建窗口实例记录
                window = WindowInstance(
                    window_id=window_id,
                    process_id=process_id,
                    status='starting',
                    created_at=datetime.utcnow(),
                    last_heartbeat=datetime.utcnow(),
                    resource_usage={}
                )
                
                self.windows[window_id] = window
                
                # 3. 启动健康监控
                await self.health_monitor.start_monitoring(window_id)
                
                # 4. 等待窗口就绪
                await self._wait_for_window_ready(window_id)
                
                logger.info("窗口创建成功", window_id=window_id)
                return window_id
                
            except Exception as e:
                logger.error("窗口创建失败", window_id=window_id, error=str(e))
                await self._cleanup_failed_window(window_id)
                raise
        
        async def destroy_window(self, window_id: str) -> bool:
            """销毁指定的窗口实例"""
            if window_id not in self.windows:
                return False
                
            window = self.windows[window_id]
            
            try:
                # 1. 停止健康监控
                await self.health_monitor.stop_monitoring(window_id)
                
                # 2. 优雅关闭窗口进程
                await self._graceful_shutdown(window)
                
                # 3. 清理资源
                await self._cleanup_window_resources(window_id)
                
                # 4. 移除记录
                del self.windows[window_id]
                
                logger.info("窗口销毁成功", window_id=window_id)
                return True
                
            except Exception as e:
                logger.error("窗口销毁失败", window_id=window_id, error=str(e))
                return False
        
        async def get_window_status(self, window_id: str) -> Optional[WindowInstance]:
            """获取窗口状态"""
            return self.windows.get(window_id)
        
        async def list_windows(self) -> List[WindowInstance]:
            """列出所有窗口"""
            return list(self.windows.values())
        
        async def health_check(self) -> dict:
            """整体健康检查"""
            healthy_windows = sum(
                1 for w in self.windows.values() 
                if w.status == 'running'
            )
            
            return {
                "total_windows": len(self.windows),
                "healthy_windows": healthy_windows,
                "max_windows": self.max_windows,
                "resource_usage": await self.resource_tracker.get_overall_usage()
            }
    ```
  - Claude Code客户端:
    ```python
    import httpx
    from tenacity import retry, stop_after_attempt, wait_exponential
    
    class ClaudeCodeClient:
        def __init__(self, api_key: str, base_url: str = None):
            self.api_key = api_key
            self.base_url = base_url or "https://api.anthropic.com/v1"
            self.client = httpx.AsyncClient(timeout=60.0)
            
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=4, max=10)
        )
        async def create_window_session(self, window_config: dict) -> str:
            """创建Claude Code窗口会话"""
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 4000,
                "system": window_config.get("system_prompt", ""),
                "messages": []
            }
            
            response = await self.client.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise ClaudeAPIError(f"API调用失败: {response.text}")
                
            result = response.json()
            return result.get("id", "")
        
        async def send_message(self, session_id: str, message: str) -> dict:
            """向窗口发送消息"""
            # 实现消息发送逻辑
            pass
            
        async def check_session_health(self, session_id: str) -> bool:
            """检查会话健康状态"""
            # 实现健康检查逻辑
            pass
    ```
  - 健康监控系统:
    ```python
    import asyncio
    from typing import Callable, Dict
    
    class HealthMonitor:
        def __init__(self):
            self.monitors: Dict[str, asyncio.Task] = {}
            self.health_callbacks: Dict[str, Callable] = {}
            
        async def start_monitoring(self, window_id: str):
            """开始监控指定窗口"""
            if window_id in self.monitors:
                return  # 已在监控中
                
            task = asyncio.create_task(self._monitor_window(window_id))
            self.monitors[window_id] = task
            
        async def stop_monitoring(self, window_id: str):
            """停止监控指定窗口"""
            if window_id in self.monitors:
                self.monitors[window_id].cancel()
                del self.monitors[window_id]
                
        async def _monitor_window(self, window_id: str):
            """窗口监控主循环"""
            while True:
                try:
                    # 1. 检查进程状态
                    process_alive = await self._check_process_alive(window_id)
                    
                    # 2. 检查API响应
                    api_responsive = await self._check_api_responsive(window_id)
                    
                    # 3. 检查资源使用
                    resource_healthy = await self._check_resource_usage(window_id)
                    
                    # 4. 综合评估健康状态
                    is_healthy = process_alive and api_responsive and resource_healthy
                    
                    if not is_healthy:
                        await self._handle_unhealthy_window(window_id)
                        
                    # 5. 更新心跳时间
                    await self._update_heartbeat(window_id)
                    
                    await asyncio.sleep(10)  # 10秒检查一次
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error("窗口监控错误", window_id=window_id, error=str(e))
                    await asyncio.sleep(5)  # 错误后等待5秒再试
    ```

- **实现策略**:
  1. 建立Claude Code API客户端和认证机制
  2. 实现基础的窗口生命周期管理
  3. 开发进程池和资源管理系统
  4. 建立健康监控和自动恢复机制
  5. 实现完整的错误处理和日志系统
  6. 编写全面的单元测试和集成测试

- **调试指南**:
  - 窗口管理调试:
    ```python
    # 启用详细日志
    logging.basicConfig(level=logging.DEBUG)
    
    # 窗口状态检查
    async def debug_window_status():
        manager = WindowManager()
        status = await manager.health_check()
        print(f"系统状态: {status}")
        
        for window_id in manager.windows:
            window = await manager.get_window_status(window_id)
            print(f"窗口 {window_id}: {window.status}")
    
    # 资源使用监控
    async def debug_resource_usage():
        tracker = ResourceTracker()
        usage = await tracker.get_overall_usage()
        print(f"资源使用: {usage}")
    ```

**成功标准(S)**:
- **基础达标**:
  - WindowManager类实现完成，接口符合类型定义
  - Claude Code API集成成功，可以稳定创建和管理窗口
  - 所有单元测试通过，代码覆盖率≥80%
  - 支持4个并发窗口的创建、管理、销毁
  - 窗口故障能够自动检测和恢复

- **预期品质**:
  - 窗口启动时间<5秒，销毁时间<3秒
  - 窗口存活率≥95%，故障恢复时间<10秒
  - 系统资源使用合理，无内存泄漏
  - 错误处理完善，异常情况能够优雅降级
  - 日志记录详细，便于问题排查和性能分析

- **卓越表现**:
  - 实现智能的窗口调度和负载均衡
  - 支持窗口的热备份和故障转移
  - 实现预测性的故障检测和预防
  - 提供详细的性能指标和监控面板
  - 支持窗口配置的动态调整和优化
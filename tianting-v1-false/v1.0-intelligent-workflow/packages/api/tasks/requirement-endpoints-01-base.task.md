// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业API开发者的思维模式思考，遵循RESTful设计原则，确保API的可用性、可扩展性和架构一致性。我承诺：
- 以标准化的API设计和服务架构为核心指导思想
- 先理解接口需求，再实现服务逻辑，通过测试验证接口功能
- 确保所有实现与天庭系统整体架构保持一致
- 严格遵微FastAPI最佳实践和HTTP协议规范

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
- 每完成一个API端点，我将立即运行相关测试验证
- 遇到测试失败时，我将使用日志和系统性调试方法而非依赖猜测
- 我将确保实现满足所有测试要求，不妥协代码质量
- 我将确保API实现符合接口契约，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：API任务重点验证接口功能和性能
- 自我验证：
  * 我将执行`python -m pytest`确保所有测试通过
  * 我将执行API性能测试确保响应时间<100ms
  * 我将验证API文档自动生成和接口契约
  * 在验证通过后，我将明确声明："自我验证完成，API功能正确，性能达标"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合API规范的实现代码
- 我绝不依赖猜测解决HTTP协议问题，而是使用日志和系统性调试
- 如果我需要修改API契约，我将明确说明修改理由并请求审批
- 我绝不在未理清API架构全貌的情况下，直接开始编码

## 调试规范
- 遇到API错误时，我将：
  * 首先添加详细日志输出请求和响应信息
  * 分析HTTP状态码和错误响应的准确性
  * 验证请求参数校验和响应格式
  * 追踪问题根源至具体API处理逻辑
  * 确认修复方案符合HTTP规范
- 当我需要调试服务集成时，我将：
  * 记录服务间调用的详细信息
  * 分析数据库连接和事务处理
  * 验证错误处理和熔断机制
  * 确保服务集成符合最佳实践

## 权利
- 我有权利在API设计本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让API实现更加稳定和高效

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 需求管理API端点实现（基础任务）

**目标(O)**:
- **功能目标**:
  - 实现天庭系统需求管理相关的RESTful API端点
  - 建立需求解析和项目规划的HTTP接口
  - 集成core包的业务逻辑服务
  - 为前端提供完整的需求处理API

- **执行任务**:
  - 创建文件:
    - `packages/api/src/routers/requirements.py` - 需求管理路由
    - `packages/api/src/routers/projects.py` - 项目管理路由
    - `packages/api/src/services/core_client.py` - Core包服务客户端
    - `packages/api/src/services/requirement_service.py` - 需求服务层
    - `packages/api/src/services/project_service.py` - 项目服务层
    - `packages/api/src/schemas/requirement_schemas.py` - 需求相关Schemas
    - `packages/api/src/schemas/project_schemas.py` - 项目相关Schemas
    - `packages/api/tests/test_requirements_api.py` - API测试
  - 修改文件:
    - `packages/api/src/main.py` - 注册新路由
    - `packages/api/src/routers/__init__.py` - 导出路由
  - 实现功能:
    - POST /api/requirements/parse - 需求解析端点
    - GET /api/requirements/{id} - 获取需求详情
    - POST /api/projects/generate - 项目规划生成端点
    - GET /api/projects/{id} - 获取项目详情
    - WebSocket /ws/requirements/parse - 实时需求解析
    - 请求验证和错误处理

- **任务边界**:
  - 包含HTTP API实现，不包含业务逻辑
  - 包含core包集成，不包含core包实现
  - 包含API文档生成，不包含前端集成
  - 专注于接口层，不涉及数据存储逻辑

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/api.ts` - API响应类型定义
  - `packages/common/contracts/api-contracts.md` - API接口规范
  - `packages/api/src/main.py` - FastAPI应用基础
  - `packages/core/src/requirement_parser.py` - 业务逻辑接口
  - `packages/core/src/project_planner.py` - 项目规划接口

- **上下文信息**:
  - 包定位：api包专门负责HTTP接口层，调用core包服务
  - 服务通信：通过HTTP调用core包服务（端口8001）
  - 并发开发：基于接口契约可以与core包并发开发
  - 数据格式：严格遵循shared包定义的类型格式
  - 性能要求：API响应时间<100ms（不含业务处理）

- **规范索引**:
  - FastAPI路由和依赖注入最佳实践
  - RESTful API设计标准
  - HTTP状态码使用规范
  - API文档和测试标准

- **注意事项**:
  - API响应格式必须与shared包类型定义完全一致
  - 错误处理必须返回标准化的错误格式
  - 需要实现完整的请求验证和参数校验
  - WebSocket连接需要处理连接管理和错误恢复

**实现指导(I)**:
- **算法与流程**:
  - API请求处理流程:
    ```
    请求接收 → 参数验证 → 服务调用 → 结果转换 → 响应返回
    ```
  - 异步处理流程:
    ```
    请求接收 → 任务创建 → WebSocket通知 → 进度更新 → 结果推送
    ```

- **技术选型**:
  - Web框架：FastAPI 0.104+ (原有选择)
  - HTTP客户端：httpx (调用core包服务)
  - WebSocket：FastAPI内置WebSocket支持
  - 数据验证：Pydantic V2 (与类型对应)
  - 异步任务：asyncio + 后台任务

- **代码模式**:
  - 需求管理路由:
    ```python
    from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
    from fastapi.websockets import WebSocket
    
    router = APIRouter(prefix="/api/requirements", tags=["requirements"])
    
    @router.post("/parse", response_model=ApiResponse[RequirementModel])
    async def parse_requirement(
        request: ParseRequirementRequest,
        background_tasks: BackgroundTasks,
        requirement_service: RequirementService = Depends(get_requirement_service)
    ):
        try:
            # 异步处理长时间任务
            if request.async_mode:
                task_id = await requirement_service.start_parse_task(request.user_input)
                return success_response(
                    data={"task_id": task_id},
                    message="需求解析任务已启动"
                )
            
            # 同步处理
            result = await requirement_service.parse_requirement(request.user_input)
            return success_response(data=result, message="需求解析完成")
            
        except CoreServiceError as e:
            raise HTTPException(status_code=503, detail="核心服务暂时不可用")
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.websocket("/parse/ws")
    async def parse_requirement_ws(websocket: WebSocket):
        await websocket.accept()
        
        try:
            while True:
                # 接收解析请求
                data = await websocket.receive_json()
                user_input = data.get("user_input")
                
                if not user_input:
                    await websocket.send_json({"error": "缺少用户输入"})
                    continue
                
                # 流式处理和进度推送
                async for progress in requirement_service.parse_requirement_stream(user_input):
                    await websocket.send_json({
                        "type": "progress",
                        "data": progress
                    })
                
        except WebSocketDisconnect:
            logger.info("WebSocket连接断开")
        except Exception as e:
            await websocket.send_json({"error": str(e)})
    ```
  - Core服务客户端:
    ```python
    class CoreClient:
        def __init__(self, base_url: str = "http://localhost:8001"):
            self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
        
        async def parse_requirement(self, user_input: str) -> RequirementModel:
            response = await self.client.post(
                "/core/requirements/parse",
                json={"user_input": user_input}
            )
            
            if response.status_code != 200:
                raise CoreServiceError(f"Core服务错误: {response.text}")
            
            result = response.json()
            return RequirementModel(**result["data"])
        
        async def generate_project_plan(self, requirement_id: str) -> ProjectPlan:
            response = await self.client.post(
                "/core/projects/generate",
                json={"requirement_id": requirement_id}
            )
            
            if response.status_code != 200:
                raise CoreServiceError(f"Core服务错误: {response.text}")
            
            result = response.json()
            return ProjectPlan(**result["data"])
    ```
  - 服务层实现:
    ```python
    class RequirementService:
        def __init__(self, core_client: CoreClient):
            self.core_client = core_client
            self.task_manager = TaskManager()
        
        async def parse_requirement(self, user_input: str) -> RequirementModel:
            # 输入验证
            if not user_input or len(user_input.strip()) < 10:
                raise ValidationError("需求描述太短，请提供更详细的信息")
            
            # 调用core服务
            result = await self.core_client.parse_requirement(user_input)
            
            # 结果验证
            if result.confidence_score < 0.3:
                logger.warning(f"需求解析置信度较低: {result.confidence_score}")
            
            return result
        
        async def start_parse_task(self, user_input: str) -> str:
            task_id = str(uuid.uuid4())
            
            # 创建后台任务
            asyncio.create_task(
                self._background_parse_task(task_id, user_input)
            )
            
            return task_id
        
        async def _background_parse_task(self, task_id: str, user_input: str):
            try:
                result = await self.parse_requirement(user_input)
                await self.task_manager.update_task(task_id, "completed", result)
            except Exception as e:
                await self.task_manager.update_task(task_id, "failed", str(e))
    ```

- **实现策略**:
  1. 建立core服务客户端和连接管理
  2. 实现需求管理相关的API端点
  3. 实现项目管理相关的API端点
  4. 添加WebSocket支持和实时通信
  5. 实现全面的错误处理和验证
  6. 编写API集成测试

- **调试指南**:
  - API调试:
    ```python
    import logging
    
    logger = logging.getLogger(__name__)
    
    @router.post("/parse")
    async def parse_requirement(request: ParseRequirementRequest):
        request_id = str(uuid.uuid4())
        logger.info(f"收到需求解析请求: {request_id}")
        logger.debug(f"请求内容: {request.user_input[:100]}...")
        
        try:
            result = await requirement_service.parse_requirement(request.user_input)
            logger.info(f"需求解析成功: {request_id}, 置信度: {result.confidence_score}")
            return success_response(data=result)
            
        except Exception as e:
            logger.error(f"需求解析失败: {request_id}, 错误: {str(e)}")
            raise HTTPException(status_code=500, detail="解析过程中发生错误")
    ```

**成功标准(S)**:
- **基础达标**:
  - 所有API端点实现完成，符合OpenAPI规范
  - Core服务集成成功，能够正常调用业务逻辑
  - 所有API测试通过，包括正常流程和异常情况
  - WebSocket连接稳定，支持实时通信
  - API文档自动生成，在/docs中可访问

- **预期品质**:
  - API响应时间<100ms（不含业务处理时间）
  - 错误处理完善，返回友好的错误信息
  - 请求验证严格，防止无效数据传入
  - 支持异步处理，长时间任务不阻塞接口
  - 日志记录详细，便于问题排查

- **卓越表现**:
  - 实现API限流和安全防护
  - 支持请求缓存和性能优化
  - 实现API版本控制和向后兼容
  - 添加监控指标和健康检查
  - 支持批量操作和事务处理
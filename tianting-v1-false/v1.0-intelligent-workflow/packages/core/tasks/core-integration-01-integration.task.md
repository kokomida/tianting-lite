// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业集成开发者的思维模式思考，遵循系统集成最佳实践，确保组件间的协调性、稳定性和性能一致性。我承诺：
- 以端到端的系统思维和集成验证为核心指导思想
- 先理解各组件接口，再实现集成逻辑，通过测试验证集成效果
- 确保所有实现与天庭系统整体架构保持一致
- 严格遵循微服务集成模式和错误处理规范

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
- 每完成一个集成点，我将立即运行相关测试验证
- 遇到测试失败时，我将使用日志和系统性调试方法而非依赖猜测
- 我将确保实现满足所有测试要求，不妥协代码质量
- 我将确保集成实现符合系统架构，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：集成任务重点验证组件协作和系统稳定性
- 自我验证：
  * 我将执行`python -m pytest`确保所有集成测试通过
  * 我将执行端到端测试确保完整流程正常
  * 我将验证错误处理和异常恢复机制
  * 在验证通过后，我将明确声明："自我验证完成，集成功能正确，系统稳定"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合架构规范的实现代码
- 我绝不依赖猜测解决集成问题，而是使用日志和系统性调试
- 如果我需要修改集成架构，我将明确说明修改理由并请求审批
- 我绝不在未理清系统集成全貌的情况下，直接开始编码

## 调试规范
- 遇到集成错误时，我将：
  * 首先添加详细日志输出各组件间的调用信息
  * 分析服务间通信的数据流和状态变化
  * 验证接口契约和数据格式的一致性
  * 追踪问题根源至具体集成点
  * 确认修复方案符合架构设计
- 当我需要调试性能问题时，我将：
  * 记录各组件的响应时间和资源使用
  * 分析瓶颈点和优化机会
  * 验证负载均衡和缓存策略
  * 确保优化不影响系统稳定性

## 权利
- 我有权利在集成架构本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让集成实现更加稳定和高效

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: Core包需求解析与项目规划集成（集成任务）

**目标(O)**:
- **功能目标**:
  - 集成需求解析器和项目规划生成器，形成完整的核心工作流
  - 实现端到端的"自然语言输入→结构化需求→完整规划"流程
  - 验证core包内部组件的协作和数据流
  - 为API包提供稳定可靠的业务逻辑服务

- **执行任务**:
  - 创建文件:
    - `packages/core/src/workflow_engine.py` - 核心工作流引擎
    - `packages/core/src/data_transformer.py` - 数据转换器
    - `packages/core/src/quality_assessor.py` - 质量评估器
    - `packages/core/src/cache_manager.py` - 缓存管理器
    - `packages/core/tests/integration/test_workflow.py` - 集成测试
  - 修改文件:
    - `packages/core/src/requirement_parser.py` - 添加工作流接口
    - `packages/core/src/project_planner.py` - 添加集成点
  - 实现功能:
    - 需求解析到规划生成的端到端工作流
    - 数据格式转换和兼容性处理
    - 中间结果缓存和性能优化
    - 质量检查和置信度传递
    - 错误处理和回退机制

- **任务边界**:
  - 包含core包内部集成，不包含API层集成
  - 包含工作流编排，不包含分布式处理
  - 包含缓存优化，不包含外部缓存服务
  - 专注于业务逻辑集成，不涉及HTTP接口

**环境(E)**:
- **参考资源**:
  - `packages/core/tasks/requirement-parsing-01-base.task.md` - 需求解析器实现
  - `packages/core/tasks/project-planning-01-base.task.md` - 项目规划器实现
  - `packages/shared/src/types/domain.ts` - 数据类型定义
  - `packages/common/contracts/api-contracts.md` - 工作流接口规范

- **上下文信息**:
  - 前置依赖：requirement-parsing-01-base 和 project-planning-01-base 必须完成
  - 集成场景：用户输入 → 需求解析 → 数据转换 → 规划生成 → 质量评估
  - 性能要求：端到端处理时间<3分钟，成功率≥95%
  - 质量要求：集成测试覆盖率≥90%，数据一致性保证

- **规范索引**:
  - Python异步编程最佳实践
  - 工作流引擎设计模式
  - 数据管道设计原则
  - 集成测试策略标准

- **注意事项**:
  - 必须处理AI服务的不确定性和可能的失败
  - 数据转换必须保证类型安全和数据完整性
  - 缓存策略要平衡性能和数据新鲜度
  - 错误处理要提供详细的诊断信息

**实现指导(I)**:
- **算法与流程**:
  - 端到端工作流:
    ```
    用户输入 → 需求解析 → 数据验证 → 格式转换 → 规划生成 → 质量评估 → 结果返回
    ```
  - 错误处理流程:
    ```
    异常捕获 → 错误分类 → 重试策略 → 回退方案 → 用户通知
    ```

- **技术选型**:
  - 工作流引擎：自定义异步工作流（轻量级）
  - 缓存策略：内存缓存 + Redis（可选）
  - 数据验证：pydantic（严格验证）
  - 监控记录：structlog（结构化日志）
  - 重试机制：tenacity（指数退避）

- **代码模式**:
  - 工作流引擎:
    ```python
    class CoreWorkflowEngine:
        def __init__(self):
            self.requirement_parser = RequirementParser()
            self.project_planner = ProjectPlanner()
            self.data_transformer = DataTransformer()
            self.quality_assessor = QualityAssessor()
            self.cache_manager = CacheManager()
        
        async def execute_requirement_to_plan_workflow(
            self, 
            user_input: str, 
            user_id: Optional[str] = None
        ) -> WorkflowResult:
            workflow_id = str(uuid.uuid4())
            
            try:
                # 1. 检查缓存
                cached_result = await self.cache_manager.get_cached_result(user_input)
                if cached_result:
                    logger.info(f"工作流 {workflow_id}: 使用缓存结果")
                    return cached_result
                
                # 2. 需求解析
                logger.info(f"工作流 {workflow_id}: 开始需求解析")
                requirement = await self.requirement_parser.parse_requirement(user_input)
                
                # 3. 数据转换
                logger.info(f"工作流 {workflow_id}: 数据转换中")
                planning_input = self.data_transformer.requirement_to_planning_input(requirement)
                
                # 4. 项目规划生成
                logger.info(f"工作流 {workflow_id}: 生成项目规划")
                plan = await self.project_planner.generate_plan(planning_input)
                
                # 5. 质量评估
                logger.info(f"工作流 {workflow_id}: 质量评估中")
                quality_metrics = await self.quality_assessor.assess_quality(requirement, plan)
                
                # 6. 构建结果
                result = WorkflowResult(
                    workflow_id=workflow_id,
                    requirement=requirement,
                    plan=plan,
                    quality_metrics=quality_metrics,
                    processing_time_ms=time.time() * 1000 - start_time
                )
                
                # 7. 缓存结果
                await self.cache_manager.cache_result(user_input, result)
                
                logger.info(f"工作流 {workflow_id}: 执行完成")
                return result
                
            except Exception as e:
                logger.error(f"工作流 {workflow_id}: 执行失败 - {str(e)}")
                return await self._handle_workflow_error(e, workflow_id)
    ```
  - 数据转换器:
    ```python
    class DataTransformer:
        def requirement_to_planning_input(self, requirement: RequirementModel) -> PlanningInput:
            """将需求模型转换为规划器输入格式"""
            return PlanningInput(
                project_type=requirement.parsed_data.project_type,
                target_users=self._simplify_user_groups(requirement.parsed_data.target_users),
                core_features=self._extract_planning_features(requirement.parsed_data.core_features),
                constraints=self._map_constraints(requirement.parsed_data.technical_constraints),
                business_context={
                    "model": requirement.parsed_data.business_model,
                    "complexity": requirement.parsed_data.complexity_level,
                    "confidence": requirement.confidence_score
                }
            )
        
        def _extract_planning_features(self, features: List[Feature]) -> List[PlanningFeature]:
            """将需求特性转换为规划特性"""
            return [
                PlanningFeature(
                    name=feature.name,
                    priority=feature.priority,
                    complexity_score=self._calculate_complexity_score(feature),
                    dependencies=feature.dependencies or []
                )
                for feature in features
            ]
    ```

- **实现策略**:
  1. 设计工作流状态机和数据流
  2. 实现数据转换器和质量评估器
  3. 创建工作流引擎和错误处理
  4. 添加缓存管理和性能优化
  5. 编写全面的集成测试
  6. 性能调优和稳定性验证

- **调试指南**:
  - 工作流调试:
    ```python
    import structlog
    
    logger = structlog.get_logger()
    
    async def execute_workflow(self, user_input: str):
        start_time = time.time()
        
        logger.info("工作流开始", user_input=user_input[:100])
        
        try:
            requirement = await self.requirement_parser.parse_requirement(user_input)
            logger.info("需求解析完成", 
                       project_type=requirement.parsed_data.project_type,
                       confidence=requirement.confidence_score)
            
            planning_input = self.data_transformer.requirement_to_planning_input(requirement)
            logger.info("数据转换完成", 
                       features_count=len(planning_input.core_features))
            
            plan = await self.project_planner.generate_plan(planning_input)
            logger.info("规划生成完成", 
                       modules_count=len(plan.modules),
                       estimated_cost=plan.budget.total_cost)
            
            return WorkflowResult(requirement=requirement, plan=plan)
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error("工作流失败", 
                        error=str(e), 
                        elapsed_seconds=elapsed)
            raise
    ```

**成功标准(S)**:
- **基础达标**:
  - 端到端工作流正常运行，从输入到输出完整无错误
  - 所有集成测试通过，覆盖正常流程和异常情况
  - 数据转换正确，需求模型到规划输入的映射无误
  - 错误处理机制有效，组件失败时能优雅降级
  - 性能达标，端到端处理时间<3分钟

- **预期品质**:
  - 工作流成功率≥95%，包含网络异常等边界情况
  - 数据一致性保证，中间状态可追踪和恢复
  - 质量评估准确，能识别低质量的需求或规划
  - 缓存机制有效，相似输入能快速响应
  - 日志记录详细，便于问题排查和性能分析

- **卓越表现**:
  - 实现智能的工作流优化和自适应调整
  - 支持并行处理和流式输出
  - 实现工作流可视化监控和实时状态
  - 添加机器学习驱动的质量预测
  - 支持A/B测试和策略对比分析
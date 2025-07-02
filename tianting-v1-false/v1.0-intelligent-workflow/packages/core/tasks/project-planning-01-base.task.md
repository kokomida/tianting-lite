// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业业务架构师的思维模式思考，遵循领域驱动设计原则，确保业务逻辑的正确性、可扩展性和架构一致性。我承诺：
- 以可扩展、领域模型驱动的业务逻辑为核心指导思想
- 先理解业务需求，再实现算法逻辑，通过测试验证业务正确性
- 确保所有实现与天庭系统整体架构保持一致
- 严格遵循Python最佳实践和异步编程规范

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
- 我将确保代码实现符合业务逻辑，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：基础任务重点验证相关单元测试
- 自我验证：
  * 我将执行`pytest`确保所有测试通过
  * 我将执行类型检查确保Python类型安全
  * 我将确认没有error级别的代码质量问题
  * 在验证通过后，我将明确声明："自我验证完成，所有测试通过，业务逻辑正确"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合业务逻辑的实现代码
- 我绝不依赖猜测解决问题，而是使用日志和断点进行系统性调试
- 如果我需要修改测试，我将明确说明修改理由并请求人类审批
- 我绝不在未理清任务全貌的情况下，直接开始进行任务

## 调试规范
- 遇到测试失败时，我将：
  * 首先添加详细日志输出关键数据和执行路径
  * 分析测试失败的具体断言和条件
  * 比较预期值与实际值的差异
  * 追踪问题根源至具体代码
  * 验证修复方案的合理性
- 当我需要添加日志时，我将：
  * 在关键函数入口记录输入参数
  * 在数据转换处记录前后状态
  * 在条件分支处记录判断条件
  * 在返回值处记录最终结果

## 权利
- 我有权利在设计本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让任务完成的更好

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 项目规划生成器核心实现（基础任务）

**目标(O)**:
- **功能目标**:
  - 实现天庭系统项目规划生成的核心算法
  - 将结构化需求转换为详细的项目计划
  - 集成Claude API，实现智能的规划策略生成
  - 为用户提供可执行的项目实施方案

- **执行任务**:
  - 创建文件:
    - `packages/core/src/project_planner.py` - 核心规划器类
    - `packages/core/src/planning_strategies/web_app_strategy.py` - Web应用规划策略
    - `packages/core/src/planning_strategies/mobile_app_strategy.py` - 移动应用规划策略
    - `packages/core/src/planning_strategies/api_service_strategy.py` - API服务规划策略
    - `packages/core/src/estimators/time_estimator.py` - 时间估算器
    - `packages/core/src/estimators/cost_estimator.py` - 成本估算器
    - `packages/core/src/templates/project_template_manager.py` - 项目模板管理器
    - `packages/core/tests/test_project_planner.py` - 单元测试
  - 修改文件:
    - 无（这是core包的第二个任务）
  - 实现功能:
    - 基于项目类型的智能规划策略选择
    - 功能模块分解和依赖关系分析
    - 开发阶段划分和里程碑设置
    - 资源需求估算和成本预测
    - 风险评估和缓解策略

- **任务边界**:
  - 包含规划生成核心逻辑，不包含API路由层
  - 包含多种项目类型策略，不包含所有可能的类型
  - 包含基础估算算法，不包含复杂的机器学习模型
  - 专注于规划算法，不涉及数据持久化

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/domain.ts` - ProjectPlan类型定义
  - `packages/common/contracts/api-contracts.md` - 项目规划API规范
  - `packages/core/src/requirement_parser.py` - 需求解析器输出格式
  - `development/architecture/technical-architecture.md` - 技术架构指导
  - `resources/estimation-methods.md` - 估算方法学指导

- **上下文信息**:
  - 包定位：core包专注于业务逻辑，不包含API层
  - 数据流：接收RequirementModel，输出ProjectPlan结构
  - 性能要求：规划生成时间<60秒，方案可行性≥90%
  - 质量要求：估算准确度误差<30%，覆盖主流项目类型
  - 依赖关系：依赖shared包的类型定义，为API包提供服务

- **规范索引**:
  - 软件工程项目管理最佳实践
  - 敏捷开发规划方法论
  - 成本估算标准(COCOMO II等)
  - 风险管理框架(PMI标准)

- **注意事项**:
  - 必须严格按照shared包定义的ProjectPlan类型输出
  - 规划策略需要考虑不同行业和规模的项目特点
  - 估算算法要平衡准确性和计算效率
  - 需要提供规划依据和可调整的参数

**实现指导(I)**:
- **算法与流程**:
  - 项目规划流程:
    ```
    需求分析 → 策略选择 → 模块分解 → 依赖分析 → 阶段规划 → 资源估算 → 风险评估 → 方案生成
    ```
  - 估算算法流程:
    ```
    功能点计算 → 复杂度加权 → 历史数据对比 → 风险系数调整 → 缓冲时间 → 最终估算
    ```

- **技术选型**:
  - Python版本：3.11+ (现代异步特性)
  - 数据处理：pandas (数据分析和计算)
  - 模板引擎：Jinja2 (项目模板生成)
  - 数学计算：numpy (复杂估算算法)
  - 配置管理：pydantic (数据验证)

- **代码模式**:
  - 核心规划器类:
    ```python
    class ProjectPlanner:
        def __init__(self, claude_client: ClaudeClient):
            self.claude_client = claude_client
            self.strategy_factory = PlanningStrategyFactory()
            self.time_estimator = TimeEstimator()
            self.cost_estimator = CostEstimator()
            self.template_manager = ProjectTemplateManager()
        
        async def generate_plan(self, requirement: RequirementModel) -> ProjectPlan:
            # 1. 选择规划策略
            strategy = self.strategy_factory.get_strategy(requirement.parsed_data.project_type)
            
            # 2. 生成基础规划结构
            base_plan = await strategy.generate_base_plan(requirement)
            
            # 3. 详细估算
            time_estimates = self.time_estimator.estimate_timeline(base_plan)
            cost_estimates = self.cost_estimator.estimate_costs(base_plan, time_estimates)
            
            # 4. 风险评估
            risks = await self._assess_risks(requirement, base_plan)
            
            # 5. 构建最终方案
            return ProjectPlan(
                project_id=str(uuid.uuid4()),
                modules=base_plan.modules,
                phases=base_plan.phases,
                timeline=time_estimates,
                budget=cost_estimates,
                risks=risks,
                recommendations=await self._generate_recommendations(requirement, base_plan)
            )
    ```
  - 规划策略模式:
    ```python
    class WebAppPlanningStrategy:
        async def generate_base_plan(self, requirement: RequirementModel) -> BasePlan:
            modules = await self._decompose_web_modules(requirement.parsed_data.core_features)
            phases = self._plan_web_development_phases(modules)
            
            return BasePlan(
                modules=modules,
                phases=phases,
                architecture_type="web_application",
                tech_stack=self._recommend_web_tech_stack(requirement)
            )
        
        def _decompose_web_modules(self, features: List[Feature]) -> List[ProjectModule]:
            # 基于Web应用特点分解模块
            modules = []
            
            # 前端模块
            if self._needs_frontend(features):
                modules.append(ProjectModule(
                    name="frontend",
                    type="user_interface",
                    features=self._extract_ui_features(features),
                    estimated_complexity="medium"
                ))
            
            # 后端API模块
            if self._needs_backend(features):
                modules.append(ProjectModule(
                    name="backend_api",
                    type="server_logic",
                    features=self._extract_api_features(features),
                    estimated_complexity="high"
                ))
            
            # 数据库模块
            if self._needs_database(features):
                modules.append(ProjectModule(
                    name="database",
                    type="data_storage",
                    features=self._extract_data_features(features),
                    estimated_complexity="medium"
                ))
            
            return modules
    ```

- **实现策略**:
  1. 建立规划策略工厂和基础类结构
  2. 实现主流项目类型的规划策略
  3. 开发时间和成本估算算法
  4. 创建项目模板管理系统
  5. 实现风险评估和建议生成
  6. 编写全面的单元测试

- **调试指南**:
  - 规划过程调试:
    ```python
    import logging
    
    logger = logging.getLogger(__name__)
    
    async def generate_plan(self, requirement: RequirementModel) -> ProjectPlan:
        logger.info(f"开始生成项目规划: 类型={requirement.parsed_data.project_type}")
        
        strategy = self.strategy_factory.get_strategy(requirement.parsed_data.project_type)
        logger.debug(f"选择规划策略: {strategy.__class__.__name__}")
        
        base_plan = await strategy.generate_base_plan(requirement)
        logger.info(f"基础规划生成完成: 模块数量={len(base_plan.modules)}")
        
        time_estimates = self.time_estimator.estimate_timeline(base_plan)
        logger.debug(f"时间估算: 总工期={time_estimates.total_duration_days}天")
        
        cost_estimates = self.cost_estimator.estimate_costs(base_plan, time_estimates)
        logger.debug(f"成本估算: 总预算={cost_estimates.total_cost}")
        
        return ProjectPlan(...)
    ```

**成功标准(S)**:
- **基础达标**:
  - ProjectPlanner类实现完成，接口符合类型定义
  - 支持web_app、mobile_app、api_service三种主要项目类型
  - 所有单元测试通过，代码覆盖率≥80%
  - 能够生成包含模块、阶段、估算的完整规划
  - 规划结果符合ProjectPlan格式要求

- **预期品质**:
  - 规划生成速度<60秒（包含AI调用）
  - 时间估算准确度误差<30%（基于历史项目验证）
  - 支持5种以上不同复杂度的项目模板
  - 风险识别覆盖技术、资源、时间等主要维度
  - 规划方案具有可执行性和实用价值

- **卓越表现**:
  - 实现基于机器学习的智能估算优化
  - 支持项目规划的增量更新和版本管理
  - 添加交互式规划调整和场景分析
  - 实现规划质量评分和改进建议
  - 提供详细的规划依据和可视化展示
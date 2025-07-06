// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业业务逻辑开发者的思维模式思考，遵循领域驱动设计(DDD)原则，确保业务逻辑的准确性、可维护性和架构一致性。我承诺：
- 以清晰的业务建模和领域概念为核心指导思想
- 先理解业务需求，再设计技术实现，通过测试验证逻辑正确性
- 确保所有实现与天庭系统整体架构保持一致
- 严格遵循Python最佳实践和本地AI能力集成规范

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
- 我将确保业务逻辑实现符合需求，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：业务逻辑任务重点验证算法准确性和性能
- 自我验证：
  * 我将执行`python -m pytest`确保所有测试通过
  * 我将执行性能测试确保满足30秒解析时间要求
  * 我将验证本地AI分析器的准确性和错误处理
  * 在验证通过后，我将明确声明："自我验证完成，业务逻辑正确，性能达标"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合业务逻辑的实现代码
- 我绝不依赖猜测解决AI分析问题，而是使用日志和系统性调试
- 如果我需要修改业务模型，我将明确说明修改理由并请求审批
- 我绝不在未理清业务逻辑全貌的情况下，直接开始编码

## 调试规范
- 遇到业务逻辑错误时，我将：
  * 首先添加详细日志输出业务数据和处理流程
  * 分析业务规则的执行路径和判断条件
  * 验证输入数据和输出结果的业务合理性
  * 追踪问题根源至具体业务逻辑
  * 确认修复方案符合业务需求
- 当我需要调试AI分析功能时，我将：
  * 记录输入文本和分析结果的详细信息
  * 分析AI分析结果的质量和准确性
  * 验证错误处理和置信度评估机制
  * 确保本地AI能力使用符合最佳实践

## 权利
- 我有权利在业务逻辑设计本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让业务实现更加稳定和高效

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 需求解析器核心实现（基础任务）

**目标(O)**:
- **功能目标**:
  - 实现天庭系统需求解析的核心算法
  - 将用户自然语言输入转换为结构化RequirementModel
  - 使用Claude Code本地AI能力，实现高准确率的智能理解
  - 为项目规划生成器提供高质量的结构化输入

- **执行任务**:
  - 创建文件:
    - `packages/core/src/requirement_parser.py` - 核心解析器类
    - `packages/core/src/requirement_analyzer.py` - 本地AI分析器
    - `packages/core/src/prompts/requirement_analysis.py` - AI提示词模板
    - `packages/core/src/validators/requirement_validator.py` - 需求验证器
    - `packages/core/src/utils/text_processor.py` - 文本预处理工具
    - `packages/core/package.json` - 包配置文件
    - `packages/core/requirements.txt` - Python依赖
    - `packages/core/tests/test_requirement_parser.py` - 单元测试
  - 修改文件:
    - 无（这是core包的第一个任务）
  - 实现功能:
    - 自然语言文本预处理和清理
    - 本地AI智能分析和理解
    - 项目类型智能识别
    - 功能需求和约束条件提取
    - 置信度评估和质量验证

- **任务边界**:
  - 包含需求解析核心逻辑，不包含API路由层
  - 包含本地AI分析，不包含外部AI服务
  - 包含基础验证，不包含复杂业务规则
  - 专注于解析算法，不涉及数据持久化

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/domain.ts` - RequirementModel类型定义
  - `packages/common/contracts/api-contracts.md` - 需求解析API规范
  - `planning/user-stories-breakdown.md` - US-001到US-005需求
  - `resources/research-paper-guide.md` - 意图识别学术支持
  - `packages/common/environments/dev-environment-setup.md` - 开发环境配置

- **上下文信息**:
  - 包定位：core包专注于业务逻辑，不包含API层
  - 并发开发：与api包、frontend包完全独立开发
  - 数据流：接收文本输入，输出RequirementModel结构
  - 性能要求：解析时间<30秒，准确率≥85%
  - 依赖关系：依赖shared包的类型定义

- **规范索引**:
  - Python代码规范 (PEP 8)
  - 本地AI能力使用最佳实践
  - 异步编程规范 (asyncio)
  - 测试驱动开发标准

- **注意事项**:
  - 必须严格按照shared包定义的类型结构输出
  - 本地AI分析需要实现错误处理和置信度评估
  - 代码必须支持异步执行，适配API层调用
  - 需要详细的日志记录，便于调试和监控

**实现指导(I)**:
- **算法与流程**:
  - 需求解析流程:
    ```
    原始文本 → 预处理 → 本地AI分析 → 结构化提取 → 验证 → RequirementModel
    ```
  - AI分析流程:
    ```
    文本理解 → 模式识别 → 特征提取 → 数据结构化 → 置信度评估
    ```

- **技术选型**:
  - Python版本：3.11+ (现代异步特性)
  - 数据验证：pydantic (与TypeScript类型对应)
  - 文本处理：spacy或nltk (可选，用于高级NLP功能)
  - 测试框架：pytest (单元测试和集成测试)
  - 配置管理：python-dotenv (环境变量)

- **代码模式**:
  - 核心解析器类:
    ```python
    class RequirementParser:
        def __init__(self):
            self.analyzer = RequirementAnalyzer()
            self.text_processor = TextProcessor()
            self.validator = RequirementValidator()
        
        async def parse_requirement(self, user_input: str) -> RequirementModel:
            # 1. 文本预处理
            processed_text = self.text_processor.clean_and_normalize(user_input)
            
            # 2. 本地AI分析
            analysis_result = await self.analyzer.analyze_requirement(processed_text)
            
            # 3. 结构化数据提取
            structured_data = self._extract_structured_data(analysis_result)
            
            # 4. 验证和置信度评估
            validated_result = self.validator.validate_and_score(structured_data)
            
            return RequirementModel(**validated_result)
    ```
  - 本地AI分析器设计:
    ```python
    class RequirementAnalyzer:
        def __init__(self):
            self.keywords = self._load_keywords()
            self.patterns = self._compile_patterns()
        
        async def analyze_requirement(self, text: str) -> dict:
            """
            使用Claude Code本地AI能力进行需求分析
            我们在Claude环境中，直接实现智能分析逻辑
            """
            # 1. 项目类型识别
            project_type = self._detect_project_type(text)
            
            # 2. 功能需求提取
            core_features = self._extract_features(text)
            
            # 3. 技术约束识别
            constraints = self._identify_constraints(text)
            
            # 4. 业务模式分析
            business_model = self._analyze_business_model(text)
            
            # 5. 复杂度评估
            complexity = self._assess_complexity(text, core_features)
            
            return {
                "project_type": project_type,
                "core_features": core_features,
                "technical_constraints": constraints,
                "business_model": business_model,
                "complexity_level": complexity,
                "confidence_score": self._calculate_confidence(text)
            }
        
        def _detect_project_type(self, text: str) -> str:
            # 基于关键词和模式的项目类型识别
            if any(keyword in text.lower() for keyword in ["网站", "web", "浏览器"]):
                return "web_app"
            elif any(keyword in text.lower() for keyword in ["手机", "app", "移动"]):
                return "mobile_app"
            elif any(keyword in text.lower() for keyword in ["接口", "api", "服务"]):
                return "api_service"
            else:
                return "web_app"  # 默认
    ```

- **实现策略**:
  1. 建立包基础结构和依赖配置
  2. 实现文本预处理和本地AI分析器
  3. 开发核心解析算法
  4. 实现数据验证和置信度评估
  5. 编写全面的单元测试
  6. 优化性能和错误处理

- **调试指南**:
  - 解析流程调试:
    ```python
    import logging
    
    logger = logging.getLogger(__name__)
    
    async def parse_requirement(self, user_input: str) -> RequirementModel:
        logger.info(f"开始解析需求: {user_input[:100]}...")
        
        processed_text = self.text_processor.clean_and_normalize(user_input)
        logger.debug(f"预处理后文本: {processed_text}")
        
        analysis_result = await self.analyzer.analyze_requirement(processed_text)
        logger.debug(f"AI分析结果: {analysis_result}")
        
        structured_data = self._extract_structured_data(analysis_result)
        logger.info(f"结构化数据提取完成: 项目类型={structured_data.get('project_type')}")
        
        return RequirementModel(**structured_data)
    ```

**成功标准(S)**:
- **基础达标**:
  - RequirementParser类实现完成，接口符合类型定义
  - 本地AI分析器工作正常，可以准确分析需求文本
  - 所有单元测试通过，代码覆盖率≥80%
  - 能够解析基本的项目需求，输出符合RequirementModel格式
  - 错误处理机制完善，异常情况有适当的降级处理

- **预期品质**:
  - 需求解析准确率≥85%（基于测试数据集验证）
  - 处理时间<30秒（本地分析更快）
  - 支持中英文混合输入，文本预处理效果良好
  - 置信度评估准确，低质量输入能够被识别
  - 代码结构清晰，符合Python最佳实践

- **卓越表现**:
  - 实现智能的上下文理解和多轮对话支持
  - 添加需求理解的解释性输出和改进建议
  - 支持批量处理和增量学习机制
  - 实现高级的文本分析特性（情感分析、关键词提取）
  - 提供详细的性能指标和调试信息
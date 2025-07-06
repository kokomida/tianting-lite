// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业类库开发者的思维模式思考，遵循TDD原则，确保代码的可测试性、可维护性和架构一致性。我承诺：
- 以可复用、模块化代码结构为核心指导思想
- 先理解测试需求，再实现功能，通过测试验证实现
- 确保所有实现与天庭系统整体架构保持一致
- 严格遵循TypeScript最佳实践和类型安全原则

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
  * 我将执行`npm test`确保所有测试通过
  * 我将执行`npm run type-check`确保TypeScript编译成功
  * 我将确认没有error级别的lint错误
  * 在验证通过后，我将明确声明："自我验证完成，所有测试通过，类型检查成功"

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

## 任务: 天庭系统TypeScript类型定义基础（基础任务）

**目标(O)**:
- **功能目标**:
  - 为天庭系统建立完整的TypeScript类型系统基础
  - 定义所有包间共享的数据类型和接口规范
  - 确保类型安全，支持真正的并发开发
  - 为API契约提供严格的类型定义基础

- **执行任务**:
  - 创建文件:
    - `packages/shared/src/types/index.ts` - 主类型导出文件
    - `packages/shared/src/types/api.ts` - API相关类型定义
    - `packages/shared/src/types/domain.ts` - 业务领域类型定义
    - `packages/shared/src/types/common.ts` - 通用类型定义
    - `packages/shared/src/types/errors.ts` - 错误类型定义
    - `packages/shared/package.json` - 包配置文件
    - `packages/shared/tsconfig.json` - TypeScript配置
    - `packages/shared/tests/types.test.ts` - 类型测试文件
  - 实现功能:
    - 需求解析相关的数据类型（RequirementModel等）
    - 项目规划相关的数据类型（ProjectPlan等）
    - API请求响应的标准格式类型
    - 用户管理和认证相关类型
    - 通用工具类型和错误处理类型

- **任务边界**:
  - 仅包含类型定义，不包含具体实现逻辑
  - 包含类型验证工具，不包含业务逻辑验证
  - 包含类型文档，不包含API实现文档
  - 专注于类型系统，不涉及运行时行为

**环境(E)**:
- **参考资源**:
  - `packages/common/contracts/api-contracts.md` - API接口契约规范
  - `docs/requirements-analysis.md` - 了解业务领域概念
  - `planning/user-stories-breakdown.md` - 了解数据实体需求
  - `development/architecture/technical-architecture.md` - 技术架构约束

- **上下文信息**:
  - 角色定位：shared包是所有其他包的类型依赖基础
  - 并发要求：类型定义完成后，其他包可以立即并发开发
  - 稳定性要求：类型定义需要保持向后兼容，变更需谨慎
  - 覆盖范围：需要涵盖core、api、frontend包的所有数据交互
  - 类型安全：必须提供编译时类型检查，防止运行时错误

- **规范索引**:
  - TypeScript官方最佳实践指南
  - 函数式编程类型设计模式
  - API类型设计规范
  - 错误处理类型模式

- **注意事项**:
  - 类型定义必须与API契约完全一致
  - 需要支持未来的类型扩展和版本控制
  - 类型复杂度要平衡可读性和严格性
  - 必须考虑前端和后端的类型使用场景

**实现指导(I)**:
- **算法与流程**:
  - 类型设计流程:
    ```
    业务分析 → 领域建模 → 接口设计 → 类型定义 → 验证测试 → 文档生成
    ```
  - 类型层次结构:
    ```
    Common Types (基础类型)
    ↓
    Domain Types (业务类型)  
    ↓
    API Types (接口类型)
    ↓
    Package-Specific Types (包特定类型)
    ```

- **技术选型**:
  - 类型系统：TypeScript 5.0+ (最新特性)
  - 类型验证：zod (运行时类型验证)
  - 文档生成：typedoc (自动文档生成)
  - 测试工具：jest + @types/jest (类型测试)
  - 构建工具：tsc (TypeScript编译器)

- **代码模式**:
  - 基础类型模式:
    ```typescript
    // 通用响应格式
    export interface ApiResponse<T = any> {
      success: boolean;
      data?: T;
      message: string;
      timestamp: string;
      request_id?: string;
    }
    
    // 错误响应
    export interface ApiError {
      code: string;
      message: string;
      details?: Record<string, any>;
      stack?: string;
    }
    ```
  - 业务领域类型:
    ```typescript
    // 需求模型
    export interface RequirementModel {
      id: string;
      user_input: string;
      parsed_data: {
        project_type: ProjectType;
        target_users: UserGroup[];
        core_features: Feature[];
        technical_constraints: Constraint[];
        business_model: BusinessModel;
        complexity_level: ComplexityLevel;
      };
      confidence_score: number;
      created_at: string;
      updated_at: string;
    }
    ```
  - 枚举和联合类型:
    ```typescript
    export type ProjectType = 'web_app' | 'mobile_app' | 'api_service' | 'desktop_app';
    export type BusinessModel = 'b2b' | 'b2c' | 'c2c' | 'saas' | 'marketplace';
    export type ComplexityLevel = 'low' | 'medium' | 'high';
    ```

- **实现策略**:
  1. 分析API契约文档，提取所有数据结构
  2. 设计类型层次结构和命名规范
  3. 实现基础类型和通用类型
  4. 实现业务领域类型
  5. 实现API接口类型
  6. 编写类型验证测试
  7. 生成类型文档

- **调试指南**:
  - 类型检查调试:
    ```bash
    # 检查类型定义
    npx tsc --noEmit --strict
    
    # 生成类型声明文件
    npx tsc --declaration --emitDeclarationOnly
    
    # 类型覆盖率检查
    npx type-coverage --detail
    ```
  - 类型兼容性测试:
    ```typescript
    // 测试类型兼容性
    describe('Type Compatibility', () => {
      test('RequirementModel should be compatible with API contract', () => {
        const requirement: RequirementModel = {
          // 测试数据
        };
        
        // 类型断言测试
        expect(typeof requirement.confidence_score).toBe('number');
        expect(requirement.confidence_score).toBeGreaterThanOrEqual(0);
        expect(requirement.confidence_score).toBeLessThanOrEqual(1);
      });
    });
    ```

**成功标准(S)**:
- **基础达标**:
  - 所有类型定义文件创建完成，TypeScript编译无错误
  - 类型定义与API契约规范完全一致
  - 包配置正确，其他包可以正确导入类型
  - 基础类型测试通过，类型验证功能正常
  - 类型文档自动生成，内容清晰完整

- **预期品质**:
  - 类型覆盖率≥95%，所有主要数据结构有类型定义
  - 类型设计遵循最佳实践，可读性和严格性平衡
  - 支持泛型和高级类型特性，扩展性良好
  - 错误处理类型完善，提供友好的错误信息
  - 类型导出结构清晰，便于其他包使用

- **卓越表现**:
  - 实现运行时类型验证，确保类型安全
  - 支持类型版本控制和向后兼容
  - 提供类型工具函数，简化类型操作
  - 实现条件类型和映射类型等高级特性
  - 集成IDE支持，提供优秀的开发体验
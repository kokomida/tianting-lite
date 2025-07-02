// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业前端开发者的思维模式思考，遵循组件化设计原则，确保UI的可复用性、可维护性和用户体验一致性。我承诺：
- 以可复用组件和用户体验为核心指导思想
- 先理解设计需求，再实现组件逻辑，通过测试验证UI功能
- 确保所有实现与天庭系统整体设计语言保持一致
- 严格遵循React最佳实践和TypeScript类型安全

## 执行承诺
我将遵循严格的执行流程，不偏离既定规范。我承诺：

**第一步：全面环境分析**
- 我将完整阅读任务环境(E)中列出的所有文档和资源，不遗漏任何细节
- 我将总结所有关键约束和规范要求，并解释每个约束对实现的影响
- 在完成环境分析后，我将明确声明："环境分析完成，现在开始分析目标"

**第二步：目标与计划制定**
- 我将基于环境分析结果理解任务目标，确保目标与环境约束兼容
- 我将制定周详的实现计划，考虑所有环境约束和设计要求
- 我将将实现计划与成功标准(S)进行对照验证
- 在完成目标分析后，我将明确声明："目标分析完成，现在制定实现计划"

**第三步：测试驱动实现**
- 我将严格按照测试优先级实现功能
- 每完成一个UI组件，我将立即运行相关测试验证
- 遇到测试失败时，我将使用浏览器调试工具和系统性方法而非依赖猜测
- 我将确保实现满足所有测试要求，不妥协代码质量
- 我将确保UI实现符合设计规范，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：UI任务重点验证组件功能和视觉效果
- 自我验证：
  * 我将执行`npm test`确保所有组件测试通过
  * 我将执行`npm run type-check`确保TypeScript编译成功
  * 我将验证组件在不同视口下的响应式表现
  * 在验证通过后，我将明确声明："自我验证完成，UI组件功能正确，样式达标"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合设计规范的实现代码
- 我绝不依赖猜测解决样式和交互问题，而是使用开发者工具进行系统性调试
- 如果我需要修改组件设计，我将明确说明修改理由并请求审批
- 我绝不在未理清UI架构全貌的情况下，直接开始编码

## 调试规范
- 遇到UI错误时，我将：
  * 首先使用浏览器开发者工具检查DOM结构和样式
  * 分析组件状态变化和事件处理流程
  * 验证Props传递和状态管理的正确性
  * 追踪问题根源至具体组件逻辑
  * 确认修复方案符合React最佳实践
- 当我需要调试样式问题时，我将：
  * 检查CSS选择器和样式优先级
  * 验证响应式设计和媒体查询
  * 分析布局算法和盒模型
  * 确保跨浏览器兼容性

## 权利
- 我有权利在UI设计本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让UI实现更加美观和易用

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 前端UI组件基础实现（基础任务）

**目标(O)**:
- **功能目标**:
  - 建立天庭系统前端的React组件基础架构
  - 实现核心UI组件库，支持"言出法随"用户体验
  - 建立组件设计系统和样式规范
  - 为具体页面开发提供可复用的组件基础

- **执行任务**:
  - 创建文件:
    - `packages/frontend/src/components/ui/Button.tsx` - 按钮组件
    - `packages/frontend/src/components/ui/Input.tsx` - 输入框组件
    - `packages/frontend/src/components/ui/Textarea.tsx` - 多行文本框
    - `packages/frontend/src/components/ui/Loading.tsx` - 加载状态组件
    - `packages/frontend/src/components/ui/Card.tsx` - 卡片容器组件
    - `packages/frontend/src/components/ui/Badge.tsx` - 标签组件
    - `packages/frontend/src/styles/globals.css` - 全局样式
    - `packages/frontend/src/styles/components.css` - 组件样式
    - `packages/frontend/package.json` - 包配置文件
    - `packages/frontend/src/stories/Button.stories.tsx` - Storybook故事
    - `packages/frontend/src/tests/components/Button.test.tsx` - 组件测试
  - 实现功能:
    - 基础UI组件（按钮、输入框、卡片等）
    - 加载状态和反馈组件
    - 响应式设计和移动端适配
    - 组件属性类型定义和文档
    - 主题系统和样式变量

- **任务边界**:
  - 包含基础UI组件，不包含业务组件
  - 包含样式系统，不包含具体页面布局
  - 包含组件测试，不包含集成测试
  - 专注于组件库，不涉及状态管理和API调用

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/api.ts` - API数据类型定义
  - `packages/common/contracts/api-contracts.md` - 了解数据结构
  - `docs/user-journey-final.md` - 用户体验设计要求
  - `packages/common/environments/dev-environment-setup.md` - 开发环境配置

- **上下文信息**:
  - 包定位：frontend包专门负责用户界面，完全独立开发
  - 并发开发：可以基于Mock API完全独立于后端开发
  - 服务端口：3001（与后端包隔离）
  - 目标用户：创业者（非技术背景）、产品经理、技术团队
  - 设计目标：简洁直观、专业可信、快速上手

- **规范索引**:
  - React组件设计最佳实践
  - TypeScript React组件类型规范
  - 现代CSS设计系统
  - 无障碍性(a11y)设计标准

- **注意事项**:
  - 组件必须支持TypeScript严格类型检查
  - 样式必须支持响应式设计和暗色模式
  - 组件要考虑无障碍性和键盘导航
  - 性能优化，避免不必要的重渲染

**实现指导(I)**:
- **算法与流程**:
  - 组件开发流程:
    ```
    设计系统定义 → 组件接口设计 → 实现 → 测试 → 文档 → 集成
    ```
  - 组件层次结构:
    ```
    基础组件 (Button, Input) 
    ↓
    复合组件 (FormGroup, Modal)
    ↓
    业务组件 (RequirementInput, PlanDisplay)
    ```

- **技术选型**:
  - React版本：18+ (最新并发特性)
  - TypeScript：5.0+ (严格类型检查)
  - 样式方案：Tailwind CSS + CSS Modules
  - 组件文档：Storybook 7.0+
  - 测试工具：React Testing Library + Jest
  - 图标库：Lucide React (现代SVG图标)

- **代码模式**:
  - 基础组件模式:
    ```typescript
    interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
      variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
      size?: 'sm' | 'md' | 'lg';
      loading?: boolean;
      leftIcon?: React.ReactNode;
      rightIcon?: React.ReactNode;
    }
    
    export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
      ({ variant = 'primary', size = 'md', loading, leftIcon, rightIcon, children, className, ...props }, ref) => {
        const baseClasses = "inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2";
        const variantClasses = {
          primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
          secondary: "bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500",
          outline: "border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500",
          ghost: "text-gray-700 hover:bg-gray-100 focus:ring-gray-500"
        };
        const sizeClasses = {
          sm: "px-3 py-1.5 text-sm",
          md: "px-4 py-2 text-base", 
          lg: "px-6 py-3 text-lg"
        };
        
        return (
          <button
            ref={ref}
            className={cn(baseClasses, variantClasses[variant], sizeClasses[size], className)}
            disabled={loading || props.disabled}
            {...props}
          >
            {loading && <Spinner className="mr-2" size="sm" />}
            {!loading && leftIcon && <span className="mr-2">{leftIcon}</span>}
            {children}
            {!loading && rightIcon && <span className="ml-2">{rightIcon}</span>}
          </button>
        );
      }
    );
    ```
  - 输入组件模式:
    ```typescript
    interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
      label?: string;
      error?: string;
      helper?: string;
      maxLength?: number;
      showCount?: boolean;
    }
    
    export const Textarea: React.FC<TextareaProps> = ({
      label,
      error,
      helper,
      maxLength,
      showCount,
      className,
      ...props
    }) => {
      const [charCount, setCharCount] = useState(props.value?.toString().length || 0);
      
      const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setCharCount(e.target.value.length);
        props.onChange?.(e);
      };
      
      return (
        <div className="space-y-2">
          {label && (
            <label className="block text-sm font-medium text-gray-700">
              {label}
            </label>
          )}
          <textarea
            className={cn(
              "block w-full rounded-lg border border-gray-300 px-3 py-2 text-base",
              "focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
              error && "border-red-500 focus:border-red-500 focus:ring-red-500",
              className
            )}
            maxLength={maxLength}
            onChange={handleChange}
            {...props}
          />
          {(showCount || error || helper) && (
            <div className="flex justify-between items-center text-sm">
              <span className={error ? "text-red-600" : "text-gray-500"}>
                {error || helper}
              </span>
              {showCount && maxLength && (
                <span className="text-gray-500">
                  {charCount}/{maxLength}
                </span>
              )}
            </div>
          )}
        </div>
      );
    };
    ```

- **实现策略**:
  1. 建立React项目基础和配置
  2. 设计组件设计系统和样式规范
  3. 实现基础UI组件
  4. 添加Storybook文档和测试
  5. 实现响应式设计和主题支持
  6. 优化性能和无障碍性

- **调试指南**:
  - 组件开发调试:
    ```typescript
    // 使用React Developer Tools
    const Button = ({ children, ...props }) => {
      useEffect(() => {
        console.log('Button rendered with props:', props);
      });
      
      return <button {...props}>{children}</button>;
    };
    
    // Storybook调试
    export default {
      title: 'UI/Button',
      component: Button,
      argTypes: {
        variant: { control: 'select', options: ['primary', 'secondary'] }
      }
    };
    ```

**成功标准(S)**:
- **基础达标**:
  - React应用启动成功，监听端口3001
  - 所有基础UI组件实现完成，类型定义正确
  - 组件库在Storybook中正常展示
  - 所有组件测试通过，测试覆盖率≥80%
  - 响应式设计正常，支持桌面和移动端

- **预期品质**:
  - 组件设计一致性良好，遵循统一的设计规范
  - 性能优秀，组件渲染时间<16ms
  - 无障碍性支持，通过基础a11y测试
  - TypeScript类型完整，IDE支持良好
  - 组件文档清晰，Storybook故事覆盖主要用例

- **卓越表现**:
  - 实现高级动画和交互效果
  - 支持主题切换和自定义样式
  - 组件库支持Tree Shaking，优化打包体积
  - 实现虚拟化等性能优化技术
  - 提供完整的设计token系统
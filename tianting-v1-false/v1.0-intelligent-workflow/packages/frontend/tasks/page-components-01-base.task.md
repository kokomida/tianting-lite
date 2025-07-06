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
- 根据任务类型确定验证范围：页面任务重点验证用户流程和交互体验
- 自我验证：
  * 我将执行`npm test`确保所有组件测试通过
  * 我将执行用户流程测试确保页面导航正常
  * 我将验证响应式设计在多设备下的表现
  * 在验证通过后，我将明确声明："自我验证完成，页面功能正确，用户体验达标"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合设计规范的实现代码
- 我绝不依赖猜测解决样式和交互问题，而是使用开发者工具进行系统性调试
- 如果我需要修改页面设计，我将明确说明修改理由并请求审批
- 我绝不在未理清页面架构全貌的情况下，直接开始编码

## 调试规范
- 遇到页面错误时，我将：
  * 首先使用浏览器开发者工具检查页面结构和路由
  * 分析页面状态管理和数据流
  * 验证组件通信和Props传递
  * 追踪问题根源至具体页面逻辑
  * 确认修复方案符合用户体验设计
- 当我需要调试用户交互时，我将：
  * 测试各种用户输入和操作场景
  * 验证表单验证和错误处理
  * 分析页面性能和加载体验
  * 确保交互符合无障碍设计标准

## 权利
- 我有权利在页面设计本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让页面实现更加优雅和易用

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 页面组件和路由系统实现（基础任务）

**目标(O)**:
- **功能目标**:
  - 建立天庭系统的核心页面组件和路由架构
  - 实现需求输入和项目展示的主要用户界面
  - 集成API服务，实现完整的用户交互流程
  - 提供响应式和用户友好的"言出法随"体验

- **执行任务**:
  - 创建文件:
    - `packages/frontend/src/pages/HomePage.tsx` - 首页组件
    - `packages/frontend/src/pages/RequirementPage.tsx` - 需求输入页面
    - `packages/frontend/src/pages/ProjectPage.tsx` - 项目展示页面
    - `packages/frontend/src/pages/DashboardPage.tsx` - 用户仪表板
    - `packages/frontend/src/components/business/RequirementInput.tsx` - 需求输入组件
    - `packages/frontend/src/components/business/ProjectDisplay.tsx` - 项目展示组件
    - `packages/frontend/src/components/business/ProgressTracker.tsx` - 进度追踪组件
    - `packages/frontend/src/services/api.ts` - API服务客户端
    - `packages/frontend/src/services/websocket.ts` - WebSocket服务
    - `packages/frontend/src/hooks/useRequirement.ts` - 需求管理Hook
    - `packages/frontend/src/hooks/useProject.ts` - 项目管理Hook
    - `packages/frontend/src/router/index.tsx` - 路由配置
    - `packages/frontend/src/tests/pages/HomePage.test.tsx` - 页面测试
  - 修改文件:
    - `packages/frontend/src/App.tsx` - 集成路由系统
    - `packages/frontend/package.json` - 添加路由依赖
  - 实现功能:
    - 用户需求输入和实时反馈
    - 项目规划展示和交互
    - 进度追踪和状态管理
    - 响应式布局和移动端适配
    - 错误处理和加载状态

- **任务边界**:
  - 包含核心页面组件，不包含所有可能的页面
  - 包含API集成，不包含复杂的状态管理
  - 包含基础路由，不包含权限控制
  - 专注于用户界面，不涉及后端逻辑

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/api.ts` - API类型定义
  - `packages/common/contracts/api-contracts.md` - API接口规范
  - `packages/frontend/src/components/ui/` - 基础UI组件
  - `docs/user-journey-final.md` - 用户体验设计
  - `packages/api/src/routers/requirements.py` - API端点参考

- **上下文信息**:
  - 包定位：frontend包专门负责用户界面，调用API服务
  - 服务通信：通过HTTP/WebSocket调用API包（端口8002）
  - 并发开发：基于Mock API可以完全独立开发
  - 用户体验：简洁直观，专业可信，快速上手
  - 性能要求：页面加载<2秒，交互响应<200ms

- **规范索引**:
  - React组件设计最佳实践
  - 现代前端路由管理
  - WebSocket客户端开发标准
  - 无障碍性(a11y)设计规范

- **注意事项**:
  - 组件必须支持TypeScript严格类型检查
  - API调用需要完整的错误处理和重试机制
  - WebSocket连接需要处理断线重连
  - 页面需要考虑SEO和首屏加载性能

**实现指导(I)**:
- **算法与流程**:
  - 用户交互流程:
    ```
    首页访问 → 需求输入 → 实时解析 → 规划生成 → 结果展示 → 下载/分享
    ```
  - 状态管理流程:
    ```
    用户操作 → Hook处理 → API调用 → 状态更新 → UI重渲染
    ```

- **技术选型**:
  - 路由管理：React Router 6+ (现代路由)
  - 状态管理：Zustand (轻量级状态管理)
  - API客户端：axios (HTTP请求) + native WebSocket
  - UI动画：Framer Motion (流畅动画)
  - 表单处理：React Hook Form (性能优化)
  - 图标库：Lucide React (现代图标)

- **代码模式**:
  - 需求输入页面:
    ```typescript
    import React, { useState } from 'react';
    import { useRequirement } from '@/hooks/useRequirement';
    import { RequirementInput } from '@/components/business/RequirementInput';
    import { ProgressTracker } from '@/components/business/ProgressTracker';
    
    export const RequirementPage: React.FC = () => {
      const {
        parseRequirement,
        isLoading,
        result,
        error,
        progress
      } = useRequirement();
      
      const handleSubmit = async (userInput: string) => {
        try {
          await parseRequirement(userInput);
          // 导航到项目页面
          navigate(`/project/${result.id}`);
        } catch (error) {
          console.error('需求解析失败:', error);
        }
      };
      
      return (
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-8 text-center">
              描述您的项目需求
            </h1>
            
            <RequirementInput
              onSubmit={handleSubmit}
              isLoading={isLoading}
              error={error}
            />
            
            {isLoading && (
              <ProgressTracker
                progress={progress}
                stages={[
                  '理解需求',
                  '分析功能',
                  '评估复杂度',
                  '生成方案'
                ]}
              />
            )}
          </div>
        </div>
      );
    };
    ```
  - 需求输入组件:
    ```typescript
    interface RequirementInputProps {
      onSubmit: (userInput: string) => void;
      isLoading: boolean;
      error?: string;
    }
    
    export const RequirementInput: React.FC<RequirementInputProps> = ({
      onSubmit,
      isLoading,
      error
    }) => {
      const [userInput, setUserInput] = useState('');
      const [charCount, setCharCount] = useState(0);
      const maxLength = 5000;
      
      const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        
        if (userInput.trim().length < 50) {
          alert('请提供更详细的需求描述（至少50个字符）');
          return;
        }
        
        onSubmit(userInput.trim());
      };
      
      const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const value = e.target.value;
        setUserInput(value);
        setCharCount(value.length);
      };
      
      return (
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-lg font-medium text-gray-700 mb-4">
              详细描述您想要实现的项目
            </label>
            <textarea
              value={userInput}
              onChange={handleChange}
              maxLength={maxLength}
              rows={12}
              placeholder="例如：我想开发一个在线学习平台，用户可以注册账号、浏览课程、购买课程、观看视频、提交作业、参与讨论。管理员可以管理课程内容、用户信息、订单数据。需要支持移动端访问，集成支付功能..."
              className={cn(
                "w-full p-4 border border-gray-300 rounded-lg",
                "focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "resize-none text-base leading-relaxed",
                error && "border-red-500 focus:ring-red-500 focus:border-red-500"
              )}
              disabled={isLoading}
            />
            <div className="flex justify-between items-center mt-2 text-sm text-gray-500">
              <span>
                {error && <span className="text-red-600">{error}</span>}
              </span>
              <span>{charCount}/{maxLength}</span>
            </div>
          </div>
          
          <div className="flex justify-center">
            <Button
              type="submit"
              size="lg"
              disabled={isLoading || userInput.trim().length < 50}
              loading={isLoading}
              className="px-8 py-3"
            >
              {isLoading ? '正在分析需求...' : '开始规划项目'}
            </Button>
          </div>
        </form>
      );
    };
    ```
  - API服务客户端:
    ```typescript
    class ApiClient {
      private baseURL: string;
      private wsBaseURL: string;
      
      constructor() {
        this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8002';
        this.wsBaseURL = this.baseURL.replace(/^http/, 'ws');
      }
      
      async parseRequirement(userInput: string): Promise<RequirementModel> {
        const response = await axios.post(`${this.baseURL}/api/requirements/parse`, {
          user_input: userInput,
          async_mode: false
        });
        
        if (!response.data.success) {
          throw new Error(response.data.message || '需求解析失败');
        }
        
        return response.data.data;
      }
      
      createRequirementWebSocket(
        onProgress: (progress: ParseProgress) => void,
        onComplete: (result: RequirementModel) => void,
        onError: (error: string) => void
      ): WebSocket {
        const ws = new WebSocket(`${this.wsBaseURL}/api/requirements/parse/ws`);
        
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          
          if (data.type === 'progress') {
            onProgress(data.data);
          } else if (data.type === 'complete') {
            onComplete(data.data);
          } else if (data.error) {
            onError(data.error);
          }
        };
        
        ws.onerror = () => onError('WebSocket连接错误');
        
        return ws;
      }
    }
    
    export const apiClient = new ApiClient();
    ```
  - 自定义Hook:
    ```typescript
    export const useRequirement = () => {
      const [isLoading, setIsLoading] = useState(false);
      const [result, setResult] = useState<RequirementModel | null>(null);
      const [error, setError] = useState<string | null>(null);
      const [progress, setProgress] = useState<ParseProgress | null>(null);
      
      const parseRequirement = async (userInput: string) => {
        setIsLoading(true);
        setError(null);
        setProgress(null);
        
        try {
          // 使用WebSocket进行实时处理
          const ws = apiClient.createRequirementWebSocket(
            (progress) => setProgress(progress),
            (result) => {
              setResult(result);
              setIsLoading(false);
            },
            (error) => {
              setError(error);
              setIsLoading(false);
            }
          );
          
          // 发送解析请求
          ws.send(JSON.stringify({ user_input: userInput }));
          
        } catch (err) {
          setError(err instanceof Error ? err.message : '未知错误');
          setIsLoading(false);
        }
      };
      
      return {
        parseRequirement,
        isLoading,
        result,
        error,
        progress
      };
    };
    ```

- **实现策略**:
  1. 建立路由系统和页面基础结构
  2. 实现API服务客户端和WebSocket通信
  3. 开发核心业务组件
  4. 实现自定义Hooks和状态管理
  5. 添加响应式设计和移动端适配
  6. 编写组件测试和集成测试

- **调试指南**:
  - 组件开发调试:
    ```typescript
    const RequirementPage: React.FC = () => {
      useEffect(() => {
        console.log('RequirementPage mounted');
        
        return () => {
          console.log('RequirementPage unmounted');
        };
      }, []);
      
      const handleSubmit = async (userInput: string) => {
        console.log('提交需求:', userInput.substring(0, 100));
        
        try {
          const result = await parseRequirement(userInput);
          console.log('解析结果:', result);
        } catch (error) {
          console.error('解析失败:', error);
        }
      };
      
      // ... 组件实现
    };
    ```

**成功标准(S)**:
- **基础达标**:
  - 所有核心页面组件实现完成，路由正常工作
  - API集成成功，能够正常调用后端服务
  - WebSocket连接稳定，支持实时通信和进度更新
  - 响应式设计良好，支持桌面和移动端
  - 所有组件测试通过，覆盖主要用例

- **预期品质**:
  - 页面加载速度<2秒，交互响应<200ms
  - 错误处理完善，提供友好的用户提示
  - 无障碍性支持，通过基础a11y测试
  - 代码结构清晰，组件复用性良好
  - 用户体验流畅，符合"言出法随"的设计目标

- **卓越表现**:
  - 实现高级动画和交互效果
  - 支持离线模式和PWA功能
  - 实现智能的错误恢复和重试机制
  - 提供优秀的SEO支持和首屏性能
  - 集成用户行为分析和性能监控
# 📋 天庭系统API接口契约规范

## 🎯 接口优先设计原则

为了支持真正的并发开发，所有包间交互必须通过明确定义的接口契约。前端可以基于Mock API独立开发，后端包可以基于接口规范并发实现。

## 📡 核心API接口定义

### 1. 需求理解API (Core Package负责实现)

#### POST /api/requirements/parse
**用途**: 解析用户自然语言需求，返回结构化数据

**请求格式**:
```typescript
interface RequirementParseRequest {
  user_input: string;              // 用户原始输入
  user_id?: string;               // 可选的用户ID
  context?: {                     // 可选的上下文信息
    previous_requirements?: string[];
    project_history?: string[];
  };
}
```

**响应格式**:
```typescript
interface RequirementParseResponse {
  success: boolean;
  data: {
    requirement_id: string;       // 需求唯一标识
    parsed_data: {
      project_type: 'web_app' | 'mobile_app' | 'api_service' | 'desktop_app';
      target_users: UserGroup[];
      core_features: Feature[];
      technical_constraints: Constraint[];
      business_model: 'b2b' | 'b2c' | 'c2c' | 'saas' | 'marketplace';
      complexity_level: 'low' | 'medium' | 'high';
    };
    confidence_score: number;     // 0-1 的置信度
    suggestions?: string[];       // 改进建议
  };
  message: string;
  processing_time_ms: number;
}
```

**Mock响应示例**:
```json
{
  "success": true,
  "data": {
    "requirement_id": "req_12345",
    "parsed_data": {
      "project_type": "web_app",
      "target_users": [
        {
          "age_range": "18-35",
          "occupation": "knowledge_worker",
          "tech_savvy": "medium"
        }
      ],
      "core_features": [
        {
          "name": "user_authentication",
          "priority": "high",
          "complexity": "medium"
        },
        {
          "name": "music_recommendation",
          "priority": "high", 
          "complexity": "high"
        }
      ],
      "technical_constraints": [
        {
          "type": "performance",
          "description": "fast_response_time",
          "value": "<2s"
        }
      ],
      "business_model": "b2c",
      "complexity_level": "medium"
    },
    "confidence_score": 0.87,
    "suggestions": ["考虑添加社交分享功能", "建议支持多种音乐平台"]
  },
  "message": "需求解析完成",
  "processing_time_ms": 2340
}
```

### 2. 项目规划API (Core Package负责实现)

#### POST /api/planning/generate
**用途**: 基于解析的需求生成完整项目规划

**请求格式**:
```typescript
interface PlanningGenerateRequest {
  requirement_id: string;         // 需求ID
  user_preferences?: {            // 用户偏好
    budget_range?: {
      min: number;
      max: number;
    };
    timeline_preference?: 'fast' | 'balanced' | 'thorough';
    tech_preference?: 'cutting_edge' | 'stable' | 'simple';
  };
}
```

**响应格式**:
```typescript
interface PlanningGenerateResponse {
  success: boolean;
  data: {
    plan_id: string;
    project_overview: {
      name: string;
      description: string;
      type: string;
      estimated_duration_weeks: number;
      team_size_recommendation: number;
    };
    user_journey: {
      stages: UserJourneyStage[];
      key_touchpoints: string[];
      pain_points: string[];
    };
    technical_architecture: {
      frontend_stack: TechStack;
      backend_stack: TechStack;
      database: TechStack;
      infrastructure: TechStack;
      third_party_services: ThirdPartyService[];
    };
    project_modules: ProjectModule[];
    development_timeline: {
      phases: DevelopmentPhase[];
      milestones: Milestone[];
      critical_path: string[];
    };
    budget_estimation: {
      development_cost: CostBreakdown;
      operational_cost: CostBreakdown;
      total_investment: number;
      roi_projection: ROIProjection;
    };
    risk_assessment: RiskAssessment[];
  };
  message: string;
  processing_time_ms: number;
}
```

### 3. 工作流API (API Package负责实现)

#### POST /api/workflow/requirement-to-plan
**用途**: 端到端工作流，从需求到规划的完整流程

**请求格式**:
```typescript
interface WorkflowRequest {
  user_input: string;
  user_id?: string;
  workflow_options?: {
    enable_interactive_adjustment: boolean;
    quality_threshold: number;      // 0-1
    enable_caching: boolean;
  };
}
```

**响应格式**:
```typescript
interface WorkflowResponse {
  success: boolean;
  data: {
    workflow_id: string;
    requirement: RequirementParseResponse['data'];
    plan: PlanningGenerateResponse['data'];
    quality_metrics: {
      overall_score: number;
      completeness_score: number;
      feasibility_score: number;
      consistency_score: number;
    };
    next_steps: string[];
  };
  message: string;
  total_processing_time_ms: number;
}
```

### 4. 用户管理API (API Package负责实现)

#### POST /api/auth/register
```typescript
interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

interface RegisterResponse {
  success: boolean;
  data: {
    user_id: string;
    access_token: string;
    refresh_token: string;
    expires_in: number;
  };
  message: string;
}
```

#### POST /api/auth/login
```typescript
interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  success: boolean;
  data: {
    user_id: string;
    access_token: string;
    refresh_token: string;
    expires_in: number;
    user_profile: {
      username: string;
      email: string;
      created_at: string;
    };
  };
  message: string;
}
```

### 5. 项目管理API (API Package负责实现)

#### GET /api/projects
```typescript
interface ProjectListResponse {
  success: boolean;
  data: {
    projects: ProjectSummary[];
    total_count: number;
    page: number;
    page_size: number;
  };
  message: string;
}
```

#### POST /api/projects
```typescript
interface CreateProjectRequest {
  name: string;
  description?: string;
  requirement_id?: string;
  plan_id?: string;
}

interface CreateProjectResponse {
  success: boolean;
  data: {
    project_id: string;
    name: string;
    status: 'planning' | 'in_progress' | 'completed';
    created_at: string;
  };
  message: string;
}
```

## 🎭 Mock服务器配置

### Mock服务器启动
```bash
# 使用json-server或mockserver
npm install -g json-server
json-server --watch packages/common/mock-data/api-responses.json --port 3001
```

### Mock数据文件结构
```javascript
// packages/common/mock-data/api-responses.json
{
  "requirements": [
    {
      "id": "req_12345",
      "user_input": "我想做一个音乐推荐APP",
      "parsed_data": { /* 上面的示例数据 */ }
    }
  ],
  "plans": [
    {
      "id": "plan_12345", 
      "requirement_id": "req_12345",
      "project_overview": { /* 规划数据 */ }
    }
  ],
  "users": [
    {
      "id": "user_12345",
      "email": "test@example.com",
      "username": "testuser"
    }
  ]
}
```

## 🔄 接口版本控制

### API版本策略
- 使用语义化版本控制 (v1.0.0)
- URL路径包含版本: `/api/v1/requirements/parse`
- 向后兼容保证: 至少支持前一个主版本

### 接口变更协议
```typescript
// 新增字段 - 向后兼容
interface RequirementParseResponse_v1_1 extends RequirementParseResponse_v1_0 {
  data: RequirementParseResponse_v1_0['data'] & {
    tags?: string[];              // 新增字段，可选
    sentiment_analysis?: {        // 新增嵌套对象，可选
      positivity: number;
      concerns: string[];
    };
  };
}
```

## 📊 接口监控和测试

### 接口测试套件
```typescript
// packages/common/tests/contract-tests.ts
describe('API Contract Tests', () => {
  test('POST /api/requirements/parse 符合契约', async () => {
    const response = await fetch('/api/requirements/parse', {
      method: 'POST',
      body: JSON.stringify({
        user_input: "测试需求"
      })
    });
    
    const data = await response.json();
    
    // 验证响应格式符合契约
    expect(data).toMatchSchema(RequirementParseResponseSchema);
    expect(data.success).toBe(true);
    expect(data.data.confidence_score).toBeGreaterThan(0);
  });
});
```

### 性能基准
```yaml
接口性能要求:
  - 需求解析: <30秒 (95分位数)
  - 规划生成: <120秒 (95分位数)  
  - 用户认证: <500ms (95分位数)
  - 项目列表: <200ms (95分位数)

并发处理能力:
  - 同时处理: ≥50个请求
  - 响应时间退化: <20%
  - 错误率: <1%
```

## 🎯 前端开发支持

### API客户端代码生成
```bash
# 基于OpenAPI规范生成TypeScript客户端
npx @openapitools/openapi-generator-cli generate \
  -i packages/common/contracts/openapi.yml \
  -g typescript-fetch \
  -o packages/frontend/src/api/generated
```

### React Hook封装
```typescript
// packages/frontend/src/hooks/useRequirementParsing.ts
export const useRequirementParsing = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RequirementParseResponse | null>(null);
  
  const parseRequirement = useCallback(async (input: string) => {
    setLoading(true);
    try {
      const response = await apiClient.parseRequirement({ user_input: input });
      setResult(response);
    } finally {
      setLoading(false);
    }
  }, []);
  
  return { parseRequirement, loading, result };
};
```

---

**🎯 通过严格的接口契约，实现真正的前后端并发开发！**
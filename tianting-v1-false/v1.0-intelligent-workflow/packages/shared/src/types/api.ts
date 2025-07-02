/**
 * 天庭系统API类型定义
 * 
 * 基于API契约规范的完整接口类型定义，确保前后端类型一致性
 */

import { 
  Timestamp, 
  ApiResponse, 
  ProjectType, 
  BusinessModel, 
  ComplexityLevel,
  PaginatedResponse,
  HealthCheckData
} from './common';

// ============= 需求理解API类型 =============

/**
 * 需求解析请求
 */
export interface RequirementParseRequest {
  /** 用户原始输入 */
  user_input: string;
  /** 可选的用户ID */
  user_id?: string;
  /** 可选的上下文信息 */
  context?: {
    /** 历史需求 */
    previous_requirements?: string[];
    /** 项目历史 */
    project_history?: string[];
  };
}

/**
 * 用户群体定义
 */
export interface UserGroup {
  /** 年龄范围 */
  age_range: string;
  /** 职业 */
  occupation: string;
  /** 技术熟练度 */
  tech_savvy: 'low' | 'medium' | 'high';
  /** 收入水平 */
  income_level?: 'low' | 'medium' | 'high';
  /** 地理位置 */
  location?: string;
  /** 使用场景 */
  use_case?: string;
}

/**
 * 功能特性定义
 */
export interface Feature {
  /** 功能名称 */
  name: string;
  /** 优先级 */
  priority: 'low' | 'medium' | 'high' | 'critical';
  /** 复杂度 */
  complexity: ComplexityLevel;
  /** 功能描述 */
  description?: string;
  /** 估算工时（小时） */
  estimated_hours?: number;
  /** 依赖的其他功能 */
  dependencies?: string[];
}

/**
 * 技术约束定义
 */
export interface Constraint {
  /** 约束类型 */
  type: 'performance' | 'security' | 'budget' | 'timeline' | 'technical' | 'business';
  /** 约束描述 */
  description: string;
  /** 约束值 */
  value: string;
  /** 是否为硬性约束 */
  is_hard_constraint?: boolean;
}

/**
 * 需求解析响应数据
 */
export interface RequirementParseData {
  /** 需求唯一标识 */
  requirement_id: string;
  /** 解析后的结构化数据 */
  parsed_data: {
    /** 项目类型 */
    project_type: ProjectType;
    /** 目标用户群体 */
    target_users: UserGroup[];
    /** 核心功能 */
    core_features: Feature[];
    /** 技术约束 */
    technical_constraints: Constraint[];
    /** 商业模式 */
    business_model: BusinessModel;
    /** 复杂度级别 */
    complexity_level: ComplexityLevel;
  };
  /** 置信度分数 (0-1) */
  confidence_score: number;
  /** 改进建议 */
  suggestions?: string[];
}

/**
 * 需求解析响应
 */
export interface RequirementParseResponse extends ApiResponse<RequirementParseData> {
  /** 处理时间（毫秒） */
  processing_time_ms: number;
}

// ============= 项目规划API类型 =============

/**
 * 项目规划生成请求
 */
export interface PlanningGenerateRequest {
  /** 需求ID */
  requirement_id: string;
  /** 用户偏好 */
  user_preferences?: {
    /** 预算范围 */
    budget_range?: {
      min: number;
      max: number;
    };
    /** 时间偏好 */
    timeline_preference?: 'fast' | 'balanced' | 'thorough';
    /** 技术偏好 */
    tech_preference?: 'cutting_edge' | 'stable' | 'simple';
  };
}

/**
 * 用户旅程阶段
 */
export interface UserJourneyStage {
  /** 阶段名称 */
  name: string;
  /** 阶段描述 */
  description: string;
  /** 用户目标 */
  user_goals: string[];
  /** 用户操作 */
  user_actions: string[];
  /** 接触点 */
  touchpoints: string[];
  /** 潜在痛点 */
  pain_points: string[];
  /** 改进机会 */
  opportunities: string[];
}

/**
 * 技术栈定义
 */
export interface TechStack {
  /** 技术名称 */
  name: string;
  /** 技术版本 */
  version: string;
  /** 选择理由 */
  reason: string;
  /** 学习曲线 */
  learning_curve: 'easy' | 'medium' | 'steep';
  /** 社区支持 */
  community_support: 'poor' | 'fair' | 'good' | 'excellent';
  /** 文档质量 */
  documentation: 'poor' | 'fair' | 'good' | 'excellent';
}

/**
 * 第三方服务
 */
export interface ThirdPartyService {
  /** 服务名称 */
  name: string;
  /** 服务类型 */
  type: 'payment' | 'authentication' | 'analytics' | 'storage' | 'communication' | 'other';
  /** 服务描述 */
  description: string;
  /** 月费用估算 */
  monthly_cost: number;
  /** 免费额度 */
  free_tier?: string;
  /** 集成复杂度 */
  integration_complexity: ComplexityLevel;
}

/**
 * 项目模块
 */
export interface ProjectModule {
  /** 模块名称 */
  name: string;
  /** 模块描述 */
  description: string;
  /** 模块类型 */
  type: 'frontend' | 'backend' | 'database' | 'api' | 'service' | 'component';
  /** 包含的功能 */
  features: string[];
  /** 估算工时 */
  estimated_hours: number;
  /** 依赖的模块 */
  dependencies: string[];
  /** 优先级 */
  priority: 'low' | 'medium' | 'high' | 'critical';
}

/**
 * 开发阶段
 */
export interface DevelopmentPhase {
  /** 阶段名称 */
  name: string;
  /** 阶段描述 */
  description: string;
  /** 开始时间（相对于项目开始的天数） */
  start_day: number;
  /** 持续天数 */
  duration_days: number;
  /** 阶段目标 */
  objectives: string[];
  /** 交付物 */
  deliverables: string[];
  /** 所需技能 */
  required_skills: string[];
}

/**
 * 里程碑
 */
export interface Milestone {
  /** 里程碑名称 */
  name: string;
  /** 里程碑描述 */
  description: string;
  /** 目标日期（相对于项目开始的天数） */
  target_day: number;
  /** 成功标准 */
  success_criteria: string[];
  /** 关键交付物 */
  key_deliverables: string[];
}

/**
 * 成本分解
 */
export interface CostBreakdown {
  /** 人力成本 */
  labor_cost: number;
  /** 技术成本 */
  technology_cost: number;
  /** 基础设施成本 */
  infrastructure_cost: number;
  /** 第三方服务成本 */
  third_party_cost: number;
  /** 其他成本 */
  other_cost: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * ROI预测
 */
export interface ROIProjection {
  /** 第一年收入预测 */
  year1_revenue: number;
  /** 第二年收入预测 */
  year2_revenue: number;
  /** 第三年收入预测 */
  year3_revenue: number;
  /** 投资回收期（月） */
  payback_period_months: number;
  /** 净现值 */
  net_present_value: number;
  /** 内部收益率 */
  internal_rate_of_return: number;
}

/**
 * 风险评估
 */
export interface RiskAssessment {
  /** 风险类型 */
  type: 'technical' | 'market' | 'resource' | 'timeline' | 'budget' | 'competitive';
  /** 风险描述 */
  description: string;
  /** 发生概率 */
  probability: 'low' | 'medium' | 'high';
  /** 影响程度 */
  impact: 'low' | 'medium' | 'high';
  /** 风险等级 */
  severity: 'low' | 'medium' | 'high' | 'critical';
  /** 缓解措施 */
  mitigation_strategies: string[];
  /** 应急计划 */
  contingency_plan?: string;
}

/**
 * 项目规划数据
 */
export interface PlanningGenerateData {
  /** 规划ID */
  plan_id: string;
  /** 项目概览 */
  project_overview: {
    /** 项目名称 */
    name: string;
    /** 项目描述 */
    description: string;
    /** 项目类型 */
    type: string;
    /** 预估持续时间（周） */
    estimated_duration_weeks: number;
    /** 推荐团队规模 */
    team_size_recommendation: number;
  };
  /** 用户旅程 */
  user_journey: {
    /** 旅程阶段 */
    stages: UserJourneyStage[];
    /** 关键接触点 */
    key_touchpoints: string[];
    /** 痛点 */
    pain_points: string[];
  };
  /** 技术架构 */
  technical_architecture: {
    /** 前端技术栈 */
    frontend_stack: TechStack;
    /** 后端技术栈 */
    backend_stack: TechStack;
    /** 数据库技术栈 */
    database: TechStack;
    /** 基础设施技术栈 */
    infrastructure: TechStack;
    /** 第三方服务 */
    third_party_services: ThirdPartyService[];
  };
  /** 项目模块 */
  project_modules: ProjectModule[];
  /** 开发时间线 */
  development_timeline: {
    /** 开发阶段 */
    phases: DevelopmentPhase[];
    /** 里程碑 */
    milestones: Milestone[];
    /** 关键路径 */
    critical_path: string[];
  };
  /** 预算估算 */
  budget_estimation: {
    /** 开发成本 */
    development_cost: CostBreakdown;
    /** 运营成本 */
    operational_cost: CostBreakdown;
    /** 总投资 */
    total_investment: number;
    /** ROI预测 */
    roi_projection: ROIProjection;
  };
  /** 风险评估 */
  risk_assessment: RiskAssessment[];
}

/**
 * 项目规划响应
 */
export interface PlanningGenerateResponse extends ApiResponse<PlanningGenerateData> {
  /** 处理时间（毫秒） */
  processing_time_ms: number;
}

// ============= 工作流API类型 =============

/**
 * 工作流请求
 */
export interface WorkflowRequest {
  /** 用户输入 */
  user_input: string;
  /** 用户ID */
  user_id?: string;
  /** 工作流选项 */
  workflow_options?: {
    /** 启用交互式调整 */
    enable_interactive_adjustment: boolean;
    /** 质量阈值 (0-1) */
    quality_threshold: number;
    /** 启用缓存 */
    enable_caching: boolean;
  };
}

/**
 * 质量指标
 */
export interface QualityMetrics {
  /** 整体评分 */
  overall_score: number;
  /** 完整性评分 */
  completeness_score: number;
  /** 可行性评分 */
  feasibility_score: number;
  /** 一致性评分 */
  consistency_score: number;
}

/**
 * 工作流数据
 */
export interface WorkflowData {
  /** 工作流ID */
  workflow_id: string;
  /** 需求解析结果 */
  requirement: RequirementParseData;
  /** 项目规划结果 */
  plan: PlanningGenerateData;
  /** 质量指标 */
  quality_metrics: QualityMetrics;
  /** 下一步建议 */
  next_steps: string[];
}

/**
 * 工作流响应
 */
export interface WorkflowResponse extends ApiResponse<WorkflowData> {
  /** 总处理时间 */
  total_processing_time_ms: number;
}

// ============= 用户管理API类型 =============

/**
 * 用户注册请求
 */
export interface RegisterRequest {
  /** 用户名 */
  username: string;
  /** 邮箱 */
  email: string;
  /** 密码 */
  password: string;
}

/**
 * 用户注册响应数据
 */
export interface RegisterData {
  /** 用户ID */
  user_id: string;
  /** 访问令牌 */
  access_token: string;
  /** 刷新令牌 */
  refresh_token: string;
  /** 令牌过期时间（秒） */
  expires_in: number;
}

/**
 * 用户注册响应
 */
export interface RegisterResponse extends ApiResponse<RegisterData> {}

/**
 * 用户登录请求
 */
export interface LoginRequest {
  /** 邮箱 */
  email: string;
  /** 密码 */
  password: string;
}

/**
 * 用户简档
 */
export interface UserProfile {
  /** 用户名 */
  username: string;
  /** 邮箱 */
  email: string;
  /** 创建时间 */
  created_at: Timestamp;
  /** 头像URL */
  avatar_url?: string;
  /** 个人简介 */
  bio?: string;
}

/**
 * 用户登录响应数据
 */
export interface LoginData {
  /** 用户ID */
  user_id: string;
  /** 访问令牌 */
  access_token: string;
  /** 刷新令牌 */
  refresh_token: string;
  /** 令牌过期时间（秒） */
  expires_in: number;
  /** 用户简档 */
  user_profile: UserProfile;
}

/**
 * 用户登录响应
 */
export interface LoginResponse extends ApiResponse<LoginData> {}

// ============= 项目管理API类型 =============

/**
 * 项目摘要
 */
export interface ProjectSummary {
  /** 项目ID */
  id: string;
  /** 项目名称 */
  name: string;
  /** 项目描述 */
  description: string;
  /** 项目状态 */
  status: 'planning' | 'in_progress' | 'completed' | 'paused' | 'cancelled';
  /** 项目类型 */
  project_type: ProjectType;
  /** 创建时间 */
  created_at: Timestamp;
  /** 更新时间 */
  updated_at: Timestamp;
  /** 完成进度 (0-100) */
  progress_percentage: number;
  /** 预估完成时间 */
  estimated_completion?: Timestamp;
}

/**
 * 项目列表响应
 */
export interface ProjectListResponse extends ApiResponse<PaginatedResponse<ProjectSummary>> {}

/**
 * 创建项目请求
 */
export interface CreateProjectRequest {
  /** 项目名称 */
  name: string;
  /** 项目描述 */
  description?: string;
  /** 需求ID */
  requirement_id?: string;
  /** 规划ID */
  plan_id?: string;
}

/**
 * 创建项目响应数据
 */
export interface CreateProjectData {
  /** 项目ID */
  project_id: string;
  /** 项目名称 */
  name: string;
  /** 项目状态 */
  status: 'planning' | 'in_progress' | 'completed';
  /** 创建时间 */
  created_at: Timestamp;
}

/**
 * 创建项目响应
 */
export interface CreateProjectResponse extends ApiResponse<CreateProjectData> {}

// ============= 通用API工具类型 =============

/**
 * API端点路径
 */
export const API_ENDPOINTS = {
  // 需求理解
  REQUIREMENT_PARSE: '/api/requirements/parse',
  
  // 项目规划
  PLANNING_GENERATE: '/api/planning/generate',
  
  // 工作流
  WORKFLOW_REQUIREMENT_TO_PLAN: '/api/workflow/requirement-to-plan',
  
  // 用户管理
  AUTH_REGISTER: '/api/auth/register',
  AUTH_LOGIN: '/api/auth/login',
  
  // 项目管理
  PROJECTS: '/api/projects',
  PROJECT_BY_ID: (id: string) => `/api/projects/${id}`,
} as const;

/**
 * HTTP方法类型
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

/**
 * API请求配置
 */
export interface ApiRequestConfig {
  /** 请求方法 */
  method: HttpMethod;
  /** 请求路径 */
  path: string;
  /** 请求头 */
  headers?: Record<string, string>;
  /** 查询参数 */
  query?: Record<string, string | number | boolean>;
  /** 请求体 */
  body?: Record<string, unknown>;
  /** 超时时间（毫秒） */
  timeout?: number;
}

/**
 * API客户端接口
 */
export interface ApiClient {
  /** 发送请求 */
  request<T>(config: ApiRequestConfig): Promise<T>;
  
  /** GET请求 */
  get<T>(path: string, query?: Record<string, string | number | boolean>): Promise<T>;
  
  /** POST请求 */
  post<T>(path: string, body?: Record<string, unknown>): Promise<T>;
  
  /** PUT请求 */
  put<T>(path: string, body?: Record<string, unknown>): Promise<T>;
  
  /** DELETE请求 */
  delete<T>(path: string): Promise<T>;
}

// ============= API类型守卫 =============

/**
 * 检查是否为有效的API响应
 */
export function isApiResponse<T>(response: any): response is ApiResponse<T> {
  return (
    response &&
    typeof response === 'object' &&
    typeof response.success === 'boolean' &&
    typeof response.message === 'string' &&
    typeof response.timestamp === 'string'
  );
}

/**
 * 检查是否为需求解析请求
 */
export function isRequirementParseRequest(request: any): request is RequirementParseRequest {
  return request && typeof request.user_input === 'string';
}

/**
 * 检查是否为项目规划请求
 */
export function isPlanningGenerateRequest(request: any): request is PlanningGenerateRequest {
  return request && typeof request.requirement_id === 'string';
}

// ============= 健康检查API类型 =============

/**
 * 健康检查响应
 */
export interface HealthCheckResponse extends ApiResponse<HealthCheckData> {}
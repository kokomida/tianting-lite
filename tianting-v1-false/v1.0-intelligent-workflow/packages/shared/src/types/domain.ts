/**
 * 天庭系统业务领域类型定义
 * 
 * 包含核心业务模型、实体定义和业务逻辑相关的类型
 */

import { 
  ID, 
  Timestamp, 
  ProjectType, 
  BusinessModel, 
  ComplexityLevel,
  TaskStatus,
  PriorityLevel,
  AuditInfo,
  Metadata,
  Constraint 
} from './common';

// ============= 需求模型 =============

/**
 * 需求模型
 */
export interface RequirementModel {
  /** 需求ID */
  id: ID;
  /** 用户原始输入 */
  user_input: string;
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
  /** 解析状态 */
  status: 'pending' | 'processing' | 'completed' | 'failed';
  /** 审计信息 */
  audit: AuditInfo;
  /** 元数据 */
  metadata?: Metadata;
}

/**
 * 用户群体
 */
export interface UserGroup {
  /** 用户群体ID */
  id: ID;
  /** 群体名称 */
  name: string;
  /** 年龄范围 */
  age_range: string;
  /** 职业分类 */
  occupation: string;
  /** 技术水平 */
  tech_savvy: 'low' | 'medium' | 'high';
  /** 收入水平 */
  income_level?: 'low' | 'medium' | 'high';
  /** 地理分布 */
  location?: string;
  /** 使用场景 */
  use_cases: string[];
  /** 用户画像描述 */
  persona_description: string;
  /** 用户规模估计 */
  estimated_size?: number;
  /** 用户价值评分 */
  value_score?: number;
}

/**
 * 功能特性
 */
export interface Feature {
  /** 功能ID */
  id: ID;
  /** 功能名称 */
  name: string;
  /** 功能描述 */
  description: string;
  /** 功能类型 */
  type: 'core' | 'secondary' | 'optional' | 'future';
  /** 优先级 */
  priority: PriorityLevel;
  /** 复杂度 */
  complexity: ComplexityLevel;
  /** 估算工时（小时） */
  estimated_hours: number;
  /** 依赖关系 */
  dependencies: ID[];
  /** 验收标准 */
  acceptance_criteria: string[];
  /** 用户故事 */
  user_stories: string[];
  /** 技术要求 */
  technical_requirements?: string[];
  /** 业务价值评分 */
  business_value_score: number;
  /** 实现状态 */
  implementation_status: TaskStatus;
}

// ============= 项目规划模型 =============

/**
 * 项目规划模型
 */
export interface ProjectPlan {
  /** 规划ID */
  id: ID;
  /** 关联的需求ID */
  requirement_id: ID;
  /** 规划版本 */
  version: number;
  /** 项目概览 */
  project_overview: ProjectOverview;
  /** 用户旅程 */
  user_journey: UserJourney;
  /** 技术架构 */
  technical_architecture: TechnicalArchitecture;
  /** 项目模块 */
  modules: ProjectModule[];
  /** 开发时间线 */
  development_timeline: DevelopmentTimeline;
  /** 预算估算 */
  budget_estimation: BudgetEstimation;
  /** 风险评估 */
  risk_assessment: RiskAssessment[];
  /** 规划状态 */
  status: 'draft' | 'reviewed' | 'approved' | 'in_use' | 'archived';
  /** 质量评分 */
  quality_score: number;
  /** 审计信息 */
  audit: AuditInfo;
  /** 元数据 */
  metadata?: Metadata;
}

/**
 * 项目概览
 */
export interface ProjectOverview {
  /** 项目名称 */
  name: string;
  /** 项目描述 */
  description: string;
  /** 项目愿景 */
  vision: string;
  /** 项目目标 */
  objectives: string[];
  /** 成功标准 */
  success_criteria: string[];
  /** 项目类型 */
  type: ProjectType;
  /** 商业模式 */
  business_model: BusinessModel;
  /** 目标市场 */
  target_market: string;
  /** 预估持续时间（周） */
  estimated_duration_weeks: number;
  /** 推荐团队规模 */
  team_size_recommendation: number;
  /** 项目标签 */
  tags: string[];
}

/**
 * 用户旅程
 */
export interface UserJourney {
  /** 旅程名称 */
  name: string;
  /** 旅程描述 */
  description: string;
  /** 旅程阶段 */
  stages: UserJourneyStage[];
  /** 关键接触点 */
  key_touchpoints: string[];
  /** 痛点分析 */
  pain_points: PainPoint[];
  /** 机会点 */
  opportunities: Opportunity[];
  /** 用户情感曲线 */
  emotion_curve?: EmotionPoint[];
}

/**
 * 用户旅程阶段
 */
export interface UserJourneyStage {
  /** 阶段ID */
  id: ID;
  /** 阶段名称 */
  name: string;
  /** 阶段描述 */
  description: string;
  /** 阶段序号 */
  order: number;
  /** 用户目标 */
  user_goals: string[];
  /** 用户操作 */
  user_actions: string[];
  /** 接触点 */
  touchpoints: string[];
  /** 用户期望 */
  user_expectations: string[];
  /** 系统响应 */
  system_responses: string[];
  /** 阶段时长（分钟） */
  duration_minutes?: number;
  /** 成功指标 */
  success_metrics: string[];
}

/**
 * 痛点
 */
export interface PainPoint {
  /** 痛点ID */
  id: ID;
  /** 痛点描述 */
  description: string;
  /** 痛点类型 */
  type: 'usability' | 'performance' | 'content' | 'technical' | 'business';
  /** 严重程度 */
  severity: 'low' | 'medium' | 'high' | 'critical';
  /** 影响范围 */
  impact_scope: string;
  /** 出现频率 */
  frequency: 'rare' | 'occasional' | 'frequent' | 'always';
  /** 解决方案建议 */
  solution_suggestions: string[];
  /** 相关阶段 */
  related_stages: ID[];
}

/**
 * 机会点
 */
export interface Opportunity {
  /** 机会ID */
  id: ID;
  /** 机会描述 */
  description: string;
  /** 机会类型 */
  type: 'feature' | 'improvement' | 'optimization' | 'innovation';
  /** 商业价值 */
  business_value: 'low' | 'medium' | 'high' | 'critical';
  /** 实现难度 */
  implementation_difficulty: ComplexityLevel;
  /** 预估投入 */
  estimated_effort: string;
  /** 预期收益 */
  expected_benefit: string;
  /** 相关阶段 */
  related_stages: ID[];
}

/**
 * 情感点
 */
export interface EmotionPoint {
  /** 阶段ID */
  stage_id: ID;
  /** 情感值 (-100 到 100) */
  emotion_value: number;
  /** 情感描述 */
  emotion_description: string;
  /** 影响因素 */
  influencing_factors: string[];
}

// ============= 技术架构模型 =============

/**
 * 技术架构
 */
export interface TechnicalArchitecture {
  /** 架构ID */
  id: ID;
  /** 架构名称 */
  name: string;
  /** 架构描述 */
  description: string;
  /** 架构原则 */
  principles: string[];
  /** 技术栈 */
  technology_stacks: {
    /** 前端技术栈 */
    frontend: TechStack;
    /** 后端技术栈 */
    backend: TechStack;
    /** 数据库技术栈 */
    database: TechStack;
    /** 基础设施技术栈 */
    infrastructure: TechStack;
    /** 开发工具链 */
    development_tools: TechStack;
  };
  /** 第三方服务 */
  third_party_services: ThirdPartyService[];
  /** 系统集成 */
  system_integrations: SystemIntegration[];
  /** 部署架构 */
  deployment_architecture: DeploymentArchitecture;
  /** 数据架构 */
  data_architecture: DataArchitecture;
  /** 安全架构 */
  security_architecture: SecurityArchitecture;
  /** 性能要求 */
  performance_requirements: PerformanceRequirement[];
  /** 可扩展性设计 */
  scalability_design: ScalabilityDesign;
}

/**
 * 技术栈
 */
export interface TechStack {
  /** 技术栈ID */
  id: ID;
  /** 技术栈名称 */
  name: string;
  /** 技术分类 */
  category: 'frontend' | 'backend' | 'database' | 'infrastructure' | 'tools';
  /** 技术列表 */
  technologies: Technology[];
  /** 选择理由 */
  selection_rationale: string;
  /** 学习曲线评估 */
  learning_curve_assessment: string;
  /** 团队技能匹配度 */
  team_skill_match: 'poor' | 'fair' | 'good' | 'excellent';
  /** 社区支持评估 */
  community_support_assessment: string;
  /** 长期维护性 */
  long_term_maintainability: 'low' | 'medium' | 'high';
}

/**
 * 技术
 */
export interface Technology {
  /** 技术ID */
  id: ID;
  /** 技术名称 */
  name: string;
  /** 技术版本 */
  version: string;
  /** 技术描述 */
  description: string;
  /** 使用目的 */
  purpose: string;
  /** 选择理由 */
  selection_reason: string;
  /** 学习曲线 */
  learning_curve: 'easy' | 'medium' | 'steep';
  /** 社区支持 */
  community_support: 'poor' | 'fair' | 'good' | 'excellent';
  /** 文档质量 */
  documentation_quality: 'poor' | 'fair' | 'good' | 'excellent';
  /** 许可证类型 */
  license_type: string;
  /** 成本评估 */
  cost_assessment: string;
  /** 替代方案 */
  alternatives?: string[];
}

/**
 * 第三方服务
 */
export interface ThirdPartyService {
  /** 服务ID */
  id: ID;
  /** 服务名称 */
  name: string;
  /** 服务提供商 */
  provider: string;
  /** 服务类型 */
  type: 'payment' | 'authentication' | 'analytics' | 'storage' | 'communication' | 'ai' | 'monitoring' | 'other';
  /** 服务描述 */
  description: string;
  /** 集成方式 */
  integration_method: 'api' | 'sdk' | 'webhook' | 'embedded' | 'direct';
  /** 定价模式 */
  pricing_model: 'free' | 'freemium' | 'subscription' | 'usage_based' | 'one_time';
  /** 月费用估算 */
  monthly_cost_estimate: number;
  /** 免费额度 */
  free_tier_limits?: string;
  /** 集成复杂度 */
  integration_complexity: ComplexityLevel;
  /** SLA保证 */
  sla_guarantees?: string;
  /** 数据隐私考虑 */
  privacy_considerations: string[];
  /** 依赖风险 */
  dependency_risks: string[];
}

/**
 * 系统集成
 */
export interface SystemIntegration {
  /** 集成ID */
  id: ID;
  /** 集成名称 */
  name: string;
  /** 集成类型 */
  type: 'internal' | 'external' | 'third_party';
  /** 源系统 */
  source_system: string;
  /** 目标系统 */
  target_system: string;
  /** 集成模式 */
  integration_pattern: 'synchronous' | 'asynchronous' | 'batch' | 'real_time';
  /** 数据传输格式 */
  data_format: 'json' | 'xml' | 'csv' | 'binary' | 'custom';
  /** 传输协议 */
  transport_protocol: 'http' | 'https' | 'websocket' | 'message_queue' | 'file_transfer';
  /** 安全要求 */
  security_requirements: string[];
  /** 性能要求 */
  performance_requirements: string[];
  /** 错误处理策略 */
  error_handling_strategy: string;
  /** 监控要求 */
  monitoring_requirements: string[];
}

/**
 * 部署架构
 */
export interface DeploymentArchitecture {
  /** 部署模式 */
  deployment_model: 'monolith' | 'microservices' | 'serverless' | 'hybrid';
  /** 云服务商 */
  cloud_provider: 'aws' | 'azure' | 'gcp' | 'alibaba' | 'self_hosted' | 'multi_cloud';
  /** 容器化策略 */
  containerization_strategy: 'docker' | 'kubernetes' | 'none';
  /** 环境配置 */
  environments: DeploymentEnvironment[];
  /** CI/CD流水线 */
  cicd_pipeline: CICDPipeline;
  /** 监控和日志 */
  monitoring_and_logging: MonitoringSetup;
  /** 灾难恢复 */
  disaster_recovery: DisasterRecoveryPlan;
}

/**
 * 部署环境
 */
export interface DeploymentEnvironment {
  /** 环境名称 */
  name: 'development' | 'testing' | 'staging' | 'production';
  /** 环境描述 */
  description: string;
  /** 资源配置 */
  resource_allocation: ResourceAllocation;
  /** 访问控制 */
  access_control: string[];
  /** 数据配置 */
  data_configuration: string;
  /** 第三方服务配置 */
  third_party_configurations: string[];
}

/**
 * 资源分配
 */
export interface ResourceAllocation {
  /** CPU核心数 */
  cpu_cores: number;
  /** 内存大小（GB） */
  memory_gb: number;
  /** 存储大小（GB） */
  storage_gb: number;
  /** 网络带宽（Mbps） */
  network_bandwidth_mbps: number;
  /** 实例数量 */
  instance_count: number;
  /** 预估月费用 */
  estimated_monthly_cost: number;
}

/**
 * CI/CD流水线
 */
export interface CICDPipeline {
  /** 版本控制系统 */
  version_control: 'git' | 'svn' | 'mercurial';
  /** 代码仓库 */
  repository_platform: 'github' | 'gitlab' | 'bitbucket' | 'azure_devops' | 'self_hosted';
  /** 构建工具 */
  build_tools: string[];
  /** 测试策略 */
  testing_strategy: TestingStrategy;
  /** 部署策略 */
  deployment_strategy: 'blue_green' | 'rolling' | 'canary' | 'recreate';
  /** 自动化程度 */
  automation_level: 'manual' | 'semi_automated' | 'fully_automated';
  /** 质量门禁 */
  quality_gates: string[];
}

/**
 * 测试策略
 */
export interface TestingStrategy {
  /** 单元测试 */
  unit_testing: {
    enabled: boolean;
    coverage_threshold: number;
    tools: string[];
  };
  /** 集成测试 */
  integration_testing: {
    enabled: boolean;
    scope: string[];
    tools: string[];
  };
  /** 端到端测试 */
  e2e_testing: {
    enabled: boolean;
    scenarios: string[];
    tools: string[];
  };
  /** 性能测试 */
  performance_testing: {
    enabled: boolean;
    load_requirements: string[];
    tools: string[];
  };
  /** 安全测试 */
  security_testing: {
    enabled: boolean;
    scan_types: string[];
    tools: string[];
  };
}

/**
 * 监控设置
 */
export interface MonitoringSetup {
  /** 应用监控 */
  application_monitoring: {
    tools: string[];
    metrics: string[];
    alerts: string[];
  };
  /** 基础设施监控 */
  infrastructure_monitoring: {
    tools: string[];
    metrics: string[];
    alerts: string[];
  };
  /** 日志管理 */
  log_management: {
    tools: string[];
    log_levels: string[];
    retention_policy: string;
  };
  /** 用户体验监控 */
  user_experience_monitoring: {
    tools: string[];
    metrics: string[];
    real_user_monitoring: boolean;
  };
}

/**
 * 灾难恢复计划
 */
export interface DisasterRecoveryPlan {
  /** 备份策略 */
  backup_strategy: {
    frequency: 'daily' | 'weekly' | 'monthly';
    retention_period: string;
    backup_locations: string[];
    automated: boolean;
  };
  /** 恢复目标 */
  recovery_objectives: {
    rto_hours: number; // Recovery Time Objective
    rpo_hours: number; // Recovery Point Objective
  };
  /** 故障切换策略 */
  failover_strategy: string;
  /** 测试计划 */
  testing_schedule: string;
}

/**
 * 数据架构
 */
export interface DataArchitecture {
  /** 数据模型 */
  data_models: DataModel[];
  /** 数据流图 */
  data_flows: DataFlow[];
  /** 数据存储策略 */
  storage_strategy: DataStorageStrategy;
  /** 数据安全策略 */
  security_strategy: DataSecurityStrategy;
  /** 数据治理 */
  governance: DataGovernance;
  /** 数据备份恢复 */
  backup_recovery: DataBackupRecovery;
}

/**
 * 数据模型
 */
export interface DataModel {
  /** 模型ID */
  id: ID;
  /** 模型名称 */
  name: string;
  /** 模型类型 */
  type: 'entity' | 'value_object' | 'aggregate' | 'service';
  /** 属性列表 */
  attributes: DataAttribute[];
  /** 关系 */
  relationships: DataRelationship[];
  /** 约束条件 */
  constraints: string[];
  /** 索引策略 */
  indexing_strategy: string[];
}

/**
 * 数据属性
 */
export interface DataAttribute {
  /** 属性名称 */
  name: string;
  /** 属性类型 */
  type: string;
  /** 是否必需 */
  required: boolean;
  /** 默认值 */
  default_value?: string | number | boolean;
  /** 约束条件 */
  constraints?: string[];
  /** 描述 */
  description: string;
}

/**
 * 数据关系
 */
export interface DataRelationship {
  /** 关系类型 */
  type: 'one_to_one' | 'one_to_many' | 'many_to_many';
  /** 目标模型 */
  target_model: string;
  /** 关系描述 */
  description: string;
  /** 外键字段 */
  foreign_key?: string;
}

/**
 * 数据流
 */
export interface DataFlow {
  /** 流ID */
  id: ID;
  /** 流名称 */
  name: string;
  /** 源系统 */
  source: string;
  /** 目标系统 */
  destination: string;
  /** 数据类型 */
  data_type: string;
  /** 传输频率 */
  frequency: 'real_time' | 'batch' | 'scheduled';
  /** 数据转换 */
  transformations: string[];
  /** 质量检查 */
  quality_checks: string[];
}

/**
 * 数据存储策略
 */
export interface DataStorageStrategy {
  /** 主数据库 */
  primary_database: {
    type: 'sql' | 'nosql' | 'graph' | 'time_series';
    technology: string;
    configuration: string;
  };
  /** 缓存策略 */
  caching_strategy: {
    levels: string[];
    technologies: string[];
    policies: string[];
  };
  /** 数据分片 */
  sharding_strategy?: {
    strategy: 'horizontal' | 'vertical' | 'functional';
    criteria: string;
  };
  /** 数据复制 */
  replication_strategy?: {
    type: 'master_slave' | 'master_master' | 'cluster';
    configuration: string;
  };
}

/**
 * 数据安全策略
 */
export interface DataSecurityStrategy {
  /** 加密策略 */
  encryption: {
    at_rest: boolean;
    in_transit: boolean;
    algorithms: string[];
  };
  /** 访问控制 */
  access_control: {
    authentication: string[];
    authorization: string[];
    audit_logging: boolean;
  };
  /** 数据脱敏 */
  data_masking: {
    enabled: boolean;
    techniques: string[];
    environments: string[];
  };
  /** 隐私保护 */
  privacy_protection: {
    gdpr_compliance: boolean;
    data_retention_policies: string[];
    right_to_be_forgotten: boolean;
  };
}

/**
 * 数据治理
 */
export interface DataGovernance {
  /** 数据质量标准 */
  quality_standards: string[];
  /** 元数据管理 */
  metadata_management: {
    enabled: boolean;
    tools: string[];
    standards: string[];
  };
  /** 数据血缘 */
  data_lineage: {
    tracking_enabled: boolean;
    tools: string[];
  };
  /** 数据分类 */
  data_classification: {
    sensitivity_levels: string[];
    classification_criteria: string[];
  };
}

/**
 * 数据备份恢复
 */
export interface DataBackupRecovery {
  /** 备份策略 */
  backup_strategy: {
    full_backup_frequency: string;
    incremental_backup_frequency: string;
    backup_locations: string[];
  };
  /** 恢复策略 */
  recovery_strategy: {
    point_in_time_recovery: boolean;
    cross_region_recovery: boolean;
    automated_recovery: boolean;
  };
  /** 测试策略 */
  testing_strategy: {
    recovery_testing_frequency: string;
    automated_testing: boolean;
  };
}

/**
 * 安全架构
 */
export interface SecurityArchitecture {
  /** 认证策略 */
  authentication_strategy: AuthenticationStrategy;
  /** 授权策略 */
  authorization_strategy: AuthorizationStrategy;
  /** 网络安全 */
  network_security: NetworkSecurity;
  /** 应用安全 */
  application_security: ApplicationSecurity;
  /** 数据安全 */
  data_security: DataSecurityStrategy;
  /** 合规要求 */
  compliance_requirements: ComplianceRequirement[];
  /** 安全监控 */
  security_monitoring: SecurityMonitoring;
  /** 事件响应 */
  incident_response: IncidentResponsePlan;
}

/**
 * 认证策略
 */
export interface AuthenticationStrategy {
  /** 认证方法 */
  methods: ('password' | 'mfa' | 'sso' | 'oauth' | 'saml' | 'biometric')[];
  /** 密码策略 */
  password_policy: {
    min_length: number;
    complexity_requirements: string[];
    expiration_days: number;
    history_count: number;
  };
  /** 多因素认证 */
  multi_factor_auth: {
    enabled: boolean;
    methods: string[];
    required_for: string[];
  };
  /** 单点登录 */
  single_sign_on: {
    enabled: boolean;
    provider: string;
    protocols: string[];
  };
}

/**
 * 授权策略
 */
export interface AuthorizationStrategy {
  /** 授权模型 */
  model: 'rbac' | 'abac' | 'dac' | 'mac';
  /** 角色定义 */
  roles: Role[];
  /** 权限定义 */
  permissions: Permission[];
  /** 访问控制矩阵 */
  access_control_matrix: AccessControlRule[];
}

/**
 * 角色
 */
export interface Role {
  /** 角色ID */
  id: ID;
  /** 角色名称 */
  name: string;
  /** 角色描述 */
  description: string;
  /** 角色权限 */
  permissions: ID[];
  /** 继承关系 */
  inherits_from?: ID[];
}

/**
 * 权限
 */
export interface Permission {
  /** 权限ID */
  id: ID;
  /** 权限名称 */
  name: string;
  /** 权限描述 */
  description: string;
  /** 资源类型 */
  resource_type: string;
  /** 操作类型 */
  action: string;
  /** 条件 */
  conditions?: string[];
}

/**
 * 访问控制规则
 */
export interface AccessControlRule {
  /** 规则ID */
  id: ID;
  /** 主体 */
  subject: string;
  /** 资源 */
  resource: string;
  /** 操作 */
  action: string;
  /** 效果 */
  effect: 'allow' | 'deny';
  /** 条件 */
  conditions?: string[];
}

/**
 * 网络安全
 */
export interface NetworkSecurity {
  /** 防火墙配置 */
  firewall: {
    enabled: boolean;
    rules: string[];
    web_application_firewall: boolean;
  };
  /** VPN配置 */
  vpn: {
    enabled: boolean;
    type: string;
    protocols: string[];
  };
  /** DDoS防护 */
  ddos_protection: {
    enabled: boolean;
    provider: string;
    thresholds: string[];
  };
  /** 网络分段 */
  network_segmentation: {
    enabled: boolean;
    strategy: string;
    zones: string[];
  };
}

/**
 * 应用安全
 */
export interface ApplicationSecurity {
  /** 代码安全 */
  code_security: {
    static_analysis: boolean;
    dynamic_analysis: boolean;
    dependency_scanning: boolean;
    tools: string[];
  };
  /** 运行时保护 */
  runtime_protection: {
    waf_enabled: boolean;
    rasp_enabled: boolean;
    protection_rules: string[];
  };
  /** API安全 */
  api_security: {
    rate_limiting: boolean;
    authentication_required: boolean;
    input_validation: boolean;
    output_filtering: boolean;
  };
  /** 会话管理 */
  session_management: {
    secure_cookies: boolean;
    session_timeout: number;
    concurrent_sessions_limit: number;
  };
}

/**
 * 合规要求
 */
export interface ComplianceRequirement {
  /** 合规标准 */
  standard: 'gdpr' | 'hipaa' | 'sox' | 'pci_dss' | 'iso_27001' | 'custom';
  /** 要求描述 */
  description: string;
  /** 适用范围 */
  scope: string[];
  /** 控制措施 */
  controls: string[];
  /** 审计要求 */
  audit_requirements: string[];
  /** 合规状态 */
  compliance_status: 'compliant' | 'partial' | 'non_compliant' | 'not_assessed';
}

/**
 * 安全监控
 */
export interface SecurityMonitoring {
  /** SIEM系统 */
  siem: {
    enabled: boolean;
    tools: string[];
    log_sources: string[];
  };
  /** 威胁检测 */
  threat_detection: {
    enabled: boolean;
    detection_rules: string[];
    threat_intelligence: boolean;
  };
  /** 漏洞管理 */
  vulnerability_management: {
    scanning_frequency: string;
    tools: string[];
    remediation_sla: string;
  };
  /** 安全指标 */
  security_metrics: {
    kpis: string[];
    reporting_frequency: string;
    dashboards: string[];
  };
}

/**
 * 事件响应计划
 */
export interface IncidentResponsePlan {
  /** 响应团队 */
  response_team: {
    roles: string[];
    contacts: string[];
    escalation_matrix: string[];
  };
  /** 响应流程 */
  response_process: {
    detection: string[];
    analysis: string[];
    containment: string[];
    eradication: string[];
    recovery: string[];
    lessons_learned: string[];
  };
  /** 通信计划 */
  communication_plan: {
    internal_notifications: string[];
    external_notifications: string[];
    media_response: string[];
  };
  /** 恢复程序 */
  recovery_procedures: {
    backup_restoration: string[];
    system_rebuilding: string[];
    service_restoration: string[];
  };
}

/**
 * 性能要求
 */
export interface PerformanceRequirement {
  /** 要求ID */
  id: ID;
  /** 要求名称 */
  name: string;
  /** 指标类型 */
  metric_type: 'response_time' | 'throughput' | 'concurrent_users' | 'availability' | 'resource_usage';
  /** 目标值 */
  target_value: number;
  /** 单位 */
  unit: string;
  /** 测量条件 */
  measurement_conditions: string[];
  /** 优先级 */
  priority: PriorityLevel;
  /** 监控方法 */
  monitoring_method: string;
}

/**
 * 可扩展性设计
 */
export interface ScalabilityDesign {
  /** 水平扩展 */
  horizontal_scaling: {
    enabled: boolean;
    strategy: string;
    auto_scaling: boolean;
    scaling_triggers: string[];
  };
  /** 垂直扩展 */
  vertical_scaling: {
    enabled: boolean;
    strategy: string;
    resource_limits: string[];
  };
  /** 数据库扩展 */
  database_scaling: {
    read_replicas: boolean;
    sharding: boolean;
    caching_layers: string[];
  };
  /** 缓存策略 */
  caching_strategy: {
    levels: string[];
    technologies: string[];
    invalidation_strategy: string;
  };
  /** CDN配置 */
  cdn_configuration: {
    enabled: boolean;
    provider: string;
    caching_rules: string[];
  };
}

// ============= 项目模块 =============

/**
 * 项目模块
 */
export interface ProjectModule {
  /** 模块ID */
  id: ID;
  /** 模块名称 */
  name: string;
  /** 模块描述 */
  description: string;
  /** 模块类型 */
  type: 'frontend' | 'backend' | 'database' | 'api' | 'service' | 'component' | 'library' | 'infrastructure';
  /** 父模块 */
  parent_module_id?: ID;
  /** 子模块 */
  child_modules: ID[];
  /** 包含的功能 */
  features: ID[];
  /** 技术栈 */
  technology_stack: string[];
  /** 开发优先级 */
  development_priority: PriorityLevel;
  /** 估算工时 */
  estimated_hours: number;
  /** 实际工时 */
  actual_hours?: number;
  /** 依赖的模块 */
  dependencies: ModuleDependency[];
  /** 接口定义 */
  interfaces: ModuleInterface[];
  /** 配置参数 */
  configuration_parameters: ConfigurationParameter[];
  /** 测试要求 */
  testing_requirements: TestingRequirement[];
  /** 文档要求 */
  documentation_requirements: string[];
  /** 模块状态 */
  status: TaskStatus;
  /** 负责人 */
  assignee?: string;
  /** 审计信息 */
  audit: AuditInfo;
}

/**
 * 模块依赖
 */
export interface ModuleDependency {
  /** 依赖模块ID */
  module_id: ID;
  /** 依赖类型 */
  type: 'build' | 'runtime' | 'development' | 'test';
  /** 依赖强度 */
  strength: 'strong' | 'weak' | 'optional';
  /** 依赖描述 */
  description: string;
}

/**
 * 模块接口
 */
export interface ModuleInterface {
  /** 接口ID */
  id: ID;
  /** 接口名称 */
  name: string;
  /** 接口类型 */
  type: 'api' | 'event' | 'data' | 'service';
  /** 接口描述 */
  description: string;
  /** 输入参数 */
  input_parameters: InterfaceParameter[];
  /** 输出参数 */
  output_parameters: InterfaceParameter[];
  /** 错误处理 */
  error_handling: string[];
  /** 版本 */
  version: string;
  /** 稳定性 */
  stability: 'experimental' | 'beta' | 'stable' | 'deprecated';
}

/**
 * 接口参数
 */
export interface InterfaceParameter {
  /** 参数名称 */
  name: string;
  /** 参数类型 */
  type: string;
  /** 是否必需 */
  required: boolean;
  /** 默认值 */
  default_value?: string | number | boolean;
  /** 参数描述 */
  description: string;
  /** 验证规则 */
  validation_rules?: string[];
}

/**
 * 配置参数
 */
export interface ConfigurationParameter {
  /** 参数名称 */
  name: string;
  /** 参数类型 */
  type: string;
  /** 默认值 */
  default_value: any;
  /** 参数描述 */
  description: string;
  /** 是否敏感 */
  sensitive: boolean;
  /** 环境特定 */
  environment_specific: boolean;
  /** 验证规则 */
  validation_rules?: string[];
}

/**
 * 测试要求
 */
export interface TestingRequirement {
  /** 测试类型 */
  type: 'unit' | 'integration' | 'e2e' | 'performance' | 'security';
  /** 覆盖率要求 */
  coverage_requirement: number;
  /** 测试工具 */
  testing_tools: string[];
  /** 测试环境 */
  test_environments: string[];
  /** 自动化程度 */
  automation_level: 'manual' | 'semi_automated' | 'fully_automated';
}

// ============= 开发时间线 =============

/**
 * 开发时间线
 */
export interface DevelopmentTimeline {
  /** 时间线ID */
  id: ID;
  /** 时间线名称 */
  name: string;
  /** 项目开始日期 */
  start_date: Timestamp;
  /** 项目结束日期 */
  end_date: Timestamp;
  /** 总工期（天） */
  total_duration_days: number;
  /** 开发阶段 */
  phases: DevelopmentPhase[];
  /** 里程碑 */
  milestones: Milestone[];
  /** 关键路径 */
  critical_path: CriticalPathItem[];
  /** 资源分配 */
  resource_allocation: ResourceAllocation[];
  /** 风险缓冲 */
  risk_buffer_days: number;
  /** 并行开发策略 */
  parallel_development_strategy: string;
}

/**
 * 开发阶段
 */
export interface DevelopmentPhase {
  /** 阶段ID */
  id: ID;
  /** 阶段名称 */
  name: string;
  /** 阶段描述 */
  description: string;
  /** 阶段类型 */
  type: 'planning' | 'design' | 'development' | 'testing' | 'deployment' | 'maintenance';
  /** 开始日期 */
  start_date: Timestamp;
  /** 结束日期 */
  end_date: Timestamp;
  /** 持续天数 */
  duration_days: number;
  /** 前置阶段 */
  predecessor_phases: ID[];
  /** 后续阶段 */
  successor_phases: ID[];
  /** 阶段目标 */
  objectives: string[];
  /** 交付物 */
  deliverables: Deliverable[];
  /** 验收标准 */
  acceptance_criteria: string[];
  /** 所需技能 */
  required_skills: string[];
  /** 资源需求 */
  resource_requirements: ResourceRequirement[];
  /** 质量门禁 */
  quality_gates: QualityGate[];
  /** 阶段状态 */
  status: TaskStatus;
}

/**
 * 交付物
 */
export interface Deliverable {
  /** 交付物ID */
  id: ID;
  /** 交付物名称 */
  name: string;
  /** 交付物类型 */
  type: 'document' | 'code' | 'design' | 'prototype' | 'test_result' | 'deployment_package';
  /** 交付物描述 */
  description: string;
  /** 负责人 */
  owner: string;
  /** 交付日期 */
  delivery_date: Timestamp;
  /** 质量标准 */
  quality_standards: string[];
  /** 审核要求 */
  review_requirements: string[];
  /** 交付状态 */
  status: TaskStatus;
}

/**
 * 资源需求
 */
export interface ResourceRequirement {
  /** 资源类型 */
  type: 'human' | 'hardware' | 'software' | 'infrastructure';
  /** 资源描述 */
  description: string;
  /** 所需数量 */
  quantity: number;
  /** 技能要求 */
  skill_requirements?: string[];
  /** 使用期间 */
  usage_period: {
    start_date: Timestamp;
    end_date: Timestamp;
  };
  /** 优先级 */
  priority: PriorityLevel;
}

/**
 * 质量门禁
 */
export interface QualityGate {
  /** 门禁ID */
  id: ID;
  /** 门禁名称 */
  name: string;
  /** 检查项 */
  criteria: QualityCriterion[];
  /** 是否阻塞 */
  blocking: boolean;
  /** 负责人 */
  owner: string;
  /** 检查状态 */
  status: 'pending' | 'passed' | 'failed' | 'waived';
}

/**
 * 质量标准
 */
export interface QualityCriterion {
  /** 标准名称 */
  name: string;
  /** 标准描述 */
  description: string;
  /** 目标值 */
  target_value: any;
  /** 实际值 */
  actual_value?: any;
  /** 检查方法 */
  measurement_method: string;
  /** 是否通过 */
  passed?: boolean;
}

/**
 * 里程碑
 */
export interface Milestone {
  /** 里程碑ID */
  id: ID;
  /** 里程碑名称 */
  name: string;
  /** 里程碑描述 */
  description: string;
  /** 里程碑类型 */
  type: 'project_start' | 'phase_completion' | 'deliverable_due' | 'external_dependency' | 'project_end';
  /** 目标日期 */
  target_date: Timestamp;
  /** 实际日期 */
  actual_date?: Timestamp;
  /** 成功标准 */
  success_criteria: string[];
  /** 关键交付物 */
  key_deliverables: ID[];
  /** 负责人 */
  owner: string;
  /** 里程碑状态 */
  status: 'upcoming' | 'in_progress' | 'achieved' | 'missed' | 'rescheduled';
  /** 里程碑权重 */
  weight: number;
}

/**
 * 关键路径项
 */
export interface CriticalPathItem {
  /** 任务ID */
  task_id: ID;
  /** 任务名称 */
  task_name: string;
  /** 开始日期 */
  start_date: Timestamp;
  /** 结束日期 */
  end_date: Timestamp;
  /** 持续时间 */
  duration_days: number;
  /** 松弛时间 */
  slack_days: number;
  /** 前置任务 */
  predecessors: ID[];
  /** 后续任务 */
  successors: ID[];
}

// ============= 预算估算 =============

/**
 * 预算估算
 */
export interface BudgetEstimation {
  /** 估算ID */
  id: ID;
  /** 估算版本 */
  version: number;
  /** 估算日期 */
  estimation_date: Timestamp;
  /** 估算方法 */
  estimation_method: 'bottom_up' | 'top_down' | 'parametric' | 'analogous' | 'expert_judgment';
  /** 置信度 */
  confidence_level: number;
  /** 开发成本 */
  development_cost: CostBreakdown;
  /** 运营成本 */
  operational_cost: CostBreakdown;
  /** 总投资 */
  total_investment: number;
  /** ROI预测 */
  roi_projection: ROIProjection;
  /** 成本分摊 */
  cost_allocation: CostAllocation[];
  /** 预算假设 */
  assumptions: string[];
  /** 成本风险 */
  cost_risks: CostRisk[];
}

/**
 * 成本分解
 */
export interface CostBreakdown {
  /** 人力成本 */
  labor_cost: LaborCost;
  /** 技术成本 */
  technology_cost: TechnologyCost;
  /** 基础设施成本 */
  infrastructure_cost: InfrastructureCost;
  /** 第三方服务成本 */
  third_party_cost: ThirdPartyCost;
  /** 培训成本 */
  training_cost: number;
  /** 咨询成本 */
  consulting_cost: number;
  /** 其他成本 */
  other_cost: number;
  /** 小计 */
  subtotal: number;
  /** 应急费用（%） */
  contingency_percentage: number;
  /** 应急费用 */
  contingency_amount: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * 人力成本
 */
export interface LaborCost {
  /** 角色成本 */
  role_costs: RoleCost[];
  /** 总工时 */
  total_hours: number;
  /** 平均时薪 */
  average_hourly_rate: number;
  /** 总人力成本 */
  total_labor_cost: number;
  /** 福利成本（%） */
  benefits_percentage: number;
  /** 福利成本 */
  benefits_cost: number;
  /** 管理成本（%） */
  overhead_percentage: number;
  /** 管理成本 */
  overhead_cost: number;
  /** 总计 */
  total_with_overhead: number;
}

/**
 * 角色成本
 */
export interface RoleCost {
  /** 角色名称 */
  role: string;
  /** 工时 */
  hours: number;
  /** 时薪 */
  hourly_rate: number;
  /** 人数 */
  count: number;
  /** 角色总成本 */
  total_cost: number;
}

/**
 * 技术成本
 */
export interface TechnologyCost {
  /** 软件许可 */
  software_licenses: LicenseCost[];
  /** 开发工具 */
  development_tools: ToolCost[];
  /** 库和框架 */
  libraries_frameworks: number;
  /** 总计 */
  total: number;
}

/**
 * 许可成本
 */
export interface LicenseCost {
  /** 软件名称 */
  software_name: string;
  /** 许可类型 */
  license_type: 'perpetual' | 'subscription' | 'usage_based';
  /** 用户数 */
  user_count: number;
  /** 单价 */
  unit_price: number;
  /** 期间（月） */
  duration_months: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * 工具成本
 */
export interface ToolCost {
  /** 工具名称 */
  tool_name: string;
  /** 成本类型 */
  cost_type: 'one_time' | 'monthly' | 'yearly';
  /** 成本金额 */
  cost_amount: number;
  /** 使用期间 */
  usage_duration_months: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * 基础设施成本
 */
export interface InfrastructureCost {
  /** 云服务成本 */
  cloud_services: CloudServiceCost[];
  /** 硬件成本 */
  hardware_costs: HardwareCost[];
  /** 网络成本 */
  network_costs: number;
  /** 安全服务成本 */
  security_services: number;
  /** 备份存储成本 */
  backup_storage: number;
  /** 总计 */
  total: number;
}

/**
 * 云服务成本
 */
export interface CloudServiceCost {
  /** 服务提供商 */
  provider: string;
  /** 服务类型 */
  service_type: string;
  /** 配置描述 */
  configuration: string;
  /** 月费用 */
  monthly_cost: number;
  /** 使用期间（月） */
  usage_months: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * 硬件成本
 */
export interface HardwareCost {
  /** 硬件类型 */
  hardware_type: string;
  /** 硬件描述 */
  description: string;
  /** 数量 */
  quantity: number;
  /** 单价 */
  unit_price: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * 第三方成本
 */
export interface ThirdPartyCost {
  /** 服务成本 */
  service_costs: ThirdPartyServiceCost[];
  /** API调用成本 */
  api_costs: APICost[];
  /** 数据成本 */
  data_costs: number;
  /** 总计 */
  total: number;
}

/**
 * 第三方服务成本
 */
export interface ThirdPartyServiceCost {
  /** 服务名称 */
  service_name: string;
  /** 定价模式 */
  pricing_model: string;
  /** 预估使用量 */
  estimated_usage: string;
  /** 月费用 */
  monthly_cost: number;
  /** 使用期间（月） */
  usage_months: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * API成本
 */
export interface APICost {
  /** API提供商 */
  provider: string;
  /** API类型 */
  api_type: string;
  /** 预估调用次数 */
  estimated_calls: number;
  /** 每次调用成本 */
  cost_per_call: number;
  /** 期间（月） */
  duration_months: number;
  /** 总成本 */
  total_cost: number;
}

/**
 * ROI预测
 */
export interface ROIProjection {
  /** 投资总额 */
  total_investment: number;
  /** 年度收入预测 */
  annual_revenue_projections: AnnualRevenue[];
  /** 年度成本预测 */
  annual_cost_projections: AnnualCost[];
  /** 投资回收期（月） */
  payback_period_months: number;
  /** 净现值 */
  net_present_value: number;
  /** 内部收益率 */
  internal_rate_of_return: number;
  /** 投资回报率 */
  return_on_investment: number;
  /** 敏感性分析 */
  sensitivity_analysis: SensitivityAnalysis[];
}

/**
 * 年度收入
 */
export interface AnnualRevenue {
  /** 年份 */
  year: number;
  /** 收入来源 */
  revenue_streams: RevenueStream[];
  /** 总收入 */
  total_revenue: number;
  /** 收入增长率 */
  growth_rate: number;
}

/**
 * 收入来源
 */
export interface RevenueStream {
  /** 来源名称 */
  name: string;
  /** 来源类型 */
  type: 'subscription' | 'transaction' | 'advertising' | 'licensing' | 'other';
  /** 收入金额 */
  amount: number;
  /** 收入占比 */
  percentage: number;
}

/**
 * 年度成本
 */
export interface AnnualCost {
  /** 年份 */
  year: number;
  /** 运营成本 */
  operational_costs: OperationalCost[];
  /** 总成本 */
  total_cost: number;
  /** 成本增长率 */
  growth_rate: number;
}

/**
 * 运营成本
 */
export interface OperationalCost {
  /** 成本类型 */
  type: 'personnel' | 'infrastructure' | 'marketing' | 'support' | 'other';
  /** 成本描述 */
  description: string;
  /** 成本金额 */
  amount: number;
  /** 成本占比 */
  percentage: number;
}

/**
 * 敏感性分析
 */
export interface SensitivityAnalysis {
  /** 变量名称 */
  variable_name: string;
  /** 基准值 */
  base_value: number;
  /** 变化范围 */
  variation_range: VariationScenario[];
  /** 对ROI的影响 */
  roi_impact: number[];
}

/**
 * 变化情景
 */
export interface VariationScenario {
  /** 情景名称 */
  scenario: string;
  /** 变化百分比 */
  change_percentage: number;
  /** 变化后的值 */
  new_value: number;
}

/**
 * 成本分摊
 */
export interface CostAllocation {
  /** 分摊维度 */
  dimension: 'phase' | 'module' | 'team' | 'functional_area';
  /** 分摊项目 */
  allocations: AllocationItem[];
}

/**
 * 分摊项目
 */
export interface AllocationItem {
  /** 项目名称 */
  item_name: string;
  /** 分摊金额 */
  allocated_amount: number;
  /** 分摊比例 */
  allocation_percentage: number;
  /** 分摊理由 */
  allocation_rationale: string;
}

/**
 * 成本风险
 */
export interface CostRisk {
  /** 风险ID */
  id: ID;
  /** 风险描述 */
  description: string;
  /** 风险类型 */
  type: 'scope_creep' | 'resource_cost' | 'technology_change' | 'market_change' | 'external_factor';
  /** 发生概率 */
  probability: number;
  /** 潜在影响金额 */
  potential_impact: number;
  /** 风险等级 */
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  /** 缓解措施 */
  mitigation_strategies: string[];
  /** 应急预算 */
  contingency_budget: number;
}

// ============= 风险评估 =============

/**
 * 风险评估
 */
export interface RiskAssessment {
  /** 风险ID */
  id: ID;
  /** 风险名称 */
  name: string;
  /** 风险描述 */
  description: string;
  /** 风险类型 */
  type: 'technical' | 'market' | 'resource' | 'timeline' | 'budget' | 'competitive' | 'regulatory' | 'operational';
  /** 风险分类 */
  category: 'internal' | 'external' | 'project_specific' | 'organizational';
  /** 发生概率 */
  probability: 'very_low' | 'low' | 'medium' | 'high' | 'very_high';
  /** 影响程度 */
  impact: 'negligible' | 'minor' | 'moderate' | 'major' | 'catastrophic';
  /** 风险等级 */
  severity: 'low' | 'medium' | 'high' | 'critical';
  /** 风险评分 */
  risk_score: number;
  /** 风险触发条件 */
  trigger_conditions: string[];
  /** 早期预警信号 */
  early_warning_signals: string[];
  /** 影响领域 */
  impact_areas: ImpactArea[];
  /** 缓解措施 */
  mitigation_strategies: MitigationStrategy[];
  /** 应急计划 */
  contingency_plan?: ContingencyPlan;
  /** 负责人 */
  risk_owner: string;
  /** 风险状态 */
  status: 'identified' | 'analyzed' | 'planned' | 'monitored' | 'closed';
  /** 审核信息 */
  audit: AuditInfo;
}

/**
 * 影响领域
 */
export interface ImpactArea {
  /** 领域名称 */
  area: 'scope' | 'schedule' | 'cost' | 'quality' | 'resources' | 'stakeholders';
  /** 影响描述 */
  impact_description: string;
  /** 影响程度 */
  impact_level: 'low' | 'medium' | 'high';
  /** 量化影响 */
  quantified_impact?: {
    metric: string;
    value: number;
    unit: string;
  };
}

/**
 * 缓解策略
 */
export interface MitigationStrategy {
  /** 策略ID */
  id: ID;
  /** 策略类型 */
  type: 'avoid' | 'mitigate' | 'transfer' | 'accept';
  /** 策略描述 */
  description: string;
  /** 实施步骤 */
  implementation_steps: string[];
  /** 所需资源 */
  required_resources: string[];
  /** 实施成本 */
  implementation_cost: number;
  /** 预期效果 */
  expected_effectiveness: number;
  /** 实施时间线 */
  implementation_timeline: string;
  /** 负责人 */
  responsible_person: string;
  /** 成功指标 */
  success_metrics: string[];
  /** 策略状态 */
  status: TaskStatus;
}

/**
 * 应急计划
 */
export interface ContingencyPlan {
  /** 计划名称 */
  name: string;
  /** 计划描述 */
  description: string;
  /** 触发条件 */
  trigger_conditions: string[];
  /** 响应步骤 */
  response_steps: ResponseStep[];
  /** 资源需求 */
  resource_requirements: string[];
  /** 预算分配 */
  budget_allocation: number;
  /** 时间要求 */
  time_requirements: string;
  /** 决策权限 */
  decision_authority: string;
  /** 沟通计划 */
  communication_plan: string[];
}

/**
 * 响应步骤
 */
export interface ResponseStep {
  /** 步骤序号 */
  step_number: number;
  /** 步骤描述 */
  description: string;
  /** 负责人 */
  responsible_person: string;
  /** 估算时间 */
  estimated_duration: string;
  /** 前置条件 */
  prerequisites: string[];
  /** 输出结果 */
  expected_output: string;
}

// ============= 类型守卫函数 =============

/**
 * 检查是否为需求模型
 */
export function isRequirementModel(obj: any): obj is RequirementModel {
  return obj && typeof obj.id === 'string' && typeof obj.user_input === 'string' && obj.parsed_data;
}

/**
 * 检查是否为项目规划
 */
export function isProjectPlan(obj: any): obj is ProjectPlan {
  return obj && typeof obj.id === 'string' && obj.project_overview && obj.technical_architecture;
}

/**
 * 检查是否为项目模块
 */
export function isProjectModule(obj: any): obj is ProjectModule {
  return obj && typeof obj.id === 'string' && typeof obj.name === 'string' && obj.type;
}

/**
 * 检查是否为风险评估
 */
export function isRiskAssessment(obj: any): obj is RiskAssessment {
  return obj && typeof obj.id === 'string' && obj.type && obj.probability && obj.impact;
}
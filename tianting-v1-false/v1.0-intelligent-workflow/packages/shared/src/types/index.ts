/**
 * 天庭系统共享类型定义主导出文件
 * 
 * 统一导出所有类型定义，为其他包提供类型支持
 */

// ============= 基础类型导出 =============
export type {
  ID,
  Timestamp,
  ProjectType,
  BusinessModel,
  ComplexityLevel,
  ProjectStatus,
  TaskStatus,
  PriorityLevel,
  KeyValueMap,
  ApiResponse,
  PaginationInfo,
  PaginatedResponse,
  HealthCheckData,
  HealthCheckResponse,
  AuditInfo,
  Metadata,
  Constraint
} from './common';

// ============= 错误类型导出 =============
export type {
  ErrorLevel,
  ErrorCategory,
  BaseError,
  ApiError,
  ValidationError,
  BusinessError,
  SystemError
} from './errors';

export {
  CommonErrorCodes,
  BusinessErrorCodes,
  createApiError,
  createValidationError,
  createBusinessError,
  createSystemError,
  ErrorCollector,
  isApiError,
  isValidationError,
  isBusinessError,
  isSystemError,
  formatErrorResponse,
  formatMultipleErrors
} from './errors';

// ============= API类型导出（重命名以避免冲突） =============
export type {
  RequirementParseRequest,
  RequirementParseResponse,
  RequirementParseData,
  PlanningGenerateRequest,
  PlanningGenerateResponse,
  PlanningGenerateData,
  WorkflowRequest,
  WorkflowResponse,
  WorkflowData,
  QualityMetrics,
  RegisterRequest,
  RegisterResponse,
  RegisterData,
  LoginRequest,
  LoginResponse,
  LoginData,
  UserProfile,
  ProjectSummary,
  ProjectListResponse,
  CreateProjectRequest,
  CreateProjectResponse,
  CreateProjectData,
  HttpMethod,
  ApiRequestConfig,
  ApiClient,
  
  // API特定类型，重命名以避免冲突
  UserGroup as ApiUserGroup,
  Feature as ApiFeature,
  UserJourneyStage as ApiUserJourneyStage,
  TechStack as ApiTechStack,
  ThirdPartyService as ApiThirdPartyService,
  ProjectModule as ApiProjectModule,
  DevelopmentPhase as ApiDevelopmentPhase,
  Milestone as ApiMilestone,
  CostBreakdown as ApiCostBreakdown,
  ROIProjection as ApiROIProjection,
  RiskAssessment as ApiRiskAssessment
} from './api';

export {
  API_ENDPOINTS,
  isApiResponse,
  isRequirementParseRequest,
  isPlanningGenerateRequest
} from './api';

// ============= 业务领域类型导出 =============
export type {
  RequirementModel,
  ProjectPlan,
  ProjectOverview,
  UserJourney,
  TechnicalArchitecture,
  DevelopmentTimeline,
  BudgetEstimation,
  PainPoint,
  Opportunity,
  EmotionPoint,
  Technology,
  SystemIntegration,
  DeploymentArchitecture,
  DataArchitecture,
  SecurityArchitecture,
  ModuleDependency,
  ModuleInterface,
  CriticalPathItem,
  
  // 领域特定类型，重命名以避免冲突
  UserGroup as DomainUserGroup,
  Feature as DomainFeature,
  UserJourneyStage as DomainUserJourneyStage,
  TechStack as DomainTechStack,
  ThirdPartyService as DomainThirdPartyService,
  ProjectModule as DomainProjectModule,
  DevelopmentPhase as DomainDevelopmentPhase,
  Milestone as DomainMilestone,
  CostBreakdown as DomainCostBreakdown,
  ROIProjection as DomainROIProjection,
  RiskAssessment as DomainRiskAssessment
} from './domain';

export {
  isRequirementModel,
  isProjectPlan,
  isProjectModule,
  isRiskAssessment
} from './domain';

// ============= 运行时验证导出 =============
export {
  RuntimeValidator,
  createValidationResult,
  createTypeAssertion,
  assertIsRequirementParseRequest,
  assertIsProjectType,
  assertIsBusinessModel,
  ProjectTypeSchema,
  BusinessModelSchema,
  ComplexityLevelSchema,
  RequirementParseRequestSchema,
  RequirementParseDataSchema,
} from './runtime-validation';

export type {
  ValidationResult,
} from './runtime-validation';

// ============= 高级类型导出 =============
export type {
  TechStackByProjectType,
  PricingModelByBusiness,
  TeamSizeByComplexity,
  ExtractApiData,
  IsErrorType,
  PartialDeep,
  RequiredDeep,
  StringKeys,
  NumberKeys,
  ReadonlyKeys,
  WritableKeys,
  NonNullableDeep,
  FunctionParams,
  FunctionReturn,
  PromiseResolve,
  UnionToIntersection,
  ValueOf,
  KeyValuePair,
  ProjectConfig,
  RequirementAnalysis,
  ProjectStateMachine,
  StateTransition,
  ExecutableAction,
  ObjectToTuple,
  TupleToUnion,
  Head,
  Tail,
  Reverse,
  Length,
  ApiPath,
  CamelCase,
  SnakeCase,
  EventName,
  GetterName,
  SetterName,
  Flatten,
  DeepMerge,
  Path,
  PathValue,
} from './advanced-types';

export {
  hasKey,
  filterByType,
  mapObjectKeys,
} from './advanced-types';

// ============= 类型版本信息 =============

/**
 * 类型定义版本信息
 */
export const TYPE_DEFINITIONS_VERSION = {
  /** 主版本号 */
  major: 1,
  /** 次版本号 */
  minor: 1,
  /** 修订版本号 */
  patch: 0,
  /** 预发布标识 */
  prerelease: '',
  /** 构建元数据 */
  build: '',
  /** 完整版本字符串 */
  full: '1.1.0',
  /** 发布日期 */
  release_date: '2024-06-30',
  /** 版本特性 */
  features: [
    'runtime-validation',
    'advanced-types',
    'improved-type-coverage',
    'api-contract-compliance'
  ]
} as const;

/**
 * 类型定义兼容性信息
 */
export const TYPE_COMPATIBILITY = {
  /** 最低支持的API版本 */
  min_api_version: '1.0.0',
  /** 最高支持的API版本 */
  max_api_version: '1.9.9',
  /** 支持的TypeScript版本范围 */
  typescript_versions: '>=5.0.0',
  /** 支持的Node.js版本范围 */
  node_versions: '>=18.0.0'
} as const;

// ============= 工具函数 =============

/**
 * 检查类型定义版本兼容性
 */
export function isCompatibleVersion(version: string): boolean {
  const versionParts = version.split('.').map(Number);
  const minVersionParts = TYPE_COMPATIBILITY.min_api_version.split('.').map(Number);
  const maxVersionParts = TYPE_COMPATIBILITY.max_api_version.split('.').map(Number);
  
  const major = versionParts[0] ?? 0;
  const minor = versionParts[1] ?? 0;
  const minMajor = minVersionParts[0] ?? 0;
  const minMinor = minVersionParts[1] ?? 0;
  const maxMajor = maxVersionParts[0] ?? 0;
  const maxMinor = maxVersionParts[1] ?? 0;
  
  if (major < minMajor || major > maxMajor) {
    return false;
  }
  
  if (major === minMajor && minor < minMinor) {
    return false;
  }
  
  if (major === maxMajor && minor > maxMinor) {
    return false;
  }
  
  return true;
}

/**
 * 获取类型定义摘要信息
 */
export function getTypeDefinitionsSummary() {
  return {
    version: TYPE_DEFINITIONS_VERSION.full,
    compatibility: TYPE_COMPATIBILITY,
    modules: {
      common: '通用类型和工具类型',
      errors: '错误处理和异常类型',
      api: 'API接口和请求响应类型',
      domain: '业务领域和实体类型'
    },
    total_types: 'Dynamic - 根据实际导出计算',
    last_updated: new Date().toISOString()
  };
}

// ============= 运行时类型验证工具 =============

/**
 * 运行时类型验证工具
 */
export const TypeValidators = {
  /**
   * 验证API响应格式
   */
  validateApiResponse<T>(response: any): response is import('./common').ApiResponse<T> {
    return (
      response &&
      typeof response.success === 'boolean' &&
      typeof response.message === 'string' &&
      typeof response.timestamp === 'string'
    );
  },

  /**
   * 验证需求模型
   */
  validateRequirementModel(obj: any): boolean {
    return obj && typeof obj.id === 'string' && typeof obj.user_input === 'string' && obj.parsed_data;
  },

  /**
   * 验证项目规划
   */
  validateProjectPlan(obj: any): boolean {
    return obj && typeof obj.id === 'string' && obj.project_overview && obj.technical_architecture;
  },

  /**
   * 验证错误对象
   */
  validateError(obj: any): boolean {
    return (
      obj &&
      typeof obj.code === 'string' &&
      typeof obj.message === 'string' &&
      typeof obj.level === 'string' &&
      typeof obj.category === 'string' &&
      typeof obj.timestamp === 'string'
    );
  }
};

// ============= 工具函数 =============

/**
 * 类型转换工具
 */
export const TypeConverters = {
  /**
   * 检查API响应是否有效
   */
  isValidApiResponse(response: any): boolean {
    return !!(response && response.success === true && response.data);
  },

  /**
   * 从时间戳创建审计信息
   */
  createAuditInfo(timestamp: string): import('./common').AuditInfo {
    return {
      created_at: timestamp,
      updated_at: timestamp,
      version: 1
    };
  }
};

// ============= 默认导出 =============

/**
 * 默认导出：类型定义包的主要信息
 */
export default {
  version: TYPE_DEFINITIONS_VERSION,
  compatibility: TYPE_COMPATIBILITY,
  validators: TypeValidators,
  converters: TypeConverters,
  summary: getTypeDefinitionsSummary(),
  isCompatible: isCompatibleVersion
};
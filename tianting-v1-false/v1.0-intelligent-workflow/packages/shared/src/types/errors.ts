/**
 * 天庭系统错误类型定义
 * 
 * 包含统一的错误处理类型、错误码定义和错误响应格式
 */

import { Timestamp, KeyValueMap } from './common';

// ============= 错误级别 =============

/**
 * 错误级别
 */
export type ErrorLevel = 
  | 'debug'         // 调试信息
  | 'info'          // 一般信息
  | 'warning'       // 警告
  | 'error'         // 错误
  | 'critical';     // 严重错误

/**
 * 错误分类
 */
export type ErrorCategory = 
  | 'validation'    // 验证错误
  | 'authentication' // 认证错误
  | 'authorization' // 授权错误
  | 'business'      // 业务逻辑错误
  | 'network'       // 网络错误
  | 'database'      // 数据库错误
  | 'external'      // 外部服务错误
  | 'system'        // 系统错误
  | 'unknown';      // 未知错误

// ============= 基础错误类型 =============

/**
 * 基础错误信息
 */
export interface BaseError {
  /** 错误代码 */
  code: string;
  /** 错误消息 */
  message: string;
  /** 错误级别 */
  level: ErrorLevel;
  /** 错误分类 */
  category: ErrorCategory;
  /** 错误时间戳 */
  timestamp: Timestamp;
  /** 错误详情 */
  details?: KeyValueMap;
  /** 错误堆栈 */
  stack?: string;
  /** 请求ID */
  request_id?: string;
  /** 用户ID */
  user_id?: string;
}

/**
 * API错误响应
 */
export interface ApiError extends BaseError {
  /** HTTP状态码 */
  status_code: number;
  /** 错误路径 */
  path: string;
  /** 请求方法 */
  method: string;
  /** 建议的解决方案 */
  suggestions?: string[];
  /** 相关文档链接 */
  documentation_url?: string;
}

/**
 * 验证错误详情
 */
export interface ValidationError extends BaseError {
  /** 验证失败的字段 */
  field: string;
  /** 验证失败的值 */
  value: unknown;
  /** 验证规则 */
  rule: string;
  /** 期望的值类型或格式 */
  expected: string;
}

/**
 * 业务逻辑错误
 */
export interface BusinessError extends BaseError {
  /** 业务规则ID */
  rule_id: string;
  /** 业务规则描述 */
  rule_description: string;
  /** 违反的条件 */
  violated_condition: string;
  /** 当前状态 */
  current_state?: Record<string, unknown>;
  /** 期望状态 */
  expected_state?: Record<string, unknown>;
}

/**
 * 系统错误
 */
export interface SystemError extends BaseError {
  /** 错误来源组件 */
  component: string;
  /** 错误类型 */
  error_type: 'memory' | 'disk' | 'network' | 'cpu' | 'timeout' | 'resource' | 'configuration';
  /** 系统信息 */
  system_info?: {
    memory_usage?: number;
    cpu_usage?: number;
    disk_usage?: number;
    uptime?: number;
  };
}

// ============= 错误代码定义 =============

/**
 * 通用错误代码
 */
export const CommonErrorCodes = {
  // 通用错误 (1000-1999)
  UNKNOWN_ERROR: 'COMMON_1000',
  INTERNAL_SERVER_ERROR: 'COMMON_1001',
  SERVICE_UNAVAILABLE: 'COMMON_1002',
  TIMEOUT_ERROR: 'COMMON_1003',
  RATE_LIMIT_EXCEEDED: 'COMMON_1004',

  // 请求错误 (2000-2999)
  BAD_REQUEST: 'REQUEST_2000',
  INVALID_PARAMETER: 'REQUEST_2001',
  MISSING_PARAMETER: 'REQUEST_2002',
  INVALID_FORMAT: 'REQUEST_2003',
  PARAMETER_OUT_OF_RANGE: 'REQUEST_2004',

  // 认证错误 (3000-3999)
  UNAUTHORIZED: 'AUTH_3000',
  INVALID_TOKEN: 'AUTH_3001',
  TOKEN_EXPIRED: 'AUTH_3002',
  INVALID_CREDENTIALS: 'AUTH_3003',
  ACCOUNT_LOCKED: 'AUTH_3004',
  ACCOUNT_NOT_FOUND: 'AUTH_3005',

  // 授权错误 (4000-4999)
  FORBIDDEN: 'AUTHZ_4000',
  INSUFFICIENT_PERMISSIONS: 'AUTHZ_4001',
  RESOURCE_ACCESS_DENIED: 'AUTHZ_4002',
  OPERATION_NOT_ALLOWED: 'AUTHZ_4003',

  // 资源错误 (5000-5999)
  RESOURCE_NOT_FOUND: 'RESOURCE_5000',
  RESOURCE_ALREADY_EXISTS: 'RESOURCE_5001',
  RESOURCE_CONFLICT: 'RESOURCE_5002',
  RESOURCE_LOCKED: 'RESOURCE_5003',
  RESOURCE_QUOTA_EXCEEDED: 'RESOURCE_5004',
} as const;

/**
 * 业务特定错误代码
 */
export const BusinessErrorCodes = {
  // 需求解析错误 (10000-10999)
  REQUIREMENT_PARSE_FAILED: 'REQ_10000',
  REQUIREMENT_TOO_VAGUE: 'REQ_10001',
  REQUIREMENT_TOO_COMPLEX: 'REQ_10002',
  REQUIREMENT_INCONSISTENT: 'REQ_10003',
  REQUIREMENT_INCOMPLETE: 'REQ_10004',

  // 项目规划错误 (11000-11999)
  PLANNING_GENERATION_FAILED: 'PLAN_11000',
  PLANNING_CONSTRAINTS_CONFLICT: 'PLAN_11001',
  PLANNING_BUDGET_EXCEEDED: 'PLAN_11002',
  PLANNING_TIMELINE_UNREALISTIC: 'PLAN_11003',
  PLANNING_TECHNOLOGY_MISMATCH: 'PLAN_11004',

  // 多窗口协调错误 (12000-12999)
  WINDOW_CREATION_FAILED: 'WINDOW_12000',
  WINDOW_COMMUNICATION_FAILED: 'WINDOW_12001',
  WINDOW_SYNC_CONFLICT: 'WINDOW_12002',
  WINDOW_TASK_ASSIGNMENT_FAILED: 'WINDOW_12003',
  WINDOW_INTEGRATION_FAILED: 'WINDOW_12004',

  // AI服务错误 (13000-13999)
  AI_API_ERROR: 'AI_13000',
  AI_QUOTA_EXCEEDED: 'AI_13001',
  AI_RESPONSE_INVALID: 'AI_13002',
  AI_MODEL_UNAVAILABLE: 'AI_13003',
  AI_CONTEXT_TOO_LONG: 'AI_13004',
} as const;

// ============= 错误工厂函数 =============

/**
 * 创建API错误
 */
export function createApiError(
  code: string,
  message: string,
  statusCode: number,
  options?: Partial<ApiError>
): ApiError {
  return {
    code,
    message,
    level: 'error',
    category: 'system',
    status_code: statusCode,
    path: options?.path || '',
    method: options?.method || '',
    timestamp: new Date().toISOString(),
    ...options,
  };
}

/**
 * 创建验证错误
 */
export function createValidationError(
  field: string,
  value: unknown,
  rule: string,
  expected: string,
  options?: Partial<ValidationError>
): ValidationError {
  return {
    code: CommonErrorCodes.INVALID_PARAMETER,
    message: `Validation failed for field '${field}': ${rule}`,
    level: 'error',
    category: 'validation',
    field,
    value,
    rule,
    expected,
    timestamp: new Date().toISOString(),
    ...options,
  };
}

/**
 * 创建业务错误
 */
export function createBusinessError(
  ruleId: string,
  ruleDescription: string,
  violatedCondition: string,
  options?: Partial<BusinessError>
): BusinessError {
  return {
    code: `BUSINESS_${ruleId}`,
    message: `Business rule violation: ${ruleDescription}`,
    level: 'error',
    category: 'business',
    rule_id: ruleId,
    rule_description: ruleDescription,
    violated_condition: violatedCondition,
    timestamp: new Date().toISOString(),
    ...options,
  };
}

/**
 * 创建系统错误
 */
export function createSystemError(
  component: string,
  errorType: SystemError['error_type'],
  message: string,
  options?: Partial<SystemError>
): SystemError {
  return {
    code: CommonErrorCodes.INTERNAL_SERVER_ERROR,
    message: `System error in ${component}: ${message}`,
    level: 'error',
    category: 'system',
    component,
    error_type: errorType,
    timestamp: new Date().toISOString(),
    ...options,
  };
}

// ============= 错误处理工具 =============

/**
 * 错误处理器接口
 */
export interface ErrorHandler {
  handle(error: BaseError): void;
  canHandle(error: BaseError): boolean;
}

/**
 * 错误收集器
 */
export class ErrorCollector {
  private errors: BaseError[] = [];

  /**
   * 添加错误
   */
  add(error: BaseError): void {
    this.errors.push(error);
  }

  /**
   * 获取所有错误
   */
  getAll(): BaseError[] {
    return [...this.errors];
  }

  /**
   * 按级别过滤错误
   */
  getByLevel(level: ErrorLevel): BaseError[] {
    return this.errors.filter(error => error.level === level);
  }

  /**
   * 按分类过滤错误
   */
  getByCategory(category: ErrorCategory): BaseError[] {
    return this.errors.filter(error => error.category === category);
  }

  /**
   * 检查是否有错误
   */
  hasErrors(): boolean {
    return this.errors.length > 0;
  }

  /**
   * 检查是否有严重错误
   */
  hasCriticalErrors(): boolean {
    return this.errors.some(error => error.level === 'critical');
  }

  /**
   * 清空错误
   */
  clear(): void {
    this.errors = [];
  }

  /**
   * 获取错误摘要
   */
  getSummary(): {
    total: number;
    byLevel: Record<ErrorLevel, number>;
    byCategory: Record<ErrorCategory, number>;
    } {
    const byLevel = {} as Record<ErrorLevel, number>;
    const byCategory = {} as Record<ErrorCategory, number>;

    this.errors.forEach(error => {
      byLevel[error.level] = (byLevel[error.level] || 0) + 1;
      byCategory[error.category] = (byCategory[error.category] || 0) + 1;
    });

    return {
      total: this.errors.length,
      byLevel,
      byCategory,
    };
  }
}

// ============= 错误类型守卫 =============

/**
 * 检查是否为API错误
 */
export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === 'object' && 
    error !== null && 
    'status_code' in error && 
    'path' in error &&
    typeof (error as any).status_code === 'number' && 
    typeof (error as any).path === 'string'
  );
}

/**
 * 检查是否为验证错误
 */
export function isValidationError(error: unknown): error is ValidationError {
  return (
    typeof error === 'object' && 
    error !== null && 
    'field' in error && 
    'rule' in error &&
    typeof (error as any).field === 'string' && 
    typeof (error as any).rule === 'string'
  );
}

/**
 * 检查是否为业务错误
 */
export function isBusinessError(error: unknown): error is BusinessError {
  return (
    typeof error === 'object' && 
    error !== null && 
    'rule_id' in error && 
    'rule_description' in error &&
    typeof (error as any).rule_id === 'string' && 
    typeof (error as any).rule_description === 'string'
  );
}

/**
 * 检查是否为系统错误
 */
export function isSystemError(error: unknown): error is SystemError {
  return (
    typeof error === 'object' && 
    error !== null && 
    'component' in error && 
    'error_type' in error &&
    typeof (error as any).component === 'string' && 
    typeof (error as any).error_type === 'string'
  );
}

// ============= 错误响应格式化 =============

/**
 * 格式化错误响应
 */
export function formatErrorResponse(error: BaseError): {
  error: {
    code: string;
    message: string;
    level: ErrorLevel;
    category: ErrorCategory;
    timestamp: Timestamp;
    details?: KeyValueMap;
  };
} {
  return {
    error: {
      code: error.code,
      message: error.message,
      level: error.level,
      category: error.category,
      timestamp: error.timestamp,
      ...(error.details && { details: error.details }),
    },
  };
}

/**
 * 格式化多个错误
 */
export function formatMultipleErrors(errors: BaseError[]): {
  errors: Array<{
    code: string;
    message: string;
    level: ErrorLevel;
    category: ErrorCategory;
  }>;
  summary: {
    total: number;
    critical: number;
    errors: number;
    warnings: number;
  };
} {
  const summary = {
    total: errors.length,
    critical: errors.filter(e => e.level === 'critical').length,
    errors: errors.filter(e => e.level === 'error').length,
    warnings: errors.filter(e => e.level === 'warning').length,
  };

  return {
    errors: errors.map(error => ({
      code: error.code,
      message: error.message,
      level: error.level,
      category: error.category,
    })),
    summary,
  };
}
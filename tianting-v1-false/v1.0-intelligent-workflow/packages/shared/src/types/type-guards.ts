/**
 * 简化的类型守卫函数
 * 避免复杂的unknown类型检查
 */

import type { 
  ApiResponse,
  RequirementParseRequest,
  PlanningGenerateRequest,
  RequirementModel,
  ProjectPlan,
  BaseError
} from './index';

/**
 * 安全的对象属性检查
 */
function hasProperty<T extends Record<string, any>, K extends string>(
  obj: T,
  prop: K
): obj is T & Record<K, any> {
  return prop in obj;
}

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
  return (
    request &&
    typeof request === 'object' &&
    typeof request.user_input === 'string'
  );
}

/**
 * 检查是否为项目规划请求
 */
export function isPlanningGenerateRequest(request: any): request is PlanningGenerateRequest {
  return (
    request &&
    typeof request === 'object' &&
    typeof request.requirement_id === 'string'
  );
}

/**
 * 检查是否为需求模型
 */
export function isRequirementModel(obj: any): obj is RequirementModel {
  return (
    obj &&
    typeof obj === 'object' &&
    typeof obj.id === 'string' &&
    typeof obj.user_input === 'string' &&
    obj.parsed_data
  );
}

/**
 * 检查是否为项目规划
 */
export function isProjectPlan(obj: any): obj is ProjectPlan {
  return (
    obj &&
    typeof obj === 'object' &&
    typeof obj.id === 'string' &&
    obj.project_overview &&
    obj.technical_architecture
  );
}

/**
 * 检查是否为项目模块
 */
export function isProjectModule(obj: any): boolean {
  return (
    obj &&
    typeof obj === 'object' &&
    typeof obj.id === 'string' &&
    typeof obj.name === 'string' &&
    obj.type
  );
}

/**
 * 检查是否为风险评估
 */
export function isRiskAssessment(obj: any): boolean {
  return (
    obj &&
    typeof obj === 'object' &&
    typeof obj.id === 'string' &&
    obj.type &&
    obj.probability &&
    obj.impact
  );
}

/**
 * 检查是否为API错误
 */
export function isApiError(error: any): boolean {
  return (
    error &&
    typeof error === 'object' &&
    typeof error.status_code === 'number' &&
    typeof error.path === 'string'
  );
}

/**
 * 检查是否为验证错误
 */
export function isValidationError(error: any): boolean {
  return (
    error &&
    typeof error === 'object' &&
    typeof error.field === 'string' &&
    typeof error.rule === 'string'
  );
}

/**
 * 检查是否为业务错误
 */
export function isBusinessError(error: any): boolean {
  return (
    error &&
    typeof error === 'object' &&
    typeof error.rule_id === 'string' &&
    typeof error.rule_description === 'string'
  );
}

/**
 * 检查是否为系统错误
 */
export function isSystemError(error: any): boolean {
  return (
    error &&
    typeof error === 'object' &&
    typeof error.component === 'string' &&
    typeof error.error_type === 'string'
  );
}
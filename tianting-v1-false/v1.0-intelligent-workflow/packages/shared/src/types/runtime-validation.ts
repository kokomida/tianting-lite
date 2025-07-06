/**
 * 天庭系统运行时类型验证
 * 
 * 使用 zod 提供运行时类型验证，确保类型安全
 */

import { z } from 'zod';
import type { 
  ProjectType, 
  BusinessModel, 
  ComplexityLevel,
  RequirementParseRequest,
  RequirementParseData,
  ProjectStatus,
  TaskStatus
} from './index';

// ============= 基础类型验证Schema =============

export const ProjectTypeSchema = z.enum(['web_app', 'mobile_app', 'api_service', 'desktop_app']);
export const BusinessModelSchema = z.enum(['b2b', 'b2c', 'c2c', 'saas', 'marketplace']);
export const ComplexityLevelSchema = z.enum(['low', 'medium', 'high']);
export const ProjectStatusSchema = z.enum(['planning', 'in_progress', 'testing', 'completed', 'paused', 'cancelled']);
export const TaskStatusSchema = z.enum(['pending', 'in_progress', 'completed', 'failed', 'cancelled']);

// ============= API请求验证Schema =============

export const RequirementParseRequestSchema = z.object({
  user_input: z.string().min(1, 'User input is required'),
  user_id: z.string().optional(),
  context: z.object({
    previous_requirements: z.array(z.string()).optional(),
    project_history: z.array(z.string()).optional(),
  }).optional(),
});

export const UserGroupSchema = z.object({
  age_range: z.string(),
  occupation: z.string(),
  tech_savvy: z.enum(['low', 'medium', 'high']),
  income_level: z.enum(['low', 'medium', 'high']).optional(),
  location: z.string().optional(),
  use_case: z.string().optional(),
});

export const FeatureSchema = z.object({
  name: z.string(),
  priority: z.enum(['low', 'medium', 'high', 'critical']),
  complexity: ComplexityLevelSchema,
  description: z.string().optional(),
  estimated_hours: z.number().positive().optional(),
  dependencies: z.array(z.string()).optional(),
});

export const ConstraintSchema = z.object({
  type: z.enum(['performance', 'security', 'budget', 'timeline', 'technical', 'business']),
  description: z.string(),
  value: z.string(),
  is_hard_constraint: z.boolean().optional(),
});

export const RequirementParseDataSchema = z.object({
  requirement_id: z.string(),
  parsed_data: z.object({
    project_type: ProjectTypeSchema,
    target_users: z.array(UserGroupSchema),
    core_features: z.array(FeatureSchema),
    technical_constraints: z.array(ConstraintSchema),
    business_model: BusinessModelSchema,
    complexity_level: ComplexityLevelSchema,
  }),
  confidence_score: z.number().min(0).max(1),
  suggestions: z.array(z.string()).optional(),
});

// ============= 错误验证Schema =============

export const ApiErrorSchema = z.object({
  code: z.string(),
  message: z.string(),
  level: z.enum(['debug', 'info', 'warning', 'error', 'critical']),
  category: z.enum(['validation', 'authentication', 'authorization', 'business', 'network', 'database', 'external', 'system', 'unknown']),
  timestamp: z.string(),
  status_code: z.number(),
  path: z.string(),
  method: z.string(),
  details: z.record(z.unknown()).optional(),
  stack: z.string().optional(),
  request_id: z.string().optional(),
  user_id: z.string().optional(),
});

// ============= 运行时验证函数 =============

/**
 * 运行时类型验证器
 */
export class RuntimeValidator {
  /**
   * 验证需求解析请求
   */
  static validateRequirementParseRequest(data: unknown): any {
    return RequirementParseRequestSchema.parse(data);
  }

  /**
   * 安全验证需求解析请求（不抛出异常）
   */
  static safeValidateRequirementParseRequest(data: unknown): { 
    success: true; 
    data: any 
  } | { 
    success: false; 
    error: z.ZodError 
  } {
    const result = RequirementParseRequestSchema.safeParse(data);
    return result.success 
      ? { success: true, data: result.data }
      : { success: false, error: result.error };
  }

  /**
   * 验证需求解析数据
   */
  static validateRequirementParseData(data: unknown): any {
    return RequirementParseDataSchema.parse(data);
  }

  /**
   * 验证项目类型
   */
  static validateProjectType(type: unknown): ProjectType {
    return ProjectTypeSchema.parse(type);
  }

  /**
   * 验证业务模式
   */
  static validateBusinessModel(model: unknown): BusinessModel {
    return BusinessModelSchema.parse(model);
  }

  /**
   * 验证复杂度级别
   */
  static validateComplexityLevel(level: unknown): ComplexityLevel {
    return ComplexityLevelSchema.parse(level);
  }

  /**
   * 验证并清理API错误数据
   */
  static validateApiError(error: unknown) {
    return ApiErrorSchema.parse(error);
  }

  /**
   * 批量验证数组数据
   */
  static validateArray<T>(
    schema: z.ZodSchema<T>, 
    data: unknown[], 
    itemName: string = 'item'
  ): T[] {
    if (!Array.isArray(data)) {
      throw new z.ZodError([{
        code: 'invalid_type',
        expected: 'array',
        received: typeof data,
        path: [],
        message: `Expected array, received ${typeof data}`,
      }]);
    }

    const results: T[] = [];
    const errors: z.ZodIssue[] = [];

    data.forEach((item, index) => {
      const result = schema.safeParse(item);
      if (result.success) {
        results.push(result.data);
      } else {
        result.error.issues.forEach(issue => {
          errors.push({
            ...issue,
            path: [index, ...issue.path],
            message: `${itemName}[${index}]: ${issue.message}`,
          });
        });
      }
    });

    if (errors.length > 0) {
      throw new z.ZodError(errors);
    }

    return results;
  }
}

// ============= 类型断言辅助函数 =============

/**
 * 创建类型安全的断言函数
 */
export function createTypeAssertion<T>(
  schema: z.ZodSchema<T>, 
  typeName: string
) {
  return function(data: unknown, context?: string): asserts data is T {
    try {
      schema.parse(data);
    } catch (error) {
      if (error instanceof z.ZodError) {
        const contextMsg = context ? ` in ${context}` : '';
        throw new Error(
          `Type assertion failed for ${typeName}${contextMsg}: ${error.issues.map(i => i.message).join(', ')}`
        );
      }
      throw error;
    }
  };
}

// ============= 预定义断言函数 =============

export const assertIsRequirementParseRequest = createTypeAssertion(
  RequirementParseRequestSchema, 
  'RequirementParseRequest'
);

export const assertIsProjectType = createTypeAssertion(
  ProjectTypeSchema, 
  'ProjectType'
);

export const assertIsBusinessModel = createTypeAssertion(
  BusinessModelSchema, 
  'BusinessModel'
);

// ============= 验证结果类型 =============

export type ValidationResult<T> = {
  success: true;
  data: T;
} | {
  success: false;
  error: {
    message: string;
    issues: Array<{
      path: (string | number)[];
      message: string;
      code: string;
    }>;
  };
};

/**
 * 统一的验证结果处理函数
 */
export function createValidationResult<T>(
  schema: z.ZodSchema<T>, 
  data: unknown
): ValidationResult<T> {
  const result = schema.safeParse(data);
  
  if (result.success) {
    return { success: true, data: result.data };
  }
  
  return {
    success: false,
    error: {
      message: `Validation failed: ${result.error.issues.length} error(s)`,
      issues: result.error.issues.map(issue => ({
        path: issue.path,
        message: issue.message,
        code: issue.code,
      })),
    },
  };
}
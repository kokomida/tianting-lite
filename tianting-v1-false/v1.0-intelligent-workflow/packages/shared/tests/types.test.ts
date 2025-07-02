/**
 * 天庭系统类型定义测试
 * 
 * 验证所有类型定义的正确性和完整性
 */

import {
  // 通用类型
  ID,
  Timestamp,
  ProjectType,
  BusinessModel,
  ComplexityLevel,
  ApiResponse,
  PaginatedResponse,
  HealthCheckResponse,
  
  // API类型
  RequirementParseRequest,
  RequirementParseResponse,
  PlanningGenerateRequest,
  PlanningGenerateResponse,
  WorkflowRequest,
  WorkflowResponse,
  RegisterRequest,
  RegisterResponse,
  LoginRequest,
  LoginResponse,
  API_ENDPOINTS,
  
  // 错误类型
  BaseError,
  ApiError,
  ValidationError,
  BusinessError,
  SystemError,
  CommonErrorCodes,
  BusinessErrorCodes,
  createApiError,
  createValidationError,
  createBusinessError,
  createSystemError,
  isApiError,
  isValidationError,
  isBusinessError,
  isSystemError,
  
  // 类型验证和转换工具
  TypeValidators,
  TypeConverters,
  TYPE_DEFINITIONS_VERSION,
  TYPE_COMPATIBILITY,
  isCompatibleVersion
} from '../src/types';

describe('通用类型测试', () => {
  test('ID类型应该是字符串', () => {
    const id: ID = 'test-id-123';
    expect(typeof id).toBe('string');
  });

  test('Timestamp类型应该是字符串', () => {
    const timestamp: Timestamp = new Date().toISOString();
    expect(typeof timestamp).toBe('string');
    expect(Date.parse(timestamp)).not.toBeNaN();
  });

  test('ProjectType联合类型应该包含正确的值', () => {
    const validTypes: ProjectType[] = ['web_app', 'mobile_app', 'api_service', 'desktop_app'];
    validTypes.forEach(type => {
      expect(['web_app', 'mobile_app', 'api_service', 'desktop_app']).toContain(type);
    });
  });

  test('BusinessModel联合类型应该包含正确的值', () => {
    const validModels: BusinessModel[] = ['b2b', 'b2c', 'c2c', 'saas', 'marketplace'];
    validModels.forEach(model => {
      expect(['b2b', 'b2c', 'c2c', 'saas', 'marketplace']).toContain(model);
    });
  });

  test('ComplexityLevel联合类型应该包含正确的值', () => {
    const validLevels: ComplexityLevel[] = ['low', 'medium', 'high'];
    validLevels.forEach(level => {
      expect(['low', 'medium', 'high']).toContain(level);
    });
  });
});

describe('API响应类型测试', () => {
  test('ApiResponse应该有正确的结构', () => {
    const response: ApiResponse<string> = {
      success: true,
      data: 'test data',
      message: 'Success',
      timestamp: new Date().toISOString(),
      request_id: 'req-123'
    };

    expect(response.success).toBe(true);
    expect(response.data).toBe('test data');
    expect(response.message).toBe('Success');
    expect(typeof response.timestamp).toBe('string');
    expect(response.request_id).toBe('req-123');
  });

  test('PaginatedResponse应该有正确的结构', () => {
    const response: PaginatedResponse<{ id: string; name: string }> = {
      data: [
        { id: '1', name: 'Item 1' },
        { id: '2', name: 'Item 2' }
      ],
      pagination: {
        total_count: 100,
        page: 1,
        page_size: 10,
        total_pages: 10
      }
    };

    expect(Array.isArray(response.data)).toBe(true);
    expect(response.data).toHaveLength(2);
    expect(response.pagination.total_count).toBe(100);
    expect(response.pagination.page).toBe(1);
    expect(response.pagination.page_size).toBe(10);
    expect(response.pagination.total_pages).toBe(10);
  });

  test('HealthCheckResponse应该继承ApiResponse', () => {
    const healthResponse: HealthCheckResponse = {
      success: true,
      data: {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        database: {
          status: 'connected',
          latency_ms: 10
        },
        redis: {
          status: 'connected',
          latency_ms: 5
        },
        external_services: {
          'claude-api': 'available',
          'promptx-mcp': 'available'
        }
      },
      message: 'System healthy',
      timestamp: new Date().toISOString()
    };

    expect(healthResponse.success).toBe(true);
    expect(healthResponse.data?.status).toBe('healthy');
    expect(healthResponse.data?.database.status).toBe('connected');
    expect(healthResponse.data?.redis.status).toBe('connected');
    expect(healthResponse.data?.external_services['claude-api']).toBe('available');
  });
});

describe('API接口类型测试', () => {
  test('RequirementParseRequest应该有正确的结构', () => {
    const request: RequirementParseRequest = {
      user_input: '我想做一个音乐推荐APP',
      user_id: 'user-123',
      context: {
        previous_requirements: ['之前的需求'],
        project_history: ['项目历史']
      }
    };

    expect(request.user_input).toBe('我想做一个音乐推荐APP');
    expect(request.user_id).toBe('user-123');
    expect(request.context?.previous_requirements).toEqual(['之前的需求']);
    expect(request.context?.project_history).toEqual(['项目历史']);
  });

  test('RequirementParseResponse应该有正确的结构', () => {
    const response: RequirementParseResponse = {
      success: true,
      data: {
        requirement_id: 'req-123',
        parsed_data: {
          project_type: 'mobile_app',
          target_users: [{
            age_range: '18-35',
            occupation: 'knowledge_worker',
            tech_savvy: 'medium'
          }],
          core_features: [{
            name: 'music_recommendation',
            priority: 'high',
            complexity: 'high'
          }],
          technical_constraints: [{
            type: 'performance',
            description: 'fast_response_time',
            value: '<2s'
          }],
          business_model: 'b2c',
          complexity_level: 'medium'
        },
        confidence_score: 0.87,
        suggestions: ['考虑添加社交分享功能']
      },
      message: '需求解析完成',
      timestamp: new Date().toISOString()
    };

    expect(response.success).toBe(true);
    expect(response.data?.requirement_id).toBe('req-123');
    expect(response.data?.parsed_data.project_type).toBe('mobile_app');
    expect(response.data?.confidence_score).toBe(0.87);
  });

  test('API_ENDPOINTS应该包含所有必要的端点', () => {
    expect(API_ENDPOINTS.REQUIREMENT_PARSE).toBe('/api/requirements/parse');
    expect(API_ENDPOINTS.PLANNING_GENERATE).toBe('/api/planning/generate');
    expect(API_ENDPOINTS.WORKFLOW_REQUIREMENT_TO_PLAN).toBe('/api/workflow/requirement-to-plan');
    expect(API_ENDPOINTS.AUTH_REGISTER).toBe('/api/auth/register');
    expect(API_ENDPOINTS.AUTH_LOGIN).toBe('/api/auth/login');
    expect(API_ENDPOINTS.PROJECTS).toBe('/api/projects');
    expect(API_ENDPOINTS.PROJECT_BY_ID('123')).toBe('/api/projects/123');
  });
});

describe('错误类型测试', () => {
  test('CommonErrorCodes应该包含所有通用错误码', () => {
    expect(CommonErrorCodes.UNKNOWN_ERROR).toBe('COMMON_1000');
    expect(CommonErrorCodes.INTERNAL_SERVER_ERROR).toBe('COMMON_1001');
    expect(CommonErrorCodes.BAD_REQUEST).toBe('REQUEST_2000');
    expect(CommonErrorCodes.UNAUTHORIZED).toBe('AUTH_3000');
    expect(CommonErrorCodes.FORBIDDEN).toBe('AUTHZ_4000');
    expect(CommonErrorCodes.RESOURCE_NOT_FOUND).toBe('RESOURCE_5000');
  });

  test('BusinessErrorCodes应该包含业务特定错误码', () => {
    expect(BusinessErrorCodes.REQUIREMENT_PARSE_FAILED).toBe('REQ_10000');
    expect(BusinessErrorCodes.PLANNING_GENERATION_FAILED).toBe('PLAN_11000');
    expect(BusinessErrorCodes.WINDOW_CREATION_FAILED).toBe('WINDOW_12000');
    expect(BusinessErrorCodes.AI_API_ERROR).toBe('AI_13000');
  });

  test('createApiError工厂函数应该创建正确的API错误', () => {
    const error = createApiError(
      CommonErrorCodes.BAD_REQUEST,
      'Invalid request format',
      400,
      {
        path: '/api/test',
        method: 'POST'
      }
    );

    expect(error.code).toBe('REQUEST_2000');
    expect(error.message).toBe('Invalid request format');
    expect(error.status_code).toBe(400);
    expect(error.level).toBe('error');
    expect(error.category).toBe('system');
    expect(error.path).toBe('/api/test');
    expect(error.method).toBe('POST');
  });

  test('createValidationError工厂函数应该创建正确的验证错误', () => {
    const error = createValidationError(
      'email',
      'invalid-email',
      'email_format',
      'valid email address'
    );

    expect(error.code).toBe('REQUEST_2001');
    expect(error.field).toBe('email');
    expect(error.value).toBe('invalid-email');
    expect(error.rule).toBe('email_format');
    expect(error.expected).toBe('valid email address');
    expect(error.level).toBe('error');
    expect(error.category).toBe('validation');
  });

  test('createBusinessError工厂函数应该创建正确的业务错误', () => {
    const error = createBusinessError(
      'DUPLICATE_EMAIL',
      'Email address already exists',
      'Email uniqueness constraint violated'
    );

    expect(error.code).toBe('BUSINESS_DUPLICATE_EMAIL');
    expect(error.rule_id).toBe('DUPLICATE_EMAIL');
    expect(error.rule_description).toBe('Email address already exists');
    expect(error.violated_condition).toBe('Email uniqueness constraint violated');
    expect(error.level).toBe('error');
    expect(error.category).toBe('business');
  });

  test('createSystemError工厂函数应该创建正确的系统错误', () => {
    const error = createSystemError(
      'database_connection',
      'timeout',
      'Connection timeout after 30 seconds'
    );

    expect(error.code).toBe('COMMON_1001');
    expect(error.component).toBe('database_connection');
    expect(error.error_type).toBe('timeout');
    expect(error.message).toBe('System error in database_connection: Connection timeout after 30 seconds');
    expect(error.level).toBe('error');
    expect(error.category).toBe('system');
  });
});

describe('错误类型守卫测试', () => {
  test('isApiError应该正确识别API错误', () => {
    const apiError = createApiError('TEST_001', 'Test error', 400, {
      path: '/test',
      method: 'GET'
    });
    
    const regularError = new Error('Regular error');

    expect(isApiError(apiError)).toBe(true);
    expect(isApiError(regularError)).toBe(false);
    expect(isApiError(null)).toBeFalsy();
    expect(isApiError(undefined)).toBeFalsy();
  });

  test('isValidationError应该正确识别验证错误', () => {
    const validationError = createValidationError('field', 'value', 'rule', 'expected');
    const apiError = createApiError('TEST_001', 'Test error', 400);

    expect(isValidationError(validationError)).toBe(true);
    expect(isValidationError(apiError)).toBe(false);
  });

  test('isBusinessError应该正确识别业务错误', () => {
    const businessError = createBusinessError('RULE_001', 'Business rule', 'Condition');
    const apiError = createApiError('TEST_001', 'Test error', 400);

    expect(isBusinessError(businessError)).toBe(true);
    expect(isBusinessError(apiError)).toBe(false);
  });

  test('isSystemError应该正确识别系统错误', () => {
    const systemError = createSystemError('component', 'timeout', 'System error');
    const apiError = createApiError('TEST_001', 'Test error', 400);

    expect(isSystemError(systemError)).toBe(true);
    expect(isSystemError(apiError)).toBe(false);
  });
});

describe('类型验证工具测试', () => {
  test('TypeValidators.validateApiResponse应该正确验证API响应', () => {
    const validResponse = {
      success: true,
      message: 'Success',
      timestamp: new Date().toISOString(),
      data: { test: 'data' }
    };

    const invalidResponse = {
      success: 'true', // 错误的类型
      message: 123, // 错误的类型
      timestamp: new Date().toISOString()
    };

    expect(TypeValidators.validateApiResponse(validResponse)).toBe(true);
    expect(TypeValidators.validateApiResponse(invalidResponse)).toBe(false);
    expect(TypeValidators.validateApiResponse(null)).toBeFalsy();
    expect(TypeValidators.validateApiResponse(undefined)).toBeFalsy();
  });

  test('TypeValidators.validateError应该正确验证错误对象', () => {
    const validError = createApiError('TEST_001', 'Test error', 400);
    const invalidError = {
      code: 123, // 错误的类型
      message: 'Test'
    };

    expect(TypeValidators.validateError(validError)).toBe(true);
    expect(TypeValidators.validateError(invalidError)).toBe(false);
  });
});

describe('版本兼容性测试', () => {
  test('TYPE_DEFINITIONS_VERSION应该有正确的结构', () => {
    expect(TYPE_DEFINITIONS_VERSION.major).toBe(1);
    expect(TYPE_DEFINITIONS_VERSION.minor).toBe(1);
    expect(TYPE_DEFINITIONS_VERSION.patch).toBe(0);
    expect(TYPE_DEFINITIONS_VERSION.full).toBe('1.1.0');
  });

  test('TYPE_COMPATIBILITY应该有正确的配置', () => {
    expect(TYPE_COMPATIBILITY.min_api_version).toBe('1.0.0');
    expect(TYPE_COMPATIBILITY.max_api_version).toBe('1.9.9');
    expect(TYPE_COMPATIBILITY.typescript_versions).toBe('>=5.0.0');
    expect(TYPE_COMPATIBILITY.node_versions).toBe('>=18.0.0');
  });

  test('isCompatibleVersion应该正确检查版本兼容性', () => {
    expect(isCompatibleVersion('1.0.0')).toBe(true);
    expect(isCompatibleVersion('1.5.0')).toBe(true);
    expect(isCompatibleVersion('1.9.9')).toBe(true);
    expect(isCompatibleVersion('0.9.0')).toBe(false);
    expect(isCompatibleVersion('2.0.0')).toBe(false);
  });
});

describe('类型转换工具测试', () => {
  test('TypeConverters.createAuditInfo应该正确创建审计信息', () => {
    const timestamp = new Date().toISOString();
    const auditInfo = TypeConverters.createAuditInfo(timestamp);
    
    expect(auditInfo.created_at).toBe(timestamp);
    expect(auditInfo.updated_at).toBe(timestamp);
    expect(auditInfo.version).toBe(1);
  });

  test('TypeConverters.isValidApiResponse应该正确验证API响应', () => {
    const validResponse = {
      success: true,
      data: { test: 'data' }
    };

    const invalidResponse = {
      success: false
    };

    expect(TypeConverters.isValidApiResponse(validResponse)).toBe(true);
    expect(TypeConverters.isValidApiResponse(invalidResponse)).toBe(false);
    expect(TypeConverters.isValidApiResponse(null)).toBe(false);
  });
});

describe('类型完整性测试', () => {
  test('应该能够导入所有必要的类型', () => {
    // 这个测试主要验证所有类型都能正确导入
    expect(CommonErrorCodes.UNKNOWN_ERROR).toBeDefined();
    expect(BusinessErrorCodes.REQUIREMENT_PARSE_FAILED).toBeDefined();
    expect(API_ENDPOINTS.REQUIREMENT_PARSE).toBeDefined();
    expect(TYPE_DEFINITIONS_VERSION.full).toBeDefined();
    expect(TypeValidators.validateApiResponse).toBeDefined();
    expect(TypeConverters.createAuditInfo).toBeDefined();
  });

  test('类型定义应该保持一致性', () => {
    // 验证不同文件中相同类型的一致性
    const projectTypes: ProjectType[] = ['web_app', 'mobile_app', 'api_service', 'desktop_app'];
    const businessModels: BusinessModel[] = ['b2b', 'b2c', 'c2c', 'saas', 'marketplace'];
    const complexityLevels: ComplexityLevel[] = ['low', 'medium', 'high'];

    // 这些应该编译通过，验证类型定义的一致性
    expect(projectTypes.length).toBe(4);
    expect(businessModels.length).toBe(5);
    expect(complexityLevels.length).toBe(3);
  });
});
/**
 * 天庭系统高级类型特性
 * 
 * 包含条件类型、映射类型、工具类型等高级TypeScript特性
 */

import type { 
  ProjectType, 
  BusinessModel, 
  ComplexityLevel, 
  ApiResponse,
  RequirementModel,
  ProjectPlan,
  BaseError 
} from './index';

// ============= 条件类型 =============

/**
 * 根据项目类型确定技术栈类型
 */
export type TechStackByProjectType<T extends ProjectType> = 
  T extends 'web_app' ? {
    frontend: 'react' | 'vue' | 'angular';
    backend: 'node' | 'python' | 'java';
    database: 'postgresql' | 'mysql' | 'mongodb';
  } :
  T extends 'mobile_app' ? {
    platform: 'react-native' | 'flutter' | 'native';
    backend: 'node' | 'python' | 'java';
    database: 'sqlite' | 'firebase' | 'realm';
  } :
  T extends 'api_service' ? {
    framework: 'express' | 'fastapi' | 'spring-boot';
    database: 'postgresql' | 'mysql' | 'mongodb';
    cache: 'redis' | 'memcached';
  } :
  T extends 'desktop_app' ? {
    framework: 'electron' | 'tauri' | 'qt';
    language: 'typescript' | 'rust' | 'cpp';
    database: 'sqlite' | 'embedded';
  } : never;

/**
 * 根据业务模式确定收费模式
 */
export type PricingModelByBusiness<T extends BusinessModel> = 
  T extends 'b2b' ? 'subscription' | 'enterprise' | 'per-seat' :
  T extends 'b2c' ? 'freemium' | 'premium' | 'advertising' :
  T extends 'c2c' ? 'commission' | 'listing-fee' | 'subscription' :
  T extends 'saas' ? 'monthly' | 'yearly' | 'usage-based' :
  T extends 'marketplace' ? 'commission' | 'listing-fee' | 'subscription' : never;

/**
 * 根据复杂度级别确定开发团队规模
 */
export type TeamSizeByComplexity<T extends ComplexityLevel> = 
  T extends 'low' ? 1 | 2 | 3 :
  T extends 'medium' ? 3 | 4 | 5 | 6 :
  T extends 'high' ? 6 | 7 | 8 | 9 | 10 : never;

/**
 * 提取API响应的数据类型
 */
export type ExtractApiData<T> = T extends ApiResponse<infer U> ? U : never;

/**
 * 检查类型是否为错误类型
 */
export type IsErrorType<T> = T extends BaseError ? true : false;

// ============= 映射类型 =============

/**
 * 将所有属性变为可选
 */
export type PartialDeep<T> = {
  [P in keyof T]?: T[P] extends object ? PartialDeep<T[P]> : T[P];
};

/**
 * 将所有属性变为必需
 */
export type RequiredDeep<T> = {
  [P in keyof T]-?: T[P] extends object ? RequiredDeep<T[P]> : T[P];
};

/**
 * 提取对象的所有字符串键
 */
export type StringKeys<T> = {
  [K in keyof T]: T[K] extends string ? K : never;
}[keyof T];

/**
 * 提取对象的所有数字键
 */
export type NumberKeys<T> = {
  [K in keyof T]: T[K] extends number ? K : never;
}[keyof T];

/**
 * 将对象的某些属性变为只读
 */
export type ReadonlyKeys<T, K extends keyof T> = Readonly<Pick<T, K>> & Omit<T, K>;

/**
 * 将对象的某些属性变为可写
 */
export type WritableKeys<T, K extends keyof T> = Omit<T, K> & {
  -readonly [P in K]: T[P];
};

/**
 * 创建一个去除null和undefined的类型
 */
export type NonNullable<T> = T extends null | undefined ? never : T;

/**
 * 深度去除null和undefined
 */
export type NonNullableDeep<T> = {
  [P in keyof T]-?: NonNullableDeep<NonNullable<T[P]>>;
};

// ============= 工具类型 =============

/**
 * 获取函数的参数类型
 */
export type FunctionParams<T extends (...args: any[]) => any> = 
  T extends (...args: infer P) => any ? P : never;

/**
 * 获取函数的返回类型
 */
export type FunctionReturn<T extends (...args: any[]) => any> = 
  T extends (...args: any[]) => infer R ? R : never;

/**
 * 获取Promise的resolve类型
 */
export type PromiseResolve<T> = T extends Promise<infer U> ? U : T;

/**
 * 创建联合类型到交叉类型的转换
 */
export type UnionToIntersection<U> = 
  (U extends any ? (k: U) => void : never) extends 
  ((k: infer I) => void) ? I : never;

/**
 * 获取对象的值类型联合
 */
export type ValueOf<T> = T[keyof T];

/**
 * 创建键值对类型
 */
export type KeyValuePair<T> = {
  [K in keyof T]: { key: K; value: T[K] };
}[keyof T];

// ============= 业务特定的高级类型 =============

/**
 * 项目配置类型，根据项目类型动态生成
 */
export type ProjectConfig<T extends ProjectType> = {
  type: T;
  name: string;
  description: string;
  tech_stack: TechStackByProjectType<T>;
  complexity: ComplexityLevel;
  team_size: TeamSizeByComplexity<ComplexityLevel>;
  estimated_duration: number;
} & (T extends 'web_app' ? {
  seo_requirements: boolean;
  responsive_design: boolean;
  browser_support: string[];
} : {}) & (T extends 'mobile_app' ? {
  target_platforms: ('ios' | 'android')[];
  offline_support: boolean;
  push_notifications: boolean;
} : {}) & (T extends 'api_service' ? {
  rate_limiting: boolean;
  api_versioning: boolean;
  authentication: 'jwt' | 'oauth' | 'api-key';
} : {}) & (T extends 'desktop_app' ? {
  target_os: ('windows' | 'macos' | 'linux')[];
  auto_update: boolean;
  installer_type: 'msi' | 'dmg' | 'appimage';
} : {});

/**
 * 需求分析结果类型，支持泛型约束
 */
export type RequirementAnalysis<T extends ProjectType> = {
  project_type: T;
  confidence: number;
  features: Array<{
    name: string;
    complexity: ComplexityLevel;
    priority: 'low' | 'medium' | 'high' | 'critical';
    feasibility: number;
  }>;
  technical_requirements: TechStackByProjectType<T>;
  estimated_effort: {
    development_hours: number;
    testing_hours: number;
    deployment_hours: number;
  };
  risks: Array<{
    type: 'technical' | 'business' | 'resource';
    severity: 'low' | 'medium' | 'high';
    description: string;
    mitigation: string;
  }>;
};

/**
 * 状态机类型，用于项目状态管理
 */
export type ProjectStateMachine = {
  'planning': {
    transitions: ['in_progress', 'cancelled'];
    actions: ['create_plan', 'assign_team', 'estimate_cost'];
  };
  'in_progress': {
    transitions: ['testing', 'paused', 'cancelled'];
    actions: ['develop_feature', 'update_progress', 'resolve_issue'];
  };
  'testing': {
    transitions: ['completed', 'in_progress'];
    actions: ['run_tests', 'fix_bugs', 'validate_requirements'];
  };
  'completed': {
    transitions: never;
    actions: ['archive_project', 'generate_report'];
  };
  'paused': {
    transitions: ['in_progress', 'cancelled'];
    actions: ['resume_project', 'update_timeline'];
  };
  'cancelled': {
    transitions: never;
    actions: ['cleanup_resources', 'document_lessons'];
  };
};

/**
 * 状态转换类型
 */
export type StateTransition<
  From extends keyof ProjectStateMachine,
  To extends ProjectStateMachine[From]['transitions']
> = {
  from: From;
  to: To;
  timestamp: string;
  reason?: string;
  actor: string;
};

/**
 * 可执行动作类型
 */
export type ExecutableAction<State extends keyof ProjectStateMachine> = 
  ProjectStateMachine[State]['actions'] extends readonly (infer U)[] ? U : never;

// ============= 类型断言和验证工具 =============

/**
 * 类型安全的对象键检查
 */
export function hasKey<T extends object, K extends PropertyKey>(
  obj: T,
  key: K
): obj is T & Record<K, unknown> {
  return key in obj;
}

/**
 * 类型安全的数组过滤
 */
export function filterByType<T, U extends T>(
  array: T[],
  predicate: (item: T) => item is U
): U[] {
  return array.filter(predicate);
}

/**
 * 类型安全的对象属性映射
 */
export function mapObjectKeys<T extends Record<string, any>, U>(
  obj: T,
  mapper: <K extends keyof T>(key: K, value: T[K]) => U
): Record<keyof T, U> {
  const result = {} as Record<keyof T, U>;
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      result[key] = mapper(key, obj[key]);
    }
  }
  return result;
}

// ============= 类型变换工具 =============

/**
 * 将对象类型转换为元组类型
 */
export type ObjectToTuple<T extends Record<string, any>> = {
  [K in keyof T]: [K, T[K]];
}[keyof T];

/**
 * 将元组类型转换为联合类型
 */
export type TupleToUnion<T extends readonly any[]> = T[number];

/**
 * 获取数组第一个元素的类型
 */
export type Head<T extends readonly any[]> = T extends readonly [any, ...any[]] ? T[0] : never;

/**
 * 获取数组除第一个元素外的类型
 */
export type Tail<T extends readonly any[]> = T extends readonly [any, ...infer U] ? U : [];

/**
 * 反转元组类型
 */
export type Reverse<T extends readonly any[]> = T extends readonly [...infer U, infer V] 
  ? [V, ...Reverse<U>] 
  : [];

/**
 * 计算元组长度
 */
export type Length<T extends readonly any[]> = T['length'];

// ============= 模板字面量类型 =============

/**
 * API路径模板类型
 */
export type ApiPath<T extends string> = `/api/${T}`;

/**
 * 驼峰命名转换
 */
export type CamelCase<S extends string> = S extends `${infer P1}_${infer P2}${infer P3}`
  ? `${P1}${Uppercase<P2>}${CamelCase<P3>}`
  : S;

/**
 * 蛇形命名转换
 */
export type SnakeCase<S extends string> = S extends `${infer T}${infer U}`
  ? `${T extends Capitalize<T> ? '_' : ''}${Lowercase<T>}${SnakeCase<U>}`
  : S;

/**
 * 生成事件名称类型
 */
export type EventName<T extends string> = `on${Capitalize<T>}`;

/**
 * 生成Getter名称类型
 */
export type GetterName<T extends string> = `get${Capitalize<T>}`;

/**
 * 生成Setter名称类型
 */
export type SetterName<T extends string> = `set${Capitalize<T>}`;

// ============= 递归类型 =============

/**
 * 递归数组扁平化
 */
export type Flatten<T> = T extends readonly (infer U)[]
  ? U extends readonly any[]
    ? Flatten<U>
    : U
  : T;

/**
 * 深度合并类型
 */
export type DeepMerge<T, U> = {
  [K in keyof (T & U)]: K extends keyof U
    ? K extends keyof T
      ? T[K] extends object
        ? U[K] extends object
          ? DeepMerge<T[K], U[K]>
          : U[K]
        : U[K]
      : U[K]
    : K extends keyof T
    ? T[K]
    : never;
};

/**
 * 路径类型生成器
 */
export type Path<T, K extends keyof T = keyof T> = K extends string
  ? T[K] extends Record<string, any>
    ? K | `${K}.${Path<T[K]>}`
    : K
  : never;

/**
 * 根据路径获取值类型
 */
export type PathValue<T, P extends string> = P extends `${infer K}.${infer Rest}`
  ? K extends keyof T
    ? PathValue<T[K], Rest>
    : never
  : P extends keyof T
  ? T[P]
  : never;
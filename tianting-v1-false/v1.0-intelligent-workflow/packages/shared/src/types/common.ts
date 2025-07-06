/**
 * 天庭系统通用类型定义
 */

export type ID = string;
export type Timestamp = string;
export type ProjectType = 'web_app' | 'mobile_app' | 'api_service' | 'desktop_app';
export type BusinessModel = 'b2b' | 'b2c' | 'c2c' | 'saas' | 'marketplace';
export type ComplexityLevel = 'low' | 'medium' | 'high';
export type ProjectStatus = 'planning' | 'in_progress' | 'testing' | 'completed' | 'paused' | 'cancelled';
export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
export type PriorityLevel = 'low' | 'medium' | 'high' | 'critical';

export type KeyValueMap<T = any> = Record<string, T>;

export interface AuditInfo {
  created_at: Timestamp;
  created_by?: ID;
  updated_at: Timestamp;
  updated_by?: ID;
  version: number;
}

export interface Metadata {
  tags?: string[];
  category?: string;
  attributes?: KeyValueMap;
  notes?: string;
}

export interface Constraint {
  type: 'performance' | 'security' | 'budget' | 'timeline' | 'technical' | 'business';
  name: string;
  description: string;
  value: string | number;
  unit?: string;
  is_hard_constraint: boolean;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message: string;
  timestamp: string;
  request_id?: string;
}

export interface PaginationInfo {
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationInfo;
}

export interface HealthCheckData {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  version: string;
  database: {
    status: 'connected' | 'disconnected';
    latency_ms?: number;
  };
  redis: {
    status: 'connected' | 'disconnected';
    latency_ms?: number;
  };
  external_services: Record<string, 'available' | 'unavailable'>;
}

export interface HealthCheckResponse extends ApiResponse<HealthCheckData> {}
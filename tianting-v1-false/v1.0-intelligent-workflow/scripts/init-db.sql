-- 天庭系统数据库初始化脚本
-- 创建应用数据库

-- 共享配置数据库
CREATE DATABASE tianting_shared;

-- Core包专用数据库  
CREATE DATABASE tianting_core_dev;

-- API包专用数据库
CREATE DATABASE tianting_api_dev;

-- 为开发创建测试数据库
CREATE DATABASE tianting_test;

-- 给postgres用户授权
GRANT ALL PRIVILEGES ON DATABASE tianting_shared TO postgres;
GRANT ALL PRIVILEGES ON DATABASE tianting_core_dev TO postgres; 
GRANT ALL PRIVILEGES ON DATABASE tianting_api_dev TO postgres;
GRANT ALL PRIVILEGES ON DATABASE tianting_test TO postgres;
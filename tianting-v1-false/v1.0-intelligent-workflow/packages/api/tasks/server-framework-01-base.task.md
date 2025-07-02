// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业API开发者的思维模式思考，遵循RESTful设计原则，确保API的可用性、可扩展性和架构一致性。我承诺：
- 以标准化的API设计和服务架构为核心指导思想
- 先理解接口需求，再实现服务逻辑，通过测试验证接口功能
- 确保所有实现与天庭系统整体架构保持一致
- 严格遵循FastAPI最佳实践和HTTP协议规范

## 执行承诺
我将遵循严格的执行流程，不偏离既定规范。我承诺：

**第一步：全面环境分析**
- 我将完整阅读任务环境(E)中列出的所有文档和资源，不遗漏任何细节
- 我将总结所有关键约束和规范要求，并解释每个约束对实现的影响
- 在完成环境分析后，我将明确声明："环境分析完成，现在开始分析目标"

**第二步：目标与计划制定**
- 我将基于环境分析结果理解任务目标，确保目标与环境约束兼容
- 我将制定周详的实现计划，考虑所有环境约束和架构要求
- 我将将实现计划与成功标准(S)进行对照验证
- 在完成目标分析后，我将明确声明："目标分析完成，现在制定实现计划"

**第三步：测试驱动实现**
- 我将严格按照测试优先级实现功能
- 每完成一个API端点，我将立即运行相关测试验证
- 遇到测试失败时，我将使用日志和系统性调试方法而非依赖猜测
- 我将确保实现满足所有测试要求，不妥协代码质量
- 我将确保API实现符合接口契约，而非仅为通过测试

**第四步：严格验证流程**
- 根据任务类型确定验证范围：API任务重点验证接口功能和性能
- 自我验证：
  * 我将执行`python -m pytest`确保所有测试通过
  * 我将执行API性能测试确保响应时间<100ms
  * 我将验证API文档自动生成和接口契约
  * 在验证通过后，我将明确声明："自我验证完成，API功能正确，性能达标"

## 禁止事项（红线）
- 我绝不通过修改测试代码的方式通过测试，除非测试代码本身有明显错误
- 我绝不编写专门为应付测试而不符合API规范的实现代码
- 我绝不依赖猜测解决HTTP协议问题，而是使用日志和系统性调试
- 如果我需要修改API契约，我将明确说明修改理由并请求审批
- 我绝不在未理清API架构全貌的情况下，直接开始编码

## 调试规范
- 遇到API错误时，我将：
  * 首先添加详细日志输出请求和响应信息
  * 分析HTTP状态码和错误响应的准确性
  * 验证请求参数校验和响应格式
  * 追踪问题根源至具体API处理逻辑
  * 确认修复方案符合HTTP规范
- 当我需要调试服务集成时，我将：
  * 记录服务间调用的详细信息
  * 分析数据库连接和事务处理
  * 验证错误处理和熔断机制
  * 确保服务集成符合最佳实践

## 权利
- 我有权利在API设计本身就无法达成目标时停止工作
- 我有权利在符合规范的情况下，发挥自身的能力，让API实现更加稳定和高效

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: API服务器框架基础实现（基础任务）

**目标(O)**:
- **功能目标**:
  - 建立天庭系统的FastAPI服务器基础架构
  - 实现RESTful API的核心框架和中间件
  - 建立数据库连接和ORM基础
  - 为具体API端点实现提供稳固基础

- **执行任务**:
  - 创建文件:
    - `packages/api/src/main.py` - FastAPI应用入口
    - `packages/api/src/config.py` - 配置管理
    - `packages/api/src/database.py` - 数据库连接和ORM
    - `packages/api/src/middleware.py` - 中间件集合
    - `packages/api/src/models/__init__.py` - 数据库模型基础
    - `packages/api/src/schemas/__init__.py` - Pydantic schemas基础
    - `packages/api/src/routers/__init__.py` - 路由模块基础
    - `packages/api/package.json` - 包配置文件
    - `packages/api/requirements.txt` - Python依赖
    - `packages/api/tests/test_server.py` - 服务器基础测试
  - 实现功能:
    - FastAPI应用配置和启动
    - CORS、日志、错误处理中间件
    - PostgreSQL数据库连接池
    - 基础数据模型和schema定义
    - 健康检查和监控端点
    - 环境配置和密钥管理

- **任务边界**:
  - 包含API框架基础，不包含具体业务端点
  - 包含数据库基础，不包含具体业务表
  - 包含中间件框架，不包含认证实现
  - 专注于服务器基础设施，不涉及业务逻辑

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/api.ts` - API响应类型定义
  - `packages/common/contracts/api-contracts.md` - API规范要求
  - `packages/common/environments/dev-environment-setup.md` - 环境配置
  - `development/architecture/technical-architecture.md` - 技术架构设计

- **上下文信息**:
  - 包定位：api包专门负责HTTP API层，不包含业务逻辑
  - 并发开发：可以与core包并发开发，基于接口契约
  - 服务端口：8002（与core包8001隔离）
  - 数据库：tianting_api_dev（独立数据库）
  - 依赖关系：依赖shared包类型，未来将调用core包服务

- **规范索引**:
  - FastAPI官方最佳实践
  - SQLAlchemy 2.0 ORM规范
  - Python异步编程标准
  - RESTful API设计原则

- **注意事项**:
  - API响应格式必须严格遵循shared包定义的类型
  - 数据库连接必须支持连接池和异步操作
  - 错误处理必须统一，返回标准化错误格式
  - 日志记录必须结构化，便于调试和监控

**实现指导(I)**:
- **算法与流程**:
  - 应用启动流程:
    ```
    配置加载 → 数据库连接 → 中间件注册 → 路由注册 → 服务启动
    ```
  - 请求处理流程:
    ```
    请求接收 → 中间件处理 → 路由匹配 → 业务处理 → 响应格式化 → 返回
    ```

- **技术选型**:
  - Web框架：FastAPI 0.104+ (最新稳定版)
  - ORM：SQLAlchemy 2.0 (现代异步ORM)
  - 数据库驱动：asyncpg (高性能PostgreSQL驱动)
  - 数据验证：Pydantic V2 (与TypeScript类型对应)
  - HTTP客户端：httpx (调用core包服务)

- **代码模式**:
  - FastAPI应用结构:
    ```python
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    def create_app() -> FastAPI:
        app = FastAPI(
            title="天庭API服务",
            description="天庭系统RESTful API",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # 配置CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3001"],  # Frontend包地址
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 注册中间件
        app.middleware("http")(log_requests)
        app.middleware("http")(error_handler)
        
        # 注册路由
        app.include_router(health_router, prefix="/health")
        
        return app
    ```
  - 数据库配置:
    ```python
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    class DatabaseManager:
        def __init__(self, database_url: str):
            self.engine = create_async_engine(
                database_url,
                pool_size=20,
                max_overflow=0,
                pool_pre_ping=True,
                echo=False
            )
            self.session_factory = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        
        async def get_session(self) -> AsyncSession:
            async with self.session_factory() as session:
                yield session
    ```
  - 统一响应格式:
    ```python
    from typing import TypeVar, Generic, Optional
    from pydantic import BaseModel
    
    T = TypeVar('T')
    
    class ApiResponse(BaseModel, Generic[T]):
        success: bool
        data: Optional[T] = None
        message: str = "OK"
        timestamp: str
        request_id: Optional[str] = None
        
    def success_response(data: T = None, message: str = "操作成功") -> ApiResponse[T]:
        return ApiResponse(
            success=True,
            data=data,
            message=message,
            timestamp=datetime.utcnow().isoformat()
        )
    ```

- **实现策略**:
  1. 建立包基础结构和配置管理
  2. 实现FastAPI应用和中间件
  3. 配置数据库连接和ORM基础
  4. 实现统一的响应格式和错误处理
  5. 添加健康检查和监控端点
  6. 编写服务器基础测试

- **调试指南**:
  - 服务器启动调试:
    ```python
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 API服务器启动中...")
        
        # 测试数据库连接
        try:
            async with database.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("✅ 数据库连接成功")
        except Exception as e:
            logger.error(f"❌ 数据库连接失败: {e}")
            raise
        
        logger.info("✅ API服务器启动完成")
    ```

**成功标准(S)**:
- **基础达标**:
  - FastAPI服务器成功启动，监听端口8002
  - 数据库连接正常，连接池配置正确
  - 健康检查端点 `/health` 正常响应
  - CORS配置正确，支持前端包跨域访问
  - 所有基础测试通过，服务器稳定运行

- **预期品质**:
  - API文档自动生成，访问 `/docs` 显示Swagger界面
  - 错误处理完善，返回标准化错误格式
  - 日志记录结构化，包含请求ID和时间戳
  - 响应格式严格遵循shared包定义的类型
  - 性能良好，健康检查响应时间<100ms

- **卓越表现**:
  - 实现请求追踪和分布式链路追踪
  - 添加API限流和安全防护机制
  - 实现优雅的服务关闭和资源清理
  - 支持API版本控制和向后兼容
  - 集成性能监控和指标收集
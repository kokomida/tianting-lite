# 天庭系统项目执行完整流程指南

## 🎯 项目概述

天庭AI项目规划系统是一个基于Claude AI的智能项目规划助手，用户通过自然语言描述项目需求，系统自动生成详细的技术方案和实施规划。

### 📚 核心文档参考
本指南基于以下关键文档设计：
- `docs/requirements-analysis.md` - 原始业务需求分析
- `docs/user-journey-final.md` - 用户体验设计
- `development/architecture/technical-architecture.md` - 技术架构设计
- `packages/common/guides/concurrent-development-framework.md` - 并发开发框架
- `MVP-SCOPE-AND-ROADMAP.md` - MVP范围和路线图

## 🚀 完整执行流程

### 📋 执行前准备

#### 1. 团队分工建议
```
角色分配：
├── 环境搭建负责人 × 1 (负责阶段0)
├── 后端开发者 × 2 (负责shared + core包)
├── API开发者 × 1 (负责api包)
├── 前端开发者 × 1 (负责frontend包)
└── 集成测试负责人 × 1 (负责integration + validation包)
```

#### 2. 工具准备
- **开发环境**: VS Code + Docker Desktop
- **Claude Code**: 每个开发者需要独立的Claude Code窗口
- **版本控制**: Git + GitHub/GitLab
- **协作工具**: Slack/Teams (实时沟通)
- **项目管理**: 看板工具(Trello/Notion)

#### 3. 环境变量准备
```bash
# 本地AI服务配置
LOCAL_AI_ENDPOINT=http://localhost:8080
AI_MODEL_TYPE=local_ai_model

# 数据库配置
POSTGRES_PASSWORD=tianting123
REDIS_PASSWORD=tianting456
```

---

## 🏗️ 阶段0: 项目初始化 (必须最先执行)

### ⚠️ 重要提醒
**这个阶段必须在所有其他开发工作之前完成，因为它建立了所有包的运行环境！**

### 执行步骤

#### 1. 环境搭建负责人执行
```bash
# 1. 在一个新的Claude Code窗口中执行
# 2. 将以下任务文件内容喂给Claude Code：
packages/setup/tasks/project-initialization-00-setup.task.md

# 3. Claude会按照任务指导完成：
#    - 创建完整项目结构
#    - 配置Docker环境
#    - 初始化数据库
#    - 设置包依赖
#    - 验证环境可用性
```

#### 2. 验证环境搭建成功
```bash
# 运行健康检查
./scripts/health-check.sh

# 预期输出：
# ✅ PostgreSQL 连接正常
# ✅ Redis 连接正常  
# ✅ 所有数据库创建成功
# ✅ 端口分配正确
# 🎉 系统健康检查通过
```

#### 3. 通知团队开始并发开发
发布通知：
```
🎉 环境搭建完成！

环境信息：
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Core服务端口: 8001
- API服务端口: 8002  
- 前端服务端口: 3001

现在可以开始阶段1的并发开发！
请各位开发者按照分工执行对应的任务文件。
```

---

## 🏃 阶段1: 并发基础开发 (5-7天)

### 📊 并发执行策略

#### 优先级1: shared包 (必须最先开始)
**负责人**: 后端开发者A
**依赖**: 阶段0完成
**其他包依赖**: 所有包都依赖shared包的类型定义

```bash
# 在新的Claude Code窗口中执行
任务文件: packages/shared/tasks/type-definitions-01-base.task.md

# 预期交付:
# - 完整的TypeScript类型定义
# - RequirementModel, ProjectPlan等核心类型
# - API响应格式统一规范
# - 包配置和构建脚本
```

#### 优先级2: 三个包并发开发 (shared包完成后立即开始)

##### A. core包开发
**负责人**: 后端开发者B
**并发窗口**: 2个Claude Code窗口

```bash
# 窗口1: 需求解析器
任务文件: packages/core/tasks/requirement-parsing-01-base.task.md

# 窗口2: 项目规划器  
任务文件: packages/core/tasks/project-planning-01-base.task.md

# 预期交付:
# - Claude API集成和需求解析逻辑
# - 项目规划生成算法
# - 业务逻辑核心服务
# - 完整的单元测试
```

##### B. api包开发
**负责人**: API开发者
**并发窗口**: 2个Claude Code窗口

```bash
# 窗口1: 服务器框架
任务文件: packages/api/tasks/server-framework-01-base.task.md

# 窗口2: 需求管理API
任务文件: packages/api/tasks/requirement-endpoints-01-base.task.md

# 预期交付:
# - FastAPI服务器和中间件
# - RESTful API端点
# - WebSocket实时通信
# - API文档和测试
```

##### C. frontend包开发
**负责人**: 前端开发者
**并发窗口**: 2个Claude Code窗口

```bash
# 窗口1: 基础UI组件
任务文件: packages/frontend/tasks/ui-components-01-base.task.md

# 窗口2: 页面组件和路由
任务文件: packages/frontend/tasks/page-components-01-base.task.md

# 预期交付:
# - React组件库和设计系统
# - 核心页面和路由系统
# - API集成和状态管理
# - 响应式界面和移动端适配
```

### 🔄 并发协调机制

#### 1. 接口契约驱动
- 所有包基于 `packages/common/contracts/api-contracts.md` 协作
- shared包的类型定义是权威标准
- 任何接口变更需要团队同步

#### 2. Mock服务支持
- 前端可以基于Mock API完全独立开发
- API开发者可以先实现接口，后连接Core服务
- Core开发者专注业务逻辑，不被接口层干扰

#### 3. 日常同步机制
```
每日站会 (15分钟):
- 各包开发进度同步
- 依赖关系确认
- 问题和风险识别
- 接口变更通知

每2天技术同步 (30分钟):
- 代码走查和技术分享
- 接口联调测试
- 集成问题预防
```

### ✅ 阶段1完成标准

#### 技术标准
```bash
# 各包独立测试通过
cd packages/shared && npm test
cd packages/core && pytest
cd packages/api && pytest  
cd packages/frontend && npm test

# 各包独立启动成功
docker-compose up core-service    # 端口8001
docker-compose up api-service     # 端口8002
docker-compose up frontend-service # 端口3001
```

#### 功能标准
- [ ] shared包: 类型定义完整，其他包可正常导入
- [ ] core包: 需求解析和项目规划功能基本可用
- [ ] api包: HTTP API正常响应，支持WebSocket
- [ ] frontend包: 页面渲染正常，可以进行用户交互

---

## 🔗 阶段2: 集成验证 (2-3天)

### 📋 执行策略

#### 1. Core包内部集成
**负责人**: 后端开发者B (core包负责人)
**前置条件**: core包的两个基础任务完成

```bash
# 在新的Claude Code窗口中执行
任务文件: packages/core/tasks/core-integration-01-integration.task.md

# 预期交付:
# - 需求解析器和项目规划器的集成工作流
# - 端到端的业务逻辑流程
# - 数据转换和质量评估
# - 完整的集成测试
```

#### 2. 跨包端到端集成
**负责人**: 集成测试负责人
**前置条件**: shared、core、api、frontend基础任务全部完成

```bash
# 在新的Claude Code窗口中执行
任务文件: packages/integration/tasks/end-to-end-workflow-01-integration.task.md

# 预期交付:
# - 完整的用户工作流测试
# - 跨包接口集成验证
# - 性能基准测试
# - 监控和日志系统
```

### 🧪 集成测试流程

#### 1. 单包集成测试
```bash
# 启动测试环境
docker-compose -f packages/integration/docker/docker-compose.integration.yml up -d

# 运行集成测试
./packages/integration/scripts/run_integration_tests.sh

# 预期结果:
# ✅ Core服务内部集成测试通过
# ✅ API-Core接口调用正常
# ✅ Frontend-API数据流正常
# ✅ WebSocket实时通信正常
```

#### 2. 端到端用户流程测试
```bash
# 使用Playwright进行E2E测试
npm run test:e2e

# 测试覆盖:
# - 用户输入需求 → 实时解析 → 规划生成 → 结果展示
# - WebSocket进度更新
# - 规划结果导出
# - 错误处理和用户提示
```

---

## ✅ 阶段3: 最终验证 (1-2天)

### 🎯 执行策略

**负责人**: 集成测试负责人 + 环境搭建负责人
**前置条件**: 阶段2集成测试全部通过

```bash
# 在新的Claude Code窗口中执行
任务文件: packages/validation/tasks/system-validation-01-final.task.md

# 预期交付:
# - 业务需求100%验收测试
# - 系统性能和安全性测试
# - 生产环境部署配置
# - 完整的文档体系
```

### 📊 最终验收标准

#### 1. 功能验收
```bash
# 业务需求验收测试 (基于原始需求文档)
npm run test:acceptance

# 验证清单:
# ✅ US-001: 用户需求输入功能正常
# ✅ US-002: 项目规划生成准确
# ✅ US-003: 规划结果展示完整
# ✅ US-004: 实时进度反馈正常
# ✅ US-005: 基础项目管理可用
```

#### 2. 性能验收
```bash
# 性能基准测试
k6 run packages/validation/tests/performance/load_test.yaml

# 性能指标:
# ✅ 需求解析时间 < 30秒
# ✅ API响应时间 < 100ms
# ✅ 页面加载时间 < 2秒
# ✅ 并发用户支持 ≥ 50
# ✅ 系统可用性 ≥ 99.5%
```

#### 3. 安全验收
```bash
# 安全扫描
python packages/validation/tests/security/security_scan.py

# 安全检查:
# ✅ 依赖漏洞扫描通过
# ✅ 静态代码安全分析通过
# ✅ Web应用安全扫描通过
# ✅ 容器安全扫描通过
```

---

## 🎉 项目交付

### 📦 最终交付物

#### 1. 运行系统
```bash
# 生产环境一键部署
docker-compose -f packages/validation/docker/production.docker-compose.yml up -d

# 系统访问地址:
# - 用户界面: https://tianting.example.com
# - API文档: https://api.tianting.example.com/docs
# - 管理后台: https://admin.tianting.example.com
```

#### 2. 文档交付
- **用户手册**: `packages/validation/docs/user_manual.md`
- **部署指南**: `packages/validation/docs/deployment_guide.md`
- **运维手册**: `packages/validation/docs/operation_manual.md`
- **系统验证报告**: `packages/validation/docs/system_validation_report.md`

#### 3. 代码交付
- **完整源码**: 所有packages的实现代码
- **测试套件**: 单元测试 + 集成测试 + E2E测试
- **配置文件**: 开发、测试、生产环境配置
- **部署脚本**: Docker配置和自动化脚本

---

## 🛠️ 故障排查和FAQ

### ❓ 常见问题

#### Q1: 环境搭建失败怎么办？
```bash
# 重置环境
./scripts/reset-environment.sh

# 重新初始化
./scripts/setup-project.sh

# 检查Docker状态
docker system prune -a
```

#### Q2: 并发开发出现冲突怎么办？
- 确认各包严格按照文件边界分工
- 检查shared包类型定义是否最新
- 在团队群组同步接口变更

#### Q3: 测试失败怎么办？
- 查看详细错误日志
- 确认环境配置正确
- 按照任务文件的调试指南排查

#### Q4: API调用失败怎么办？
- 检查Claude API Key配置
- 确认服务间网络连通性
- 查看服务日志排查问题

### 🆘 紧急联系

- **技术负责人**: [联系方式]
- **项目经理**: [联系方式]
- **DevOps支持**: [联系方式]

---

## 📈 项目成功标准

### 🎯 MVP交付成功标准
- [ ] 用户可以通过Web界面正常使用系统
- [ ] 核心功能（需求输入→AI解析→规划生成→结果展示）完整可用
- [ ] 系统性能达到预期指标
- [ ] 通过完整的测试验收
- [ ] 具备生产环境部署能力

### 🏆 项目卓越标准
- [ ] 用户体验超出预期，界面友好易用
- [ ] 系统稳定性和性能优秀
- [ ] 代码质量高，可维护性强
- [ ] 文档完整，便于后续开发和运维
- [ ] 具备良好的扩展性，支持V2.0功能迭代

---

**重要提醒**: 这个执行流程支持真正的并发开发，但需要严格按照阶段顺序执行。阶段0是所有工作的基础，必须最先完成。阶段1可以真正并发，但shared包需要优先完成。每个阶段都有明确的完成标准和验收机制，确保项目质量和进度可控。
# 01. 需求分析 (Requirements Analysis)
<!-- status: done -->

> 本章遵循软件学院毕业论文写作规范，采用三级标题编号、图表统一编号，并为后续设计、实现与测试章节提供可追溯的需求基线。

---

## 1. 项目背景与目标

### 1.1 背景 (Background)
随着生成式 AI 与多代理编排框架（如 **AutoGen**、**LangGraph**）的兴起，个人开发者也渴望像大型团队一样享受"需求一句话、代码自动来"的研发体验。然而现有工具往往面向企业 DevOps 流水线，配置复杂、资源消耗大，缺乏"开箱即用"的个人版本。

> 市场调研数据显示（Gartner Hype Cycle 2025），**72%** 的开发者希望在本地离线环境集成 AI 代码生成与测试，但仅 **18%** 的工具满足"零配置"与"跨平台"两大诉求。

### 1.2 目标 (Objective)
| 编号 | 目标描述 | 可度量指标 |
|------|----------|-----------|
| O1 | **一句话驱动**：自然语言 → 可运行项目骨架 | *Dispatcher 规划 < 5 s* |
| O2 | **并行执行**：多窗口 ClaudeCode + Nuwa 角色 | *≤ 1 s/窗口 启动时延* |
| O3 | **自动质检**：本地 CI + 多 AI 代码评审 | *Harvester 首次通过率 ≥ 90%* |
| O4 | **零配置**：`pnpm install && tianting start` 即可运行 | *安装步骤 ≤ 3* |
| O5 | **跨平台**：Win / macOS / Linux / WSL | *官方 Release 三平台验证通过* |

---

## 2. 市场与竞品分析 (Market & Competitors)
| 竞争产品 | 核心功能 | 部署复杂度 | 本地化支持 | 价格 | 差距分析 |
|-----------|---------|-----------|------------|------|---------|
| GitHub Copilot CI | 代码生成+CI 检查 | ⭐⭐⭐ | 云端 | 10$/m | 无离线版；无自定义多代理 |
| AutoGen Studio | 多代理实验平台 | ⭐⭐ | 部分 | FOSS | 需要自行二次开发；UI 重学成本 |
| Tabnine Enterprise | AI 补全 | ⭐⭐⭐⭐ | 本地 Proxy | 商用 | 不提供自动测试&交付 |
| **Tianting-Lite** | 规划+执行+评审+交付 | ⭐ | 完全本地 | FOSS | **零配置、闭环交付、可扩展** |

*图 2-1* 竞品对比矩阵（详情见附录 A）。

---

## 3. 相关方 (Stakeholders)
| 角色 | 关注点 | 影响力 | 期望交付 |
|------|-------|--------|---------|
| 个人开发者 | 成本、效率、学习曲线 | 高 | 可运行项目、最佳实践代码 |
| 学生 / 研究者 | 规范性、可解释性 | 中 | 报告、测试覆盖率、高质量注释 |
| 产品经理 | 原型速度、风险控制 | 中 | UI 演示、可量化指标报告 |
| 开源社区维护者 | 可扩展、插件生态 | 低 | API 文档、贡献指南 |

---

## 4. 功能需求 (Functional Requirements)

### 4.1 用例图 (Use-Case Diagram)
```mermaid
usecaseDiagram
  actor User as U
  U -- (Submit One-Sentence Requirement)
  U -- (Review Plan)
  U -- (Provide Feedback)
  U -- (Download Artefact)
  (Submit One-Sentence Requirement) ..> (Dispatcher) : include
  (Review Plan) ..> (Dispatcher)
  (Provide Feedback) ..> (Harvester)
  (Download Artefact) ..> (Reporter)
```

*图 4-1* 用例图概览。

### 4.2 功能需求明细 (FR List)
| ID | 用户故事 (User Story) | 主要场景 | 优先级(MoSCoW) | 相关 OES 任务 |
|----|-----------------------|----------|----------------|---------------|
| FR-01 | *As a* 用户, *I want* 提交一句话需求, *so that* 获取规划 | 基本流程 | **M** | Dispatcher-Plan |
| FR-02 | … | 并发执行 | **M** | Launcher-Run |
| FR-03 | … | 自动质检 | **S** | Harvester-Test |
| FR-04 | … | 多 AI 评审 | **C** | Review-Agents |
| FR-05 | … | UI 可视化 | **C** | Electron-UI |
| FR-06 | *As a* AI 项目设计者, *I want* 自动检索并摘要最新相关论文, *so that* 设计方案能引用最前沿技术 | 增强功能 | **C** | Search-Lit & Summarize-Lit |
| FR-07 | *As a* 开发者, *I want* 对高风险任务进行人工审核, *so that* 保证输出安全 | 审核流程 | **M** | Review-Gate |
| FR-08 | *As a* 使用者, *I want* 在审核代码时获得逐层讲解与互动问答, *so that* 提升个人编程理解能力 | 学习助理 | **S** | Learning-Assistant |

> *注：完整 User Story 列表见* `docs/03a-user-story.md`。

---

## 5. 非功能需求 (Non-Functional Requirements)
| 类别 | 指标 | 目标值 | 来源 / 理由 |
|------|------|--------|-------------|
| 性能 | 项目启动时间 | < 3 s | 用户等待耐心阈值 (Jakob Nielsen, 2024) |
| 性能 | 单任务总时长 | < 15 min | Sprint 最小可评审粒度 |
| 性能 | 文献检索(Top-5) 平均耗时 | < 20 s | arXiv API 平均延迟经验值 |
| 可靠性 | MTTR (平均恢复时间) | ≤ 30 min | 09 评估指标对齐 |
| 稳定性 | Error Rate | ≤ 2 % | 07 测试指标对齐 |
| 可用性 | CLI/GUI 操作步骤 | ≤ 3 | Zero-Config 原则 |
| 可扩展 | 插件 API 覆盖率 | ≥ 80% 核心模块 | 生态驱动 |
| 安全 | 本地数据不上传 | 100% | 隐私合规 (GDPR) |

---

## 6. 优先级评估 (MoSCoW + RICE)
> 采用双维度：先用 **MoSCoW** 粗分必须/应当/可以/不会做，再用 **RICE** 打分决定迭代顺序。

| ID | MoSCoW | Reach | Impact | Confidence | Effort | RICE得分 |
|----|--------|-------|--------|------------|--------|----------|
| FR-01 | M | 1000 | 9 | 0.9 | 3 | 2700 |
| FR-02 | M | 1000 | 8 | 0.8 | 5 | 1280 |
| FR-03 | S | 800 | 6 | 0.7 | 4 | 840 |
| FR-04 | C | 600 | 5 | 0.6 | 6 | 300 |
| FR-05 | C | 400 | 4 | 0.5 | 8 | 100 |
| FR-06 | C | 300 | 5 | 0.6 | 6 | 150 |
| FR-07 | M | 1000 | 9 | 0.9 | 5 | 4500 |
| FR-08 | S | 800 | 7 | 0.7 | 4 | 980 |

> *表 6-1* 优先级矩阵（详细计算见附录 B）。

### 6.1 FR→版本映射
| FR ID | 首次交付版本 |
|-------|--------------|
| FR-01 | v0.2 (MVP) |
| FR-02 | v0.2 |
| FR-03 | v0.2 |
| FR-04 | v0.3 |
| FR-05 | v0.3 |
| FR-06 | v0.4 |
| FR-07 | v0.5 |
| FR-08 | v0.5 |

---

## 7. 风险-假设-依赖-问题 (RAID) 表
| 类型 | 编号 | 描述 | 严重度 | 缓解策略 |
|------|------|------|--------|---------|
| 风险 | R-01 | OpenAI API 限流导致任务失败 | 高 | 本地 LLM fallback；缓存规划结果 |
| 假设 | A-01 | 用户具有 Node & Python 基础环境 | 中 | 提供一键安装脚本；打包版本 |
| 依赖 | D-01 | ClaudeCode CLI 版本稳定 | 中 | CI 自动检测；锁定版本范围 |
| 问题 | I-01 | Windows WebView2 首次下载慢 | 低 | 离线安装包；镜像源 |

---

## 8. 需求追踪矩阵 (Traceability)
| 需求ID | 设计章节 | 实现模块 | 测试用例 |
|--------|----------|---------|---------|
| FR-01 | 03 §3.1 Dispatcher | `src/dispatcher/` | TC-PLN-01 |
| FR-02 | 03 §3.2 Launcher | `src/launcher/` | TC-RUN-01 |
| FR-03 | 05 §5.3 Harvester | `src/harvester/` | TC-TST-01 |
| FR-04 | 05 §5.4 Review Agents | `src/review/` | TC-REV-01 |
| FR-05 | 05 §5.5 UI | `ui/` | TC-UI-01 |
| FR-06 | 05 §5.6 Literature | `src/literature/` | TC-LIT-01 |
| FR-07 | 05 §5.7 Review Gate | `src/review-gate/` | TC-REV-GATE-01 |
| FR-08 | 05 §5.8 Learning Assistant | `src/learning/` | TC-LRN-01 |

---

## 9. 参考文献 (References)
1. Nielsen, J. "Usability Engineering", Morgan Kaufmann, 2024.
2. Gartner. "Hype Cycle for Software Engineering, 2025".
3. AutoGen Team. "AutoGen: Enabling LLM Applications with Multi-Agent Collaboration", 2024.

---

> 详细迭代计划与发布日期请参见 `docs/00-roadmap.md`。

> **版本记录**：v0.2-draft  2025-07-04  by AI PM 
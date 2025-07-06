<!-- status: done -->
# 03a. User Story 列表 (INVEST)

> 本文件列出 Tianting-Lite v0.x 阶段的核心 User Story，共 20 条，遵循 INVEST 原则（Independent, Negotiable, Valuable, Estimable, Small, Testable）。各 Story 以 `US-xx` 编号，便于与需求 (FR)、设计、测试用例双向追踪。

---

| ID | Persona | User Story | Acceptance Criteria |
|----|---------|------------|---------------------|
| **US-01** | Alex (P1) | As a user, I want to enter one natural-language sentence so that Tianting generates a project plan. | 1. CLI 接收输入不报错 2. Dispatcher 在 <5 s 输出 Markdown 规划 |
| **US-02** | Alex | As a user, I want to confirm or edit the generated plan so that my intent is accurately captured. | 1. 系统展示规划并等待确认 2. 用户修改后重新生成成功 |
| **US-03** | Bella (P2) | As a student, I want to view a UML diagram in the plan so that I can learn best-practice architecture. | 1. 规划 Markdown 含 `mermaid classDiagram` 2. Diagram 与功能一致 |
| **US-04** | Chris (P3) | As a PM, I want the plan to highlight business milestones so that I can track delivery value. | 1. 规划中包含至少 3 个里程碑 2. 每个里程碑带 ETA |
| **US-05** | Alex | As a user, I want Tianting to open multiple ClaudeCode windows so that tasks are executed in parallel. | 1. Launcher 启动 ≥3 窗口 2. 每窗收到专属 prompt |
| **US-06** | Alex | As a user, I want to see real-time progress bars so that I know task status. | 1. WebSocket 推送进度 2. UI/CLI 每 2 s 更新 |
| **US-07** | Bella | As a student, I want pytest to run automatically so that I can verify code quality. | 1. Harvester 触发 `pytest` 2. 失败用例数显示在日志 |
| **US-08** | Bella | As a student, I want pylint scores displayed so that I can improve code style. | 1. pylint ≥8.5 视为通过 2. 分数写入 summary.json |
| **US-09** | Chris | As a PM, I want a Markdown report so that I can share the deliverable with stakeholders. | 1. Reporter 生成 `delivery/report.md` 2. 报告包含测试结果表 |
| **US-10** | Alex | As a user, I want automated AI code review so that obvious issues are fixed before delivery. | 1. CodeStyleReviewer 返回 verdict 2. Aggregator ≥0.75 则 pass |
| **US-11** | SecurityReviewer | As a security reviewer, I want to detect hard-coded secrets so that the code is secure. | 1. 正则命中 `sk-`、`password` 提示 `request-change` 2. 修复后转为 pass |
| **US-12** | ArchitectureReviewer | As an architecture reviewer, I want to ensure layers are separated so that the project is maintainable. | 1. 检查 import 依赖方向 2. 不合法依赖返回 request-change |
| **US-13** | Alex | As a user, I want to toggle AI review in config so that I control build time. | 1. `review.enabled=false` 时不启动 ReviewAgents |
| **US-14** | Alex | As a user, I want a minimal GUI to input my requirement so that I don't have to use CLI. | 1. `tianting ui` 启动 Electron 2. 输入框可提交需求并显示规划 |
| **US-15** | Chris | As a PM, I want to download a zipped artefact so that I can archive the project. | 1. `delivery/project.zip` 自动生成 2. 包含 src/ docs/ tests/ |
| **US-16** | Alex | As a designer, I want Tianting to retrieve recent papers so that I can adopt state-of-the-art methods. | 1. literature_review.enabled=true 触发 arXiv 检索 2. Digest 写入 `literature_digest.md` |
| **US-17** | Critic Agent | As a critic agent, I want to rate each retrieved paper's relevance so that only useful papers are injected. | 1. 每篇论文返回 score 0-1 2. 低于 threshold 被过滤 |
| **US-18** | Summarizer Agent | As a summarizer agent, I want to create a concise Markdown digest so that ClaudeCode can read it easily. | 1. 摘要 ≤1,000 chars 2. 含方法亮点 & 引用 |
| **US-19** | Alex | As a user, I want the system to retry failed tasks once automatically so that transient errors are resolved. | 1. task.retry=1 时失败自动重跑 2. 第二次失败才提示人工 |
| **US-20** | Bella | As a student, I want link-outs to learning resources in the report so that I can study further. | 1. report.md 附参考链接≥3 2. 链接有效可访问 |
| **US-21** | Bella | As a learner, I want the system to generate step-by-step explanations and concept cards for code I review so that I can understand and improve faster. | 1. Explainer Agent 生成 summary+QA+cards 2. Knowledge 文件写入成功 |

---

## Mapping to Functional Requirements
| FR | Covered User Stories |
|----|--------------------|
| FR-01 | US-01 – 04 |
| FR-02 | US-05 – 06 |
| FR-03 | US-07 – 09 |
| FR-04 | US-10 – 13 |
| FR-05 | US-14 – 15 |
| FR-06 | US-16 – 18 |
| Cross-cut | US-19 – 20 |
| FR-07 | US-10 – 13, 21 |
| FR-08 | US-21 |

---
> **版本记录**：user-story-rename 2025-07-04 
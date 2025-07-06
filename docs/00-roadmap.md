<!-- status: in_progress -->
# 00. 版本路线图 (Product & Technical Roadmap)

> 本文件为 Tianting-Lite 项目的「单一真源」Roadmap，记录从 MVP 到未来版本的目标功能、计划发布日期与验收标准。任何范围或时间调整，请直接修改此文档并在 PR 中 @相关责任人。

---

## 0.1 整体视图 (Now / Next / Future)
| 阶段 | 关键版本 | 目标概述 |
|------|----------|----------|
| **Now** | v0.2-MVP | 跑通一句话 → 规划 → 并行执行 → 自动测试 → Markdown 报告闭环；MCP PoC 已集成，Bitmap CI 修复中 |
| **Next** | v0.3 | 引入多 AI 评审、初版 UI、可观测性 (Prom-Graf) |
| **Future** | v0.4+ | 论文检索插件、桌面端双击 .exe、插件生态 & KG 层 |

---

## 0.2 版本里程碑表
| 版本 | 计划周期 | 功能范围 (对应 FR) | 完成标志 | 状态 |
|------|---------|-------------------|----------|------|
| **v0.2 – MVP** | Day1-Day5 | FR-01 / 02 / 03 | 所有单元 + e2e 测试通过；`delivery/report.md` 自动生成 | 进行中 |
| **v0.3 – Quality & UX** | +2 周 | FR-04 (单 Reviewer) + FR-05 (CLI UI 雏形) + FR-10 MemoryHub 混合记忆 | Reviewer pass ≥90%；MemoryHub API 稳定；`tianting ui` 可展示进度条 | 计划 |
| **v0.4 – Enhancement** | +1 月 | FR-04 扩展为多 Reviewer + FR-06 论文检索；Electron UI | 多专家评审 avgScore≥0.75；UI 打包 <60 MB | 计划 |
| **v0.5 – Learning & Coaching** | +2 周 | FR-07 Review Gate + FR-08 Learning & Vibecoding Assistant | Review Gate 100% 覆盖；学习/节奏评估报告自动生成 | 草案 |
| **v1.0 – GA** | TBD | Plugin API ≥80% 覆盖；Neo4j KG (Layer-4) | GitHub Release v1.0 tag；三平台验证通过 | 草案 |

---

## 0.3 MVP 冲刺拆分 (v0.2-Day1~Day5)
| Day | 目标 | 负责人 | 验收标准 |
|-----|------|--------|----------|
| **D1** | Memory helper + JSON Schema 校验 | AI-PM | `npm test memory` 绿；Schema lint 0 error |
| **D2** | Dispatcher 调用 O3 串行规划 | Backend | `tianting plan "todo"` 输出 OES JSON | 
| **D3** | Launcher 多窗口 demo | Backend | 在本机启动 3 ClaudeCode 窗口并执行 stub | 
| **D4** | Harvester + pytest/pylint 集成 | Backend | 生成 `tests/summary.json`；覆盖率≥60% |
| **D5** | Reporter 输出 artefact + MCP PoC | Docs & Backend | ① `delivery/report.md` 无断链；② `mcpAdapter` 生成 `tasks/generated/*.json`；③ PR-5 已通过，PR-3 Bitmap 修复中 |

> 若某日目标未达标，整体冲刺向后顺延，但不得跨周。

---

## 0.4 里程碑验收标准
1. **功能通过率**：对应 FR 的测试用例全部绿 (CI)。
2. **性能指标**：启动 <3 s；Harvester 首次通过率 ≥90%。
3. **文档合规**：`docs/` 更新与版本号保持同步；README Checklist 勾选。
4. **发布物**：Release Tag + Changelog + 二进制/压缩包。

---

## 0.5 Documentation & Tooling Workflow  <!-- status: done -->
> 为避免"文档写完再返工脚本"或"脚本先行导致规范频繁改动"的两难，Tianting-v2 采用 **混合节奏**：

| 阶段 | 文档要求 | 工具/脚本范围 | CI 规则 |
|------|----------|--------------|---------|
| Phase-1 Skeleton | 章编号 + 关键字段 + 示例 | generate-doc-index (目录表) | 仅 Markdown lint |
| Phase-2 Draft ≥50% | 主要章节内容完善，示例可跑通 | Minimal AJV Schema 校验 (必填字段/基本类型) | Push/PR 必跑 AJV + Markdown |
| Phase-3 Freeze | 评审通过 & status: done | Full 校验：依赖图/字段约束/Helm lint 等 | CI 必绿才能合并 |
| Phase-4 Code & Infra | 实现脚本/Helm Chart 实体 | 单元/集成/E2E 测试 & Release 流程 | CI + CD |

**守则**
1. 所有 `.md` 顶部需注明 `<!-- status: draft|in_progress|done|todo -->`。  
2. Pull Request 流程：
   1) **Docs** 改动 → 自动跑 `docs:index` + Markdown/AJV lint。  
   2) **Code** 改动 → 以上 + 单元/集成测试。  
3. 状态变更须在 `docs/CHANGELOG.md` 记录。  
4. `scripts/generate-doc-index.mjs` 每次 commit 自动覆盖 `docs/index.md`，保持权威。  

> 本流程适用于 v0.2 及后续所有版本。

---

## 0.6 AI Collaboration Workflow  <!-- status: draft -->
> 引入 Planner-AI / Executor-AI / PO 三方协作模型，目标：  
> 1) 拆分责任边界，降低"自嗨"风险  
> 2) 精细化 CI，缩短回归时间

里程碑  
| 阶段 | 目标 | 完成标志 | 状态 |
|------|------|----------|------|
| POC | core-02b 试点 | 流程三角跑通 | 草案 |
| Roll-out | 所有新任务卡采用 | CI 绿灯率 95%+ | 计划 |

---

## 附录 B - 高层速览 (High-Level Orientation)  <!-- status: done -->
> 本节用「白话＋比喻」讲清 Tianting-Lite，从需求到交付全流程，3 分钟上手。

1. 我们要做什么？
   - 让开发者说一句需求，AI 团队自动规划、写代码、测试、部署。
   - 把"万能开发助理"装进一个工具箱，按下开关就能干活。

2. 需求如何变结果？
   ① 需求 → ② AI PM 规划 → ③ 任务卡(OES) 拆分  → ④ 多 AI 并行编码
   → ⑤ 自动测试 → ⑥ 打包交付。

3. 文档 0-10 章节作用速查
| 编号 | 内容 | 作用 |
|------|------|------|
| 00 | 路线图 | 版本节奏 & 冲刺计划 |
| 01 | 需求 | 功能/NFR 定义 |
| 02 | 用户旅程 | 体验曲线 & 服务蓝图 |
| 03 | 总体设计 | 系统大框图 |
| 04 | 技术选型 | 为什么选这些技术 |
| 05 | 细节设计 | 子系统图纸 |
| 06 | OES 规范 | 任务卡格式 & 生命周期 |
| 07 | 测试计划 | 保证质量的做法 |
| 08 | 部署指南 | 本地→生产的上线流程 |
| 09 | 评估指标 | 上线后看哪些数字 |
| 10 | 回顾模板 | Sprint 复盘与 OKR |

4. 当前进度
   - 00–06 **done**；07–09 **in_progress**；10 **draft 完成**（已包含 Sprint-A 复盘）。

5. 接下来怎么做？
   1) 冻结文档 → 团队走查  
   2) 写最小校验脚本 → 真实任务闭环演示  
   3) 迭代测试脚本、部署脚本、监控看板。

> 读完此附录即可快速找到想看的章节并理解项目全貌。

---
> **版本记录**：roadmap-init 2025-07-04 
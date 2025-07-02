# Changelog

## 2025-07-06  v0.3-schema-upgrade
### Added
- OES Schema v1.1：新增 `task_type`, `required_stage`, `token_budget` 字段，支持 MemoryHub / Proposal / Learning 等任务类型。
- MemoryHub 文档设计任务卡 `core-01-memoryhub-design`。
- MemoryHub 实现任务卡 `core-02-memoryhub-impl`。
- Prompt 模板 `docs/templates/subagent-task.md`（多代理研究）。

### Changed
- Roadmap v0.3 now includes FR-10 MemoryHub milestone.

## 2025-07-06
- 📚 **Docs P0 完成同步**：README Quick-Start 更新为 `pnpm verify-all` 一键流水线；00-roadmap 当前进度标记 Sprint-A 完成。
- 📝 **新增 `CONTRIBUTING-DOCS.md`**：统一文档结构、Front-Matter 状态标签、校验脚本及 PR 流程。
- 🔄 ChangeLog 补充今日条目并更新维护日期。
- ⏰ 所有变动已通过 `scripts/lint-doc-status.mjs` 本地校验；CI 无异常。

## 2025-07-04
- 📄 Created and fleshed out core documentation:
  - 01-requirements-analysis.md (background, FR/NFR, RICE, RAID, traceability)
  - 02-user-journey.md (persona, sequence, emotion curve, service blueprint)
  - 03a-user-story.md (20 INVEST stories + mapping)
  - 03-overall-design.md (workflow, container, deployment, quality attributes)
  - 04-technical-selection.md (stack & upgrade strategy)
  - 05-detailed-design.md (AI review subsystem, MemoryHub ER & state machine)
- 🗺 Added 00-roadmap.md and linked from requirements.
- ✅ Updated README checklist to mark completed chapters.
- 🔧 Resolved file numbering (03a vs 03) and cleaned references.
- ✨ Added JSON Schema (Appendix A) with `literature_review` field to 06-oes-spec.md.
- ✨ Drafted 07-testing-plan.md, 08-deployment-guide.md, 09-evaluation.md.
- 🔨 Refined 06-oes-spec.md: added Example section, QA flow, stricter JSON Schema (implementation_guide required, additionalProperties=false).
- 🧩 Added Task-Splitting workflow, state machine, human review gates, and extended JSON Schema in 06-oes-spec.md.
- 📝 Created templates/role-activation.md for AI role activation.

## 2025-07-05
- 🛠️ 实现 `scripts/lint-oes.mjs`：自动提取 JSON-Schema 并用 AJV 校验所有任务 JSON；彩色输出并集成 CI 失败退出码。
- 📦 在 tianting-v2 根目录添加 `package.json`，新增脚本 `npm run lint-oes`，锁定 `ajv@^8.12`。
- 📄 更新 10-retrospective.md：待办列表移除 lint-oes，动作项标记已完成，问题清单调整严重度。

## 2025-07-02
- ✅ demo-01 / demo-02 / demo-03 通过 Verification Pipeline v1：unit & compose stages，报告生成于 `delivery/report.md`。
- ✨ Verifier 新增 `unit` Stage 支持；compose 阶段在 demo-03 首次验证成功。
- ⚠️ 发现缺测试/缺依赖常见问题；已记录 Sprint-B 动作为：
  1. Verifier compose→Dockerfile/Testcontainers fallback + 端口自动探测。
  2. 新增 Stage：security(Trivy)、contract(Schemathesis)、coverage Gate。
  3. Prompt 模板强制交付 docker-compose.yml / Dockerfile。
  4. CI Workflow 切换至 `pnpm verify-all` 并上传 artefact。
  5. 清理 SQLAlchemy、Pydantic Deprecation 警告（代码升级至 2.x API）。

## Next Planned
- 实现 `scripts/lint-learning-schema.mjs` 校验学习助手输出 Schema。
- 实现 `scripts/build-knowledge-index.mjs`，生成 docs/knowledge/index.json 并接入 CI。
- Populate 07-testing-plan.md with concrete test cases & coverage reports.
- Add helm chart templates under `k8s/chart/` referenced by 08-deployment-guide.md.
- Define data collection pipeline scripts referenced in 09-evaluation.md.

- 🗂️ Documentation restructuring: added docs/index.md, simplified root README, moved docs/README pointer, added scripts/generate-doc-index.mjs.
- 📃 Added documentation & tooling workflow section to 00-roadmap.md (0.5).
- 🏷️ Inserted `status` metadata to 07-09 docs; created 10-retrospective.md skeleton.
- 🧪 Expanded 07-testing-plan.md with roles, entry/exit, deliverables, CI workflow, template, OES mapping; status → in_progress.
- 🚢 Expanded 08-deployment-guide.md with Helm chart skeleton, GitOps pipeline, security, scaling, backup; status → in_progress.
- 📈 Expanded 09-evaluation.md with monitoring dashboard, data pipeline, alert rules, A/B governance, reporting cadence, privacy; status → in_progress.
- 🗺️ Added Appendix B High-Level Orientation to 00-roadmap.md for newcomer quick overview.
- 🛠️ P1 consistency fixes: added quantitative NFR (MTTR, Error Rate) & FR→version mapping in 01; inserted architecture chart note & placeholder in 03; added $id & version fields to 06 schema + priority in example; aligned error rate metric in 07; noted Chart.yaml version in 08.
- 🔒 Added requires_human_review field to OES schema & example; new metric in 09; added FR-07 human review gating in 01.
- 📚 Added Learning Assistant feature: FR-08 in 01, section 5.8 in 05, learning_mode field in 06, new KPIs in 09.
- 📝 Added US-21 learning story; mapping tables; MemoryHub knowledge card storage strategy; CI learning schema step; sample knowledge card created.
- ✅ Sprint-0 retrospective added with action items; docs/index status updated to in_progress for 10.
- 🗂️ 新建 docs/11-glossary.md + README 链接，Samples 占位。
- 🛠️ 新脚本 `lint-doc-status.mjs` 校验文档状态标签。
- 🛠️ 新脚本 `build-knowledge-index.mjs` 扫描概念卡片生成 index.json。
- 📄 更新 05-detailed-design.md：插入 LearningOutput JSON Schema (comment tag)。
- 📄 更新 10-retrospective.md：标记 build-knowledge-index 完成。
- 🗓️ 记录 Sprint-1 Execution Plan（Dispatcher→Reporter 四步）到 10-retrospective.md。
- 🆕 生成 `tasks/demo` 目录与 3 张 OES 任务 + PLAN.md，用于生产线 Demo。
- 🚀 实现 Launcher (tmux+claude) & Harvester (pytest watcher) 脚本；新增 `launch`, `harvest` npm scripts.
- 📦 实现 Reporter：生成 delivery/report.md + workspace project.zip；新增 `report` npm script.
- ✅ Resolved: Launcher skips Claude trust prompt via `--dangerously-skip-permissions`; initial color mode may require manual selection (choose 4. Light mode). 
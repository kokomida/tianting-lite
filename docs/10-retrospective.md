<!-- status: draft -->
# 10 Retrospective & OKR Alignment (Sprint-0 Doc Freeze)

> Sprint 时间：2025-07-04 ~ 2025-07-05  
> 目标：文档 0–9 章节冻结 + 学习助手功能纳入规范

## 1. Sprint 目标完成度
| 目标 | 结果 | 备注 |
|------|------|------|
| 完成 0–9 文档骨架 | ✅ 已完成 | 所有章 `status` 进入 in_progress / done |
| 加入人工审核 Gate | ✅ FR-07 + Schema 字段 `requires_human_review` |
| 加入学习助手模式 | ✅ FR-08 + Learning Assistant 设计 |
| 文档一致性二轮审查 | ✅ 通过，无阻断性问题 |
| 生成首个知识卡片示例 | ✅ docs/knowledge/2025/07/04/acid.md |

## 2. 成就亮点
- 高层速览（附录 B）让新人上手 <3 min。
- OES Schema 版本化，支持向后兼容升级。
- 文档→测试→指标全链闭合，KPI 与 Alert 阈值一致。

## 3. 待改进事项
| 问题 | 严重度 | 动作 |
|------|--------|------|
| 03 架构图仍为 ASCII，占位未换 Mermaid | 中 | P2：用 Mermaid 重绘并放 assets |
| MemoryHub 索引自动生成脚本已接入 | 低 | 继续打通 CI & nightly cron |
| 文档 CI lint 已上线 (AJV, lint-oes) | 低 | 后续补充 learning-schema 校验 |

## 4. 改进行动 (Action Item)
| # | 行动 | Owner | 截止 |
|---|------|-------|------|
| 1 | Mermaid 架构图替换 | AI-FE | 07-07 |
| 2 | 知识卡片索引脚本 + CI | AI-BE | ✅ build-index 完成 07-05 |
| 3 | Implement `npm run test:lint-oes` & `test:lint-learning-schema` | AI-BE | ✅ 两脚本均完成 07-05，CI 集成待做 |
| 4 | Nightly Cron 定时 CI（记录，暂缓实现） | DevOps | P3 Backlog |

## 5. OKR 对齐
| Objective | KR | Status |
|-----------|----|--------|
| O: 建立可复制的文档→交付闭环 | KR1：0–9 章冻结 | Done |
| | KR2：新增学习助手设计 | Done |
| O: 提升个人学习效率 | KR1：概念卡片系统上线 | 50 % |

## 6. Handover Cheat-Sheet (For Next Dialogue)
| 项目状态 | 主要文件 | 说明 |
|-----------|----------|------|
| 文档冻结 | docs/00–10 | 已全部完善并通过三轮审核；查阅顺序建议：00→06→07→08→05.8 |
| 核心 Schema | docs/06-oes-spec.md | 版本 1.0.0，字段含 `requires_human_review` & `learning_mode` |
| 示例数据 | docs/knowledge/2025/07/04/acid.md | 概念卡片生成样例；用于验证学习助手流程 |
| 待办脚本 | scripts/generate-doc-index.mjs (已)；`lint-oes.mjs` (已)；`lint-learning-schema.mjs` (已)；`build-knowledge-index.mjs` (已) |

**下一步（Sprint-1）优先级**
1. 编写 AJV 校验脚本 `scripts/lint-oes.mjs` & `lint-learning-schema.mjs`，并在 GitHub Actions 集成。
2. 开发 `scripts/build-knowledge-index.mjs` 生成 docs/knowledge/index.json；更新 CI。
3. 选取真实需求（建议"小型 Flask Todo API"），生成 OES 任务卡，跑完整闭环 Demo。

> 下一段对话可直接切入「P1 任务 1：编写 lint-oes 脚本」。

---
> 下 Sprint（2025-07-06~07-10）目标：最小脚本实现（Schema 校验、任务闭环 Demo）、补 Mermaid 图 & 索引脚本。

## 7. Sprint-1 Execution Plan – Production Line MVP
| Step | 模块 | 目标 | 关键产物 |
|------|------|------|---------|
| 1 | Dispatcher | 一句话需求→Level-1 OES 自动拆票；新增 `max_parallel` | `src/dispatcher/autoPlan.mjs`, 单元测试 |
| 2 | Demo Tasks | 生成 Flask-Todo OES 任务 (API / tests / Dockerfile) | ✅ tasks/demo 完成 07-05 |
| 3 | Launcher & Harvester | 多窗口 ClaudeCode 执行；pytest/pylint 更新状态 | ✅ 脚本完成 07-05，已使用 `--dangerously-skip-permissions` 自动跳过权限；首次运行需手动选择颜色（推荐选 4. Light mode） |
| 4 | Reporter | 汇总 artefact & Markdown 报告闭环 | ✅ 脚本完成 07-05，待任务执行后生成 |

> 目标：07-10 前本地 `tianting plan/start` 全流程绿灯。

### 7.1 Sprint-1 Mini-Fix（2025-07-06）
| # | 主题 | 结果 | 影响 |
|---|------|------|------|
| 1 | Launcher 信任提示 | ✅ 使用 `--dangerously-skip-permissions` 一次性跳过"Do you trust the files in this folder?" | 生产线首次启动无需交互，可直接进入 Claude 对话 |
| 2 | Launcher 清理旧窗口 | ✅ 启动前自动 `tmux kill-window` (demo-*) | 避免窗口堆积、资源泄漏 |
| 3 | 颜色模式 | 🟡 首次仍需手动选择 `4. Light mode` & `y` 确认；随后 CLI 记忆配置，不再提示 | 不影响 CI；可评估后续读写 `~/.claude/config.json` 实现预设 |
| 4 | 自动发送系统提示 | ✅ 启动命令直接包含系统提示字符串，省去 `tmux send-keys` 键序 | 流程更稳定，简化维护 |

## 7.2 Sprint-B Preview – Verification Pipeline v2  <!-- status: todo -->
| # | Theme | Action | Owner | ETA |
|---|-------|--------|-------|-----|
| 1 | Verifier Fallback | 若 `compose` 文件缺失→自动 fallback 到 Dockerfile / Testcontainers；端口自动探测 | BE | 07-08 |
| 2 | Stage 扩展 | 新增 `security` (Trivy), `contract` (Schemathesis) & `coverage` Gate | QA/BE | 07-09 |
| 3 | Prompt 模板 | 系统提示明确交付物：Dockerfile 或 docker-compose.yml 必须存在 | PM | 07-07 |
| 4 | CI Workflow | GitHub Actions DAG：lint→unit→compose|dockerfile→security→report；上传 artefact | DevOps | 07-09 |
| 5 | Tech-Debt Cleanup | 升级 demo 代码：`sqlalchemy.orm.declarative_base()`、`model_dump()` 等消除 2.x 警告 | AI-BE | 07-10 |
| 6 | Docs & Tests | 补 Verification v2 设计文档 & 单元测试覆盖 fallback 路径 | Docs | 07-08 |

> 目标：Sprint-B 结束时，`tianting start` 在干净环境 0 配置即可通过完整 Pipeline；CI 全绿且无 Deprecation 警告。

---
> 下一段对话可直接切入「P1 任务 1：编写 lint-oes 脚本」。

---
> 下 Sprint（2025-07-06~07-10）目标：最小脚本实现（Schema 校验、任务闭环 Demo）、补 Mermaid 图 & 索引脚本。

## 7. Sprint-1 Execution Plan – Production Line MVP
| Step | 模块 | 目标 | 关键产物 |
|------|------|------|---------|
| 1 | Dispatcher | 一句话需求→Level-1 OES 自动拆票；新增 `max_parallel` | `src/dispatcher/autoPlan.mjs`, 单元测试 |
| 2 | Demo Tasks | 生成 Flask-Todo OES 任务 (API / tests / Dockerfile) | ✅ tasks/demo 完成 07-05 |
| 3 | Launcher & Harvester | 多窗口 ClaudeCode 执行；pytest/pylint 更新状态 | ✅ 脚本完成 07-05，已使用 `--dangerously-skip-permissions` 自动跳过权限；首次运行需手动选择颜色（推荐选 4. Light mode） |
| 4 | Reporter | 汇总 artefact & Markdown 报告闭环 | ✅ 脚本完成 07-05，待任务执行后生成 |

> 目标：07-10 前本地 `tianting plan/start` 全流程绿灯。

### 7.1 Sprint-1 Mini-Fix（2025-07-06）
| # | 主题 | 结果 | 影响 |
|---|------|------|------|
| 1 | Launcher 信任提示 | ✅ 使用 `--dangerously-skip-permissions` 一次性跳过"Do you trust the files in this folder?" | 生产线首次启动无需交互，可直接进入 Claude 对话 |
| 2 | Launcher 清理旧窗口 | ✅ 启动前自动 `tmux kill-window` (demo-*) | 避免窗口堆积、资源泄漏 |
| 3 | 颜色模式 | 🟡 首次仍需手动选择 `4. Light mode` & `y` 确认；随后 CLI 记忆配置，不再提示 | 不影响 CI；可评估后续读写 `~/.claude/config.json` 实现预设 |
| 4 | 自动发送系统提示 | ✅ 启动命令直接包含系统提示字符串，省去 `tmux send-keys` 键序 | 流程更稳定，简化维护 |

## 0. Sprint-A Completion Summary  <!-- status: done -->
| 项目里程碑 | 结果 |
|-----------|------|
| 最小生产线 MVP | Dispatcher → Launcher → Harvester → Verifier → Reporter 全链跑通，本地三张 demo 任务 `✅ verified` |
| 任务卡 & Schema | OES v1.1 (verification) 通过 lint-oes 校验；unit / compose Stage 实战验证 |
| 依赖缺口 | requests / sqlalchemy / httpx / pytest-cov 等已补；CI 将引入自动 pip-install 策略 |
| 代码仓库 | `kokomida/tianting-lite` 创建并推送；SSH 免密登录；官方 PromptX 以 **submodule** 形式接入 |
| 文档 | 新增 Verification v2 设计（05-detailed-design §5.8）、Sprint-B 计划（本章 §7.2）、Changelog 2025-07-02 |
| 下一步 | Sprint-B：Verifier fallback + Testcontainers、Security Stage、CI Workflow、Tech-Debt 清理 |

---
> 下一段对话可直接切入「P1 任务 1：编写 lint-oes 脚本」。

---
> 下 Sprint（2025-07-06~07-10）目标：最小脚本实现（Schema 校验、任务闭环 Demo）、补 Mermaid 图 & 索引脚本。

## 7. Sprint-1 Execution Plan – Production Line MVP
| Step | 模块 | 目标 | 关键产物 |
|------|------|------|---------|
| 1 | Dispatcher | 一句话需求→Level-1 OES 自动拆票；新增 `max_parallel` | `src/dispatcher/autoPlan.mjs`, 单元测试 |
| 2 | Demo Tasks | 生成 Flask-Todo OES 任务 (API / tests / Dockerfile) | ✅ tasks/demo 完成 07-05 |
| 3 | Launcher & Harvester | 多窗口 ClaudeCode 执行；pytest/pylint 更新状态 | ✅ 脚本完成 07-05，已使用 `--dangerously-skip-permissions` 自动跳过权限；首次运行需手动选择颜色（推荐选 4. Light mode） |
| 4 | Reporter | 汇总 artefact & Markdown 报告闭环 | ✅ 脚本完成 07-05，待任务执行后生成 |

> 目标：07-10 前本地 `tianting plan/start` 全流程绿灯。

### 7.1 Sprint-1 Mini-Fix（2025-07-06）
| # | 主题 | 结果 | 影响 |
|---|------|------|------|
| 1 | Launcher 信任提示 | ✅ 使用 `--dangerously-skip-permissions` 一次性跳过"Do you trust the files in this folder?" | 生产线首次启动无需交互，可直接进入 Claude 对话 |
| 2 | Launcher 清理旧窗口 | ✅ 启动前自动 `tmux kill-window` (demo-*) | 避免窗口堆积、资源泄漏 |
| 3 | 颜色模式 | 🟡 首次仍需手动选择 `4. Light mode` & `y` 确认；随后 CLI 记忆配置，不再提示 | 不影响 CI；可评估后续读写 `~/.claude/config.json` 实现预设 |
| 4 | 自动发送系统提示 | ✅ 启动命令直接包含系统提示字符串，省去 `tmux send-keys` 键序 | 流程更稳定，简化维护 | 
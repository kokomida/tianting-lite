# Tianting-v2 – Context & Engineering Guide

> 本文件作为 **LLM 上下文工程** 的单一真源，供所有 Claude 窗口加载，共享统一的项目背景与约束。修改后请在 PR 描述中注明 `update:CLAUDE.md`。

## 1. 项目简介
Tianting-v2 是一套「多 AI 协作交付」中枢，核心目标：
1. 输入一句需求 → 规划 → 并行编码 → 自动测试 → 生成报告。
2. 通过 MemoryHub 四层存储、OES 任务卡、CI Matrix 实现可观测与可回滚。

## 2. 目录速查
| 路径 | 作用 |
|------|------|
| `src/launcher/` | 启动与管理多 ClaudeCode 窗口 |
| `src/dispatcher/` | 任务规划与拆分 (OES) |
| `src/memoryhub/` | 记忆系统（RoaringBitmap + DAO） |
| `src/harvester/` | 收集测试 / LLM 日志 |
| `src/reporter/`  | 自动生成 `delivery/report.md` |
| `tasks/` | `*.task.json` 任务卡（OES）|
| `docs/`  | 0~10 章文档；`pitfalls.md` 记录踩坑 & 解决 |
| `.claude/` | hooks & 自动化脚本（见 §5） |

## 3. 协作流程 (EXPLORE → PLAN → CODE → COMMIT)
1. **EXPLORE**  阅读需求 / 资料；输出调研结论。
2. **PLAN**    O3 生成任务卡；ClaudeCode 先审计划、先写失败测试。
3. **CODE**    ClaudeCode 编码直至测试通过；遇坑写入 `docs/pitfalls.md`。
4. **COMMIT**  ClaudeCode 用 `gh` 起草 PR；O3 审计；人类最终 merge。

## 4. 上下文工程组成
```
┌─────────┐  tasks/*.json   ┌───────────┐
│ Roadmap │───────────────▶│ Dispatcher│
└─────────┘               └──────┬────┘
        MemoryHub.search_chunks() │
                                  ▼
                          ┌────────────┐
                          │ LLM Prompt │
                          └────────────┘
```
* **固定提示**：本文件 & 规范
* **动态上下文**：MemoryHub 相关代码 / 文档片段（检索注入）

## 5. Claude Code Hooks（试点）
Hooks 配置位于 `.claude/settings.json`：
* `PostToolUse` – 自动 `ruff --fix` 保证 Python 代码格式。
* `PreToolUse`  – 阻止修改 `tianting-v2/production/` 目录。

详见 `.claude/scripts/guard-prod-path.sh`。

## 6. 质量门控
| 阶段 | Gate |
|-------|------|
| Commit | 代码通过 `ruff`, `pytest -q`, 文档 lint |
| PR    | CI Matrix (Linux+Windows) all green, Benchmark ≤ 35 ms |
| Merge | 任务卡 `status` 更新 + `docs/index.md` 自动刷新 |

---
_Last updated: 2025-07-05_ 
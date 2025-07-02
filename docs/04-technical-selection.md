<!-- status: done -->
# 04. 技术选型与升级策略 (Technical Selection)

> 本章阐述 Tianting-Lite 的技术栈选择、替代方案评估、依赖升级与回滚策略，作为后续实现与运维的决策基线。

---

## 4.1 技术栈总览
| 层级 | 选型 | 版本 | 主要用途 | 替代方案 |
|------|------|------|----------|----------|
| 运行时 | Node.js | 18 LTS | Core modules, CLI | Bun 1.x (flag `FORCE_NODE=false`) |
| 运行时 | Python | 3.10 | Harvester, AutoGen | Python 3.12 (CI matrix) |
| AI API | OpenAI O3 | 2025-06 | LLM plan & review | Local LLM (Mistral 7B) |
| 多代理 | AutoGen | ^0.9 | Dispatcher orchestration | LangGraph, CrewAI |
| 编辑器 | ClaudeCode CLI | latest | Code generation windows | VSCode-AI extension |
| 数据库 | SQLite | 3.45 | Layer-2 tasks / stats | Postgres (prod) |
| 前端 GUI | Electron + React | 28 / 18 | Desktop UI | Tauri + Vite |
| 测试 | pytest / pylint | 7.x / 2.17 | Unit, Lint | nose2, ruff |
| 容器 | Docker | 25.x | Deploy & CI | Podman |
- | 组件 | 备选方案 | 选型 | 主要理由 |
| AI Explain LLM | GPT-4o | 2025-05 | Learning Assistant summaries | Claude 3 |

---

## 4.2 选型原则
1. **零配置即用**：首选可嵌入 / 无服务依赖的解决方案（SQLite, Electron）。
2. **生态成熟**：Node18 + React + pytest 社区庞大，文档与插件丰富。
3. **可替换**：每层保留至少 1 个兼容备选，并提供 Adapter/Plugin 机制。
4. **学习曲线可控**：避免小众框架；选择有官方 LTS 的版本。

---

## 4.3 依赖升级 & 回滚
| 工具 | 升级渠道 | 自动化 | 回滚策略 |
|------|----------|--------|-----------|
| npm / pnpm pkg | Renovate PR | ✅ | `changeset revert` + lockfile pin |
| Python pkg | Dependabot | ✅ | `pip-tools` compile ≈ lock |
| Docker base | GHCR watch | ✅ | Tag pin (`python:3.10-slim`) |
| LLM API | hand-controlled | ⛔ | env var `OPENAI_BASE_URL` 指向旧版本 |

自动化流程见 `.github/workflows/upgrade.yml`：
```yaml
schedule: weekly
jobs:
  renovate:
    steps:
      - uses: renovatebot/github-action@v39
  test:
    needs: renovate
    steps: [unit, e2e, docker-build]
  rollback:
    if: failure()
    steps:
      - name: Revert Lockfile
        run: changeset revert
```

---

## 4.4 fallback / adapter 机制
| 场景 | Trigger | Adapter | 详细说明 |
|------|---------|---------|----------|
| 本地无 GPU → 走云 O3 | `CUDA_VISIBLE_DEVICES=""` | `src/adapters/llm-remote.js` | 自动切换 REST endpoint |
| 无网或 API 限流 | HTTP 429 连续 3 次 | `llm-local.ts` | 使用 Mistral 7B gguf + llama.cpp |
| CLI-only 环境 | `NO_ELECTRON=1` | `ui-tui.ts` | 渲染 TUI 进度条替代 GUI |

---

## 4.5 依赖矩阵 (CI)
| Node | Bun | Python | OS |
|------|-----|--------|----|
| 18 LTS | 1.x | 3.10 | ubuntu-latest |
| 20 | — | 3.12 | windows-latest |
| — | — | — | macos-latest |

---

## 4.6 安全与合规
1. **SBOM 生成**：`syft` 自动输出 SPDX；随 Release 附带。  
2. **License Check**：`license-checker` 阻止 GPLv3 依赖进入 `main`。  
3. **隐私**：默认关闭任何遥测；OpenAI 日志仅存 task_id, cost。

---
> **版本记录**：tech-selection-init 2025-07-04 
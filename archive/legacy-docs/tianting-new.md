# 天庭系统蓝皮书 v0.1

> 记录日期：2025-06-30  
> 维护人：AI 产品经理 & 开发助理（PromptX + ClaudeCode）

---

## 0. 背景缘起
- 用户（你）倡导以中国神话/道家文化为意象，打造一个"一句话驱动"的 AI 协同开发平台——「天庭」。
- 天庭 = 调度中枢 + 多角色 AI 专家（PromptX 角色）+ 并行执行环境（Claude Code 多窗口）+ 混合记忆系统（四层存储）+ 人工审查（Human-in-the-Loop）。
- 目标：用户只需提出需求，其余流程由 AI 自动拆分、规划、并发执行，人类负责关键节点审核。

## 1. 需求分析（功能 & 非功能）
### 1.1 功能需求
1. 一句话需求接收与语义解析（玉帝中枢）。  
2. 串行规划流水线：产品经理 → 架构师 → OES 设计师。  
3. 原子任务分发与并行执行（天兵天将）。  
4. 混合记忆系统：记录需求、决策、人工反馈。  
5. 监控与可视化：任务状态、置信度、错误告警。  
6. 人工审查节点：低置信度自动进入人工队列。

### 1.2 非功能需求
- 启动 < 3 s；平均检索 < 1 ms；内存占用 ≤ 12 MB（核心层）。  
- 可插拔：PromptX 源码零修改，全部外部实现。  
- 扩展性：支持一次唤起 N 个 Claude Code 窗口。  
- 合规安全：输出前必须通过人工复核或置信度阈值。

## 2. 参考技术评估
| 框架/论文 | 关键价值 | 适配建议 |
|-----------|---------|---------|
| **Microsoft AutoGen** | 成熟多代理编排 & 事件驱动 | 用于天庭调度器，实现 Router-Agent + Worker-Agent |
| **Symbolic-MoE (2025)** | 技能级专家路由，16 专家 1 GPU | 借鉴"技能标签 + 批量路由"节省显存 |
| **Mixtral 8×7B** | 稀疏 MoE，高效推理 | 未来可替换 PromptX 基础模型，提高推理吞吐 |
| **ChatLaw** | MoE+多代理+SOP 减少幻觉 | 借鉴其双层 SOP，作为人类审查环节参考 |
| **Durable-Swarm** | 可恢复长任务，多代理持久化 | 结合混合记忆层存储事件日志，实现故障恢复 |

## 3. 混合记忆系统（PromptX Hybrid Memory v2.0）
```
Layer-1  XML-DPML   → 规则 / 角色元数据
Layer-2  SQLite     → 结构化记忆 / 索引查询
Layer-3  JSON       → 会话上下文 / 原子任务
Layer-4  知识图谱   → 语义关联 / 推理
```
- 三层加载策略：核心(39) / 应用(43) / 归档(28)。  
- 启动时间 ↓64.8%；内存 ↓75.3%。

## 4. 总体流程（文字版）
1. **需求入口**：`一句话` → `天庭·调度器`。  
2. **规划串行**：产品经理 → 架构师 → OES设计师（每步写记忆 & 人工签字）。  
3. **并行执行**：调度器批量启动 Claude Code 窗口（角色 = 天神），分配原子任务。  
4. **结果整合**：调度器收集 artefacts → 触发测试/部署脚本。  
5. **监控&记忆**：性能指标、错误、人工反馈持续写入混合记忆。  

## 5. 人工审核策略
| 等级 | 置信度区间 | 处理方式 |
|------|-----------|---------|
| A | ≥0.9 | 自动通过 |
| B | 0.6-0.9 | 抽样人工复核 |
| C | <0.6 | 必须人工确认并给出修改意见 |

## 6. 下一步 MVP 计划
1. **搭建调度器**：基于 AutoGen，先支持串行规划→人工审批。  
2. **集成 Claude Code**：CLI 多窗口调用 demo，验证并行执行能力。  
3. **接入混合记忆层**：用 JSON 栈快速落地核心+应用层。  
4. **指标监控**：Prometheus + Grafana；先关注启动/检索延迟。  
5. **用户验收**：跑通「宠物相册小程序」示例，完成串行+并行闭环。

## 7. 附录
- 关键词：MoE, AutoGen, Expert Routing, OES, MCP, Hybrid Memory, Claude Code.  
- 参考链接见第 2 节。  
- 任何修改请在 PR 中 @AI 助理。

---
*此文档持续更新，最新版本存放于 `tianting-new.md`*

## 8. v0.2 — Tianting-Lite 个人版实现蓝图（2025-07-02）

### 8.1 版本定位
面向"单开发者效率助手"，强调：PromptX 零修改、ClaudeCode 多窗口编码、O3 规划/评审、四层混合记忆本地化。暂不考虑公网部署与分布式。

### 8.2 模块划分
| 模块 | 主要职责 |
|------|----------|
| **Dispatcher** | 调用 O3 完成需求→OES 串行规划；写 Layer-3 会话 & Layer-2 任务表 |
| **Launcher** | 读取待执行任务，在 tmux/终端 多开 ClaudeCode 窗口并注入 prompt |
| **Harvester** | 监听 `workspace/<task_id>` 输出；运行 pytest/pylint；更新任务状态 |
| **Reporter** | 汇总 artefact，生成 README/压缩包；写 Layer-1 `logbook.dpml.xml` |
| **Memory Layer** | 1.XML 规则 2.SQLite 任务&窗口 3.JSONL 会话 4.(预留)Neo4j KG |

### 8.3 数据契约
```jsonc
// OES 单任务
{
  "task_id": "T20250702_001",
  "role": "backend-dev",
  "type": "CODE",           // CODE|DOC|REVIEW
  "object": "FlaskTodoAPI",
  "event": "create_crud_endpoints",
  "service": "ClaudeCode",
  "prompt": "使用 Flask 创建 /todos CRUD …",
  "accept_criteria": ["pytest 绿", "pylint≥8.5"]
}
```
• `oes_task.schema.json` 以 JSON Schema 定义，Dispatcher 强校验。

### 8.4 运行链路
1. 用户一句请求 → Dispatcher → O3 串行规划。
2. 规划结果写 Layer-3 会话，拆分为 OES JSON，入库(tasks)。
3. Launcher 多窗口 ClaudeCode 执行 CODE 任务。
4. Harvester 执行测试与准入标准，更新状态。
5. 所有任务 done → Reporter 输出交付物。

### 8.5 混合记忆接入
| 层 | 存储内容 | 说明 |
|----|----------|------|
| Layer-1 XML | 角色 & 流程规则 | 仅 39 条核心，启动即加载 |
| Layer-2 SQLite | tasks/windows/stats | 事务保障；可查询回滚 |
| Layer-3 JSONL | O3 & ClaudeCode 全对话 | 按日期文件；近期自动加载 |
| Layer-4 Neo4j | (留空) | 未来跨项目知识图 |

### 8.6 MVP 交付里程碑
Day1 内：Memory helper + Schema 校验 ✔︎  
Day2：Dispatcher → O3 串行规划可通过 ✔︎  
Day3：Launcher 多开窗口 demo ✔︎  
Day4：Harvester + 测试脚本 ✔︎  
Day5：Reporter 输出 artefact ✔︎  

---
> v0.2 维护人：AI 产品经理 & 开发助理（PromptX + ClaudeCode）

## 9. v0.3 — Tianting-Lite 个人高效开发机（2025-07-03）

> 再版说明：在充分收集用户反馈后，我们对 v0.2 进行全面重构：强调「零配置即用」、任务最短路径、可观察性，以及对非技术用户友好的输出格式。以下内容覆盖 v0.2 并作增补，v0.2 可作为对照历史保留。

### 9.1 核心价值主张（One-Sentence-Pitch）
"让任何个人开发者只需一句话，即可拥有一支随叫随到的 AI 工程团队。"

### 9.2 设计原则
1. **Zero-Config**：克隆仓库 → `pnpm install` → `tianting start`，一分钟内可用。
2. **Explainable AI**：所有规划与决策生成 Markdown 报告，普通人也能看得懂。
3. **Fail-Fast**：每个原子任务最长 15 min，超时自动拆分/降级。
4. **Observable**：Prometheus 默认采集 CPU/内存/任务时长；Grafana 即插即用。
5. **Modular**：五大模块松耦合，支持替换任一实现（如把 ClaudeCode 换成 VSCode-Dev-AI）。

### 9.3 总体架构（ASCII 示意）
```
┌────────┐   ①一句需求    ┌────────────┐ ②规划(O3)
│  User  ├────────────────►│ Dispatcher │────────────────┐
└────────┘                 └────────────┘                │
      ▲                         │③写 Memory              │
      │                         ▼                         │
      │                   ┌────────────┐④启动窗口         │
      │                   │  Launcher   ├──────────────┐  │
      │                   └────────────┘              │  │
      │                         │                     │  │
      │                     ⑤执行任务                │  │
      │                         ▼                     │  │
      │                   ┌────────────┐⑥测试&验证     │  │
      │                   │ Harvester  │──────────────┘  │
      │                   └────────────┘                 │
      │                         │⑦写 Memory             ▼
      │                         ▼                 ┌────────────┐
      │                   ┌────────────┐⑧汇总输出 ├───────────►│ Reporter   │
      │                   │  MemoryHub │──────────┘           └────────────┘
      │                   └────────────┘                       │⑨Markdown
      │                         ▲                               ▼
      └─────────────────────────┴───────────────────────────────┘
```

- **①** 用户自然语言输入
- **②** Dispatcher 调用 O3 串行规划
- **③** 规划结果写入 MemoryHub (SQLite + JSONL)
- **④** Launcher 打开 N 个 ClaudeCode 窗口
- **⑤** ClaudeCode 完成 CODE/DOC/REVIEW
- **⑥** Harvester 自动运行 pytest/pylint 等
- **⑦** 执行日志写 MemoryHub
- **⑧** 所有任务完成，Reporter 汇总 artefact
- **⑨** 输出 `delivery/report.md` + ZIP 交付包

### 9.4 模块清单 & 接口
| 模块 | 输入 | 处理 | 输出 | 依赖 |
|------|------|------|------|------|
| Dispatcher | 用户输入 | O3 规划、任务拆分 | OES JSON 任务表 | OpenAI/O3 API |
| Launcher | tasks.sqlite | spawn `claude-code` CLI | 任务窗口 PID | tmux / native shell |
| Harvester | workspace/* | pytest, pylint, coverage | task_status 更新 | Python3, pytest |
| Reporter | artefact/, tasks.sqlite | md-report 渲染 | delivery/report.md, zip | Pandoc |
| MemoryHub | 各模块日志 | 统一归档、查询 | SQLite + JSONL | sql.js, fs |

> Interface 采用 **EventBus（node-events）+ SQLite TRIGGER**，降低耦合。

### 9.5 配置示例 `config/tianting-lite.yaml`
```yaml
openai_api_key: sk-****
max_parallel_windows: 4
pytest_cmd: "pytest -q"
pylint_threshold: 8.5
report_template: templates/report.njk
```

### 9.6 数据契约更新
`oes_task.schema.json` 新增字段：
- `timeout_min`: 单任务超时时间
- `retry`: 失败自动重试次数

```jsonc
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OES Task",
  "type": "object",
  "required": ["task_id", "role", "type", "object", "event", "prompt"],
  "properties": {
    "task_id": {"type": "string"},
    "role": {"type": "string"},
    "type": {"enum": ["CODE", "DOC", "REVIEW"]},
    "object": {"type": "string"},
    "event": {"type": "string"},
    "prompt": {"type": "string"},
    "timeout_min": {"type": "integer", "default": 15},
    "retry": {"type": "integer", "default": 1},
    "accept_criteria": {"type": "array", "items": {"type": "string"}}
  }
}
```

### 9.7 开箱即用脚本
```bash
pnpm install        # 安装依赖
pnpm run dev        # 本地热重载
npx tianting plan "给我一个 FastAPI Todo Demo"  # 一句话规划
npx tianting start   # 并行执行 + 实时监控
```

### 9.8 MVP 里程碑（5 天冲刺）
| Day | 目标 | 可交付物 |
|-----|-----|---------|
| 1 | MemoryHub & Schema | `src/memory/` + 单元测试 |
| 2 | Dispatcher(O3) | `src/dispatcher/` + e2e 流程测试 |
| 3 | Launcher | `src/launcher/` + CLI demo |
| 4 | Harvester | `src/harvester/` + pytest/pylint 集成 |
| 5 | Reporter & Docs | `src/reporter/`, `delivery/report.md`, 更新 README |

### 9.9 风险 & 预案
1. **API 限流**：缓存规划结果；支持本地 LLM。
2. **窗口爆炸**：max_parallel_windows 动态调度；采用队列。
3. **测试依赖**：允许 task 定义 `requirements.txt`，Harvester 自动 `pip install -r`。 

### 9.10 术语表
- **O3**：OpenAI Orchestrator-3，引擎级规划接口。
- **OES**：Objective-Execution-Spec，可执行任务说明书。
- **Artefact**：生成的代码/文档/报告等交付物。
- **MemoryHub**：统一记忆存取中间件。

---
> *此再版由 AI 产品经理 2025-07-03 更新，若有疑问请在 Issue 中@我*

## 10. v0.4 — Tianting-Lite UI 设计提案（2025-07-04）

### 10.1 为什么需要 UI？
- **零学习成本**：普通用户害怕命令行，图形界面可降低使用门槛。
- **自然语言交互第一入口**：Chat 窗口让用户感觉 "像跟助手聊天"，不必记任何命令。
- **可视化监控**：任务进度条、日志流、Artefact 下载一目了然。

### 10.2 设计目标
1. **No-Server-Setup**：UI 与核心逻辑同进程启动，`tianting ui` 一键开启。
2. **跨平台 .exe**：Windows 用户双击可用；Mac/Linux 保持相同包。
3. **实时反馈**：自然语言输入后  <1s 看到规划结果；任务状态 WebSocket 持续推送。
4. **轻量**：打包后 < 60 MB；首次加载 < 2 s。

### 10.3 技术路线评估
| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| **Electron** | 打包成熟、社区生态大、API 丰富 | 体积大（>80 MB） | ✅ 首选（易落地） |
| **Tauri (Rust + WebView2)** | 体积小（<20 MB）、性能好 | Rust toolchain 学习成本 | ⏳ 备选（后续优化） |
| **PyInstaller + Gradio** | 上手快、纯 Python | 界面欠美观、定制有限 | ❌ 放弃 |
| **Web-only SPA (React/Vite)** | 纯前端、部署灵活 | 需用户启动浏览器，本地端口冲突 | ❌ 不符合双击.exe 诉求 |

> **决定**：v0.4 使用 Electron + React（Vite）实现桌面客户端，同时暴露 `yarn dev:web` 供浏览器访问。

### 10.4 功能原型（低保真）
```
┌───────────────────────────────────────────┐
│ Tianting-Lite v0.4                       │  ⟳ Settings ⚙
├───────────────────────────────────────────┤
│ Chat                                      │
│ > 一句话描述你的需求… [Send]              │
│-------------------------------------------│
│ ○ Dispatcher: 规划中…                     │
│ ● Launcher: 3/5 Windows Running           │
│ ○ Harvester: Tests Passing (12/15)        │
│ ● Reporter: Packaging artefacts…          │
│-------------------------------------------│
│ [▣] task_T20250704_001  ████▌ 75%         │
│   └ logs…                                   │
│-------------------------------------------│
│ Artefacts                                 │
│  - report.md   [Open] [Download]          │
│  - project.zip [Download]                 │
└───────────────────────────────────────────┘
```

### 10.5 架构拓扑
```
[Renderer(UI)] ↔  IPC  ↔ [Electron Main] ↔  Node EventBus ↔ Core Modules
                                   │
                                   └─ Socket.io Server (Task Stream)
```
- **Electron Main**：启动核心模块（Dispatcher/Launcher/...）。
- **Renderer**：React + ChakraUI；通过 IPC 调用 Main 侧 API。
- **Socket.io**：广播任务进度；Renderer 通过 WebSocket 订阅并刷新 UI。

### 10.6 API 设计示例
```ts
// preload.ts
contextBridge.exposeInMainWorld('tianting', {
  plan: (sentence) => ipcRenderer.invoke('plan', sentence),
  start: () => ipcRenderer.invoke('start'),
  onProgress: (cb) => ipcRenderer.on('progress', cb)
});
```

### 10.7 包结构新增
```
ui/
  ├─ public/
  ├─ src/
  │   ├─ components/
  │   ├─ pages/
  │   └─ main.tsx
  ├─ electron/
  │   ├─ main.ts
  │   └─ preload.ts
  ├─ vite.config.ts
  └─ package.json
```

### 10.8 打包 & 运行
```bash
pnpm run ui:dev      # 热更新 + 自动重启 Electron
pnpm run ui:pack     # electron-builder → dist/Tianting-Lite Setup.exe
```

### 10.9 迭代计划（MVP+2 天）
| Day | 目标 | 交付物 |
|-----|-----|--------|
| 6 | Electron 壳 + IPC 通道 | 可弹窗、输入一句话、返回 stub 规划 |
| 7 | 任务进度 Socket.io | 进度条实时刷新 |
| 8 | Artefact 列表 | 下载 report.md & zip |

### 10.10 风险 & 缓解
1. **Electron 体积超标** → 使用 `electron-builder --compression=maximum`，并剥离 devDeps。
2. **WebView2 依赖下载慢** → 离线安装包 & 镜像源。
3. **权限问题** → 采用签名证书；路径使用用户目录可写区。

---
> *v0.4 UI 提案由 AI 产品经理 2025-07-04 撰写，等待用户确认后排进冲刺计划。*

## 11. 核心问题解答与决策记录（2025-07-04）

### 11.1 远程部署下的子女娲克隆可行性
| 问题 | 结论 | 关键要点 |
|------|------|---------|
| 是否可以在云端 PromptX 实例通过 **MCP** 远程调用 `NuwaFactory.clone()`？ | **可以** | 1. MCP 本质是 RPC，对文件系统无感知；<br>2. 远程容器需**写**挂载卷或 Git/S3；<br>3. Tianting 侧只需 **读** 角色文件作为 ClaudeCode System Prompt。|
> 权限：确保云容器对角色目录有写权限；Tianting 不需写权限。

### 11.2 工具与依赖升级策略
1. **锁文件双份**：`pnpm-lock.yaml` (JS) + `poetry.lock/requirements.txt` (Py)。
2. **自动化 PR**：启用 Renovate/Dependabot → 打补丁、minor 自动；major 需人工审。
3. **CI 兼容矩阵**：Node 18 + Bun 最新 + Python 3.10/3.12，提前捕获破坏性变更。
4. **容器隔离**：PromptX、Memory MCP、ClaudeCode Runner 各自 Docker，降低冲突。
5. **双运行时 fallback**：`FORCE_NODE=true tianting start` 可切 Node；默认跑 Bun。

### 11.3 混合记忆系统：嵌入式 vs. MCP 微服务
| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|---------|
| 嵌入式库 | 零 RPC 延迟、部署简单 | 与主程序强耦合、升级需重打包 | 单机脚本、极致性能 |
| MCP 微服务 (推荐) | 高解耦、可跨机、Docker 滚动更新 | 多一次 HTTP 调用延迟 | Tianting-Lite & 将来云部署 |
> 先以**同机不同端口**运行的 MCP 形式落地；后迁云只需改部署。

### 11.4 版本管理 & 自动化发布
1. **Monorepo + Changesets**：所有 packages & Dockerfile 同仓库；PR 合并触发 `changeset version` → 自动 tag。
2. **GitHub Actions Release**：自动推 npm 包 + Docker 镜像；Tauri App 用 `tauri-updater` 拉增量补丁。
3. **自动回滚**：主干 CI 必跑 e2e；Release 若失败自动撤销。

### 11.5 开源组件升级监控
| 组件 | 升级通道 | 冲突检测 |
|------|---------|----------|
| PromptX | upstream git remote + Renovate | 单元 & e2e | 
| ClaudeCode CLI | brew/npm tag monitor | Launcher smoke-test |
| AutoGen/LangGraph | PyPI watch | Dispatcher unit-test |

---
> 本节将持续更新，用于跟踪关键决策与技术风险。

<!-- NOTE: AI 多专家评审设计已迁移至 docs/05-detailed-design.md -->

## 12. 近期进展速览（2025-07-05）

| 项目面 | 进展 | 位置 |
|---------|------|------|
| 文档冻结 | Sprint-0 完成，0–10 章进入 in_progress/done | docs/00–10 |
| 核心 Schema | `learning_mode`, `requires_human_review` 字段入 06 | docs/06-oes-spec.md |
| 校验脚本 | `lint-oes.mjs` 已完成，CI 强校验 | scripts/ |
| 术语表 | 新增 Glossary，集中管理缩写 | docs/11-glossary.md |
| 下一步 | lint-learning-schema, knowledge-index, Flask Todo Demo | 10-retrospective §6 |

> 本节每次 Sprint 结束后更新，供快速对齐。
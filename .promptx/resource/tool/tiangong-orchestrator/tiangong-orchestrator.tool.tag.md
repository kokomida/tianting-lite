<tool>
<purpose>
## 核心问题定义
为在Windows+WSL环境中同时运行的多个`Claude Code`实例（AI开发者），提供一个统一的、零Token消耗的本地项目管理办公室（PMO），解决并发任务的启动、监控、状态同步和关闭难题。

## 价值主张
- 🎯 **AI团队协作**: 将多个独立的`Claude Code`实例整合成一个协同工作的AI开发团队。
- 🚀 **零成本管理**: 编排器本身的所有操作（启动、监控、停止）均为本地系统命令，不产生任何API Token消耗。
- 🌟 **实时全局视野**: 在单一总控台中实时查看所有AI开发者的工作日志，告别多窗口切换的混乱。
- ⚙️ **持久化会话**: 任务状态通过本地会话文件管理，即使关闭总控台，也能随时恢复对任务的管理。

## 应用边界
- ✅ **适用场景**:
  - `Windows + WSL (Ubuntu)` 开发环境。
  - 需要同时启动和管理多个`Claude Code`实例。
  - 需要一个统一的界面来监控所有实例的实时输出。
- ❌ **不适用场景**:
  - 非WSL环境。
  - 单一`Claude Code`任务场景。
</purpose>

<usage>
## 使用时机
- 当您需要组建一个AI开发团队，让多个`Claude Code`实例并发工作时。
- 当您希望像管理一个项目团队一样，清晰地分配、监控和结束AI任务时。

## 完整操作流程

### 阶段1: 分配任务 (`tiangong:start`)
启动您的AI开发团队，并为每位成员分配初始任务。
```json
{
  "action": "tiangong:start",
  "logDir": "./tiangong-logs/project-alpha",
  "tasks": [
    {
      "name": "ai-developer-db",
      "command": "claude-code --task '设计数据库模式'",
      "workdir": "/home/user/project-alpha"
    },
    {
      "name": "ai-developer-api",
      "command": "claude-code --task '开发核心API'"
    }
  ]
}
```

### 阶段2: 开启项目看板 (`tiangong:monitor`)
启动您的"总控台"屏幕，实时查看所有AI开发者的工作进展。
```json
{
  "action": "tiangong:monitor",
  "logDir": "./tiangong-logs/project-alpha"
}
```
**注意**: 此命令会持续运行，实时输出日志。按`CTRL+C`可退出监控。

### 阶段3: 检查团队状态 (`tiangong:status`)
快速了解当前所有AI开发者的在岗情况。
```json
{
  "action": "tiangong:status",
  "logDir": "./tiangong-logs/project-alpha"
}
```

### 阶段4: 宣布项目收工 (`tiangong:stop`)
一键结束所有正在运行的AI开发者任务。
```json
{
  "action": "tiangong:stop",
  "logDir": "./tiangong-logs/project-alpha"
}
```

## 最佳实践
- 🎯 **项目隔离**: 为每个不同的项目使用独立的`logDir`，以保持会话和日志的清晰。
- 🎯 **开发者命名**: 为每个`Claude Code`实例赋予清晰、有意义的名称，如`backend-expert`, `frontend-specialist`。
</usage>

<parameter>
## 核心参数
| 参数名 | 类型 | 描述 |
|---|---|---|
| `action` | string | **必需。** 您要下达的指令。 |
| `logDir` | string | **必需。** 用于存放项目日志和会话文件的目录。 |
| `tasks` | array | 仅在`tiangong:start`时必需。定义了AI开发者的任务列表。 |
| `refreshInterval`| number | 可选。监控日志的刷新频率（毫秒），默认为1000。|

## `action`指令详解
- `tiangong:start`: 启动并分配任务。
- `tiangong:monitor`: 开启实时监控看板。
- `tiangong:status`: 检查所有任务的运行状态。
- `tiangong:stop`: 结束所有任务。

## `tasks`数组结构
每个任务对象定义了一位AI开发者的工作：
```json
{
  "name": "AI开发者的唯一代号",
  "command": "要ta执行的`claude-code`命令",
  "workdir": "（可选）在WSL中的工作目录" 
}
```
</parameter>

<outcome>
## 预期结果

### `tiangong:start` 成功响应
```json
{
  "success": true,
  "data": {
    "message": "成功启动 2 个任务。",
    "results": [
      { "name": "ai-developer-db", "status": "started", "pid": 12345 },
      { "name": "ai-developer-api", "status": "started", "pid": 12346 }
    ],
    "sessionFile": "./tiangong-logs/project-alpha/.tiangong-session.json"
  }
}
```

### `tiangong:status` 成功响应
```json
{
  "success": true,
  "data": {
    "tasks": [
      { "name": "ai-developer-db", "pid": 12345, "status": "running" },
      { "name": "ai-developer-api", "pid": 12346, "status": "stopped" }
    ]
  }
}
```

### 错误处理格式
```json
{
  "success": false,
  "error": {
    "code": "NO_SESSION",
    "message": "Session file not found. Have you started any tasks?"
  }
}
```
</outcome>
</tool> 
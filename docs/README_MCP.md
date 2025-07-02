# 神庭MCP集成系统

基于MCP (Model Context Protocol) 的多智能体任务编排系统原型实现。

## 🎯 核心优势
                                  
相比原有架构，MCP-First设计具有以下优势：

### 1. **简化架构**
- 去除了复杂的中间层（自建API网关、Redis集群等）
- 直接使用MCP协议进行工具调用
- Claude Code原生支持，无需额外集成工作

### 2. **标准化接口**
- 遵循MCP标准，具备良好的兼容性
- 工具定义清晰，易于扩展
- 支持资源访问和实时查询

### 3. **状态管理简化**
- MCP服务器自动处理会话状态
- 无需复杂的分布式状态同步
- 内存状态足够支撑原型阶段

## 🏗️ 架构设计

```
您 → Claude Code → 神庭MCP服务器 → 任务编排 & 角色管理
                    ↓
                PostgreSQL知识库 & PromptX角色库
```

## 🚀 快速开始

### 1. 安装依赖
```bash
cd /mnt/d/kokovsc/koko/Python/promptX+
python start_shenting.py --install
```

### 2. 测试MCP服务器
```bash
python start_shenting.py --test
```

### 3. 启动MCP服务器
```bash
python start_shenting.py --start
```

### 4. 配置Claude Desktop
将 `claude_desktop_config.json` 的内容添加到您的Claude Desktop配置中：

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

### 5. 重启Claude Desktop并测试

在Claude Desktop中尝试以下对话：
```
请帮我创建一个任务：实现用户认证功能
```

## 🛠️ 可用工具

### 任务管理
- `create_task`: 创建新任务
- `update_task`: 更新任务状态
- `get_task`: 获取任务详情
- `list_tasks`: 列出任务（可按状态过滤）

### 角色管理
- `add_role`: 添加新角色
- `list_roles`: 列出所有角色

### 系统监控
- `get_system_status`: 获取系统运行状态

## 📋 使用示例

### 创建任务工作流
```python
# 1. 创建战略任务
task_id = create_task(
    name="AI系统架构设计",
    description="设计分布式AI多智能体系统",
    assigned_role="taibai"
)

# 2. 分解为具体任务
sub_task = create_task(
    name="API接口设计", 
    description="设计MCP服务器接口",
    assigned_role="jumang"
)

# 3. 执行实现
update_task(sub_task, "running")
# ... 执行代码 ...
update_task(sub_task, "completed", result={"api_count": 7})
```

### 角色协作示例
```python
# 太白金星进行战略分析
taibai_analysis = call_role("taibai", {
    "task": "分析AI系统需求",
    "context": user_requirements
})

# 句芒分解任务
jumang_plan = call_role("jumang", {
    "strategy": taibai_analysis,
    "goal": "制定开发计划"
})

# 鲁班执行实现
luban_result = call_role("luban", {
    "plan": jumang_plan,
    "action": "代码实现"
})
```

## 🔄 与原架构对比

| 特性 | 原架构 | MCP架构 |
|------|--------|---------|
| 复杂度 | 高（多层中间件） | 低（直接MCP调用） |
| 部署难度 | 高（需Docker、Redis等） | 低（单一Python进程） |
| 扩展性 | 需要复杂配置 | 简单添加MCP工具 |
| 调试难度 | 高（分布式调试） | 低（单进程调试） |
| 开发速度 | 慢（需搭建基础设施） | 快（专注业务逻辑） |

## 🔮 未来扩展

### 阶段一：当前MCP原型 ✅
- 基本任务管理
- 角色定义和调用
- 系统状态监控

### 阶段二：知识库集成
- PostgreSQL MCP服务器
- 知识图谱查询工具
- PromptX角色模板管理

### 阶段三：高级编排
- 工作流引擎
- 并发任务处理
- 错误恢复机制

### 阶段四：生产就绪
- 持久化存储
- 分布式部署
- 监控告警

## 🤝 协作模式

使用这个MCP系统，您可以：

1. **直接对话**：告诉我您的需求，我会通过MCP工具创建任务
2. **任务跟踪**：随时查看任务进度和系统状态
3. **角色协作**：不同角色分工协作，各司其职
4. **知识沉淀**：任务结果自动存储，形成知识积累

## 📞 支持

如有问题，请查看：
1. 启动日志输出
2. MCP服务器错误信息
3. Claude Desktop连接状态

---

*神庭系统 - 让AI协作更简单* 🏛️
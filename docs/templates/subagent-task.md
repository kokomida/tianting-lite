<!-- status: done -->
# Subagent Task Prompt Template

> 引用：Anthropic Engineering – "How we built our multi-agent research system" (2025-06-13)

## 📌 任务设计四要素  
1. **Objective** – 明确子代理要解决的子问题，一句话内描述。  
2. **Tool Scope** – 列出允许调用的工具 / API（如 `web_search`, `repo_browse`）。  
3. **Output Format** – 规定 JSON / Markdown 结构，方便主代理解析。  
4. **Effort Budget** – 约束 token & 调用次数，防止过度探索。

```yaml
# 模板示例 (YAML 嵌入)
objective: "调研 2025 年最常用的向量数据库，并输出评分表"
tool_scope:
  - web_search
  - web_read
output_format: |
  ```json
  {
    "top_dbs": [
      {"name": "", "stars": 0, "reason": ""}
    ]
  }
  ```
effort_budget:
  max_tool_calls: 10
  max_tokens: 2000
```

## ✅ Prompt Skeleton
```text
You are a research sub-agent. Your task:
1. {{objective}}
2. Only use tools: {{tool_scope}}
3. Produce output EXACTLY in the following format:
{{output_format}}
4. Stay within {{effort_budget.max_tool_calls}} tool calls and {{effort_budget.max_tokens}} tokens.
```

## 经验法则（节选自 Anthropic 实践）
- **Think like your agents**：离线模拟并观察完整决策链，迭代 prompt。
- **Scale effort to complexity**：简单事实查找用 1 agent，复杂研究可 4–10 agents 并行。
- **End-state evaluation**：关注最终产物是否满足需求，而非逐步过程。
- **Observability**：全链路 tracing，每次工具调用都记录到 MemoryHub。

> 本模板将在 v0.4 引入的 Source-Collector 子系统中默认使用。 
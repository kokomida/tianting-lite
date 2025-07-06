<!-- status: in_progress -->
# 07a. AI 三方协作工作流 (Planner–Executor–PO)

1. 角色与责任  
   - planner-ai：任务拆分 / 设计评审 / 纠偏  
   - executor-ai：代码 & 文档实现  
   - human-po：业务目标、验收、Merge

2. 流程时序（Mermaid）  
   sequenceDiagram …

3. OES 任务卡映射  
   | role | task_type | required_stage | CI scope |

4. CI 工作流差分  
   - planner-ai 只跑 lint/schema  
   - executor-ai 跑 lint + pytest + compose

5. 落地计划  
   - T+0：新增 2 role tags & docs  
   - T+1：试点 core-02b / ci-01  
   - T+2：全面迁移

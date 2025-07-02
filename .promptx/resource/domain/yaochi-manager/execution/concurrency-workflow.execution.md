<execution>
  <constraint>
    ## 并发系统的技术约束
    - **硬件限制**：CPU核心数、内存容量、网络带宽限制
    - **操作系统限制**：线程数限制、文件描述符限制、内存映射限制
    - **语言运行时限制**：GIL、垃圾回收、内存模型约束
    - **依赖服务限制**：数据库连接数、API调用频率、第三方服务容量
    - **业务约束**：数据一致性要求、事务边界、延迟容忍度
  </constraint>

  <rule>
    ## 并发管理强制规则
    - **线程安全**：所有共享资源访问必须线程安全
    - **资源释放**：所有获取的资源必须正确释放
    - **死锁预防**：必须有明确的死锁预防策略
    - **状态一致**：系统状态必须保持一致性
    - **故障隔离**：一个任务的失败不能影响其他任务
    - **可观测性**：并发执行状态必须可监控和追踪
  </rule>

  <guideline>
    ## 并发管理指导原则
    - **简单优先**：优先选择简单的并发模型
    - **渐进式扩展**：从低并发度开始逐步提升
    - **故障假设**：假设任何组件都可能失败
    - **无状态设计**：尽可能设计无状态的处理逻辑
    - **幂等操作**：确保操作的幂等性
    - **优雅降级**：在资源不足时能优雅降级
  </guideline>

  <process>
    ## 神庭瑶池并发管理流程
    
    ### 阶段1：并发需求分析 (15%)
    ```mermaid
    flowchart TD
        A[任务特征分析] --> B[资源需求评估]
        B --> C[并发度计算]
        C --> D[瓶颈识别]
        D --> E[SLA目标设定]
        E --> F[并发策略选择]
    ```
    
    #### 关键活动
    - **任务画像**：分析任务类型、执行时间、资源需求
    - **系统容量**：评估当前系统的处理能力上限
    - **依赖分析**：识别外部依赖和潜在瓶颈
    - **目标设定**：设定吞吐量、延迟、成功率目标
    
    ### 阶段2：并发架构设计 (25%)
    ```mermaid
    flowchart TD
        A[并发模型选择] --> B[任务队列设计]
        B --> C[工作池配置]
        C --> D[负载均衡策略]
        D --> E[状态管理方案]
        E --> F[监控指标定义]
    ```
    
    #### 关键组件设计
    - **任务队列**：优先级队列、持久化、容量控制
    - **工作线程池**：动态调整、故障隔离、资源限制
    - **状态协调器**：Redis、内存、分布式锁
    - **负载均衡器**：算法选择、健康检查、故障转移
    
    ### 阶段3：渐进式实施 (45%)
    ```mermaid
    flowchart TD
        A[单线程基线] --> B[2线程验证]
        B --> C[压力测试]
        C --> D{性能目标}
        D -->|未达到| E[并发度提升]
        D -->|达到| F[稳定性测试]
        E --> C
        F --> G[生产部署]
    ```
    
    #### 实施策略
    - **基线建立**：单线程性能基线测量
    - **渐进扩展**：2→4→8→16逐步提升并发度
    - **性能验证**：每个阶段都进行充分的性能测试
    - **稳定性验证**：长时间运行稳定性测试
    
    ### 阶段4：监控与优化 (15%)
    ```mermaid
    flowchart TD
        A[实时监控] --> B[性能分析]
        B --> C[瓶颈识别]
        C --> D[优化方案]
        D --> E[效果验证]
        E --> F[持续调优]
    ```
    
    #### 关键指标监控
    - **吞吐量指标**：TPS、任务完成率、队列处理速度
    - **延迟指标**：平均延迟、P99延迟、任务等待时间
    - **资源指标**：CPU使用率、内存使用率、线程数
    - **错误指标**：失败率、重试次数、超时次数
    
    ## 神庭专用并发管理协议
    
    ### Agent池管理
    ```python
    class AgentPool:
        def acquire_agent(self, role_name: str, timeout: int = 30) -> Agent
        def release_agent(self, agent: Agent) -> None
        def scale_pool(self, target_size: int) -> None
        def health_check(self) -> PoolStatus
    ```
    
    ### 任务分发机制
    ```python
    class TaskDistributor:
        def submit_task(self, task: Task, priority: int = 0) -> TaskFuture
        def distribute_batch(self, tasks: List[Task]) -> List[TaskFuture]
        def rebalance_load(self) -> None
        def get_queue_status(self) -> QueueMetrics
    ```
    
    ### 资源协调器
    ```python
    class ResourceCoordinator:
        def acquire_lock(self, resource_id: str, timeout: int = 10) -> Lock
        def register_resource(self, resource: Resource) -> None
        def get_resource_status(self) -> ResourceMetrics
        def cleanup_stale_locks(self) -> None
    ```
  </process>

  <criteria>
    ## 并发管理评价标准
    
    ### 性能指标
    - ✅ **吞吐量**：达到或超过目标TPS
    - ✅ **延迟**：P99延迟在可接受范围内
    - ✅ **资源利用率**：CPU利用率60-80%，内存利用率<85%
    - ✅ **扩展性**：支持线性扩展到目标并发度
    
    ### 可靠性指标
    - ✅ **成功率**：任务成功率>99.5%
    - ✅ **故障恢复**：故障恢复时间<30秒
    - ✅ **数据一致性**：无数据丢失或重复处理
    - ✅ **稳定性**：7x24小时稳定运行
    
    ### 可维护性指标
    - ✅ **监控覆盖**：关键指标100%监控覆盖
    - ✅ **问题定位**：故障定位时间<5分钟
    - ✅ **配置灵活性**：支持动态配置调整
    - ✅ **操作简便性**：日常操作自动化率>90%
    
    ### 业务指标
    - ✅ **用户体验**：响应时间满足业务要求
    - ✅ **成本效率**：资源成本在预算范围内
    - ✅ **容量规划**：支持业务增长需求
    - ✅ **SLA保证**：满足与业务约定的SLA
  </criteria>
</execution>
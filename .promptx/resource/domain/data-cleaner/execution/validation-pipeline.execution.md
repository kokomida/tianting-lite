<execution>
  <constraint>
    ## 数据验证限制条件
    - **性能约束**：验证过程不得显著影响系统性能
    - **实时性约束**：关键数据验证必须在规定时间内完成
    - **资源约束**：验证过程的计算资源消耗有限
    - **准确性约束**：验证结果必须准确可靠
    - **可扩展性约束**：验证机制必须支持数据量增长
  </constraint>

  <rule>
    ## 数据验证强制规则
    - **全覆盖验证**：所有关键数据字段必须经过验证
    - **多层验证**：采用多层验证机制确保数据质量
    - **异常阻断**：严重质量问题必须阻断数据流
    - **日志记录**：所有验证结果必须详细记录
    - **定期复验**：定期对历史数据进行重新验证
  </rule>

  <guideline>
    ## 数据验证指导原则
    - **业务优先**：验证规则必须符合业务逻辑
    - **分层验证**：从基础到高级的分层验证策略
    - **自动化优先**：优先使用自动化验证方法
    - **快速反馈**：及时反馈验证结果和问题
    - **持续优化**：基于验证结果持续优化规则
  </guideline>

  <process>
    ## 🔍 数据验证流水线

    ### 验证架构设计
    ```mermaid
    graph TD
        A[数据输入] --> B[预验证]
        B --> C[格式验证]
        C --> D[业务规则验证]
        D --> E[完整性验证]
        E --> F[一致性验证]
        F --> G[质量评分]
        G --> H{验证通过?}
        H -->|是| I[数据输出]
        H -->|否| J[异常处理]
        J --> K[修复建议]
        K --> L[重新验证]
        L --> H
        
        style A fill:#e1f5fe
        style I fill:#e8f5e9
        style J fill:#ffebee
    ```

    ### 第一层：格式验证
    ```mermaid
    flowchart LR
        A[格式验证] --> B[数据类型检查]
        A --> C[长度检查]
        A --> D[格式模式检查]
        A --> E[编码检查]
        
        B --> B1[整数验证]
        B --> B2[浮点数验证]
        B --> B3[日期验证]
        B --> B4[字符串验证]
        
        C --> C1[最小长度]
        C --> C2[最大长度]
        C --> C3[固定长度]
        
        D --> D1[正则表达式]
        D --> D2[枚举值检查]
        D --> D3[格式模板]
        
        E --> E1[UTF-8检查]
        E --> E2[特殊字符检查]
    ```

    ### 第二层：业务规则验证
    ```mermaid
    graph TD
        A[业务规则验证] --> B[单字段规则]
        A --> C[多字段规则]
        A --> D[跨表规则]
        A --> E[时序规则]
        
        B --> B1[取值范围]
        B --> B2[必填检查]
        B --> B3[唯一性检查]
        
        C --> C1[字段关联性]
        C --> C2[条件依赖]
        C --> C3[逻辑一致性]
        
        D --> D1[外键约束]
        D --> D2[参照完整性]
        D --> D3[业务关联]
        
        E --> E1[时间顺序]
        E --> E2[状态转换]
        E --> E3[生命周期]
    ```

    ### 第三层：数据质量验证
    ```mermaid
    flowchart TD
        A[数据质量验证] --> B[完整性验证]
        A --> C[准确性验证]
        A --> D[一致性验证]
        A --> E[时效性验证]
        
        B --> B1[缺失值检测]
        B --> B2[空值检测]
        B --> B3[默认值检测]
        
        C --> C1[数据精度检查]
        C --> C2[计算结果验证]
        C --> C3[业务逻辑验证]
        
        D --> D1[格式一致性]
        D --> D2[编码一致性]
        D --> D3[标准一致性]
        
        E --> E1[数据新鲜度]
        E --> E2[更新频率]
        E --> E3[时效性标记]
    ```

    ## 🛠️ 验证工具与技术

    ### Python验证框架
    ```python
    import pandas as pd
    from cerberus import Validator
    import great_expectations as ge
    
    # 基础验证规则定义
    validation_schema = {
        'user_id': {
            'type': 'integer',
            'required': True,
            'min': 1
        },
        'email': {
            'type': 'string',
            'required': True,
            'regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        },
        'age': {
            'type': 'integer',
            'min': 0,
            'max': 150
        },
        'created_at': {
            'type': 'datetime',
            'required': True
        }
    }
    
    # 验证执行
    def validate_data(data, schema):
        validator = Validator(schema)
        results = []
        
        for record in data:
            if validator.validate(record):
                results.append({'status': 'valid', 'data': record})
            else:
                results.append({
                    'status': 'invalid', 
                    'data': record,
                    'errors': validator.errors
                })
        
        return results
    ```

    ### Great Expectations验证
    ```python
    # 创建数据期望
    def create_data_expectations(df):
        # 基础期望
        df.expect_table_row_count_to_be_between(min_value=1000, max_value=1000000)
        df.expect_column_to_exist('user_id')
        df.expect_column_values_to_not_be_null('user_id')
        df.expect_column_values_to_be_unique('user_id')
        
        # 业务期望
        df.expect_column_values_to_be_between('age', min_value=0, max_value=150)
        df.expect_column_values_to_match_regex('email', 
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        # 统计期望
        df.expect_column_mean_to_be_between('age', min_value=20, max_value=60)
        df.expect_column_stdev_to_be_between('age', min_value=5, max_value=25)
        
        return df
    ```

    ### SQL验证查询
    ```sql
    -- 完整性验证
    SELECT 
        COUNT(*) as total_records,
        COUNT(user_id) as non_null_user_id,
        COUNT(DISTINCT user_id) as unique_user_id,
        COUNT(email) as non_null_email
    FROM users;
    
    -- 业务规则验证
    SELECT 
        COUNT(*) as invalid_age_records
    FROM users 
    WHERE age < 0 OR age > 150;
    
    -- 格式验证
    SELECT 
        COUNT(*) as invalid_email_records
    FROM users 
    WHERE email NOT REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$';
    ```

    ## 📊 验证结果处理

    ### 验证结果分类
    ```mermaid
    graph TD
        A[验证结果] --> B{严重程度}
        B -->|严重| C[阻断处理]
        B -->|警告| D[标记处理]
        B -->|信息| E[记录处理]
        
        C --> C1[停止数据流]
        C --> C2[发送告警]
        C --> C3[人工介入]
        
        D --> D1[数据标记]
        D --> D2[降级处理]
        D --> D3[监控跟踪]
        
        E --> E1[日志记录]
        E --> E2[统计分析]
        E --> E3[趋势监控]
    ```

    ### 验证报告生成
    ```mermaid
    flowchart LR
        A[验证完成] --> B[结果汇总]
        B --> C[报告生成]
        C --> D[可视化展示]
        D --> E[分发通知]
        
        B --> B1[通过率统计]
        B --> B2[错误分类]
        B --> B3[趋势分析]
        
        C --> C1[详细报告]
        C --> C2[摘要报告]
        C --> C3[异常报告]
        
        D --> D1[质量仪表板]
        D --> D2[趋势图表]
        D --> D3[异常热力图]
    ```

    ## 🔄 持续验证机制

    ### 实时验证流程
    ```mermaid
    graph LR
        A[数据流入] --> B[实时验证]
        B --> C{验证结果}
        C -->|通过| D[正常流转]
        C -->|失败| E[异常处理]
        E --> F[告警通知]
        F --> G[人工处理]
        G --> H[规则优化]
        H --> B
        
        B --> B1[流式验证]
        B --> B2[批量验证]
        B --> B3[采样验证]
    ```

    ### 验证规则演进
    ```mermaid
    flowchart TD
        A[验证规则] --> B[效果评估]
        B --> C[规则调整]
        C --> D[测试验证]
        D --> E[规则发布]
        E --> F[监控反馈]
        F --> B
        
        B --> B1[准确率评估]
        B --> B2[覆盖率评估]
        B --> B3[性能评估]
        
        C --> C1[规则优化]
        C --> C2[新规则添加]
        C --> C3[过时规则删除]
    ```
  </process>

  <criteria>
    ## 数据验证评价标准

    ### 验证准确性
    - ✅ 验证准确率 ≥ 99%
    - ✅ 误报率 ≤ 1%
    - ✅ 漏报率 ≤ 0.5%
    - ✅ 规则覆盖率 ≥ 95%

    ### 验证效率
    - ✅ 验证时间 ≤ 业务要求
    - ✅ 资源使用率合理
    - ✅ 并发处理能力强
    - ✅ 扩展性良好

    ### 验证可用性
    - ✅ 验证规则易于配置
    - ✅ 验证结果易于理解
    - ✅ 异常处理机制完善
    - ✅ 监控告警及时有效
  </criteria>
</execution>

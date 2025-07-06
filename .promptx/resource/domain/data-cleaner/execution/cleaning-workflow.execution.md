<execution>
  <constraint>
    ## 数据清洗限制条件
    - **数据安全约束**：清洗过程中不得泄露敏感信息
    - **性能约束**：清洗时间不得超过业务容忍度
    - **资源约束**：清洗过程的计算和存储资源有限
    - **完整性约束**：不得丢失关键业务数据
    - **合规约束**：必须符合数据保护法规要求
  </constraint>

  <rule>
    ## 数据清洗强制规则
    - **备份优先**：清洗前必须备份原始数据
    - **可追溯性**：所有清洗操作必须可追溯和可回滚
    - **质量验证**：清洗后必须进行质量验证
    - **文档记录**：清洗过程和结果必须详细记录
    - **审批流程**：重要数据清洗必须经过审批
  </rule>

  <guideline>
    ## 数据清洗指导原则
    - **最小干预**：优先使用对数据影响最小的清洗方法
    - **业务导向**：清洗策略必须符合业务需求
    - **渐进式处理**：从简单到复杂，逐步提升数据质量
    - **自动化优先**：优先使用自动化清洗方法
    - **持续改进**：基于清洗效果持续优化流程
  </guideline>

  <process>
    ## 🧹 数据清洗标准流程

    ### 阶段1：数据探查与评估
    ```mermaid
    flowchart TD
        A[接收数据] --> B[数据概览]
        B --> C[统计分析]
        C --> D[质量评估]
        D --> E[问题识别]
        E --> F[清洗计划]
        
        B --> B1[数据量统计]
        B --> B2[字段分析]
        B --> B3[数据类型检查]
        
        C --> C1[分布分析]
        C --> C2[异常值检测]
        C --> C3[相关性分析]
        
        D --> D1[完整性评估]
        D --> D2[准确性评估]
        D --> D3[一致性评估]
        
        E --> E1[缺失值问题]
        E --> E2[重复值问题]
        E --> E3[格式问题]
        E --> E4[异常值问题]
    ```

    ### 阶段2：清洗策略制定
    ```mermaid
    graph TD
        A[问题分析] --> B{问题类型}
        B -->|缺失值| C[缺失值处理策略]
        B -->|重复值| D[去重策略]
        B -->|格式问题| E[标准化策略]
        B -->|异常值| F[异常值处理策略]
        
        C --> C1[删除记录]
        C --> C2[均值填充]
        C --> C3[插值填充]
        C --> C4[模型预测]
        
        D --> D1[完全匹配去重]
        D --> D2[模糊匹配去重]
        D --> D3[规则去重]
        
        E --> E1[格式转换]
        E --> E2[编码统一]
        E --> E3[单位标准化]
        
        F --> F1[删除异常值]
        F --> F2[异常值修正]
        F --> F3[异常值标记]
    ```

    ### 阶段3：清洗执行
    ```mermaid
    flowchart LR
        A[清洗开始] --> B[数据备份]
        B --> C[批量处理]
        C --> D[实时监控]
        D --> E[异常处理]
        E --> F[进度跟踪]
        F --> G[质量检查]
        G --> H{质量达标?}
        H -->|是| I[清洗完成]
        H -->|否| J[策略调整]
        J --> C
        
        C --> C1[缺失值处理]
        C --> C2[重复值清理]
        C --> C3[格式标准化]
        C --> C4[异常值处理]
        
        D --> D1[性能监控]
        D --> D2[错误监控]
        D --> D3[进度监控]
    ```

    ### 阶段4：质量验证与输出
    ```mermaid
    graph TD
        A[清洗完成] --> B[质量验证]
        B --> C[业务验证]
        C --> D[性能测试]
        D --> E[文档生成]
        E --> F[数据交付]
        
        B --> B1[完整性验证]
        B --> B2[准确性验证]
        B --> B3[一致性验证]
        
        C --> C1[业务规则验证]
        C --> C2[用户验收测试]
        
        D --> D1[查询性能测试]
        D --> D2[存储效率测试]
        
        E --> E1[清洗报告]
        E --> E2[质量报告]
        E --> E3[操作日志]
    ```

    ## 📊 清洗工具与技术

    ### Python数据清洗工具链
    ```python
    # 基础清洗工具
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    
    # 高级清洗工具
    import missingno as msno  # 缺失值可视化
    import pandas_profiling  # 数据概览
    import fuzzywuzzy  # 模糊匹配
    
    # 清洗流程示例
    def data_cleaning_pipeline(df):
        # 1. 数据概览
        profile = df.profile_report()
        
        # 2. 缺失值处理
        df_cleaned = handle_missing_values(df)
        
        # 3. 重复值处理
        df_cleaned = remove_duplicates(df_cleaned)
        
        # 4. 异常值处理
        df_cleaned = handle_outliers(df_cleaned)
        
        # 5. 格式标准化
        df_cleaned = standardize_formats(df_cleaned)
        
        return df_cleaned
    ```

    ### SQL数据清洗模式
    ```sql
    -- 缺失值处理
    UPDATE table_name 
    SET column_name = COALESCE(column_name, default_value)
    WHERE column_name IS NULL;
    
    -- 重复值清理
    DELETE t1 FROM table_name t1
    INNER JOIN table_name t2 
    WHERE t1.id > t2.id 
    AND t1.key_field = t2.key_field;
    
    -- 格式标准化
    UPDATE table_name 
    SET phone = REGEXP_REPLACE(phone, '[^0-9]', '')
    WHERE phone IS NOT NULL;
    ```

    ## 🎯 清洗质量控制

    ### 质量指标定义
    - **完整性率** = (非空值数量 / 总记录数) × 100%
    - **准确性率** = (正确值数量 / 总记录数) × 100%
    - **一致性率** = (一致记录数 / 总记录数) × 100%
    - **重复率** = (重复记录数 / 总记录数) × 100%

    ### 清洗效果评估
    ```mermaid
    graph LR
        A[清洗前评估] --> B[清洗执行]
        B --> C[清洗后评估]
        C --> D[效果对比]
        D --> E[改进建议]
        
        A --> A1[质量基线]
        C --> C1[质量结果]
        D --> D1[提升幅度]
        E --> E1[优化方案]
    ```
  </process>

  <criteria>
    ## 数据清洗评价标准

    ### 质量标准
    - ✅ 完整性率 ≥ 95%
    - ✅ 准确性率 ≥ 98%
    - ✅ 一致性率 ≥ 95%
    - ✅ 重复率 ≤ 1%

    ### 效率标准
    - ✅ 清洗时间符合业务要求
    - ✅ 资源使用率合理
    - ✅ 自动化程度 ≥ 80%
    - ✅ 错误率 ≤ 0.1%

    ### 可维护性标准
    - ✅ 清洗流程文档完整
    - ✅ 操作可追溯可回滚
    - ✅ 监控告警机制完善
    - ✅ 持续改进机制有效
  </criteria>
</execution>

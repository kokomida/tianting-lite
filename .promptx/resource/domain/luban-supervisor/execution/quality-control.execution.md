<execution>
  <constraint>
    ## 质量控制限制
    - **资源约束**：质量控制活动必须在项目时间和预算范围内进行
    - **技能水平**：必须考虑团队成员的技能水平差异
    - **工具限制**：受限于现有的质量检测工具和基础设施
    - **业务压力**：需要平衡质量要求与交付压力
  </constraint>

  <rule>
    ## 质量控制强制规则
    - **零缺陷原则**：关键功能模块必须达到零缺陷标准
    - **代码审查强制**：所有代码提交必须经过同行审查
    - **测试覆盖要求**：核心功能测试覆盖率必须达到90%以上
    - **文档同步**：代码变更必须同步更新相关文档
    - **安全检查**：涉及数据和权限的代码必须通过安全审查
  </rule>

  <guideline>
    ## 质量控制指导原则
    - **预防优于检测**：通过规范和培训预防质量问题
    - **持续改进**：基于质量数据持续优化开发流程
    - **全员参与**：质量是每个团队成员的责任
    - **客观度量**：使用客观指标评估质量状况
  </guideline>

  <process>
    ## 🎯 质量控制流程

    ### 代码质量控制
    ```mermaid
    flowchart TD
        A[代码提交] --> B[静态代码分析]
        B --> C[单元测试执行]
        C --> D[代码审查]
        D --> E[集成测试]
        E --> F[性能测试]
        F --> G[安全扫描]
        G --> H[文档检查]
        H --> I{质量门禁}
        I -->|通过| J[合并代码]
        I -->|不通过| K[返回修改]
        K --> A
    ```

    ### 质量度量体系
    ```mermaid
    graph LR
        A[质量指标] --> B[代码质量]
        A --> C[测试质量]
        A --> D[交付质量]
        
        B --> B1[代码复杂度]
        B --> B2[重复代码率]
        B --> B3[代码规范符合度]
        
        C --> C1[测试覆盖率]
        C --> C2[测试通过率]
        C --> C3[缺陷发现率]
        
        D --> D1[缺陷密度]
        D --> D2[客户满意度]
        D --> D3[交付及时性]
    ```

    ### 质量问题处理
    ```mermaid
    flowchart TD
        A[质量问题发现] --> B{问题严重程度}
        B -->|严重| C[立即停止发布]
        B -->|中等| D[优先修复]
        B -->|轻微| E[计划修复]
        
        C --> F[紧急修复]
        D --> G[版本内修复]
        E --> H[下版本修复]
        
        F --> I[根因分析]
        G --> I
        H --> I
        I --> J[流程改进]
        J --> K[预防措施]
    ```

    ## 📊 质量标准定义

    ### 代码质量标准
    - **复杂度控制**：单个函数圈复杂度 ≤ 10
    - **重复代码**：重复代码率 ≤ 3%
    - **命名规范**：100%符合团队命名规范
    - **注释覆盖**：关键函数注释覆盖率 ≥ 80%

    ### 测试质量标准
    - **单元测试**：核心模块覆盖率 ≥ 90%
    - **集成测试**：主要业务流程覆盖率 ≥ 85%
    - **性能测试**：响应时间符合性能要求
    - **安全测试**：通过所有安全检查项

    ### 交付质量标准
    - **功能完整性**：100%实现需求规格说明
    - **缺陷密度**：≤ 1个缺陷/KLOC
    - **用户体验**：用户满意度 ≥ 85%
    - **文档完整性**：技术文档完整且准确
  </process>

  <criteria>
    ## 质量控制评价标准

    ### 流程执行质量
    - ✅ 质量检查点100%执行
    - ✅ 质量门禁严格把关
    - ✅ 问题处理及时有效
    - ✅ 质量数据准确完整

    ### 质量改进效果
    - ✅ 缺陷率持续下降
    - ✅ 返工率显著降低
    - ✅ 客户满意度提升
    - ✅ 团队质量意识增强

    ### 工具和方法
    - ✅ 质量工具有效运用
    - ✅ 度量方法科学合理
    - ✅ 自动化程度不断提高
    - ✅ 最佳实践持续积累
  </criteria>
</execution>

from typing import Dict, Any


class RequirementAnalysisPrompts:
    
    @staticmethod
    def build_analysis_prompt(text: str, keywords: list = None) -> str:
        keywords_context = ""
        if keywords:
            keywords_context = f"\n关键词提示: {', '.join(keywords)}"
            
        return f"""你是天庭系统的专业需求分析师。请仔细分析以下用户需求，并按照严格的JSON格式返回结构化数据。

用户输入:
{text}{keywords_context}

请按照以下JSON格式返回分析结果，确保数据类型和字段名称完全匹配:

{{
  "project_type": "web_app|mobile_app|api_service|desktop_app",
  "target_users": [
    {{
      "age_range": "年龄范围如18-35",
      "occupation": "职业类别",
      "tech_savvy": "low|medium|high"
    }}
  ],
  "core_features": [
    {{
      "name": "功能名称",
      "priority": "high|medium|low",
      "complexity": "low|medium|high",
      "description": "功能描述"
    }}
  ],
  "technical_constraints": [
    {{
      "type": "performance|security|compatibility|scalability",
      "description": "约束描述",
      "value": "具体要求"
    }}
  ],
  "business_model": "b2b|b2c|c2c|saas|marketplace",
  "complexity_level": "low|medium|high",
  "confidence_analysis": {{
    "overall_confidence": 0.85,
    "uncertainties": ["不确定的方面"],
    "assumptions": ["假设条件"]
  }}
}}

分析要求:
1. 项目类型识别: 基于用户描述判断最符合的项目类型
2. 目标用户分析: 从描述中提取或推断目标用户特征
3. 核心功能提取: 识别明确提到的和隐含的功能需求
4. 技术约束理解: 从性能、安全、兼容性等角度分析约束
5. 商业模式判断: 基于用户群体和功能判断商业模式
6. 复杂度评估: 综合考虑功能数量、技术难度、用户规模

注意事项:
- 返回格式必须是有效的JSON，不要包含任何其他文本
- 所有枚举值必须使用指定的选项
- 如果信息不足，基于常识进行合理推断
- confidence_analysis中的overall_confidence应为0-1之间的数值
- 所有数组至少包含一个元素"""

    @staticmethod
    def build_validation_prompt(parsed_data: Dict[str, Any], original_text: str) -> str:
        return f"""请验证以下需求解析结果是否与原始用户输入一致，并评估解析质量。

原始用户输入:
{original_text}

解析结果:
{parsed_data}

请从以下维度评估并返回JSON格式的验证结果:

{{
  "validation_score": 0.85,
  "consistency_check": {{
    "project_type_match": true,
    "features_coverage": 0.9,
    "user_target_accuracy": 0.8
  }},
  "completeness_analysis": {{
    "missing_features": ["可能遗漏的功能"],
    "over_interpretation": ["过度解读的内容"],
    "completeness_score": 0.85
  }},
  "quality_assessment": {{
    "clarity_score": 0.9,
    "specificity_score": 0.8,
    "feasibility_score": 0.85
  }},
  "suggestions": [
    "改进建议1",
    "改进建议2"
  ],
  "confidence_adjustment": 0.82
}}

评估标准:
1. validation_score: 整体验证分数(0-1)
2. consistency_check: 解析结果与原文的一致性
3. completeness_analysis: 解析的完整性分析
4. quality_assessment: 解析质量评估
5. suggestions: 针对性的改进建议
6. confidence_adjustment: 调整后的置信度

请确保返回有效的JSON格式，所有分数均为0-1之间的数值。"""

    @staticmethod
    def build_refinement_prompt(parsed_data: Dict[str, Any], user_feedback: str) -> str:
        return f"""基于用户反馈，请优化需求解析结果。

当前解析结果:
{parsed_data}

用户反馈:
{user_feedback}

请根据用户反馈调整解析结果，返回优化后的JSON数据，格式与原始解析结果保持一致:

{{
  "project_type": "调整后的项目类型",
  "target_users": [调整后的目标用户],
  "core_features": [调整后的核心功能],
  "technical_constraints": [调整后的技术约束],
  "business_model": "调整后的商业模式",
  "complexity_level": "调整后的复杂度",
  "confidence_analysis": {{
    "overall_confidence": 调整后的置信度,
    "uncertainties": ["剩余不确定因素"],
    "assumptions": ["新的假设条件"]
  }},
  "refinement_summary": {{
    "changes_made": ["所做的具体调整"],
    "rationale": ["调整理由"],
    "improvement_score": 提升分数
  }}
}}

优化原则:
1. 严格按照用户反馈进行调整
2. 保持数据结构和格式的一致性
3. 确保调整后的结果更加准确和具体
4. 在refinement_summary中详细说明调整内容
5. 更新置信度以反映改进程度"""

    @staticmethod
    def build_batch_analysis_prompt(texts: list) -> str:
        texts_formatted = "\n\n".join([f"需求{i+1}:\n{text}" for i, text in enumerate(texts)])
        
        return f"""你需要批量分析多个项目需求。请对每个需求进行独立分析，并识别它们之间的关联性。

用户需求列表:
{texts_formatted}

请返回以下格式的JSON结果:

{{
  "individual_analysis": [
    {{
      "requirement_id": 1,
      "project_type": "web_app|mobile_app|api_service|desktop_app",
      "target_users": [...],
      "core_features": [...],
      "technical_constraints": [...],
      "business_model": "b2b|b2c|c2c|saas|marketplace",
      "complexity_level": "low|medium|high"
    }}
  ],
  "cross_analysis": {{
    "common_patterns": ["共同模式"],
    "complementary_features": ["互补功能"],
    "integration_opportunities": ["整合机会"],
    "resource_sharing": ["资源共享可能性"]
  }},
  "batch_insights": {{
    "overall_complexity": "low|medium|high",
    "recommended_priority": [1, 2, 3],
    "synergy_score": 0.75
  }}
}}

分析要求:
1. 对每个需求进行独立的结构化分析
2. 识别需求间的共同点和差异
3. 评估需求间的协同效应
4. 提供优先级建议"""
import logging
from typing import Dict, Any, List, Tuple, Optional
from pydantic import BaseModel, ValidationError, Field
from enum import Enum


logger = logging.getLogger(__name__)


class ProjectType(str, Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    DESKTOP_APP = "desktop_app"


class BusinessModel(str, Enum):
    B2B = "b2b"
    B2C = "b2c"
    C2C = "c2c"
    SAAS = "saas"
    MARKETPLACE = "marketplace"


class ComplexityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TechSavvy(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ConstraintType(str, Enum):
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"
    SCALABILITY = "scalability"


class UserGroup(BaseModel):
    age_range: str = Field(..., min_length=1, max_length=50)
    occupation: str = Field(..., min_length=1, max_length=100)
    tech_savvy: TechSavvy


class Feature(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    priority: Priority
    complexity: ComplexityLevel
    description: str = Field(default="", max_length=500)


class Constraint(BaseModel):
    type: ConstraintType
    description: str = Field(..., min_length=1, max_length=200)
    value: str = Field(..., min_length=1, max_length=100)


class ConfidenceAnalysis(BaseModel):
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    uncertainties: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class RequirementModel(BaseModel):
    project_type: ProjectType
    target_users: List[UserGroup] = Field(..., min_items=1)
    core_features: List[Feature] = Field(..., min_items=1)
    technical_constraints: List[Constraint] = Field(default_factory=list)
    business_model: BusinessModel
    complexity_level: ComplexityLevel
    confidence_analysis: ConfidenceAnalysis


class ValidationResult(BaseModel):
    is_valid: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    validation_errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    quality_metrics: Dict[str, float] = Field(default_factory=dict)


class RequirementValidator:
    def __init__(self):
        self.min_confidence_threshold = 0.5
        self.max_features_count = 20
        self.max_constraints_count = 10
        
    def validate_and_score(self, data: Dict[str, Any]) -> ValidationResult:
        logger.info("开始验证需求解析数据")
        logger.debug(f"输入数据: {data}")
        
        result = ValidationResult(
            is_valid=True,
            confidence_score=0.0,
            quality_metrics={}
        )
        
        try:
            validated_model = RequirementModel(**data)
            logger.info("Pydantic模型验证通过")
            
            result.confidence_score = validated_model.confidence_analysis.overall_confidence
            
            result = self._perform_business_validation(validated_model, result)
            result = self._assess_quality_metrics(validated_model, result)
            result = self._generate_suggestions(validated_model, result)
            
            logger.info(f"验证完成，置信度: {result.confidence_score:.2f}")
            
        except ValidationError as e:
            logger.error(f"Pydantic验证失败: {e}")
            result.is_valid = False
            result.confidence_score = 0.0
            
            for error in e.errors():
                error_msg = f"字段 {'.'.join(str(loc) for loc in error['loc'])}: {error['msg']}"
                result.validation_errors.append(error_msg)
                
        except Exception as e:
            logger.error(f"验证过程发生未知错误: {str(e)}")
            result.is_valid = False
            result.confidence_score = 0.0
            result.validation_errors.append(f"验证失败: {str(e)}")
        
        return result
    
    def _perform_business_validation(self, model: RequirementModel, result: ValidationResult) -> ValidationResult:
        logger.debug("执行业务逻辑验证")
        
        if len(model.core_features) > self.max_features_count:
            result.warnings.append(f"功能数量过多({len(model.core_features)})，建议控制在{self.max_features_count}个以内")
        
        if len(model.technical_constraints) > self.max_constraints_count:
            result.warnings.append(f"技术约束过多({len(model.technical_constraints)})，建议控制在{self.max_constraints_count}个以内")
        
        high_priority_features = [f for f in model.core_features if f.priority == Priority.HIGH]
        if len(high_priority_features) == 0:
            result.warnings.append("没有高优先级功能，建议明确核心功能")
        elif len(high_priority_features) > 5:
            result.warnings.append("高优先级功能过多，建议精简核心功能")
        
        project_complexity_map = {
            ProjectType.API_SERVICE: ComplexityLevel.MEDIUM,
            ProjectType.WEB_APP: ComplexityLevel.MEDIUM,
            ProjectType.MOBILE_APP: ComplexityLevel.HIGH,
            ProjectType.DESKTOP_APP: ComplexityLevel.HIGH
        }
        
        expected_complexity = project_complexity_map.get(model.project_type)
        if expected_complexity and model.complexity_level == ComplexityLevel.LOW and expected_complexity != ComplexityLevel.LOW:
            result.warnings.append(f"{model.project_type}项目复杂度通常不会是低等级")
        
        business_project_match = {
            BusinessModel.B2B: [ProjectType.API_SERVICE, ProjectType.WEB_APP],
            BusinessModel.B2C: [ProjectType.WEB_APP, ProjectType.MOBILE_APP],
            BusinessModel.SAAS: [ProjectType.WEB_APP, ProjectType.API_SERVICE],
            BusinessModel.MARKETPLACE: [ProjectType.WEB_APP, ProjectType.MOBILE_APP],
            BusinessModel.C2C: [ProjectType.WEB_APP, ProjectType.MOBILE_APP]
        }
        
        expected_types = business_project_match.get(model.business_model, [])
        if expected_types and model.project_type not in expected_types:
            result.warnings.append(f"商业模式{model.business_model}与项目类型{model.project_type}匹配度较低")
        
        if model.confidence_analysis.overall_confidence < self.min_confidence_threshold:
            result.warnings.append(f"置信度过低({model.confidence_analysis.overall_confidence:.2f})，建议获取更多信息")
        
        return result
    
    def _assess_quality_metrics(self, model: RequirementModel, result: ValidationResult) -> ValidationResult:
        logger.debug("评估质量指标")
        
        result.quality_metrics['feature_completeness'] = min(len(model.core_features) / 5.0, 1.0)
        
        result.quality_metrics['user_specificity'] = self._calculate_user_specificity(model.target_users)
        
        result.quality_metrics['constraint_coverage'] = min(len(model.technical_constraints) / 3.0, 1.0)
        
        feature_priority_score = 0
        for feature in model.core_features:
            if feature.priority == Priority.HIGH:
                feature_priority_score += 1.0
            elif feature.priority == Priority.MEDIUM:
                feature_priority_score += 0.6
            else:
                feature_priority_score += 0.3
        result.quality_metrics['priority_clarity'] = min(feature_priority_score / len(model.core_features), 1.0)
        
        confidence_factors = {
            'base_confidence': model.confidence_analysis.overall_confidence,
            'feature_completeness': result.quality_metrics['feature_completeness'],
            'user_specificity': result.quality_metrics['user_specificity'],
            'constraint_coverage': result.quality_metrics['constraint_coverage'],
            'priority_clarity': result.quality_metrics['priority_clarity']
        }
        
        adjusted_confidence = (
            confidence_factors['base_confidence'] * 0.4 +
            confidence_factors['feature_completeness'] * 0.2 +
            confidence_factors['user_specificity'] * 0.2 +
            confidence_factors['constraint_coverage'] * 0.1 +
            confidence_factors['priority_clarity'] * 0.1
        )
        
        result.confidence_score = min(adjusted_confidence, 1.0)
        result.quality_metrics['adjusted_confidence'] = result.confidence_score
        
        return result
    
    def _calculate_user_specificity(self, users: List[UserGroup]) -> float:
        specificity_score = 0
        for user in users:
            score = 0
            
            if '-' in user.age_range and len(user.age_range.split('-')) == 2:
                score += 0.4
            
            if len(user.occupation) > 5 and user.occupation != "general":
                score += 0.4
            
            score += 0.2
            
            specificity_score += score
        
        return min(specificity_score / len(users), 1.0)
    
    def _generate_suggestions(self, model: RequirementModel, result: ValidationResult) -> ValidationResult:
        logger.debug("生成改进建议")
        
        if len(model.core_features) < 3:
            result.suggestions.append("建议添加更多核心功能描述，至少包含3-5个主要功能")
        
        if len(model.target_users) == 1 and model.target_users[0].occupation == "general":
            result.suggestions.append("建议更具体地描述目标用户群体")
        
        if len(model.technical_constraints) == 0:
            result.suggestions.append("建议添加技术约束，如性能要求、安全要求等")
        
        if model.complexity_level == ComplexityLevel.LOW and len(model.core_features) > 8:
            result.suggestions.append("功能数量较多但复杂度标记为低，建议重新评估复杂度")
        
        high_complexity_features = [f for f in model.core_features if f.complexity == ComplexityLevel.HIGH]
        if len(high_complexity_features) > 3:
            result.suggestions.append("高复杂度功能较多，建议考虑分阶段实现")
        
        mobile_security_features = ['login', 'authentication', 'payment', 'personal']
        if model.project_type == ProjectType.MOBILE_APP:
            has_security_concern = any(
                any(keyword in feature.name.lower() for keyword in mobile_security_features) 
                for feature in model.core_features
            )
            if has_security_concern and not any(c.type == ConstraintType.SECURITY for c in model.technical_constraints):
                result.suggestions.append("移动应用涉及敏感功能，建议添加安全约束")
        
        return result
    
    def validate_batch(self, data_list: List[Dict[str, Any]]) -> List[ValidationResult]:
        logger.info(f"开始批量验证{len(data_list)}个需求")
        results = []
        
        for i, data in enumerate(data_list):
            logger.debug(f"验证第{i+1}/{len(data_list)}个需求")
            result = self.validate_and_score(data)
            results.append(result)
        
        logger.info(f"批量验证完成，成功: {sum(1 for r in results if r.is_valid)}/{len(results)}")
        return results
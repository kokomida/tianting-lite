import time
import logging
import uuid
from typing import Dict, Any, Optional, List
from .requirement_analyzer import RequirementAnalyzer, RequirementAnalysisError
from .utils.text_processor import TextProcessor
from .prompts.requirement_analysis import RequirementAnalysisPrompts
from .validators.requirement_validator import RequirementValidator, ValidationResult, RequirementModel


logger = logging.getLogger(__name__)


class RequirementParsingError(Exception):
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


class RequirementParseResult:
    def __init__(self, 
                 requirement_id: str,
                 parsed_data: RequirementModel,
                 confidence_score: float,
                 validation_result: ValidationResult,
                 processing_time_ms: int,
                 suggestions: List[str] = None):
        self.requirement_id = requirement_id
        self.parsed_data = parsed_data
        self.confidence_score = confidence_score
        self.validation_result = validation_result
        self.processing_time_ms = processing_time_ms
        self.suggestions = suggestions or []
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "parsed_data": {
                "project_type": self.parsed_data.project_type.value,
                "target_users": [
                    {
                        "age_range": user.age_range,
                        "occupation": user.occupation,
                        "tech_savvy": user.tech_savvy.value
                    } for user in self.parsed_data.target_users
                ],
                "core_features": [
                    {
                        "name": feature.name,
                        "priority": feature.priority.value,
                        "complexity": feature.complexity.value,
                        "description": feature.description
                    } for feature in self.parsed_data.core_features
                ],
                "technical_constraints": [
                    {
                        "type": constraint.type.value,
                        "description": constraint.description,
                        "value": constraint.value
                    } for constraint in self.parsed_data.technical_constraints
                ],
                "business_model": self.parsed_data.business_model.value,
                "complexity_level": self.parsed_data.complexity_level.value
            },
            "confidence_score": self.confidence_score,
            "suggestions": self.suggestions,
            "processing_time_ms": self.processing_time_ms,
            "validation_details": {
                "is_valid": self.validation_result.is_valid,
                "warnings": self.validation_result.warnings,
                "quality_metrics": self.validation_result.quality_metrics
            }
        }


class RequirementParser:
    def __init__(self, analyzer: Optional[RequirementAnalyzer] = None):
        self.analyzer = analyzer or RequirementAnalyzer()
        self.text_processor = TextProcessor()
        self.validator = RequirementValidator()
        self.prompts = RequirementAnalysisPrompts()
        
        self.max_processing_time = 30
        self.min_confidence_threshold = 0.5
        
        logger.info("RequirementParser初始化完成")
        
    async def parse_requirement(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> RequirementParseResult:
        start_time = time.time()
        requirement_id = str(uuid.uuid4())
        
        logger.info(f"开始解析需求: {requirement_id}")
        logger.debug(f"用户输入长度: {len(user_input)}")
        
        try:
            if not user_input or not user_input.strip():
                raise RequirementParsingError("用户输入不能为空")
            
            logger.debug("第1步: 文本预处理")
            processed_text = self.text_processor.clean_and_normalize(user_input)
            if not processed_text:
                raise RequirementParsingError("文本预处理后为空")
            
            keywords = self.text_processor.extract_keywords(processed_text)
            text_analysis = self.text_processor.analyze_complexity(processed_text)
            
            logger.debug(f"文本分析结果: {text_analysis}")
            logger.debug(f"提取关键词: {keywords}")
            
            logger.debug("第2步: 构建AI分析提示词")
            analysis_prompt = self.prompts.build_analysis_prompt(processed_text, keywords)
            
            logger.debug("第3步: 调用本地AI分析器进行分析")
            analysis_result = await self.analyzer.analyze_requirement(processed_text)
                
            logger.debug(f"Claude分析结果: {analysis_result}")
            
            logger.debug("第4步: 结构化数据提取和验证")
            validation_result = self.validator.validate_and_score(analysis_result)
            
            if not validation_result.is_valid:
                error_msg = f"数据验证失败: {', '.join(validation_result.validation_errors)}"
                logger.error(error_msg)
                raise RequirementParsingError(error_msg)
            
            logger.debug("第5步: 创建需求模型")
            requirement_model = RequirementModel(**analysis_result)
            
            logger.debug("第6步: 生成最终结果")
            processing_time = int((time.time() - start_time) * 1000)
            
            if processing_time > self.max_processing_time * 1000:
                logger.warning(f"处理时间超出预期: {processing_time}ms > {self.max_processing_time * 1000}ms")
            
            confidence_score = validation_result.confidence_score
            if confidence_score < self.min_confidence_threshold:
                logger.warning(f"置信度过低: {confidence_score} < {self.min_confidence_threshold}")
            
            suggestions = validation_result.suggestions.copy()
            if text_analysis['complexity_level'] == 'high':
                suggestions.append("项目复杂度较高，建议考虑分阶段实现")
            
            result = RequirementParseResult(
                requirement_id=requirement_id,
                parsed_data=requirement_model,
                confidence_score=confidence_score,
                validation_result=validation_result,
                processing_time_ms=processing_time,
                suggestions=suggestions
            )
            
            logger.info(f"需求解析完成: {requirement_id}, 置信度: {confidence_score:.2f}, 耗时: {processing_time}ms")
            
            return result
            
        except RequirementAnalysisError as e:
            processing_time = int((time.time() - start_time) * 1000)
            error_msg = f"本地AI分析失败: {str(e)}"
            logger.error(error_msg)
            raise RequirementParsingError(error_msg, e)
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            error_msg = f"需求解析过程发生错误: {str(e)}"
            logger.error(error_msg)
            raise RequirementParsingError(error_msg, e)
    
    async def refine_requirement(self, 
                               original_result: RequirementParseResult, 
                               user_feedback: str) -> RequirementParseResult:
        start_time = time.time()
        
        logger.info(f"开始优化需求: {original_result.requirement_id}")
        logger.debug(f"用户反馈: {user_feedback}")
        
        try:
            if not user_feedback or not user_feedback.strip():
                raise RequirementParsingError("用户反馈不能为空")
            
            processed_feedback = self.text_processor.clean_and_normalize(user_feedback)
            
            refinement_prompt = self.prompts.build_refinement_prompt(
                original_result.parsed_data.dict(), 
                processed_feedback
            )
            
            refined_result = await self.analyzer.analyze_requirement(processed_feedback)
            
            validation_result = self.validator.validate_and_score(refined_result)
            
            if not validation_result.is_valid:
                error_msg = f"优化后数据验证失败: {', '.join(validation_result.validation_errors)}"
                logger.error(error_msg)
                raise RequirementParsingError(error_msg)
            
            requirement_model = RequirementModel(**refined_result)
            processing_time = int((time.time() - start_time) * 1000)
            
            result = RequirementParseResult(
                requirement_id=original_result.requirement_id + "_refined",
                parsed_data=requirement_model,
                confidence_score=validation_result.confidence_score,
                validation_result=validation_result,
                processing_time_ms=processing_time,
                suggestions=validation_result.suggestions
            )
            
            logger.info(f"需求优化完成: {result.requirement_id}, 置信度: {result.confidence_score:.2f}")
            
            return result
            
        except Exception as e:
            error_msg = f"需求优化过程发生错误: {str(e)}"
            logger.error(error_msg)
            raise RequirementParsingError(error_msg, e)
    
    async def batch_parse_requirements(self, user_inputs: List[str]) -> List[RequirementParseResult]:
        logger.info(f"开始批量解析{len(user_inputs)}个需求")
        
        results = []
        for i, user_input in enumerate(user_inputs):
            try:
                logger.debug(f"处理第{i+1}/{len(user_inputs)}个需求")
                result = await self.parse_requirement(user_input)
                results.append(result)
                
            except Exception as e:
                logger.error(f"批量解析第{i+1}个需求失败: {str(e)}")
                error_result = RequirementParseResult(
                    requirement_id=f"error_{i+1}",
                    parsed_data=None,
                    confidence_score=0.0,
                    validation_result=None,
                    processing_time_ms=0,
                    suggestions=[f"解析失败: {str(e)}"]
                )
                results.append(error_result)
        
        success_count = sum(1 for r in results if r.parsed_data is not None)
        logger.info(f"批量解析完成: 成功 {success_count}/{len(user_inputs)}")
        
        return results
    
    async def validate_analyzer_connection(self) -> Dict[str, Any]:
        logger.info("验证本地AI分析器连接")
        
        try:
            result = await self.analyzer.validate_connection()
                
            logger.info(f"分析器连接验证结果: {result['status']}")
            return result
            
        except Exception as e:
            error_msg = f"分析器连接验证失败: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "error_type": type(e).__name__
            }
    
    def get_parser_status(self) -> Dict[str, Any]:
        return {
            "parser_version": "1.0.0",
            "max_processing_time": self.max_processing_time,
            "min_confidence_threshold": self.min_confidence_threshold,
            "components": {
                "text_processor": "active",
                "analyzer": "active",
                "validator": "active",
                "prompts": "active"
            }
        }
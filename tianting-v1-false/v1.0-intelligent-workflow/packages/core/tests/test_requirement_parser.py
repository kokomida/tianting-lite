import pytest
import asyncio
import json
from unittest.mock import AsyncMock, Mock, patch
from src.requirement_parser import RequirementParser, RequirementParsingError
from src.requirement_analyzer import RequirementAnalyzer, RequirementAnalysisError
from src.validators.requirement_validator import ValidationResult


class TestRequirementParser:
    
    @pytest.fixture
    def mock_analyzer(self):
        analyzer = AsyncMock(spec=RequirementAnalyzer)
        return analyzer
    
    @pytest.fixture
    def parser(self, mock_analyzer):
        return RequirementParser(analyzer=mock_analyzer)
    
    @pytest.fixture
    def sample_claude_response(self):
        return {
            "project_type": "web_app",
            "target_users": [
                {
                    "age_range": "18-35",
                    "occupation": "knowledge_worker", 
                    "tech_savvy": "medium"
                }
            ],
            "core_features": [
                {
                    "name": "user_authentication",
                    "priority": "high",
                    "complexity": "medium",
                    "description": "用户登录注册系统"
                },
                {
                    "name": "music_recommendation", 
                    "priority": "high",
                    "complexity": "high",
                    "description": "音乐推荐算法"
                }
            ],
            "technical_constraints": [
                {
                    "type": "performance",
                    "description": "响应时间要求",
                    "value": "<2s"
                }
            ],
            "business_model": "b2c",
            "complexity_level": "medium",
            "confidence_analysis": {
                "overall_confidence": 0.87,
                "uncertainties": ["用户数量规模不确定"],
                "assumptions": ["用户主要使用移动端"]
            }
        }
    
    @pytest.mark.asyncio
    async def test_parse_requirement_success(self, parser, mock_analyzer, sample_claude_response):
        """测试成功解析需求"""
        # 设置Mock
        mock_analyzer.analyze_requirement.return_value = sample_claude_response
        
        # 执行测试
        user_input = "我想做一个音乐推荐APP，主要面向年轻用户"
        result = await parser.parse_requirement(user_input)
        
        # 验证结果
        assert result is not None
        assert result.requirement_id is not None
        assert result.parsed_data.project_type.value == "web_app"
        assert len(result.parsed_data.core_features) == 2
        assert result.confidence_score > 0
        assert result.processing_time_ms > 0
        
        # 验证分析器调用
        mock_analyzer.analyze_requirement.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_parse_requirement_empty_input(self, parser):
        """测试空输入处理"""
        with pytest.raises(RequirementParsingError, match="用户输入不能为空"):
            await parser.parse_requirement("")
            
        with pytest.raises(RequirementParsingError, match="用户输入不能为空"):
            await parser.parse_requirement("   ")
    
    @pytest.mark.asyncio
    async def test_parse_requirement_analyzer_error(self, parser, mock_analyzer):
        """测试分析器错误处理"""
        # 设置Mock抛出异常
        mock_analyzer.analyze_requirement.side_effect = RequirementAnalysisError("分析失败")
        
        # 执行测试并验证异常
        with pytest.raises(RequirementParsingError, match="本地AI分析失败"):
            await parser.parse_requirement("测试输入")
    
    @pytest.mark.asyncio
    async def test_parse_requirement_invalid_response(self, parser, mock_analyzer):
        """测试无效响应处理"""
        # 设置Mock返回无效数据
        mock_analyzer.analyze_requirement.return_value = {
            "invalid_field": "invalid_value"
        }
        
        # 执行测试并验证异常
        with pytest.raises(RequirementParsingError, match="数据验证失败"):
            await parser.parse_requirement("测试输入")
    
    @pytest.mark.asyncio
    async def test_refine_requirement_success(self, parser, mock_analyzer, sample_claude_response):
        """测试需求优化功能"""
        # 首先创建原始结果
        mock_analyzer.analyze_requirement.return_value = sample_claude_response
        
        original_result = await parser.parse_requirement("原始需求")
        
        # 设置优化后的响应
        refined_response = sample_claude_response.copy()
        refined_response["confidence_analysis"]["overall_confidence"] = 0.92
        mock_analyzer.analyze_requirement.return_value = refined_response
        
        # 执行优化
        refined_result = await parser.refine_requirement(original_result, "增加社交分享功能")
        
        # 验证结果
        assert refined_result is not None
        assert refined_result.requirement_id.endswith("_refined")
        assert refined_result.confidence_score == 0.92
    
    @pytest.mark.asyncio
    async def test_batch_parse_requirements(self, parser, mock_analyzer, sample_claude_response):
        """测试批量解析功能"""
        # 设置Mock
        mock_analyzer.analyze_requirement.return_value = sample_claude_response
        
        # 准备测试数据
        user_inputs = [
            "我想做一个电商网站",
            "我需要一个移动APP",
            "我要开发API服务"
        ]
        
        # 执行批量解析
        results = await parser.batch_parse_requirements(user_inputs)
        
        # 验证结果
        assert len(results) == 3
        assert all(result.parsed_data is not None for result in results)
        assert mock_analyzer.analyze_requirement.call_count == 3
    
    @pytest.mark.asyncio
    async def test_batch_parse_with_errors(self, parser, mock_analyzer, sample_claude_response):
        """测试批量解析中的错误处理"""
        # 设置Mock - 第二个请求失败
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RequirementAnalysisError("第二个请求失败")
            return sample_claude_response
        
        mock_analyzer.analyze_requirement.side_effect = side_effect
        
        # 执行批量解析
        user_inputs = ["需求1", "需求2", "需求3"]
        results = await parser.batch_parse_requirements(user_inputs)
        
        # 验证结果
        assert len(results) == 3
        assert results[0].parsed_data is not None  # 第一个成功
        assert results[1].parsed_data is None      # 第二个失败
        assert results[2].parsed_data is not None  # 第三个成功
        assert "解析失败" in results[1].suggestions[0]
    
    @pytest.mark.asyncio
    async def test_validate_analyzer_connection(self, parser, mock_analyzer):
        """测试分析器连接验证"""
        # 设置Mock
        mock_analyzer.validate_connection.return_value = {
            "status": "success",
            "message": "本地AI分析正常"
        }
        
        # 执行测试
        result = await parser.validate_analyzer_connection()
        
        # 验证结果
        assert result["status"] == "success"
        assert "正常" in result["message"]
    
    def test_get_parser_status(self, parser):
        """测试获取解析器状态"""
        status = parser.get_parser_status()
        
        assert "parser_version" in status
        assert status["parser_version"] == "1.0.0"
        assert "components" in status
        assert all(comp == "active" for comp in status["components"].values())
    
    @pytest.mark.asyncio
    async def test_complex_user_input_processing(self, parser, mock_analyzer, sample_claude_response):
        """测试复杂用户输入的处理"""
        # 设置Mock
        mock_analyzer.analyze_requirement.return_value = sample_claude_response
        
        # 复杂的用户输入
        complex_input = """
        我想开发一个大型电商平台，需要支持：
        1. 用户注册登录（手机号、邮箱、第三方登录）
        2. 商品展示和搜索功能
        3. 购物车和订单管理
        4. 支付系统（支持支付宝、微信支付）
        5. 用户评价和推荐系统
        6. 后台管理系统
        
        技术要求：
        - 支持高并发（万级QPS）
        - 数据安全和隐私保护
        - 移动端和Web端同步
        
        目标用户主要是18-45岁的消费者，预计用户规模100万+
        """
        
        # 执行测试
        result = await parser.parse_requirement(complex_input)
        
        # 验证结果
        assert result is not None
        assert result.parsed_data is not None
        
        # 验证文本预处理被调用（通过检查处理时间大于0）
        assert result.processing_time_ms > 0
        
        # 验证分析器被调用
        mock_analyzer.analyze_requirement.assert_called_once()
        
        # 获取调用参数并验证包含关键信息
        call_args = mock_analyzer.analyze_requirement.call_args[0][0]
        assert "电商" in call_args or "商品" in call_args or "购物" in call_args
    
    @pytest.mark.asyncio
    async def test_performance_timeout_warning(self, parser, mock_analyzer, sample_claude_response):
        """测试处理时间超时警告"""
        # 设置Mock，模拟慢响应
        async def slow_response(*args, **kwargs):
            await asyncio.sleep(0.1)  # 模拟慢响应
            return sample_claude_response
        
        mock_analyzer.analyze_requirement.side_effect = slow_response
        
        # 降低超时阈值以便测试
        parser.max_processing_time = 0.05  # 50ms
        
        # 执行测试
        result = await parser.parse_requirement("测试输入")
        
        # 验证结果（应该成功，但会有警告日志）
        assert result is not None
        assert result.processing_time_ms > 50  # 超过阈值
    
    @pytest.mark.asyncio
    async def test_low_confidence_warning(self, parser, mock_analyzer, sample_claude_response):
        """测试低置信度警告"""
        # 设置低置信度响应
        low_confidence_response = sample_claude_response.copy()
        low_confidence_response["confidence_analysis"]["overall_confidence"] = 0.3
        
        mock_analyzer.analyze_requirement.return_value = low_confidence_response
        
        # 执行测试
        result = await parser.parse_requirement("模糊的需求描述")
        
        # 验证结果
        assert result is not None
        assert result.confidence_score < 0.5  # 低于默认阈值
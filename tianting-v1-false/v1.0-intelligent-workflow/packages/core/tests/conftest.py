import pytest
import os
import sys
from unittest.mock import patch

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture(scope="session")
def mock_env_vars():
    """模拟环境变量"""
    with patch.dict(os.environ, {
        'CLAUDE_API_KEY': 'test_api_key_12345',
        'LOG_LEVEL': 'DEBUG',
        'ENVIRONMENT': 'test'
    }):
        yield

@pytest.fixture(autouse=True)
def setup_logging():
    """设置测试日志"""
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

@pytest.fixture
def sample_user_inputs():
    """提供测试用的用户输入样例"""
    return [
        "我想做一个音乐推荐APP",
        "需要开发电商网站，支持在线支付",
        "想要一个项目管理工具，支持团队协作",
        "开发API服务，提供数据分析功能",
        "制作移动端新闻阅读应用"
    ]

@pytest.fixture  
def complex_user_input():
    """复杂用户输入样例"""
    return """
    我要开发一个综合性的在线教育平台，具体需求如下：

    核心功能：
    1. 用户管理：学生、教师、管理员三种角色
    2. 课程系统：视频播放、课件下载、作业提交
    3. 直播教学：实时互动、录制回放
    4. 考试系统：在线考试、自动评分
    5. 支付系统：课程购买、会员订阅
    
    技术要求：
    - 支持1万+并发用户
    - 视频播放流畅，支持多种分辨率
    - 数据安全，符合教育行业合规要求
    - 支持PC端和移动端
    
    目标用户：
    - 主要用户：K12学生及家长，大学生
    - 次要用户：培训机构教师
    - 年龄范围：6-25岁学生，25-45岁教师和家长
    
    商业模式：
    - 课程付费
    - 会员订阅
    - 机构入驻分成
    """

@pytest.fixture
def invalid_user_inputs():
    """无效用户输入样例"""
    return [
        "",
        "   ",
        None,
        "a" * 10000,  # 过长输入
        "？？？？",      # 无意义输入
    ]
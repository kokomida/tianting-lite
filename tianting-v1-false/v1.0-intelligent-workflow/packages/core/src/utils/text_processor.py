import re
import logging
from typing import Dict, List


logger = logging.getLogger(__name__)


class TextProcessor:
    def __init__(self):
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'[\+]?[1-9]?[0-9]{7,15}')
        self.excessive_whitespace = re.compile(r'\s+')
        
    def clean_and_normalize(self, text: str) -> str:
        if not text or not isinstance(text, str):
            logger.warning(f"输入文本无效: {type(text)}")
            return ""
            
        logger.debug(f"开始处理文本，长度: {len(text)}")
        
        original_text = text
        
        text = text.strip()
        
        text = self.url_pattern.sub('[URL]', text)
        text = self.email_pattern.sub('[EMAIL]', text)  
        text = self.phone_pattern.sub('[PHONE]', text)
        
        text = self.excessive_whitespace.sub(' ', text)
        
        text = self._normalize_punctuation(text)
        
        text = self._remove_repeated_chars(text)
        
        if len(text) > 5000:
            logger.warning(f"文本过长，截断到5000字符: {len(text)}")
            text = text[:5000] + "..."
            
        logger.debug(f"文本处理完成，原长度: {len(original_text)}, 处理后长度: {len(text)}")
        
        return text
    
    def _normalize_punctuation(self, text: str) -> str:
        punctuation_map = {
            '。': '.',
            '，': ',',
            '？': '?',
            '！': '!',
            '；': ';',
            '：': ':',
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '（': '(',
            '）': ')',
            '【': '[',
            '】': ']'
        }
        
        for chinese_punct, english_punct in punctuation_map.items():
            text = text.replace(chinese_punct, english_punct)
            
        return text
    
    def _remove_repeated_chars(self, text: str) -> str:
        text = re.sub(r'([.!?]){3,}', r'\1\1\1', text)
        text = re.sub(r'([哈哈哈]){4,}', r'\1\1\1', text)  
        text = re.sub(r'([呵呵呵]){4,}', r'\1\1\1', text)
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        if not text:
            return []
            
        text = text.lower()
        
        tech_keywords = [
            'web', 'app', 'mobile', 'api', 'website', 'system', 'platform',
            'database', 'mysql', 'postgresql', 'redis', 'mongodb',
            'react', 'vue', 'angular', 'python', 'java', 'nodejs', 'php',
            'ai', 'ml', 'machine learning', 'deep learning', '人工智能', '机器学习',
            'blockchain', '区块链', 'iot', '物联网', 'cloud', '云计算',
            'microservice', '微服务', 'docker', 'kubernetes', 'devops'
        ]
        
        business_keywords = [
            'user', 'customer', 'client', 'business', 'ecommerce', 'payment',
            'order', 'product', 'service', 'management', 'admin', 'dashboard',
            '用户', '客户', '商业', '电商', '支付', '订单', '产品', '服务', '管理'
        ]
        
        feature_keywords = [
            'login', 'register', 'authentication', 'authorization', 'search',
            'filter', 'sort', 'upload', 'download', 'chat', 'message', 'notification',
            '登录', '注册', '认证', '授权', '搜索', '筛选', '排序', '上传', '下载',
            '聊天', '消息', '通知', '推荐', '分享', '评论', '点赞'
        ]
        
        all_keywords = tech_keywords + business_keywords + feature_keywords
        found_keywords = []
        
        for keyword in all_keywords:
            if keyword in text:
                found_keywords.append(keyword)
                
        return list(set(found_keywords))
    
    def analyze_complexity(self, text: str) -> Dict[str, any]:
        if not text:
            return {
                'complexity_level': 'low',
                'word_count': 0,
                'sentence_count': 0,
                'feature_mentions': 0,
                'tech_mentions': 0
            }
        
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        keywords = self.extract_keywords(text)
        
        tech_count = 0
        feature_count = 0
        
        for keyword in keywords:
            if keyword in ['web', 'app', 'api', 'database', 'react', 'vue', 'python', 'java']:
                tech_count += 1
            elif keyword in ['login', 'search', 'upload', 'chat', 'payment']:
                feature_count += 1
        
        complexity_score = len(words) * 0.1 + len(sentences) * 2 + feature_count * 5 + tech_count * 3
        
        if complexity_score < 50:
            complexity_level = 'low'
        elif complexity_score < 150:
            complexity_level = 'medium'
        else:
            complexity_level = 'high'
            
        return {
            'complexity_level': complexity_level,
            'complexity_score': complexity_score,
            'word_count': len(words),
            'sentence_count': len(sentences),
            'feature_mentions': feature_count,
            'tech_mentions': tech_count,
            'keywords': keywords
        }
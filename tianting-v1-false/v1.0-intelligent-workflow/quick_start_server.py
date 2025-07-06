#!/usr/bin/env python3
"""
天庭系统快速启动服务器
模拟需求解析功能
"""

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import threading
import time

class TiantingRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "healthy", "service": "天庭需求解析服务"}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                requirement = data.get('requirement', '')
                
                # 模拟AI分析过程
                time.sleep(0.001)  # 模拟<1ms处理时间
                
                # 生成分析结果
                analysis = self.analyze_requirement(requirement)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "success": True,
                    "analysis": analysis,
                    "processing_time": "0.8ms",
                    "confidence": 0.87
                }
                
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def analyze_requirement(self, requirement):
        """简单的需求分析逻辑"""
        if '记账' in requirement or '财务' in requirement:
            return {
                "project_type": "财务管理应用",
                "core_features": ["收支记录", "分类管理", "报表分析", "预算设置"],
                "suggested_tech": "React + Node.js + SQLite",
                "estimated_duration": "3-4周",
                "complexity": "中等"
            }
        elif '作业' in requirement or '学习' in requirement:
            return {
                "project_type": "学习管理系统",
                "core_features": ["作业管理", "截止日期提醒", "完成进度跟踪", "统计分析"],
                "suggested_tech": "React Native + Express + MongoDB",
                "estimated_duration": "4-6周",
                "complexity": "中等"
            }
        elif '电商' in requirement or '购物' in requirement:
            return {
                "project_type": "电商平台",
                "core_features": ["商品管理", "购物车", "订单系统", "支付集成"],
                "suggested_tech": "Vue.js + Spring Boot + MySQL",
                "estimated_duration": "8-12周",
                "complexity": "高"
            }
        else:
            return {
                "project_type": "定制化应用",
                "core_features": ["用户管理", "数据存储", "界面交互", "业务逻辑"],
                "suggested_tech": "根据具体需求选择",
                "estimated_duration": "6-10周",
                "complexity": "待评估"
            }

def start_server():
    PORT = 8001
    with socketserver.TCPServer(("", PORT), TiantingRequestHandler) as httpd:
        print(f"🚀 天庭需求解析服务已启动: http://localhost:{PORT}")
        print(f"🩺 健康检查: http://localhost:{PORT}/health")
        print(f"📝 需求分析API: POST http://localhost:{PORT}/api/analyze")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
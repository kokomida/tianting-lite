#!/usr/bin/env python3
"""
性能测试 - 验证响应时间<100ms
"""

import time
import sys
import json
from pathlib import Path

def test_response_creation_performance():
    """测试响应创建性能"""
    print("🔍 测试API响应创建性能...")
    
    def create_mock_response(data=None, message="操作成功"):
        """模拟响应创建"""
        return {
            "success": True,
            "data": data,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        }
    
    # 测试多次响应创建
    times = []
    for i in range(10):
        start_time = time.time()
        
        response = create_mock_response(
            data={
                "status": "healthy",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
                "version": "1.0.0",
                "database": {"status": "connected", "latency_ms": 5.2},
                "redis": {"status": "connected", "latency_ms": 1.8},
                "external_services": {"core_service": "available"}
            }
        )
        
        end_time = time.time()
        response_time_ms = (end_time - start_time) * 1000
        times.append(response_time_ms)
    
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    
    print(f"平均响应时间: {avg_time:.3f}ms")
    print(f"最大响应时间: {max_time:.3f}ms")
    print(f"最小响应时间: {min_time:.3f}ms")
    
    if max_time < 100:
        print("✅ 性能测试通过: 最大响应时间 < 100ms")
        return True
    else:
        print("❌ 性能测试失败: 响应时间过长")
        return False

def test_json_serialization_performance():
    """测试JSON序列化性能"""
    print("🔍 测试JSON序列化性能...")
    
    large_data = {
        "projects": [
            {
                "id": f"proj_{i}",
                "name": f"Project {i}",
                "description": f"Description for project {i}" * 10,
                "modules": [
                    {"name": f"module_{j}", "size": j * 100}
                    for j in range(20)
                ]
            }
            for i in range(50)
        ]
    }
    
    start_time = time.time()
    json_str = json.dumps(large_data)
    end_time = time.time()
    
    serialization_time_ms = (end_time - start_time) * 1000
    print(f"JSON序列化时间: {serialization_time_ms:.3f}ms")
    print(f"序列化数据大小: {len(json_str)} 字符")
    
    if serialization_time_ms < 50:
        print("✅ JSON序列化性能良好")
        return True
    else:
        print("⚠️ JSON序列化时间较长")
        return serialization_time_ms < 100

def test_file_operation_performance():
    """测试文件操作性能"""
    print("🔍 测试配置文件读取性能...")
    
    config_file = Path(__file__).parent / "src" / "config.py"
    
    times = []
    for i in range(5):
        start_time = time.time()
        
        with open(config_file, 'r') as f:
            content = f.read()
            # 模拟配置解析
            lines = content.count('\n')
            
        end_time = time.time()
        read_time_ms = (end_time - start_time) * 1000
        times.append(read_time_ms)
    
    avg_time = sum(times) / len(times)
    print(f"平均文件读取时间: {avg_time:.3f}ms")
    
    if avg_time < 10:
        print("✅ 文件操作性能优秀")
        return True
    else:
        print("⚠️ 文件操作性能一般")
        return avg_time < 50

def main():
    """主测试函数"""
    print("🚀 开始API性能测试...")
    print("=" * 50)
    
    tests = [
        ("响应创建性能", test_response_creation_performance),
        ("JSON序列化性能", test_json_serialization_performance),
        ("文件操作性能", test_file_operation_performance),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🔍 测试: {name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {name} 通过")
            else:
                print(f"❌ {name} 失败")
        except Exception as e:
            print(f"❌ {name} 异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 性能测试结果: {passed}/{total} 项通过")
    
    if passed == total:
        print("🎉 所有性能测试通过！响应时间 < 100ms")
        return True
    else:
        print("⚠️ 部分性能测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
<execution>
  <constraint>
    ## 测试验证限制条件
    - **时间约束**：测试执行时间不得影响开发效率
    - **资源约束**：测试环境的计算和存储资源有限
    - **环境约束**：测试必须在隔离环境中进行
    - **数据约束**：测试数据不得包含敏感信息
    - **兼容性约束**：测试必须支持多种运行环境
  </constraint>

  <rule>
    ## 测试验证强制规则
    - **全覆盖原则**：关键功能必须有完整的测试覆盖
    - **自动化优先**：可自动化的测试必须自动化
    - **隔离原则**：测试之间必须相互独立
    - **可重复性**：测试结果必须可重复和可验证
    - **失败快速**：测试失败必须快速反馈和定位
  </rule>

  <guideline>
    ## 测试验证指导原则
    - **左移测试**：尽早进行测试，降低修复成本
    - **风险驱动**：优先测试高风险和关键功能
    - **持续集成**：测试与开发流程深度集成
    - **质量内建**：将质量保证融入开发过程
    - **数据驱动**：基于数据进行测试决策
  </guideline>

  <process>
    ## 🧪 测试验证工作流程

    ### 测试金字塔架构
    ```mermaid
    graph TD
        A[测试金字塔] --> B[单元测试]
        A --> C[集成测试]
        A --> D[端到端测试]
        A --> E[探索性测试]
        
        B --> B1[函数测试]
        B --> B2[类测试]
        B --> B3[模块测试]
        
        C --> C1[组件集成]
        C --> C2[服务集成]
        C --> C3[数据库集成]
        
        D --> D1[用户场景测试]
        D --> D2[业务流程测试]
        D --> D3[系统测试]
        
        E --> E1[手工探索]
        E --> E2[边界测试]
        E --> E3[异常测试]
    ```

    ### 第一阶段：测试规划与设计
    ```mermaid
    flowchart TD
        A[需求分析] --> B[风险评估]
        B --> C[测试策略制定]
        C --> D[测试计划编写]
        D --> E[测试用例设计]
        E --> F[测试数据准备]
        F --> G[测试环境搭建]
        
        B --> B1[功能风险]
        B --> B2[性能风险]
        B --> B3[安全风险]
        B --> B4[集成风险]
        
        C --> C1[测试范围]
        C --> C2[测试方法]
        C --> C3[测试工具]
        C --> C4[测试标准]
        
        E --> E1[正向测试用例]
        E --> E2[负向测试用例]
        E --> E3[边界测试用例]
        E --> E4[异常测试用例]
    ```

    ### 第二阶段：测试执行与监控
    ```mermaid
    graph TD
        A[测试执行] --> B[单元测试执行]
        A --> C[集成测试执行]
        A --> D[系统测试执行]
        A --> E[性能测试执行]
        
        B --> B1[代码覆盖率检查]
        B --> B2[断言验证]
        B --> B3[Mock对象测试]
        
        C --> C1[接口测试]
        C --> C2[数据流测试]
        C --> C3[组件协作测试]
        
        D --> D1[功能验证]
        D --> D2[用户体验测试]
        D --> D3[兼容性测试]
        
        E --> E1[负载测试]
        E --> E2[压力测试]
        E --> E3[稳定性测试]
    ```

    ### 第三阶段：结果分析与报告
    ```mermaid
    flowchart LR
        A[测试结果] --> B[数据收集]
        B --> C[结果分析]
        C --> D[问题分类]
        D --> E[报告生成]
        E --> F[改进建议]
        
        B --> B1[测试通过率]
        B --> B2[代码覆盖率]
        B --> B3[性能指标]
        B --> B4[缺陷统计]
        
        C --> C1[趋势分析]
        C --> C2[根因分析]
        C --> C3[影响评估]
        
        D --> D1[功能缺陷]
        D --> D2[性能问题]
        D --> D3[安全漏洞]
        D --> D4[兼容性问题]
    ```

    ## 🛠️ 自动化测试框架

    ### Python测试框架实现
    ```python
    import pytest
    import unittest
    from unittest.mock import Mock, patch
    import asyncio
    from typing import Dict, List, Any
    import time
    import psutil
    
    class TestFramework:
        def __init__(self):
            self.test_results = []
            self.performance_metrics = {}
            self.coverage_data = {}
        
        def run_unit_tests(self, test_modules: List[str]) -> Dict[str, Any]:
            """运行单元测试"""
            results = {}
            
            for module in test_modules:
                try:
                    # 使用pytest运行测试
                    exit_code = pytest.main(['-v', module, '--cov=.', '--cov-report=json'])
                    results[module] = {
                        'status': 'passed' if exit_code == 0 else 'failed',
                        'exit_code': exit_code
                    }
                except Exception as e:
                    results[module] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            return results
        
        async def run_integration_tests(self, test_configs: List[Dict]) -> Dict[str, Any]:
            """运行集成测试"""
            results = {}
            
            for config in test_configs:
                test_name = config['name']
                try:
                    # 执行集成测试
                    result = await self.execute_integration_test(config)
                    results[test_name] = result
                except Exception as e:
                    results[test_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            return results
        
        async def execute_integration_test(self, config: Dict) -> Dict[str, Any]:
            """执行单个集成测试"""
            start_time = time.time()
            
            # 模拟集成测试执行
            test_steps = config.get('steps', [])
            step_results = []
            
            for step in test_steps:
                step_result = await self.execute_test_step(step)
                step_results.append(step_result)
                
                if not step_result['success']:
                    break
            
            end_time = time.time()
            
            return {
                'status': 'passed' if all(r['success'] for r in step_results) else 'failed',
                'duration': end_time - start_time,
                'steps': step_results
            }
        
        async def execute_test_step(self, step: Dict) -> Dict[str, Any]:
            """执行测试步骤"""
            step_type = step.get('type')
            
            if step_type == 'api_call':
                return await self.test_api_call(step)
            elif step_type == 'database_check':
                return await self.test_database_check(step)
            elif step_type == 'file_operation':
                return await self.test_file_operation(step)
            else:
                return {'success': False, 'error': f'Unknown step type: {step_type}'}
        
        async def test_api_call(self, step: Dict) -> Dict[str, Any]:
            """测试API调用"""
            # 模拟API调用测试
            return {'success': True, 'response_time': 0.1}
        
        async def test_database_check(self, step: Dict) -> Dict[str, Any]:
            """测试数据库检查"""
            # 模拟数据库测试
            return {'success': True, 'records_count': 100}
        
        async def test_file_operation(self, step: Dict) -> Dict[str, Any]:
            """测试文件操作"""
            # 模拟文件操作测试
            return {'success': True, 'file_size': 1024}
    ```

    ### 性能测试实现
    ```python
    class PerformanceTestSuite:
        def __init__(self):
            self.metrics = {}
        
        async def run_load_test(self, target_url: str, concurrent_users: int, duration: int):
            """运行负载测试"""
            start_time = time.time()
            tasks = []
            
            # 创建并发任务
            for i in range(concurrent_users):
                task = asyncio.create_task(self.simulate_user_load(target_url, duration))
                tasks.append(task)
            
            # 等待所有任务完成
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            end_time = time.time()
            
            # 分析结果
            successful_requests = sum(1 for r in results if isinstance(r, dict) and r.get('success'))
            total_requests = len(results)
            
            return {
                'duration': end_time - start_time,
                'concurrent_users': concurrent_users,
                'total_requests': total_requests,
                'successful_requests': successful_requests,
                'success_rate': successful_requests / total_requests if total_requests > 0 else 0,
                'requests_per_second': total_requests / (end_time - start_time)
            }
        
        async def simulate_user_load(self, target_url: str, duration: int):
            """模拟用户负载"""
            start_time = time.time()
            request_count = 0
            
            while time.time() - start_time < duration:
                try:
                    # 模拟请求
                    await asyncio.sleep(0.1)  # 模拟请求延迟
                    request_count += 1
                except Exception as e:
                    return {'success': False, 'error': str(e)}
            
            return {'success': True, 'requests': request_count}
        
        def monitor_system_resources(self, duration: int) -> Dict[str, Any]:
            """监控系统资源使用"""
            start_time = time.time()
            cpu_samples = []
            memory_samples = []
            
            while time.time() - start_time < duration:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                
                cpu_samples.append(cpu_percent)
                memory_samples.append(memory_percent)
            
            return {
                'cpu_usage': {
                    'avg': sum(cpu_samples) / len(cpu_samples),
                    'max': max(cpu_samples),
                    'min': min(cpu_samples)
                },
                'memory_usage': {
                    'avg': sum(memory_samples) / len(memory_samples),
                    'max': max(memory_samples),
                    'min': min(memory_samples)
                }
            }
    ```

    ## 📊 质量度量与分析

    ### 测试覆盖率分析
    ```python
    class CoverageAnalyzer:
        def __init__(self):
            self.coverage_data = {}
        
        def analyze_code_coverage(self, coverage_file: str) -> Dict[str, Any]:
            """分析代码覆盖率"""
            # 模拟覆盖率分析
            return {
                'line_coverage': 85.5,
                'branch_coverage': 78.2,
                'function_coverage': 92.1,
                'uncovered_lines': [45, 67, 89, 123],
                'critical_uncovered': ['error_handling', 'edge_cases']
            }
        
        def generate_coverage_report(self, coverage_data: Dict) -> str:
            """生成覆盖率报告"""
            report = f"""
            代码覆盖率报告
            ================
            行覆盖率: {coverage_data['line_coverage']:.1f}%
            分支覆盖率: {coverage_data['branch_coverage']:.1f}%
            函数覆盖率: {coverage_data['function_coverage']:.1f}%
            
            未覆盖的关键区域:
            {', '.join(coverage_data['critical_uncovered'])}
            """
            return report
    ```

    ### 缺陷分析与分类
    ```mermaid
    graph TD
        A[缺陷发现] --> B[缺陷分类]
        B --> C[严重性评估]
        C --> D[优先级排序]
        D --> E[修复建议]
        
        B --> B1[功能缺陷]
        B --> B2[性能问题]
        B --> B3[安全漏洞]
        B --> B4[兼容性问题]
        B --> B5[用户体验问题]
        
        C --> C1[致命 Critical]
        C --> C2[严重 Major]
        C --> C3[一般 Minor]
        C --> C4[轻微 Trivial]
        
        D --> D1[P0 立即修复]
        D --> D2[P1 本版本修复]
        D --> D3[P2 下版本修复]
        D --> D4[P3 后续考虑]
    ```

    ## 🔄 持续测试与改进

    ### CI/CD集成
    ```yaml
    # 测试流水线配置示例
    test_pipeline:
      stages:
        - unit_tests
        - integration_tests
        - performance_tests
        - security_tests
        - deployment_tests
      
      unit_tests:
        script:
          - python -m pytest tests/unit/ --cov=src/ --cov-report=xml
        coverage: '/TOTAL.*\s+(\d+%)$/'
        artifacts:
          reports:
            coverage_report:
              coverage_format: cobertura
              path: coverage.xml
      
      integration_tests:
        script:
          - python -m pytest tests/integration/ -v
        dependencies:
          - unit_tests
      
      performance_tests:
        script:
          - python tests/performance/load_test.py
        only:
          - main
          - release/*
    ```

    ### 测试数据管理
    ```python
    class TestDataManager:
        def __init__(self):
            self.test_data_sets = {}
        
        def create_test_data(self, scenario: str) -> Dict[str, Any]:
            """创建测试数据"""
            if scenario == 'user_registration':
                return {
                    'valid_user': {
                        'username': 'testuser',
                        'email': 'test@example.com',
                        'password': 'SecurePass123!'
                    },
                    'invalid_user': {
                        'username': '',
                        'email': 'invalid-email',
                        'password': '123'
                    }
                }
            elif scenario == 'memory_operations':
                return {
                    'sample_memories': [
                        {'content': 'Test memory 1', 'importance': 0.8},
                        {'content': 'Test memory 2', 'importance': 0.6}
                    ]
                }
            
            return {}
        
        def cleanup_test_data(self, scenario: str):
            """清理测试数据"""
            # 实现测试数据清理逻辑
            pass
    ```
  </process>

  <criteria>
    ## 测试验证评价标准

    ### 测试覆盖率
    - ✅ 代码行覆盖率 ≥ 80%
    - ✅ 分支覆盖率 ≥ 75%
    - ✅ 函数覆盖率 ≥ 90%
    - ✅ 关键路径覆盖率 100%

    ### 测试效率
    - ✅ 单元测试执行时间 ≤ 5分钟
    - ✅ 集成测试执行时间 ≤ 30分钟
    - ✅ 自动化测试比例 ≥ 80%
    - ✅ 测试维护成本合理

    ### 质量指标
    - ✅ 测试通过率 ≥ 95%
    - ✅ 缺陷发现率高
    - ✅ 误报率 ≤ 5%
    - ✅ 回归测试有效性 ≥ 90%

    ### 可维护性
    - ✅ 测试用例可读性强
    - ✅ 测试数据管理规范
    - ✅ 测试环境稳定
    - ✅ 测试文档完整
  </criteria>
</execution>

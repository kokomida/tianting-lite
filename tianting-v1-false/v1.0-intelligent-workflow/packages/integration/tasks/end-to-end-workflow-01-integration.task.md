// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业测试工程师的思维模式思考，遵循端到端测试最佳实践，确保系统集成的完整性、稳定性和用户体验一致性。我承诺：
- 以用户视角和业务流程为核心指导思想
- 先理解业务场景，再设计测试用例，通过自动化测试验证系统功能
- 确保所有测试覆盖天庭系统的关键用户流程
- 严格遵循测试金字塔原则和持续集成规范

## 执行承诺
我将遵循严格的执行流程，不偏离既定规范。我承诺：

**第一步：全面环境分析**
- 我将完整阅读任务环境(E)中列出的所有文档和资源，不遗漏任何细节
- 我将总结所有关键约束和规范要求，并解释每个约束对实现的影响
- 在完成环境分析后，我将明确声明："环境分析完成，现在开始分析目标"

**第二步：目标与计划制定**
- 我将基于环境分析结果理解任务目标，确保目标与环境约束兼容
- 我将制定周详的实现计划，考虑所有环境约束和测试要求
- 我将将实现计划与成功标准(S)进行对照验证
- 在完成目标分析后，我将明确声明："目标分析完成，现在制定实现计划"

**第三步：测试驱动实现**
- 我将严格按照用户流程优先级设计测试用例
- 每完成一个测试场景，我将立即运行验证其有效性
- 遇到测试失败时，我将使用详细日志和系统性方法分析根因
- 我将确保测试覆盖所有关键业务流程，不妥协测试质量
- 我将确保测试实现反映真实用户行为，而非仅为通过验收

**第四步：严格验证流程**
- 根据任务类型确定验证范围：集成任务重点验证跨组件协作和端到端流程
- 自我验证：
  * 我将执行完整的测试套件确保所有用例通过
  * 我将验证测试覆盖率达到关键流程的100%
  * 我将执行性能测试确保系统响应时间达标
  * 在验证通过后，我将明确声明："自我验证完成，集成测试通过，系统功能完整"

## 禁止事项（红线）
- 我绝不编写虚假的测试用例来掩盖系统缺陷
- 我绝不为了通过测试而降低测试标准或跳过重要场景
- 我绝不依赖猜测分析测试失败原因，而是使用系统性调试方法
- 如果我发现系统设计问题，我将明确报告而非在测试中规避
- 我绝不在未理清系统集成全貌的情况下，开始编写测试

## 调试规范
- 遇到集成测试失败时，我将：
  * 首先收集完整的系统日志和错误堆栈
  * 分析各组件间的数据流和状态变化
  * 验证接口契约和数据格式的一致性
  * 追踪问题根源至具体的集成点
  * 确认修复方案不会引入新的集成问题
- 当我需要调试性能问题时，我将：
  * 监控系统资源使用和响应时间
  * 分析数据库查询和网络通信效率
  * 识别性能瓶颈和优化机会
  * 验证优化后的系统稳定性

## 权利
- 我有权利在发现系统架构问题时停止测试并报告问题
- 我有权利在符合规范的情况下，发挥自身的能力，让测试更加全面和可靠

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 端到端工作流集成验证（集成任务）

**目标(O)**:
- **功能目标**:
  - 验证天庭系统完整的端到端用户工作流
  - 集成前端、API、Core三个包的完整数据流
  - 确保跨包协作的稳定性和一致性
  - 提供完整的系统集成测试和验证

- **执行任务**:
  - 创建文件:
    - `packages/integration/tests/e2e/full_workflow.test.ts` - 端到端测试
    - `packages/integration/tests/integration/api_core_integration.test.py` - API-Core集成测试
    - `packages/integration/tests/integration/frontend_api_integration.test.tsx` - 前端-API集成测试
    - `packages/integration/scripts/start_all_services.sh` - 启动所有服务脚本
    - `packages/integration/scripts/run_integration_tests.sh` - 集成测试运行脚本
    - `packages/integration/docker/docker-compose.integration.yml` - 集成测试环境
    - `packages/integration/src/test_data/sample_requirements.json` - 测试数据集
    - `packages/integration/src/validators/workflow_validator.py` - 工作流验证器
    - `packages/integration/src/monitors/performance_monitor.py` - 性能监控器
    - `packages/integration/docs/integration-test-report.md` - 集成测试报告模板
  - 修改文件:
    - `packages/integration/package.json` - 集成测试依赖
    - 各包的配置文件 - 集成环境配置
  - 实现功能:
    - 完整的用户需求到项目规划的端到端流程验证
    - 跨包数据一致性检查
    - 性能基准测试和监控
    - 错误场景和异常处理验证
    - 并发用户场景测试

- **任务边界**:
  - 包含完整系统集成，不包含单个包的单元测试
  - 包含性能测试，不包含压力测试和安全测试
  - 包含功能验证，不包含UI/UX详细测试
  - 专注于集成验证，不涉及生产环境部署

**环境(E)**:
- **参考资源**:
  - `packages/shared/src/types/` - 所有共享类型定义
  - `packages/common/contracts/api-contracts.md` - API接口规范
  - `packages/common/environments/dev-environment-setup.md` - 开发环境配置
  - `packages/core/tasks/core-integration-01-integration.task.md` - Core包集成任务
  - 各包的基础任务文件 - 了解实现细节

- **上下文信息**:
  - 任务定位：integration包负责跨包集成验证和测试
  - 依赖关系：依赖shared、core、api、frontend所有包
  - 环境要求：需要完整的多服务环境（数据库、API、前端）
  - 测试范围：端到端用户工作流 + 跨包接口 + 性能基准
  - 验证标准：功能完整性 + 数据一致性 + 性能达标

- **规范索引**:
  - 端到端测试最佳实践
  - 微服务集成测试标准
  - 性能基准测试方法
  - 测试自动化和CI/CD标准

- **注意事项**:
  - 集成测试必须能够独立运行，不依赖外部服务
  - 测试数据必须覆盖典型场景和边界情况
  - 性能测试需要可重复和可比较
  - 错误场景测试必须覆盖所有可能的失败点

**实现指导(I)**:
- **算法与流程**:
  - 端到端测试流程:
    ```
    环境准备 → 服务启动 → 数据准备 → 测试执行 → 结果验证 → 环境清理
    ```
  - 集成验证流程:
    ```
    接口测试 → 数据流验证 → 性能测试 → 异常处理测试 → 并发测试 → 报告生成
    ```

- **技术选型**:
  - E2E测试：Playwright (现代端到端测试)
  - API测试：pytest + httpx (Python集成测试)
  - 前端测试：Jest + React Testing Library
  - 性能测试：Artillery.io (负载测试)
  - 容器化：Docker Compose (测试环境)
  - 监控：Prometheus + Grafana (性能监控)

- **代码模式**:
  - 端到端测试:
    ```typescript
    import { test, expect } from '@playwright/test';
    
    test.describe('天庭系统端到端工作流', () => {
      test.beforeEach(async ({ page }) => {
        // 确保所有服务正在运行
        await page.goto('http://localhost:3001');
        await expect(page).toHaveTitle(/天庭系统/);
      });
      
      test('完整的需求到规划工作流', async ({ page }) => {
        // 1. 访问首页
        await page.goto('http://localhost:3001');
        
        // 2. 导航到需求输入页面
        await page.click('text=开始规划项目');
        await expect(page).toHaveURL(/.*\/requirement/);
        
        // 3. 输入需求描述
        const requirementText = `
          我要开发一个在线学习平台，功能包括：
          1. 用户注册登录，支持邮箱和手机验证
          2. 课程管理，教师可以创建课程、上传视频、发布作业
          3. 学习功能，学生可以购买课程、观看视频、提交作业
          4. 支付系统，集成支付宝和微信支付
          5. 管理后台，管理员可以管理用户、课程、订单
          6. 移动端APP，支持iOS和Android
          预算在50万以内，希望3个月内完成
        `;
        
        await page.fill('textarea[placeholder*="详细描述"]', requirementText);
        
        // 4. 提交需求解析
        await page.click('button:has-text("开始规划项目")');
        
        // 5. 等待解析完成（WebSocket实时更新）
        await expect(page.locator('text=正在分析需求')).toBeVisible();
        await expect(page.locator('text=正在生成规划')).toBeVisible();
        
        // 6. 验证规划结果
        await expect(page).toHaveURL(/.*\/project\/.+/);
        await expect(page.locator('h1:has-text("项目规划")')).toBeVisible();
        
        // 7. 验证规划内容
        await expect(page.locator('text=在线学习平台')).toBeVisible();
        await expect(page.locator('text=用户管理模块')).toBeVisible();
        await expect(page.locator('text=课程管理模块')).toBeVisible();
        await expect(page.locator('text=支付系统模块')).toBeVisible();
        
        // 8. 验证估算信息
        await expect(page.locator('text=预计工期')).toBeVisible();
        await expect(page.locator('text=预算估算')).toBeVisible();
        
        // 9. 验证下载功能
        const downloadPromise = page.waitForEvent('download');
        await page.click('button:has-text("下载规划")');
        const download = await downloadPromise;
        expect(download.suggestedFilename()).toMatch(/.*\.pdf$/);
      });
      
      test('WebSocket实时通信测试', async ({ page }) => {
        await page.goto('http://localhost:3001/requirement');
        
        // 监听WebSocket消息
        const wsMessages: any[] = [];
        await page.evaluate(() => {
          const ws = new WebSocket('ws://localhost:8002/api/requirements/parse/ws');
          ws.onmessage = (event) => {
            (window as any).wsMessages = (window as any).wsMessages || [];
            (window as any).wsMessages.push(JSON.parse(event.data));
          };
        });
        
        // 提交需求
        await page.fill('textarea', '开发一个简单的博客系统');
        await page.click('button:has-text("开始规划项目")');
        
        // 验证WebSocket消息
        await page.waitForFunction(() => {
          const messages = (window as any).wsMessages || [];
          return messages.some((msg: any) => msg.type === 'progress');
        });
        
        const messages = await page.evaluate(() => (window as any).wsMessages);
        expect(messages).toHaveLength.greaterThan(0);
        expect(messages[0]).toHaveProperty('type', 'progress');
      });
    });
    ```
  - API-Core集成测试:
    ```python
    import pytest
    import asyncio
    import httpx
    from packages.core.src.requirement_parser import RequirementParser
    from packages.core.src.project_planner import ProjectPlanner
    
    class TestApiCoreIntegration:
        @pytest.fixture
        async def api_client(self):
            async with httpx.AsyncClient(base_url="http://localhost:8002") as client:
                # 等待API服务启动
                for _ in range(30):
                    try:
                        response = await client.get("/health")
                        if response.status_code == 200:
                            break
                    except:
                        await asyncio.sleep(1)
                else:
                    pytest.fail("API服务启动失败")
                
                yield client
        
        @pytest.fixture
        async def core_client(self):
            async with httpx.AsyncClient(base_url="http://localhost:8001") as client:
                # 等待Core服务启动
                for _ in range(30):
                    try:
                        response = await client.get("/health")
                        if response.status_code == 200:
                            break
                    except:
                        await asyncio.sleep(1)
                else:
                    pytest.fail("Core服务启动失败")
                
                yield client
        
        async def test_requirement_parsing_integration(self, api_client, core_client):
            # 测试数据
            test_requirement = {
                "user_input": "开发一个电商平台，支持商品管理、订单处理、用户管理、支付功能"
            }
            
            # 1. 通过API调用需求解析
            api_response = await api_client.post(
                "/api/requirements/parse",
                json=test_requirement
            )
            
            assert api_response.status_code == 200
            api_result = api_response.json()
            assert api_result["success"] is True
            
            # 2. 直接调用Core服务验证
            core_response = await core_client.post(
                "/core/requirements/parse",
                json=test_requirement
            )
            
            assert core_response.status_code == 200
            core_result = core_response.json()
            
            # 3. 验证结果一致性
            assert api_result["data"]["project_type"] == core_result["data"]["project_type"]
            assert api_result["data"]["confidence_score"] == core_result["data"]["confidence_score"]
            
            # 4. 验证数据格式
            requirement_data = api_result["data"]
            assert "id" in requirement_data
            assert "user_input" in requirement_data
            assert "parsed_data" in requirement_data
            assert "confidence_score" in requirement_data
            
            # 5. 验证业务逻辑
            parsed_data = requirement_data["parsed_data"]
            assert parsed_data["project_type"] == "web_app"
            assert len(parsed_data["core_features"]) > 0
            assert requirement_data["confidence_score"] > 0.5
        
        async def test_project_planning_integration(self, api_client):
            # 1. 先解析需求
            requirement_response = await api_client.post(
                "/api/requirements/parse",
                json={"user_input": "开发一个在线学习平台"}
            )
            
            requirement_id = requirement_response.json()["data"]["id"]
            
            # 2. 生成项目规划
            planning_response = await api_client.post(
                "/api/projects/generate",
                json={"requirement_id": requirement_id}
            )
            
            assert planning_response.status_code == 200
            planning_result = planning_response.json()
            assert planning_result["success"] is True
            
            # 3. 验证规划结果
            project_plan = planning_result["data"]
            assert "project_id" in project_plan
            assert "modules" in project_plan
            assert "phases" in project_plan
            assert "timeline" in project_plan
            assert "budget" in project_plan
            
            # 4. 验证模块内容
            modules = project_plan["modules"]
            assert len(modules) > 0
            for module in modules:
                assert "name" in module
                assert "type" in module
                assert "estimated_complexity" in module
        
        async def test_performance_benchmarks(self, api_client):
            import time
            
            # 性能基准测试
            test_cases = [
                "开发一个简单的博客系统",
                "构建一个复杂的电商平台，包含商品管理、订单处理、用户系统、支付功能、数据分析等",
                "创建一个移动端社交应用"
            ]
            
            results = []
            
            for test_input in test_cases:
                start_time = time.time()
                
                response = await api_client.post(
                    "/api/requirements/parse",
                    json={"user_input": test_input}
                )
                
                end_time = time.time()
                processing_time = end_time - start_time
                
                assert response.status_code == 200
                result = response.json()
                assert result["success"] is True
                
                results.append({
                    "input_length": len(test_input),
                    "processing_time": processing_time,
                    "confidence_score": result["data"]["confidence_score"]
                })
            
            # 验证性能指标
            avg_processing_time = sum(r["processing_time"] for r in results) / len(results)
            assert avg_processing_time < 30.0, f"平均处理时间过长: {avg_processing_time}秒"
            
            # 验证质量指标
            avg_confidence = sum(r["confidence_score"] for r in results) / len(results)
            assert avg_confidence > 0.7, f"平均置信度过低: {avg_confidence}"
    ```
  - 性能监控器:
    ```python
    import time
    import psutil
    import asyncio
    from dataclasses import dataclass
    from typing import Dict, List
    
    @dataclass
    class PerformanceMetrics:
        timestamp: float
        cpu_usage: float
        memory_usage: float
        response_time: float
        throughput: float
        error_rate: float
    
    class PerformanceMonitor:
        def __init__(self):
            self.metrics: List[PerformanceMetrics] = []
            self.start_time = time.time()
        
        async def collect_system_metrics(self) -> Dict:
            return {
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_io": psutil.net_io_counters()._asdict()
            }
        
        async def benchmark_api_performance(self, api_client, test_cases: List[str]) -> Dict:
            results = {
                "total_requests": len(test_cases),
                "successful_requests": 0,
                "failed_requests": 0,
                "total_time": 0,
                "response_times": []
            }
            
            for test_case in test_cases:
                start_time = time.time()
                
                try:
                    response = await api_client.post(
                        "/api/requirements/parse",
                        json={"user_input": test_case}
                    )
                    
                    if response.status_code == 200:
                        results["successful_requests"] += 1
                    else:
                        results["failed_requests"] += 1
                        
                except Exception:
                    results["failed_requests"] += 1
                
                end_time = time.time()
                response_time = end_time - start_time
                results["response_times"].append(response_time)
                results["total_time"] += response_time
            
            # 计算统计指标
            response_times = results["response_times"]
            results["avg_response_time"] = sum(response_times) / len(response_times)
            results["min_response_time"] = min(response_times)
            results["max_response_time"] = max(response_times)
            results["success_rate"] = results["successful_requests"] / results["total_requests"]
            
            return results
        
        def generate_performance_report(self) -> str:
            if not self.metrics:
                return "没有性能数据"
            
            report = f"""
# 天庭系统性能测试报告

## 测试概览
- 测试开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_time))}
- 测试持续时间: {time.time() - self.start_time:.2f}秒
- 数据点数量: {len(self.metrics)}

## 性能指标
- 平均CPU使用率: {sum(m.cpu_usage for m in self.metrics) / len(self.metrics):.2f}%
- 平均内存使用率: {sum(m.memory_usage for m in self.metrics) / len(self.metrics):.2f}%
- 平均响应时间: {sum(m.response_time for m in self.metrics) / len(self.metrics):.2f}秒
- 平均吞吐量: {sum(m.throughput for m in self.metrics) / len(self.metrics):.2f} req/s
- 平均错误率: {sum(m.error_rate for m in self.metrics) / len(self.metrics):.2f}%

## 性能趋势
[这里可以添加性能趋势图表]

## 建议
基于性能测试结果，建议：
1. 如果CPU使用率持续高于80%，考虑优化算法或增加计算资源
2. 如果内存使用率持续高于80%，考虑优化内存使用或增加内存
3. 如果响应时间超过30秒，考虑优化AI服务调用或增加缓存
4. 如果错误率超过5%，需要检查错误处理机制
"""
            return report
    ```

- **实现策略**:
  1. 建立集成测试环境和Docker配置
  2. 实现端到端测试用例
  3. 开发跨包集成测试
  4. 建立性能基准测试和监控
  5. 实现自动化测试脚本
  6. 生成集成测试报告

- **调试指南**:
  - 集成测试调试:
    ```bash
    # 启动所有服务
    ./packages/integration/scripts/start_all_services.sh
    
    # 检查服务状态
    curl http://localhost:8001/health  # Core服务
    curl http://localhost:8002/health  # API服务
    curl http://localhost:3001         # 前端服务
    
    # 运行集成测试
    ./packages/integration/scripts/run_integration_tests.sh
    
    # 查看测试日志
    docker-compose -f packages/integration/docker/docker-compose.integration.yml logs
    ```

**成功标准(S)**:
- **基础达标**:
  - 所有集成测试通过，端到端工作流正常运行
  - 跨包接口调用成功，数据格式一致
  - 性能测试达标，响应时间在预期范围内
  - 错误处理机制有效，异常情况能够优雅处理
  - 自动化测试脚本运行正常

- **预期品质**:
  - 端到端响应时间<60秒，成功率≥95%
  - 跨包数据一致性100%，无数据丢失或格式错误
  - 系统资源使用合理，CPU<80%，内存<80%
  - 并发处理能力良好，支持多用户同时使用
  - 测试覆盖率≥90%，包含主要功能和异常场景

- **卓越表现**:
  - 实现智能的性能优化和自适应调整
  - 支持大规模并发和压力测试
  - 实现全面的监控和告警机制
  - 提供详细的测试报告和性能分析
  - 集成CI/CD流水线和自动化部署
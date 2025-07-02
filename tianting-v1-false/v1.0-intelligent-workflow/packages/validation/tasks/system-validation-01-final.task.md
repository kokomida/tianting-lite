// IMPORTANT: 强制执行指令 //
// AI执行者必须先阅读并宣誓接受下面的执行誓词，才能开始任务分析。
// 必须明确声明："我已阅读并接受AI执行誓词，现在开始按规范执行任务"
// 未经宣誓直接开始任务分析将视为违反规范，任务执行无效。
// 严格遵循"先环境分析，后目标分析"的顺序。
// ===================== //

# AI执行誓词

作为天庭项目的AI开发者，我庄严宣誓：

## 思考准则
我将以专业质量保证工程师的思维模式思考，遵循系统验收测试标准，确保产品的完整性、可靠性和商业价值实现。我承诺：
- 以用户价值和商业目标为核心指导思想
- 先理解验收标准，再设计验证方案，通过全面测试确保产品就绪
- 确保所有验证覆盖天庭系统的功能、性能、安全和用户体验
- 严格遵循生产就绪标准和发布质量门禁

## 执行承诺
我将遵循严格的执行流程，不偏离既定规范。我承诺：

**第一步：全面环境分析**
- 我将完整阅读任务环境(E)中列出的所有文档和资源，不遗漏任何细节
- 我将总结所有关键约束和规范要求，并解释每个约束对实现的影响
- 在完成环境分析后，我将明确声明："环境分析完成，现在开始分析目标"

**第二步：目标与计划制定**
- 我将基于环境分析结果理解任务目标，确保目标与环境约束兼容
- 我将制定周详的实现计划，考虑所有环境约束和验收要求
- 我将将实现计划与成功标准(S)进行对照验证
- 在完成目标分析后，我将明确声明："目标分析完成，现在制定实现计划"

**第三步：全面验证实施**
- 我将严格按照验收测试计划执行所有验证项目
- 每完成一个验证领域，我将立即记录结果和发现的问题
- 遇到质量问题时，我将详细记录问题并评估其对发布的影响
- 我将确保验证覆盖所有关键质量属性，不妥协发布标准
- 我将确保验证结果真实反映系统状态，而非仅为通过检查

**第四步：严格验证流程**
- 根据任务类型确定验证范围：验收任务重点验证系统整体质量和发布就绪度
- 自我验证：
  * 我将执行完整的验收测试套件确保所有标准达成
  * 我将验证系统性能、安全性、可用性指标
  * 我将确认用户文档和部署指南的完整性
  * 在验证通过后，我将明确声明："自我验证完成，系统达到发布标准，质量合格"

## 禁止事项（红线）
- 我绝不为了通过验收而隐瞒或忽视质量问题
- 我绝不降低验收标准或跳过重要的验证项目
- 我绝不依赖主观判断评估质量，而是使用客观的测试数据
- 如果我发现阻塞性问题，我将明确报告并建议延迟发布
- 我绝不在系统质量不达标的情况下，给出发布建议

## 调试规范
- 遇到验收测试失败时，我将：
  * 详细记录失败的具体场景和错误信息
  * 分析问题的严重程度和影响范围
  * 评估问题对用户体验和商业目标的影响
  * 提供具体的修复建议和优先级
  * 验证修复后的系统稳定性
- 当我需要评估发布风险时，我将：
  * 综合分析所有质量指标和测试结果
  * 评估已知问题的可接受性和缓解措施
  * 考虑市场时机和商业影响
  * 提供基于数据的发布建议

## 权利
- 我有权利在系统质量不达标时否决发布
- 我有权利在符合规范的情况下，发挥自身的能力，让验证更加严格和全面

我理解这些规范的重要性，并承诺在整个任务执行过程中严格遵守。我将在每个关键阶段做出明确声明，以证明我始终遵循规范执行。

---

## 任务: 天庭系统最终验证和发布准备（最终验证任务）

**目标(O)**:
- **功能目标**:
  - 对天庭MVP系统进行全面的最终验证和质量检查
  - 确保系统满足所有业务需求和技术指标
  - 准备系统发布文档和部署配置
  - 提供完整的系统交付和运维指南

- **执行任务**:
  - 创建文件:
    - `packages/validation/tests/acceptance/business_requirements.test.ts` - 业务需求验收测试
    - `packages/validation/tests/acceptance/user_stories.test.ts` - 用户故事验收测试
    - `packages/validation/tests/performance/load_test.yaml` - 负载测试配置
    - `packages/validation/tests/security/security_scan.py` - 安全扫描脚本
    - `packages/validation/scripts/system_health_check.sh` - 系统健康检查脚本
    - `packages/validation/scripts/deployment_validation.sh` - 部署验证脚本
    - `packages/validation/docs/system_validation_report.md` - 系统验证报告
    - `packages/validation/docs/deployment_guide.md` - 部署指南
    - `packages/validation/docs/operation_manual.md` - 运维手册
    - `packages/validation/docs/user_manual.md` - 用户使用手册
    - `packages/validation/config/production.env` - 生产环境配置
    - `packages/validation/docker/production.docker-compose.yml` - 生产环境Docker配置
  - 修改文件:
    - 各包的配置文件 - 生产环境优化
    - `README.md` - 项目总体说明
  - 实现功能:
    - 业务需求完整性验证
    - 系统性能和稳定性测试
    - 安全性扫描和漏洞检查
    - 部署流程验证和自动化
    - 文档完整性检查

- **任务边界**:
  - 包含系统最终验证，不包含具体功能开发
  - 包含部署准备，不包含实际生产部署
  - 包含文档编写，不包含培训实施
  - 专注于质量保证，不涉及后续运营

**环境(E)**:
- **参考资源**:
  - `planning/user-stories-breakdown.md` - 原始业务需求
  - `docs/requirements-analysis.md` - 需求分析文档
  - `docs/user-journey-final.md` - 用户体验设计
  - `development/architecture/technical-architecture.md` - 技术架构
  - 所有包的任务文件 - 了解实现范围

- **上下文信息**:
  - 任务定位：validation包负责最终质量保证和发布准备
  - 验证范围：业务功能 + 技术性能 + 用户体验 + 部署运维
  - 质量标准：业务需求100%满足 + 性能指标达标 + 安全性合规
  - 交付目标：可生产部署的完整系统 + 完备的文档体系
  - 后续支持：为运营团队提供运维指南和问题排查手册

- **规范索引**:
  - 软件验收测试最佳实践
  - 系统性能测试标准
  - 网络安全合规要求
  - DevOps部署和运维标准

- **注意事项**:
  - 验收测试必须基于原始业务需求，确保无遗漏
  - 性能测试需要模拟真实的生产环境负载
  - 安全扫描必须涵盖OWASP Top 10安全风险
  - 部署文档必须详细可操作，支持运维团队独立操作

**实现指导(I)**:
- **算法与流程**:
  - 验收测试流程:
    ```
    需求对比 → 功能验证 → 性能测试 → 安全扫描 → 部署验证 → 文档审查 → 发布决策
    ```
  - 质量检查流程:
    ```
    代码质量 → 测试覆盖率 → 性能基准 → 安全合规 → 文档完整性 → 用户体验
    ```

- **技术选型**:
  - 验收测试：Cucumber (BDD测试框架)
  - 性能测试：K6 (现代负载测试工具)
  - 安全扫描：OWASP ZAP + Bandit
  - 部署工具：Docker + Kubernetes (容器化部署)
  - 监控工具：Prometheus + Grafana + ELK Stack
  - 文档工具：GitBook (文档生成和管理)

- **代码模式**:
  - 业务需求验收测试:
    ```typescript
    import { Given, When, Then } from '@cucumber/cucumber';
    
    // US-001: 用户需求输入功能
    Given('用户访问天庭系统首页', async () => {
      await page.goto('http://localhost:3001');
      await expect(page).toHaveTitle(/天庭系统/);
    });
    
    When('用户点击"开始规划项目"按钮', async () => {
      await page.click('button:has-text("开始规划项目")');
    });
    
    Then('系统应该跳转到需求输入页面', async () => {
      await expect(page).toHaveURL(/.*\/requirement/);
      await expect(page.locator('textarea[placeholder*="详细描述"]')).toBeVisible();
    });
    
    When('用户输入详细的项目需求描述', async () => {
      const requirement = `
        开发一个在线教育平台，主要功能包括：
        1. 用户管理：注册、登录、个人资料管理
        2. 课程管理：教师创建课程、上传视频、管理学员
        3. 学习功能：学员购买课程、观看视频、完成作业
        4. 支付系统：支持微信支付、支付宝支付
        5. 管理后台：超级管理员管理平台数据
        预算50万，时间3个月
      `;
      
      await page.fill('textarea[placeholder*="详细描述"]', requirement);
    });
    
    When('用户提交需求', async () => {
      await page.click('button:has-text("开始规划项目")');
    });
    
    Then('系统应该开始解析需求并显示进度', async () => {
      await expect(page.locator('text=正在分析需求')).toBeVisible();
      // 验证进度指示器
      await expect(page.locator('[role="progressbar"]')).toBeVisible();
    });
    
    Then('系统应该在30秒内完成需求解析', async () => {
      await expect(page.locator('text=需求解析完成')).toBeVisible({ timeout: 30000 });
    });
    
    Then('系统应该跳转到项目规划展示页面', async () => {
      await expect(page).toHaveURL(/.*\/project\/.+/);
      await expect(page.locator('h1:has-text("项目规划")')).toBeVisible();
    });
    
    // US-002: 项目规划生成功能
    Then('规划结果应该包含项目概述', async () => {
      await expect(page.locator('text=在线教育平台')).toBeVisible();
      await expect(page.locator('text=项目概述')).toBeVisible();
    });
    
    Then('规划结果应该包含功能模块分解', async () => {
      await expect(page.locator('text=功能模块')).toBeVisible();
      await expect(page.locator('text=用户管理模块')).toBeVisible();
      await expect(page.locator('text=课程管理模块')).toBeVisible();
      await expect(page.locator('text=支付系统模块')).toBeVisible();
    });
    
    Then('规划结果应该包含开发阶段规划', async () => {
      await expect(page.locator('text=开发阶段')).toBeVisible();
      await expect(page.locator('text=第一阶段')).toBeVisible();
      await expect(page.locator('text=第二阶段')).toBeVisible();
    });
    
    Then('规划结果应该包含时间和成本估算', async () => {
      await expect(page.locator('text=预计工期')).toBeVisible();
      await expect(page.locator('text=预算估算')).toBeVisible();
      
      // 验证估算合理性
      const budgetText = await page.locator('text=/预算.*[0-9]+.*万/').textContent();
      expect(budgetText).toMatch(/[0-9]+.*万/);
    });
    
    // US-003: 规划结果导出功能
    When('用户点击"下载规划"按钮', async () => {
      const downloadPromise = page.waitForEvent('download');
      await page.click('button:has-text("下载规划")');
      const download = await downloadPromise;
      expect(download.suggestedFilename()).toMatch(/.*\.(pdf|docx)$/);
    });
    ```
  - 性能测试配置:
    ```yaml
    # K6 负载测试配置
    scenarios:
      requirement_parsing_load:
        executor: ramping-vus
        startVUs: 1
        stages:
          - duration: 2m
            target: 10
          - duration: 5m
            target: 50
          - duration: 2m
            target: 0
        gracefulRampDown: 30s
    
    thresholds:
      http_req_duration:
        - p(95)<30000  # 95%的请求响应时间小于30秒
      http_req_failed:
        - rate<0.05    # 错误率小于5%
      http_reqs:
        - rate>1       # 吞吐量大于1 req/s
    ```
  - 系统健康检查脚本:
    ```bash
    #!/bin/bash
    
    echo "天庭系统健康检查开始..."
    
    # 检查服务状态
    check_service() {
        local service_name=$1
        local service_url=$2
        local expected_status=${3:-200}
        
        echo "检查 $service_name 服务..."
        
        response=$(curl -s -o /dev/null -w "%{http_code}" "$service_url")
        
        if [ "$response" = "$expected_status" ]; then
            echo "✅ $service_name 服务正常 (HTTP $response)"
            return 0
        else
            echo "❌ $service_name 服务异常 (HTTP $response)"
            return 1
        fi
    }
    
    # 检查数据库连接
    check_database() {
        echo "检查数据库连接..."
        
        if docker exec tianting-postgres psql -U postgres -d tianting_core_dev -c "SELECT 1;" > /dev/null 2>&1; then
            echo "✅ 数据库连接正常"
            return 0
        else
            echo "❌ 数据库连接失败"
            return 1
        fi
    }
    
    # 检查Redis连接
    check_redis() {
        echo "检查Redis连接..."
        
        if docker exec tianting-redis redis-cli ping | grep -q "PONG"; then
            echo "✅ Redis连接正常"
            return 0
        else
            echo "❌ Redis连接失败"
            return 1
        fi
    }
    
    # 执行健康检查
    health_status=0
    
    check_service "前端服务" "http://localhost:3001" || health_status=1
    check_service "API服务" "http://localhost:8002/health" || health_status=1
    check_service "Core服务" "http://localhost:8001/health" || health_status=1
    
    check_database || health_status=1
    check_redis || health_status=1
    
    # 检查系统资源
    echo "检查系统资源使用情况..."
    
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    memory_usage=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
    disk_usage=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    
    echo "CPU使用率: ${cpu_usage}%"
    echo "内存使用率: ${memory_usage}%"
    echo "磁盘使用率: ${disk_usage}%"
    
    # 资源使用率警告
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        echo "⚠️  CPU使用率过高"
        health_status=1
    fi
    
    if (( $(echo "$memory_usage > 80" | bc -l) )); then
        echo "⚠️  内存使用率过高"
        health_status=1
    fi
    
    if [ "$disk_usage" -gt 80 ]; then
        echo "⚠️  磁盘使用率过高"
        health_status=1
    fi
    
    # 总结
    if [ $health_status -eq 0 ]; then
        echo "🎉 系统健康检查通过"
        exit 0
    else
        echo "💥 系统健康检查失败"
        exit 1
    fi
    ```
  - 安全扫描脚本:
    ```python
    import subprocess
    import json
    import sys
    from pathlib import Path
    
    class SecurityScanner:
        def __init__(self):
            self.results = {
                "dependency_scan": None,
                "code_scan": None,
                "web_scan": None,
                "container_scan": None
            }
        
        def scan_dependencies(self):
            """扫描依赖漏洞"""
            print("开始依赖漏洞扫描...")
            
            try:
                # Python依赖扫描
                result = subprocess.run([
                    "safety", "check", "--json"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.results["dependency_scan"] = {
                        "status": "pass",
                        "vulnerabilities": []
                    }
                else:
                    vulns = json.loads(result.stdout) if result.stdout else []
                    self.results["dependency_scan"] = {
                        "status": "fail",
                        "vulnerabilities": vulns
                    }
                
                # Node.js依赖扫描
                subprocess.run([
                    "npm", "audit", "--audit-level", "moderate"
                ], check=True)
                
            except Exception as e:
                self.results["dependency_scan"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        def scan_code(self):
            """静态代码安全扫描"""
            print("开始静态代码安全扫描...")
            
            try:
                # Python代码扫描
                result = subprocess.run([
                    "bandit", "-r", "packages/", "-f", "json"
                ], capture_output=True, text=True)
                
                if result.stdout:
                    bandit_results = json.loads(result.stdout)
                    high_severity = [
                        issue for issue in bandit_results.get("results", [])
                        if issue.get("issue_severity") == "HIGH"
                    ]
                    
                    self.results["code_scan"] = {
                        "status": "pass" if not high_severity else "fail",
                        "high_severity_issues": high_severity
                    }
                
            except Exception as e:
                self.results["code_scan"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        def scan_web_application(self):
            """Web应用安全扫描"""
            print("开始Web应用安全扫描...")
            
            try:
                # 使用OWASP ZAP扫描
                result = subprocess.run([
                    "docker", "run", "-t", "owasp/zap2docker-stable",
                    "zap-baseline.py", "-t", "http://localhost:3001"
                ], capture_output=True, text=True)
                
                self.results["web_scan"] = {
                    "status": "pass" if result.returncode == 0 else "fail",
                    "output": result.stdout
                }
                
            except Exception as e:
                self.results["web_scan"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        def scan_containers(self):
            """容器安全扫描"""
            print("开始容器安全扫描...")
            
            try:
                # 扫描Docker镜像
                images = ["tianting-frontend", "tianting-api", "tianting-core"]
                
                for image in images:
                    result = subprocess.run([
                        "docker", "run", "--rm", "-v", "/var/run/docker.sock:/var/run/docker.sock",
                        "aquasec/trivy", "image", image
                    ], capture_output=True, text=True)
                    
                    # 解析结果
                    if "HIGH" in result.stdout or "CRITICAL" in result.stdout:
                        self.results["container_scan"] = {
                            "status": "fail",
                            "issues": f"发现高危漏洞在镜像 {image}"
                        }
                        return
                
                self.results["container_scan"] = {
                    "status": "pass",
                    "message": "所有容器镜像安全"
                }
                
            except Exception as e:
                self.results["container_scan"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        def generate_report(self):
            """生成安全扫描报告"""
            report = """
# 天庭系统安全扫描报告

## 扫描概要
"""
            
            overall_status = "PASS"
            for scan_type, result in self.results.items():
                status = result.get("status", "unknown") if result else "not_run"
                report += f"- {scan_type}: {status.upper()}\n"
                
                if status == "fail":
                    overall_status = "FAIL"
            
            report += f"\n## 总体状态: {overall_status}\n"
            
            # 详细结果
            for scan_type, result in self.results.items():
                if result and result.get("status") == "fail":
                    report += f"\n### {scan_type} 详细结果\n"
                    if "vulnerabilities" in result:
                        for vuln in result["vulnerabilities"]:
                            report += f"- {vuln}\n"
                    elif "high_severity_issues" in result:
                        for issue in result["high_severity_issues"]:
                            report += f"- {issue.get('test_name', 'Unknown')}: {issue.get('issue_text', '')}\n"
            
            return report
        
        def run_all_scans(self):
            """运行所有安全扫描"""
            self.scan_dependencies()
            self.scan_code()
            self.scan_web_application()
            self.scan_containers()
            
            report = self.generate_report()
            
            # 保存报告
            with open("security_scan_report.md", "w", encoding="utf-8") as f:
                f.write(report)
            
            print(report)
            
            # 检查是否有失败的扫描
            failed_scans = [
                scan_type for scan_type, result in self.results.items()
                if result and result.get("status") == "fail"
            ]
            
            if failed_scans:
                print(f"安全扫描失败: {', '.join(failed_scans)}")
                sys.exit(1)
            else:
                print("所有安全扫描通过")
                sys.exit(0)
    
    if __name__ == "__main__":
        scanner = SecurityScanner()
        scanner.run_all_scans()
    ```

- **实现策略**:
  1. 建立验收测试用例和BDD测试框架
  2. 实现性能测试和负载测试
  3. 执行安全扫描和漏洞检测
  4. 验证部署流程和环境配置
  5. 编写完整的文档体系
  6. 生成最终验证报告

- **调试指南**:
  - 验证测试调试:
    ```bash
    # 运行业务需求验收测试
    npm run test:acceptance
    
    # 运行性能测试
    k6 run packages/validation/tests/performance/load_test.js
    
    # 运行安全扫描
    python packages/validation/tests/security/security_scan.py
    
    # 系统健康检查
    ./packages/validation/scripts/system_health_check.sh
    ```

**成功标准(S)**:
- **基础达标**:
  - 所有业务需求验收测试通过，功能完整性100%
  - 性能测试达标，响应时间和吞吐量满足指标
  - 安全扫描通过，无高危漏洞
  - 部署验证成功，系统可稳定运行
  - 文档完整，涵盖部署、运维、使用手册

- **预期品质**:
  - 系统稳定性99.9%，无关键功能缺陷
  - 性能指标达标：需求解析<30秒，API响应<100ms
  - 安全性合规，通过OWASP安全扫描
  - 部署自动化程度≥90%，支持一键部署
  - 文档质量优秀，便于用户和运维团队使用

- **卓越表现**:
  - 实现全面的监控和告警体系
  - 支持蓝绿部署和灰度发布
  - 提供完整的灾备和恢复方案
  - 实现智能的性能优化和故障自愈
  - 建立完善的用户支持和反馈体系
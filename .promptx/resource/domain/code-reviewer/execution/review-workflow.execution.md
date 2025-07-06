<execution>
  <constraint>
    ## 代码审查限制条件
    - **时间约束**：代码审查不得显著延迟开发进度
    - **范围约束**：重点关注关键代码和高风险变更
    - **技能约束**：审查者必须具备相应技术栈的专业知识
    - **工具约束**：依赖静态分析工具的准确性和覆盖度
    - **人力约束**：审查资源有限，需要合理分配
  </constraint>

  <rule>
    ## 代码审查强制规则
    - **全覆盖原则**：所有生产代码必须经过审查
    - **双人审查**：关键代码必须至少两人审查
    - **文档同步**：代码变更必须同步更新文档
    - **测试要求**：新功能必须有相应的测试用例
    - **安全优先**：安全相关代码必须通过安全审查
  </rule>

  <guideline>
    ## 代码审查指导原则
    - **建设性反馈**：提供具体、可操作的改进建议
    - **知识分享**：通过审查过程传递最佳实践
    - **一致性维护**：确保代码风格和架构一致性
    - **质量提升**：持续提升代码质量和团队技能
    - **效率平衡**：在质量和效率间找到最佳平衡
  </guideline>

  <process>
    ## 👁️ 代码审查工作流程

    ### 代码审查架构
    ```mermaid
    graph TD
        A[代码提交] --> B[自动化检查]
        B --> C[人工审查]
        C --> D[反馈处理]
        D --> E[质量验证]
        E --> F[合并决策]
        
        B --> B1[静态分析]
        B --> B2[安全扫描]
        B --> B3[测试执行]
        B --> B4[覆盖率检查]
        
        C --> C1[代码质量审查]
        C --> C2[设计审查]
        C --> C3[安全审查]
        C --> C4[性能审查]
        
        D --> D1[问题修复]
        D --> D2[讨论澄清]
        D --> D3[知识分享]
        
        E --> E1[修复验证]
        E --> E2[回归测试]
        E --> E3[最终检查]
    ```

    ### 第一阶段：自动化预检查
    ```mermaid
    flowchart TD
        A[代码提交] --> B[格式检查]
        B --> C[语法检查]
        C --> D[静态分析]
        D --> E[安全扫描]
        E --> F[测试执行]
        F --> G[覆盖率分析]
        G --> H{检查通过?}
        H -->|是| I[进入人工审查]
        H -->|否| J[返回修复]
        
        B --> B1[代码格式化]
        B --> B2[命名规范]
        B --> B3[注释检查]
        
        C --> C1[语法错误]
        C --> C2[类型检查]
        C --> C3[导入检查]
        
        D --> D1[复杂度分析]
        D --> D2[重复代码检测]
        D --> D3[依赖分析]
        
        E --> E1[漏洞扫描]
        E --> E2[敏感信息检测]
        E --> E3[权限检查]
    ```

    ### 第二阶段：人工代码审查
    ```mermaid
    graph TD
        A[人工审查] --> B[代码质量审查]
        A --> C[架构设计审查]
        A --> D[业务逻辑审查]
        A --> E[性能审查]
        A --> F[安全审查]
        
        B --> B1[可读性]
        B --> B2[可维护性]
        B --> B3[代码规范]
        B --> B4[最佳实践]
        
        C --> C1[设计模式]
        C --> C2[架构一致性]
        C --> C3[模块耦合]
        C --> C4[接口设计]
        
        D --> D1[逻辑正确性]
        D --> D2[边界条件]
        D --> D3[错误处理]
        D --> D4[业务规则]
        
        E --> E1[算法效率]
        E --> E2[资源使用]
        E --> E3[并发安全]
        E --> E4[缓存策略]
        
        F --> F1[输入验证]
        F --> F2[权限控制]
        F --> F3[数据保护]
        F --> F4[注入防护]
    ```

    ### 第三阶段：反馈与改进
    ```mermaid
    flowchart LR
        A[审查反馈] --> B[问题分类]
        B --> C[优先级排序]
        C --> D[修复指导]
        D --> E[知识分享]
        E --> F[流程改进]
        
        B --> B1[严重问题]
        B --> B2[一般问题]
        B --> B3[建议改进]
        
        C --> C1[必须修复]
        C --> C2[建议修复]
        C --> C3[后续优化]
        
        D --> D1[具体建议]
        D --> D2[示例代码]
        D --> D3[参考资料]
        
        E --> E1[团队分享]
        E --> E2[文档更新]
        E --> E3[培训材料]
    ```

    ## 🛠️ 代码审查工具实现

    ### 静态代码分析器
    ```python
    import ast
    import re
    from typing import List, Dict, Any, Set
    from dataclasses import dataclass
    from enum import Enum
    import logging

    class IssueSeverity(Enum):
        CRITICAL = "critical"
        MAJOR = "major"
        MINOR = "minor"
        INFO = "info"

    @dataclass
    class CodeIssue:
        file_path: str
        line_number: int
        column: int
        severity: IssueSeverity
        category: str
        message: str
        rule_id: str
        suggestion: str = ""

    class PythonCodeAnalyzer:
        def __init__(self):
            self.logger = logging.getLogger(__name__)
            self.issues: List[CodeIssue] = []
        
        def analyze_file(self, file_path: str, content: str) -> List[CodeIssue]:
            """分析Python文件"""
            self.issues = []
            
            try:
                tree = ast.parse(content)
                
                # 执行各种检查
                self._check_complexity(tree, file_path)
                self._check_naming_conventions(tree, file_path)
                self._check_security_issues(tree, file_path, content)
                self._check_best_practices(tree, file_path)
                self._check_documentation(tree, file_path)
                
            except SyntaxError as e:
                self.issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=e.lineno or 0,
                    column=e.offset or 0,
                    severity=IssueSeverity.CRITICAL,
                    category="syntax",
                    message=f"Syntax error: {e.msg}",
                    rule_id="syntax_error"
                ))
            
            return self.issues
        
        def _check_complexity(self, tree: ast.AST, file_path: str):
            """检查代码复杂度"""
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_cyclomatic_complexity(node)
                    if complexity > 10:
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            column=node.col_offset,
                            severity=IssueSeverity.MAJOR,
                            category="complexity",
                            message=f"Function '{node.name}' has high cyclomatic complexity: {complexity}",
                            rule_id="high_complexity",
                            suggestion="Consider breaking this function into smaller functions"
                        ))
        
        def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
            """计算圈复杂度"""
            complexity = 1  # 基础复杂度
            
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1
                elif isinstance(child, ast.ExceptHandler):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
            
            return complexity
        
        def _check_naming_conventions(self, tree: ast.AST, file_path: str):
            """检查命名规范"""
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            column=node.col_offset,
                            severity=IssueSeverity.MINOR,
                            category="naming",
                            message=f"Function name '{node.name}' should be snake_case",
                            rule_id="function_naming",
                            suggestion="Use snake_case for function names"
                        ))
                
                elif isinstance(node, ast.ClassDef):
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            column=node.col_offset,
                            severity=IssueSeverity.MINOR,
                            category="naming",
                            message=f"Class name '{node.name}' should be PascalCase",
                            rule_id="class_naming",
                            suggestion="Use PascalCase for class names"
                        ))
        
        def _check_security_issues(self, tree: ast.AST, file_path: str, content: str):
            """检查安全问题"""
            # 检查SQL注入风险
            if 'execute(' in content and any(op in content for op in ['%', '.format(', 'f"']):
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and hasattr(node.func, 'attr'):
                        if node.func.attr == 'execute':
                            self.issues.append(CodeIssue(
                                file_path=file_path,
                                line_number=node.lineno,
                                column=node.col_offset,
                                severity=IssueSeverity.CRITICAL,
                                category="security",
                                message="Potential SQL injection vulnerability",
                                rule_id="sql_injection",
                                suggestion="Use parameterized queries instead of string formatting"
                            ))
            
            # 检查硬编码密码
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if any(keyword in target.id.lower() for keyword in ['password', 'secret', 'key', 'token']):
                                if isinstance(node.value, ast.Constant):
                                    self.issues.append(CodeIssue(
                                        file_path=file_path,
                                        line_number=node.lineno,
                                        column=node.col_offset,
                                        severity=IssueSeverity.CRITICAL,
                                        category="security",
                                        message=f"Hardcoded credential in variable '{target.id}'",
                                        rule_id="hardcoded_credential",
                                        suggestion="Use environment variables or secure configuration"
                                    ))
        
        def _check_best_practices(self, tree: ast.AST, file_path: str):
            """检查最佳实践"""
            for node in ast.walk(tree):
                # 检查过长的函数
                if isinstance(node, ast.FunctionDef):
                    line_count = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                    if line_count > 50:
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            column=node.col_offset,
                            severity=IssueSeverity.MAJOR,
                            category="best_practice",
                            message=f"Function '{node.name}' is too long ({line_count} lines)",
                            rule_id="long_function",
                            suggestion="Consider breaking this function into smaller functions"
                        ))
                
                # 检查空的except块
                if isinstance(node, ast.ExceptHandler):
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            column=node.col_offset,
                            severity=IssueSeverity.MAJOR,
                            category="best_practice",
                            message="Empty except block",
                            rule_id="empty_except",
                            suggestion="Handle exceptions properly or use specific exception types"
                        ))
        
        def _check_documentation(self, tree: ast.AST, file_path: str):
            """检查文档字符串"""
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            column=node.col_offset,
                            severity=IssueSeverity.MINOR,
                            category="documentation",
                            message=f"{type(node).__name__} '{node.name}' missing docstring",
                            rule_id="missing_docstring",
                            suggestion="Add a descriptive docstring"
                        ))
    ```

    ### 代码审查报告生成器
    ```python
    class CodeReviewReport:
        def __init__(self):
            self.issues: List[CodeIssue] = []
            self.metrics: Dict[str, Any] = {}
        
        def add_issues(self, issues: List[CodeIssue]):
            """添加问题列表"""
            self.issues.extend(issues)
        
        def calculate_metrics(self):
            """计算代码质量指标"""
            total_issues = len(self.issues)
            
            severity_counts = {
                IssueSeverity.CRITICAL: 0,
                IssueSeverity.MAJOR: 0,
                IssueSeverity.MINOR: 0,
                IssueSeverity.INFO: 0
            }
            
            category_counts = {}
            
            for issue in self.issues:
                severity_counts[issue.severity] += 1
                category_counts[issue.category] = category_counts.get(issue.category, 0) + 1
            
            # 计算质量分数 (0-100)
            quality_score = 100
            quality_score -= severity_counts[IssueSeverity.CRITICAL] * 20
            quality_score -= severity_counts[IssueSeverity.MAJOR] * 10
            quality_score -= severity_counts[IssueSeverity.MINOR] * 2
            quality_score = max(0, quality_score)
            
            self.metrics = {
                'total_issues': total_issues,
                'severity_distribution': {s.value: count for s, count in severity_counts.items()},
                'category_distribution': category_counts,
                'quality_score': quality_score,
                'review_status': self._determine_review_status(severity_counts)
            }
        
        def _determine_review_status(self, severity_counts: Dict[IssueSeverity, int]) -> str:
            """确定审查状态"""
            if severity_counts[IssueSeverity.CRITICAL] > 0:
                return "REJECTED"
            elif severity_counts[IssueSeverity.MAJOR] > 5:
                return "NEEDS_WORK"
            elif severity_counts[IssueSeverity.MAJOR] > 0 or severity_counts[IssueSeverity.MINOR] > 10:
                return "CONDITIONAL_APPROVAL"
            else:
                return "APPROVED"
        
        def generate_summary(self) -> str:
            """生成审查摘要"""
            if not self.metrics:
                self.calculate_metrics()
            
            summary = f"""
            代码审查报告
            ============
            
            审查状态: {self.metrics['review_status']}
            质量评分: {self.metrics['quality_score']}/100
            
            问题统计:
            - 严重问题: {self.metrics['severity_distribution']['critical']}
            - 重要问题: {self.metrics['severity_distribution']['major']}
            - 一般问题: {self.metrics['severity_distribution']['minor']}
            - 信息提示: {self.metrics['severity_distribution']['info']}
            
            问题分类:
            """
            
            for category, count in self.metrics['category_distribution'].items():
                summary += f"- {category}: {count}\n"
            
            return summary
        
        def generate_detailed_report(self) -> Dict[str, Any]:
            """生成详细报告"""
            if not self.metrics:
                self.calculate_metrics()
            
            # 按文件分组问题
            issues_by_file = {}
            for issue in self.issues:
                if issue.file_path not in issues_by_file:
                    issues_by_file[issue.file_path] = []
                issues_by_file[issue.file_path].append({
                    'line': issue.line_number,
                    'column': issue.column,
                    'severity': issue.severity.value,
                    'category': issue.category,
                    'message': issue.message,
                    'rule_id': issue.rule_id,
                    'suggestion': issue.suggestion
                })
            
            return {
                'summary': self.metrics,
                'issues_by_file': issues_by_file,
                'recommendations': self._generate_recommendations()
            }
        
        def _generate_recommendations(self) -> List[str]:
            """生成改进建议"""
            recommendations = []
            
            if self.metrics['severity_distribution']['critical'] > 0:
                recommendations.append("立即修复所有严重安全问题")
            
            if self.metrics['severity_distribution']['major'] > 5:
                recommendations.append("重构复杂度过高的函数")
            
            if self.metrics['category_distribution'].get('documentation', 0) > 0:
                recommendations.append("完善代码文档和注释")
            
            if self.metrics['category_distribution'].get('naming', 0) > 0:
                recommendations.append("统一命名规范")
            
            if self.metrics['quality_score'] < 80:
                recommendations.append("建议进行代码重构以提升整体质量")
            
            return recommendations
    ```

    ## 📊 审查质量监控

    ### 审查效果分析
    ```python
    class ReviewEffectivenessAnalyzer:
        def __init__(self):
            self.review_data = []
        
        def track_review(self, review_id: str, reviewer: str, 
                        issues_found: int, issues_fixed: int, 
                        review_time_hours: float):
            """跟踪审查效果"""
            self.review_data.append({
                'review_id': review_id,
                'reviewer': reviewer,
                'issues_found': issues_found,
                'issues_fixed': issues_fixed,
                'review_time': review_time_hours,
                'fix_rate': issues_fixed / issues_found if issues_found > 0 else 0,
                'efficiency': issues_found / review_time_hours if review_time_hours > 0 else 0
            })
        
        def analyze_reviewer_performance(self) -> Dict[str, Any]:
            """分析审查者表现"""
            reviewer_stats = {}
            
            for review in self.review_data:
                reviewer = review['reviewer']
                if reviewer not in reviewer_stats:
                    reviewer_stats[reviewer] = {
                        'total_reviews': 0,
                        'total_issues_found': 0,
                        'total_issues_fixed': 0,
                        'total_time': 0,
                        'avg_fix_rate': 0,
                        'avg_efficiency': 0
                    }
                
                stats = reviewer_stats[reviewer]
                stats['total_reviews'] += 1
                stats['total_issues_found'] += review['issues_found']
                stats['total_issues_fixed'] += review['issues_fixed']
                stats['total_time'] += review['review_time']
            
            # 计算平均值
            for reviewer, stats in reviewer_stats.items():
                if stats['total_reviews'] > 0:
                    stats['avg_fix_rate'] = stats['total_issues_fixed'] / stats['total_issues_found']
                    stats['avg_efficiency'] = stats['total_issues_found'] / stats['total_time']
            
            return reviewer_stats
    ```

    ## 🔄 持续改进机制

    ### 审查流程优化
    ```mermaid
    graph TD
        A[审查数据收集] --> B[效果分析]
        B --> C[问题识别]
        C --> D[流程改进]
        D --> E[工具优化]
        E --> F[培训更新]
        F --> A
        
        B --> B1[审查效率分析]
        B --> B2[问题发现率]
        B --> B3[修复率统计]
        
        C --> C1[流程瓶颈]
        C --> C2[工具缺陷]
        C --> C3[技能差距]
        
        D --> D1[流程简化]
        D --> D2[标准更新]
        D --> D3[自动化增强]
        
        E --> E1[规则优化]
        E --> E2[误报减少]
        E --> E3[新检查添加]
    ```
  </process>

  <criteria>
    ## 代码审查评价标准

    ### 审查覆盖率
    - ✅ 代码审查覆盖率 100%
    - ✅ 关键代码双人审查率 100%
    - ✅ 安全相关代码专项审查率 100%
    - ✅ 文档同步更新率 ≥ 95%

    ### 问题发现率
    - ✅ 严重问题发现率 ≥ 95%
    - ✅ 安全漏洞发现率 ≥ 90%
    - ✅ 设计问题识别率 ≥ 85%
    - ✅ 性能问题识别率 ≥ 80%

    ### 审查效率
    - ✅ 平均审查时间 ≤ 2小时/KLOC
    - ✅ 问题修复率 ≥ 95%
    - ✅ 审查反馈时间 ≤ 24小时
    - ✅ 误报率 ≤ 10%

    ### 质量提升
    - ✅ 代码质量评分持续提升
    - ✅ 生产环境缺陷率下降
    - ✅ 团队代码规范遵循度 ≥ 95%
    - ✅ 知识传递效果显著
  </criteria>
</execution>

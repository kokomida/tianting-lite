<!-- status: in_progress -->

# 09 Evaluation & Metrics (Draft)

> 本章确定 Tianting-v2 的效果评估框架，覆盖功能正确性、性能、可维护性与用户满意度等多维度指标。

## 1. 评估目标
1. 对齐商业与技术成功标准：上线后 3 个月保持系统稳定、用户留存率 > 30%。
2. 建立可量化指标追踪迭代效果。
3. 为 A/B 实验与后续优化提供数据依据。

## 2. 关键指标 (KPIs)
| 维度 | 指标 | 目标值 | 数据来源 |
|------|------|--------|----------|
| 正确性 | E2E 测试通过率 | ≥ 98% | Playwright 报告 |
| 性能 | P95 API Latency | ≤ 300 ms | Prometheus + Grafana |
| 可靠性 | 每月故障次数 | ≤ 2 | Incident Tracker |
| 可维护性 | Mean Time To Recovery (MTTR) | ≤ 30 min | PagerDuty |
| 用户满意度 | Net Promoter Score (NPS) | ≥ 45 | SurveyMonkey |
| 代码审核 | Human Review Pass Rate | ≥ 85 % | Harvester Report |
| 学习进度 | Concept Cards 阅读数/月 | ≥ 40 | Frontend telemetry |
| 学习效果 | Review Comment Quality | ≥ 70 % | Explainer Scoring |

## 3. 数据收集方案
- **Backend**：Prometheus Exporter + Grafana Dashboard。
- **Frontend**：Web-Vitals 上报 (FCP, LCP, CLS)。
- **User Feedback**：Intercom In-App Survey + NPS 周期性邮件。
- **Error Tracking**：Sentry for both FE & BE。

## 4. A/B 实验流程
1. Feature Flag via LaunchDarkly。
2. Random assignment with 50/50 split.
3. 观察周期：最少 2 周 or 1,000 unique users。
4. 统计显著性 (p < 0.05) 作为上线依据。

## 5. 评估里程碑
| 阶段 | 指标审查 | 负责人 |
|------|-----------|--------|
| Beta Launch | 正确性 + 性能 | QA Lead |
| Public Release | 全部 KPI | Product Owner |
| Post-Launch 30d | 用户满意度 | UX Researcher |

## 6. 结果通报
- 周报：Slack #quality-channel
- 月报：Notion Dashboard + PDF 报告
- 重大异常：PagerDuty 自动升级

## 7. Monitoring Dashboard Layout
```
├── Service-Overview
│   ├─ Requests/s (stacked)
│   ├─ Error Rate (%)
│   └─ P95 Latency (ms)
├── Database
│   ├─ QPS
│   ├─ Connection Count
│   └─ Slow Queries (>2s)
├── Frontend Web-Vitals
│   ├─ FCP / LCP / CLS Trend
│   └─ JS Error Rate
└── Business KPIs
    ├─ Active Users (DAU/WAU)
    ├─ Completed Tasks per User
    └─ NPS Score
```
Dashboard JSON saved in `infra/grafana/dashboards/*.json`。

## 8. Data Pipeline
1. **Prometheus → Thanos**：15 s scrape；6 h compaction；30 d retention。  
2. **Loki → S3**：日志 7 d 快取 + Glacier 90 d 归档。  
3. **ClickHouse**：业务埋点 (Web-Vitals、NPS) → Superset 慢查询分析。  
4. **ETL**：dbt 每日 1:00 运行，将 KPI 聚合表写入 `/data_mart/`。

## 9. Alert Rules
| 指标 | 条件 | 严重级别 | 动作 |
|------|------|----------|------|
| Error Rate | >2 % 5m | P1 | PagerDuty 呼叫 | 
| API P95 Latency | >400 ms 10m | P2 | Slack #oncall |
| DB Connection Saturation | >90 % 5m | P2 | 自动扩容 + Oncall |
| DAU 下降 | -30 % Daily | P3 | 邮件提醒 PO |

## 10. A/B Testing Governance
- 工具：LaunchDarkly + PostHog Experiment。  
- 流程：Feature Flag→Traffic Split (50/50)→Metric Delta (t-test)→治理文档。  
- 审批：Data Analyst 审核统计显著性 (p<0.05) → PO 决策。

## 11. Reporting Cadence
| 报表 | 频率 | 渠道 |
|------|------|------|
| Daily KPI Email | 每日 09:00 | 产品 & 技术群邮件 |
| Weekly Ops Digest | 周一 10:00 | Slack #quality-channel |
| Monthly OKR Review | 月初 14:00 | Notion Dashboard |

## 12. Data Governance & Privacy
- 数据存储遵循 **GDPR**：用户可导出 / 删除。  
- PII 字段在日志中以 `***` Mask；Sentry DSN 设置 `sendDefaultPii=false`。  
- 访问控制：Grafana、ClickHouse 通过 SSO (Keycloak)；最小权限原则。

---
`status: in_progress` 将在指标采集脚本 & Dashboard JSON 合并后改为 `done`。

> 指标阈值可根据实际数据调整，请在 `CHANGELOG.md` 或新的文档版本中记录修改历史。 
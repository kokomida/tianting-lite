<!-- status: in_progress -->

# 07 Testing Plan (Draft)

> 本章定义 Tianting-v2 的整体测试策略，为 Harvester / CI Pipeline 提供可执行蓝图。后续章节将在实现阶段细化测试用例与覆盖率门槛。

## 1. 目标
1. 明确测试金字塔：单元 → 集成 → 端到端 (E2E) → 性能 → 回归。
2. 将测试计划融入 Roadmap 的每一 Milestone，持续交付。
3. 为 Harvester 自动评分与 Reporter 结果可视化奠定标准。

## 2. 范围
| 层级 | 目标模块 | 主要工具 | 触发时机 |
|------|----------|---------|----------|
| 单元测试 | packages/*/src | Jest / Vitest | PR 提交时 (GitHub Actions) |
| 集成测试 | packages/integration | Jest + Supertest | 合并到 `develop` 分支 |
| 端到端 | packages/frontend + api | Playwright | 日常夜跑 & 预发环境 |
| 性能测试 | api/gateway | k6 | Release Candidate |
| 回归测试 | 全系统 | Playwright + Jest | 每个 Release 前 |

## 3. 质量指标
- 单元测试覆盖率 ≥ 80%
- 端到端关键路径 > 95% 成功率
- 95th 响应时间 ≤ 300 ms (API 层)
- 关键 UI 交互 FCP ≤ 2 s
- 服务端 Error Rate ≤ 2 %

## 4. 环境准备
1. **本地**：`pnpm test` 统一脚本，使用 `.env.local`。
2. **CI**：GitHub Actions Matrix，Node 20 + Ubuntu & Windows。
3. **预发**：Docker Compose；种子数据由 `scripts/init-db.sql` 导入。

## 5. 测试数据管理
- 使用 Factory 函数生成隔离数据。
- IDempotent 清理：每个测试文件包含 `afterEach(cleanup)`。
- 使用 Faker.js 生成随机但可复现数据（seed）。

## 6. 缺陷追踪
- 缺陷在 GitHub Issues 使用 `bug` + `subsystem/<pkg>` label。
- 每周三例行 triage，严重级别 S1/S2 必须 24 h 内修复。

## 7. 里程碑映射
| Roadmap 篇章 | 交付物 | 截止日期 |
|--------------|--------|----------|
| Sprint 1 | Core 单元测试覆盖率 60% | 2025-07-15 |
| Sprint 2 | API 集成测试通过 | 2025-07-30 |
| Sprint 3 | Frontend E2E 流程稳定 | 2025-08-15 |

## 8. 风险 & 缓解
1. **端到端测试时间过长** → 并行拆分 + 按需跳过 non-critical 流程。
2. **Mock 与真实环境不一致** → 每周对比预发日志，更新 Contract 测试。
3. **前端元素选择器易变** → 统一 `data-testid` 属性。

## 9. Roles & Responsibilities
| 角色 | 职责 |
|------|------|
| Test Engineer | 维护测试脚本、覆盖率报告、CI 配置 |
| Backend Dev | 编写单元 / 集成测试，修复后端缺陷 |
| Frontend Dev | 编写组件测试、E2E 脚本，维护 data-testid |
| DevOps | 维护测试环境、k6 脚本、性能基线 |
| AI Harvester | 自动执行测试、生成 pass/fail 结果 JSON |
| QA Lead | 每 Sprint Review 测试指标 & 缺陷趋势 |

## 10. Entry & Exit Criteria
| 阶段 | Entry 条件 | Exit 条件 |
|------|-----------|----------|
| 单元测试 | 代码编译通过；Mock 依赖就绪 | 覆盖率 ≥ 80% 且 0 Critical 缺陷 |
| 集成测试 | 关键服务 Docker 起动成功 | 所有集成用例通过；新缺陷 ≤ 2 |
| E2E | 预发环境部署完成 | 关键用户路径通过率 ≥ 95% |
| 性能 | API & DB 指标基线确定 | P95 Latency ≤ 300 ms；错误率 < 0.1% |

## 11. Deliverables
- `tests/**/*.spec.(ts|js|py)` – 测试脚本
- `coverage/lcov-report/` – 覆盖率报告 (Jest Istanbul)
- `evidence/screenshots/` – Playwright 截图
- `perf/summary.json` – k6 输出
- `reports/test-summary.md` – Harvester 自动生成汇总

## 12. CI Workflow (GitHub Actions)
```yaml
name: Test Pipeline
on: [push, pull_request]
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with: { version: 8 }
      - run: pnpm install
      - run: pnpm test:unit
      learning:
        needs: unit
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - run: pnpm run test:lint-learning-schema # AJV validate explainer_output.schema.json
  integration:
    needs: unit
    runs-on: ubuntu-latest
    services:
      db: { image: mysql:8, ports: ['3306:3306'] }
    steps:
      - uses: actions/checkout@v4
      - run: pnpm test:integration
  e2e:
    needs: integration
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm test:e2e --project=chromium
```

## 13. Test Case Template
`tests/api/users.get.spec.ts`
```ts
import request from 'supertest';
import app from '@/src/app';

describe('GET /users/:id', () => {
  it('OES:api-05 should return 200 & user object', async () => {
    const res = await request(app).get('/users/123');
    expect(res.status).toBe(200);
    expect(res.body.id).toBe('123');
  });
});
```
> 约定：测试名称必须以 `OES:<task_id>` 开头，便于 Harvester 反向追踪。

## 14. Mapping to OES Tasks
| OES Task ID | 测试文件 | 用例数 |
|-------------|---------|--------|
| api-01 | `tests/api/bootstrap.spec.ts` | 3 |
| api-05 | `tests/api/users.get.spec.ts` | 2 |
| ui-02 | `tests/e2e/todos.e2e.ts` | 5 |

## 15. Risk Matrix (updated)
| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 第三方 API 速率限制 | M | M | 使用 MockServer 在 CI 中替代真实调用 |
| CI 运行时限 (90 min) | L | H | 测试并行 + 拆分 Matrix |
| 浏览器版本更新破坏 E2E | M | M | 固定 Playwright 版本；每周升级验证 |

---
`status: in_progress` 标记将在测试脚本落地并首轮 CI 通过后改为 `done`。

> 后续将由 Test Engineer 在实现阶段基于本计划补充具体测试用例 (`tests/<pkg>/`)，并在 `CHANGELOG.md` 记录进度。 
<!-- status: in_progress -->

# 08 Deployment Guide (Draft)

> 本章面向运维 / DevOps，描述 Tianting-v2 在各环境的交付方式、部署流程与回滚策略。

## 1. 架构总览
- 三层：API (Python) + Manager (Java/Vue) + 数据库/缓存。
- 部署介质：Docker Container；
- Orchestration: Docker Compose (本地 & 预发) / Kubernetes (生产)。

## 2. 环境矩阵
| 环境 | 目标 | 域名 / 端口 | 数据源 | 部署方式 |
|------|------|-------------|---------|----------|
| Local Dev | 开发自测 | localhost | SQLite / Redis-memory | Docker Compose (dev) |
| Staging | 集成验证 | staging.tianting.ai | MySQL (RDS) / Redis | Docker Compose (staging) |
| Production | 正式发布 | tianting.ai | MySQL (Aurora) / Redis Cluster | Kubernetes + Helm |

## 3. 前置要求
- Docker ≥ 24.x，Compose v2
- `kubectl` 与 K8s ≥ 1.29
- Argo CD (可选) 或 GitHub Actions Runner

## 4. 快速开始 (Local)
```bash
# 1. 克隆仓库
$ git clone https://github.com/your-org/tianting-v2.git && cd tianting-v2

# 2. 拉取基础镜像 (先拉后构建，更稳)
$ docker pull python:3.10-slim node:18 maven:3.9.4-eclipse-temurin-21

# 3. 启动
$ docker compose -f docker-compose.yml up -d --build

# 4. 访问
# API: http://localhost:8000/health
# UI : http://localhost:8084
```

## 5. 生产部署流程 (Helm)
1. 登录 K8s 集群 `kubectl config use-context prod`。
2. 创建命名空间：`kubectl create ns tianting-prod`。
3. 配置 Secrets：`kubectl apply -f k8s/secrets.yaml`。
4. 安装 Helm Chart：
   ```bash
   helm upgrade --install tianting ./k8s/chart \
     --namespace tianting-prod \
     --values k8s/values-prod.yaml
   ```
5. 验证：`kubectl rollout status deploy/tianting-server -n tianting-prod`。

## 6. 回滚策略
- **Compose**：`docker compose rollback <service>` (compose v2 native)；
- **K8s**：`kubectl rollout undo deploy/<name>`；建议保留 2 历史版本；
- 数据库版本：Flyway migration 可回退。

## 7. 监控 & 日志
- 集成 Prometheus + Grafana; default dashboards under `infra/grafana/`。
- Loki 收集容器日志，7 天保留。

## 8. 常见问题
| Symptoms | Possible Cause | Fix |
|----------|----------------|-----|
| API 500 after deploy | Env var mismatch | Check `config/.env` |
| UI blank page | CDN cache | `purge_cache.sh` |
| Pod CrashLoopBackOff | OOM | Increase memory limit |

## 9. Helm Chart Skeleton
```
k8s/chart/
  Chart.yaml
  values.yaml               # 默认值 (dev)
  values-staging.yaml       # staging 环境覆盖
  values-prod.yaml          # prod 环境覆盖
  templates/
    _helpers.tpl
    deployment-api.yaml
    deployment-manager.yaml
    service-api.yaml
    ingress.yaml
    hpa.yaml
    # Chart.yaml 示例字段：
    #   version: 0.1.0
    #   appVersion: 0.2.0
```
> 约定：所有资源加 `app.kubernetes.io/part-of: tianting` 标签，便于统一查询。

## 10. GitOps / CI-CD Pipeline
1. **Build Stage** (`build.yml`)
   - 构建 multi-arch Docker 镜像；标签：`<version>-<sha>`。
   - 推送到 GHCR；触发 Trivy 镜像扫描。
2. **Deploy Stage** (`deploy.yml`)
   - 条件：`main` 分支、镜像扫描无 Critical；
   - 使用 `helm upgrade --install --wait` 部署至 `staging`；
   - 运行 Smoke Test (`pnpm run test:smoke`).
3. **Promote to Prod**
   - 需 QA 打 `prod/*` tag；
   - GitHub Action 触发同 helm 命令，values-prod.yaml。

## 11. Secrets & Config Management
| 机制 | 工具 | 位置 |
|------|------|------|
| 应用密钥 | sealed-secrets | `k8s/sealed/` |
| DB 密码 | AWS Secrets Manager | 外部引用 via CSI Driver |
| Env Vars | ConfigMap | `k8s/config/app-env.yaml` |

## 12. Security Hardening
- Containers 以非 root 用户运行 (`runAsUser: 10001`)。
- 启用 `readOnlyRootFilesystem: true`。
- NetworkPolicy 限制只允许 80/443/DB 端口。
- 镜像扫描：Trivy + Github CodeQL。

## 13. Resource & Scaling Policy
| Component | requests | limits | HPA |
|-----------|----------|--------|-----|
| api | 200m / 256Mi | 1CPU / 1Gi | CPU>60% 2→6 |
| manager | 100m / 128Mi | 500m / 512Mi | CPU>70% 1→4 |

## 14. Backup & Restore
- MySQL：每日 `mysqldump` 到 S3，保留 7 天；`restore-db.sh` 支持 Point-in-Time。  
- Redis：启用 AOF + hourly snapshot，存至 PVC。  
- Helm Release：`helm get manifest` 每次升级存到 `s3://tianting-backups/releases/`。

## 15. Deployment Roles & Checkpoints
| 角色 | 检查点 |
|------|---------|
| DevOps | 镜像标签、Helm values 差异、证书有效期 |
| QA | Staging Smoke & Regression Pass |
| Product Owner | 功能开关开/关、灰度百分比 |
| Security | Trivy 报告无 Critical，SBOM 存档 |

---
`status: in_progress` 将在 Helm chart PR 合并并通过 staging Smoke Test 后更新为 `done`。

> 持续更新：如需新增环境或云厂商支持，请在 `CHANGELOG.md` 登记并提交 PR。 
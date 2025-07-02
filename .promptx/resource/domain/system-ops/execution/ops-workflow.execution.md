<execution>
  <constraint>
    ## 系统运维限制条件
    - **可用性约束**：系统可用性必须达到99.5%以上
    - **性能约束**：系统响应时间不得超过业务要求
    - **资源约束**：硬件和云资源使用有预算限制
    - **安全约束**：所有操作必须符合安全规范
    - **合规约束**：必须符合相关法规和标准要求
  </constraint>

  <rule>
    ## 系统运维强制规则
    - **变更管理**：所有系统变更必须经过审批和测试
    - **备份策略**：关键数据必须定期备份和验证
    - **监控覆盖**：所有关键组件必须有监控覆盖
    - **文档更新**：系统变更必须同步更新文档
    - **权限控制**：严格控制系统访问权限
  </rule>

  <guideline>
    ## 系统运维指导原则
    - **预防优于治疗**：通过监控和预警预防问题
    - **自动化优先**：优先使用自动化工具和流程
    - **标准化操作**：建立标准化的操作流程
    - **持续改进**：基于监控数据持续优化系统
    - **快速响应**：建立快速的故障响应机制
  </guideline>

  <process>
    ## 🚀 系统运维工作流程

    ### 运维架构设计
    ```mermaid
    graph TD
        A[应用层] --> B[服务层]
        B --> C[平台层]
        C --> D[基础设施层]
        
        A --> A1[PromptX应用]
        A --> A2[MemGPT服务]
        A --> A3[Web界面]
        
        B --> B1[API网关]
        B --> B2[负载均衡]
        B --> B3[服务发现]
        
        C --> C1[容器平台]
        C --> C2[数据库]
        C --> C3[缓存系统]
        C --> C4[消息队列]
        
        D --> D1[计算资源]
        D --> D2[存储资源]
        D --> D3[网络资源]
        D --> D4[安全组件]
    ```

    ### 第一阶段：环境部署与配置
    ```mermaid
    flowchart TD
        A[环境规划] --> B[基础设施准备]
        B --> C[平台部署]
        C --> D[应用部署]
        D --> E[配置管理]
        E --> F[测试验证]
        
        B --> B1[服务器配置]
        B --> B2[网络配置]
        B --> B3[安全配置]
        
        C --> C1[Docker部署]
        C --> C2[数据库部署]
        C --> C3[监控部署]
        
        D --> D1[应用安装]
        D --> D2[依赖配置]
        D --> D3[服务启动]
        
        E --> E1[环境变量]
        E --> E2[配置文件]
        E --> E3[权限设置]
    ```

    ### 第二阶段：监控与告警
    ```mermaid
    graph TD
        A[监控体系] --> B[基础监控]
        A --> C[应用监控]
        A --> D[业务监控]
        A --> E[日志监控]
        
        B --> B1[CPU/内存/磁盘]
        B --> B2[网络流量]
        B --> B3[系统进程]
        
        C --> C1[应用性能]
        C --> C2[接口响应]
        C --> C3[错误率]
        
        D --> D1[用户行为]
        D --> D2[业务指标]
        D --> D3[转化率]
        
        E --> E1[错误日志]
        E --> E2[访问日志]
        E --> E3[审计日志]
    ```

    ### 第三阶段：故障处理与优化
    ```mermaid
    flowchart LR
        A[故障发现] --> B[问题分析]
        B --> C[影响评估]
        C --> D[应急处理]
        D --> E[根因分析]
        E --> F[永久修复]
        F --> G[预防措施]
        
        B --> B1[日志分析]
        B --> B2[监控数据]
        B --> B3[用户反馈]
        
        D --> D1[服务恢复]
        D --> D2[流量切换]
        D --> D3[临时方案]
        
        E --> E1[代码分析]
        E --> E2[环境检查]
        E --> E3[配置审查]
    ```

    ## 🛠️ PromptX系统部署实现

    ### Docker容器化部署
    ```dockerfile
    # PromptX应用Dockerfile
    FROM python:3.11-slim

    WORKDIR /app

    # 安装系统依赖
    RUN apt-get update && apt-get install -y \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

    # 复制依赖文件
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # 复制应用代码
    COPY . .

    # 创建非root用户
    RUN useradd -m -u 1000 promptx && chown -R promptx:promptx /app
    USER promptx

    # 健康检查
    HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
        CMD python -c "import requests; requests.get('http://localhost:8000/health')"

    EXPOSE 8000

    CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

    ### Docker Compose配置
    ```yaml
    version: '3.8'

    services:
      promptx-app:
        build: .
        ports:
          - "8000:8000"
        environment:
          - DATABASE_URL=sqlite:///data/promptx.db
          - LOG_LEVEL=INFO
        volumes:
          - ./data:/app/data
          - ./logs:/app/logs
        depends_on:
          - redis
        restart: unless-stopped
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
          interval: 30s
          timeout: 10s
          retries: 3

      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
        volumes:
          - redis_data:/data
        restart: unless-stopped
        healthcheck:
          test: ["CMD", "redis-cli", "ping"]
          interval: 30s
          timeout: 10s
          retries: 3

      prometheus:
        image: prom/prometheus:latest
        ports:
          - "9090:9090"
        volumes:
          - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
          - prometheus_data:/prometheus
        restart: unless-stopped

      grafana:
        image: grafana/grafana:latest
        ports:
          - "3000:3000"
        environment:
          - GF_SECURITY_ADMIN_PASSWORD=admin
        volumes:
          - grafana_data:/var/lib/grafana
          - ./monitoring/grafana:/etc/grafana/provisioning
        restart: unless-stopped

    volumes:
      redis_data:
      prometheus_data:
      grafana_data:
    ```

    ### 系统监控配置
    ```python
    import psutil
    import time
    import logging
    from typing import Dict, Any
    from dataclasses import dataclass
    from datetime import datetime

    @dataclass
    class SystemMetrics:
        timestamp: datetime
        cpu_percent: float
        memory_percent: float
        disk_usage: Dict[str, float]
        network_io: Dict[str, int]
        process_count: int

    class SystemMonitor:
        def __init__(self, check_interval: int = 60):
            self.check_interval = check_interval
            self.logger = logging.getLogger(__name__)
            
        def collect_metrics(self) -> SystemMetrics:
            """收集系统指标"""
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用率
            disk_usage = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = usage.percent
                except PermissionError:
                    continue
            
            # 网络IO
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # 进程数量
            process_count = len(psutil.pids())
            
            return SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage=disk_usage,
                network_io=network_io,
                process_count=process_count
            )
        
        def check_thresholds(self, metrics: SystemMetrics) -> List[str]:
            """检查阈值告警"""
            alerts = []
            
            # CPU告警
            if metrics.cpu_percent > 80:
                alerts.append(f"High CPU usage: {metrics.cpu_percent:.1f}%")
            
            # 内存告警
            if metrics.memory_percent > 85:
                alerts.append(f"High memory usage: {metrics.memory_percent:.1f}%")
            
            # 磁盘告警
            for mount, usage in metrics.disk_usage.items():
                if usage > 90:
                    alerts.append(f"High disk usage on {mount}: {usage:.1f}%")
            
            return alerts
        
        def start_monitoring(self):
            """启动监控"""
            self.logger.info("Starting system monitoring...")
            
            while True:
                try:
                    metrics = self.collect_metrics()
                    alerts = self.check_thresholds(metrics)
                    
                    # 记录指标
                    self.logger.info(f"System metrics: CPU={metrics.cpu_percent:.1f}%, "
                                   f"Memory={metrics.memory_percent:.1f}%, "
                                   f"Processes={metrics.process_count}")
                    
                    # 处理告警
                    for alert in alerts:
                        self.logger.warning(f"ALERT: {alert}")
                        self.send_alert(alert)
                    
                    time.sleep(self.check_interval)
                    
                except Exception as e:
                    self.logger.error(f"Monitoring error: {e}")
                    time.sleep(self.check_interval)
        
        def send_alert(self, message: str):
            """发送告警"""
            # 这里可以集成邮件、短信、Slack等告警渠道
            print(f"🚨 ALERT: {message}")
    ```

    ### 日志管理系统
    ```python
    import logging
    import logging.handlers
    import json
    from datetime import datetime
    from pathlib import Path

    class StructuredLogger:
        def __init__(self, name: str, log_dir: str = "logs"):
            self.name = name
            self.log_dir = Path(log_dir)
            self.log_dir.mkdir(exist_ok=True)
            
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.INFO)
            
            # 清除现有处理器
            self.logger.handlers.clear()
            
            # 文件处理器
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_dir / f"{name}.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            
            # JSON格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        def log_structured(self, level: str, message: str, **kwargs):
            """结构化日志记录"""
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'level': level,
                'message': message,
                'service': self.name,
                **kwargs
            }
            
            getattr(self.logger, level.lower())(json.dumps(log_data, ensure_ascii=False))
        
        def log_request(self, method: str, path: str, status_code: int, 
                       response_time: float, user_id: str = None):
            """记录请求日志"""
            self.log_structured('info', 'HTTP Request', 
                              method=method, path=path, status_code=status_code,
                              response_time_ms=response_time, user_id=user_id)
        
        def log_error(self, error: Exception, context: Dict[str, Any] = None):
            """记录错误日志"""
            self.log_structured('error', str(error),
                              error_type=type(error).__name__,
                              context=context or {})
    ```

    ## 📊 性能优化策略

    ### 应用性能监控
    ```python
    import time
    import functools
    from typing import Callable, Any

    def performance_monitor(func: Callable) -> Callable:
        """性能监控装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # 记录性能指标
                logger = StructuredLogger('performance')
                logger.log_structured('info', 'Function execution',
                                     function=func.__name__,
                                     execution_time_ms=execution_time * 1000,
                                     success=True)
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # 记录错误和性能指标
                logger = StructuredLogger('performance')
                logger.log_structured('error', 'Function execution failed',
                                     function=func.__name__,
                                     execution_time_ms=execution_time * 1000,
                                     error=str(e),
                                     success=False)
                raise
        
        return wrapper

    class PerformanceProfiler:
        def __init__(self):
            self.metrics = {}
        
        def profile_function(self, func_name: str, execution_time: float):
            """记录函数性能"""
            if func_name not in self.metrics:
                self.metrics[func_name] = {
                    'count': 0,
                    'total_time': 0,
                    'min_time': float('inf'),
                    'max_time': 0
                }
            
            metrics = self.metrics[func_name]
            metrics['count'] += 1
            metrics['total_time'] += execution_time
            metrics['min_time'] = min(metrics['min_time'], execution_time)
            metrics['max_time'] = max(metrics['max_time'], execution_time)
        
        def get_performance_report(self) -> Dict[str, Any]:
            """获取性能报告"""
            report = {}
            
            for func_name, metrics in self.metrics.items():
                avg_time = metrics['total_time'] / metrics['count']
                report[func_name] = {
                    'call_count': metrics['count'],
                    'average_time_ms': avg_time * 1000,
                    'min_time_ms': metrics['min_time'] * 1000,
                    'max_time_ms': metrics['max_time'] * 1000,
                    'total_time_ms': metrics['total_time'] * 1000
                }
            
            return report
    ```

    ## 🔄 自动化运维

    ### 部署自动化脚本
    ```bash
    #!/bin/bash
    # deploy.sh - PromptX自动化部署脚本

    set -e

    # 配置变量
    APP_NAME="promptx"
    DOCKER_IMAGE="promptx:latest"
    BACKUP_DIR="/backup"
    LOG_FILE="/var/log/deploy.log"

    # 日志函数
    log() {
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
    }

    # 健康检查
    health_check() {
        local url=$1
        local max_attempts=30
        local attempt=1
        
        while [ $attempt -le $max_attempts ]; do
            if curl -f -s $url > /dev/null; then
                log "Health check passed"
                return 0
            fi
            
            log "Health check attempt $attempt/$max_attempts failed"
            sleep 10
            ((attempt++))
        done
        
        log "Health check failed after $max_attempts attempts"
        return 1
    }

    # 备份当前版本
    backup_current() {
        log "Creating backup..."
        
        if docker ps | grep -q $APP_NAME; then
            docker commit $APP_NAME $APP_NAME:backup-$(date +%Y%m%d-%H%M%S)
            log "Backup created successfully"
        else
            log "No running container to backup"
        fi
    }

    # 部署新版本
    deploy() {
        log "Starting deployment..."
        
        # 停止旧容器
        if docker ps | grep -q $APP_NAME; then
            log "Stopping old container..."
            docker stop $APP_NAME
            docker rm $APP_NAME
        fi
        
        # 启动新容器
        log "Starting new container..."
        docker run -d \
            --name $APP_NAME \
            --restart unless-stopped \
            -p 8000:8000 \
            -v $(pwd)/data:/app/data \
            -v $(pwd)/logs:/app/logs \
            $DOCKER_IMAGE
        
        # 健康检查
        if health_check "http://localhost:8000/health"; then
            log "Deployment successful"
            return 0
        else
            log "Deployment failed, rolling back..."
            rollback
            return 1
        fi
    }

    # 回滚
    rollback() {
        log "Rolling back to previous version..."
        
        # 停止失败的容器
        docker stop $APP_NAME || true
        docker rm $APP_NAME || true
        
        # 启动备份版本
        local backup_image=$(docker images | grep "$APP_NAME:backup" | head -1 | awk '{print $1":"$2}')
        if [ -n "$backup_image" ]; then
            docker run -d \
                --name $APP_NAME \
                --restart unless-stopped \
                -p 8000:8000 \
                -v $(pwd)/data:/app/data \
                -v $(pwd)/logs:/app/logs \
                $backup_image
            
            log "Rollback completed"
        else
            log "No backup image found for rollback"
        fi
    }

    # 主流程
    main() {
        log "Starting deployment process..."
        
        backup_current
        
        if deploy; then
            log "Deployment completed successfully"
            exit 0
        else
            log "Deployment failed"
            exit 1
        fi
    }

    main "$@"
    ```
  </process>

  <criteria>
    ## 系统运维评价标准

    ### 可用性指标
    - ✅ 系统可用性 ≥ 99.5%
    - ✅ 平均故障恢复时间 ≤ 30分钟
    - ✅ 计划内停机时间 ≤ 4小时/月
    - ✅ 数据丢失率 = 0%

    ### 性能指标
    - ✅ 系统响应时间 ≤ 2秒
    - ✅ 并发用户支持 ≥ 1000
    - ✅ 资源利用率 ≤ 80%
    - ✅ 扩展性良好

    ### 安全指标
    - ✅ 安全事件响应时间 ≤ 1小时
    - ✅ 访问控制有效性 100%
    - ✅ 数据备份完整性 100%
    - ✅ 合规性检查通过率 100%

    ### 运维效率
    - ✅ 自动化程度 ≥ 80%
    - ✅ 监控覆盖率 ≥ 95%
    - ✅ 告警准确率 ≥ 90%
    - ✅ 文档完整性 ≥ 95%
  </criteria>
</execution>

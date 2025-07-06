# 🚀 天庭系统快速启动指南

> **重要**: 每次新开终端都要按这个步骤操作！

---

## 📍 在哪里启动？

### 1. 打开WSL终端
```bash
# 任何方式都可以：
# - Windows Terminal
# - VS Code集成终端  
# - 直接打开WSL
```

### 2. 进入项目目录
```bash
cd /mnt/d/kokovsc/koko/Python/promptX+/tianting/v1.0-intelligent-workflow
```

### 3. 设置环境变量（重要！）
```bash
export PATH="$HOME/.local/bin:$PATH"
```
> ⚠️ **每次新开终端都必须运行这条命令**，否则找不到poetry！

---

## 🎯 启动方式

### 方式一：一键启动（推荐新手）

```bash
# 1. 进入项目目录
cd /mnt/d/kokovsc/koko/Python/promptX+/tianting/v1.0-intelligent-workflow

# 2. 设置环境变量
export PATH="$HOME/.local/bin:$PATH"

# 3. 一键启动所有服务
./quick-start.sh
```

### 方式二：分步启动（推荐开发者）

```bash
# 1. 进入项目目录并设置环境
cd /mnt/d/kokovsc/koko/Python/promptX+/tianting/v1.0-intelligent-workflow
export PATH="$HOME/.local/bin:$PATH"

# 2. 检查数据库状态
docker-compose ps

# 3. 如果数据库没启动，运行：
docker-compose up -d postgres redis

# 4. 启动Core服务（端口8001）
poetry run python packages/core/main.py &

# 5. 启动API服务（端口8002）
poetry run python packages/api/main.py &

# 6. 启动前端服务（端口3001）
cd packages/frontend && npm start
```

---

## 📱 访问地址

启动成功后，你可以访问：

| 服务 | 地址 | 说明 |
|------|------|------|
| 🌐 **前端应用** | http://localhost:3001 | 用户界面 |
| 📡 **API文档** | http://localhost:8002/docs | 接口文档和测试 |
| 💓 **健康检查** | http://localhost:8002/health | 服务状态 |
| 🗄️ **数据库** | localhost:5432 | PostgreSQL |
| 📦 **缓存** | localhost:6379 | Redis |

---

## 🛠️ 常用管理命令

### 基础命令
```bash
# 设置环境（每次新终端必须）
export PATH="$HOME/.local/bin:$PATH"

# 查看服务状态
./quick-start.sh status

# 停止所有服务
./quick-start.sh stop

# 重启所有服务
./quick-start.sh restart

# 查看实时日志
./quick-start.sh logs
```

### 开发命令
```bash
# 运行测试
poetry run test

# 代码格式化
poetry run format

# 代码检查
poetry run lint

# 健康检查
poetry run health-check
```

### 单独启动某个服务
```bash
# 只启动Core服务
./quick-start.sh start --core-only

# 只启动API服务
./quick-start.sh start --api-only

# 启动除前端外的所有服务
./quick-start.sh start --no-frontend
```

---

## ⚠️ 常见问题

### 1. 找不到poetry命令
```bash
# 问题：bash: poetry: command not found
# 解决：每次新终端都要设置PATH
export PATH="$HOME/.local/bin:$PATH"

# 永久解决：添加到 ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 2. 端口被占用
```bash
# 查看端口占用
netstat -tulpn | grep :8002

# 停止占用进程
./quick-start.sh stop

# 或者杀死特定进程
pkill -f "uvicorn.*8002"
```

### 3. 数据库连接失败
```bash
# 检查数据库状态
docker-compose ps

# 重启数据库
docker-compose restart postgres redis

# 查看数据库日志
docker-compose logs postgres
```

### 4. 前端启动失败
```bash
# 清理node_modules重新安装
cd packages/frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📁 项目结构说明

```
tianting/v1.0-intelligent-workflow/
├── packages/
│   ├── core/       # Core服务 (端口8001)
│   ├── api/        # API服务 (端口8002)
│   ├── frontend/   # 前端服务 (端口3001)
│   └── shared/     # 共享类型定义
├── scripts/        # 工具脚本
├── logs/          # 服务日志
├── .venv/         # Python虚拟环境
├── install.sh     # 一键安装脚本
├── quick-start.sh # 快速启动脚本
└── pyproject.toml # Poetry配置
```

---

## 🎯 推荐工作流

### 第一次使用：
1. 打开WSL终端
2. 进入项目目录：`cd /mnt/d/kokovsc/koko/Python/promptX+/tianting/v1.0-intelligent-workflow`
3. 设置环境：`export PATH="$HOME/.local/bin:$PATH"`
4. 启动服务：`./quick-start.sh`
5. 访问：http://localhost:3001

### 日常开发：
1. 新开终端并进入项目目录
2. 设置环境变量
3. `./quick-start.sh status` 检查状态
4. `./quick-start.sh` 启动服务
5. 开发完成后 `./quick-start.sh stop` 停止服务

### 调试时：
1. `./quick-start.sh logs` 查看日志
2. `poetry run test` 运行测试
3. 访问 http://localhost:8002/docs 测试API

---

## 💡 提示和技巧

1. **保存常用命令**: 可以创建别名
   ```bash
   echo 'alias tt-start="cd /mnt/d/kokovsc/koko/Python/promptX+/tianting/v1.0-intelligent-workflow && export PATH=\"\$HOME/.local/bin:\$PATH\" && ./quick-start.sh"' >> ~/.bashrc
   ```

2. **多终端开发**: 可以开多个终端分别查看不同服务的日志

3. **快速重启**: 修改代码后用 `./quick-start.sh restart` 重启服务

4. **性能监控**: 访问 http://localhost:8002/docs 查看API性能

---

## 🆘 获取帮助

- **脚本帮助**: `./quick-start.sh help`
- **安装帮助**: `./install.sh --help`
- **详细文档**: 查看 `INSTALL.md`
- **项目状态**: 查看 `CURRENT-VERSION-STATUS.md`

---

**🌟 记住：每次新开终端都要先 `export PATH="$HOME/.local/bin:$PATH"`！**
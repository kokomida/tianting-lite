# 📦 天庭系统安装指南

> **一键安装**: `./install.sh` 即可完成所有依赖安装  
> **适用系统**: Ubuntu, WSL2, macOS, CentOS/RHEL

---

## 🎯 安装概览

天庭系统采用现代化的依赖管理方案，使用Poetry避免版本冲突，确保开发环境一致性。

### 核心技术栈
- **Python**: >=3.8 (推荐3.12)
- **Node.js**: >=16 (推荐18+)  
- **Poetry**: >=1.4 (Python依赖管理)
- **Docker**: 数据库服务
- **PostgreSQL**: 主数据库
- **Redis**: 缓存服务

---

## 🚀 快速安装

### 方法一：一键安装（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd tianting/v1.0-intelligent-workflow

# 一键安装所有依赖
./install.sh

# 启动服务
docker-compose up -d        # 启动数据库
poetry run start-core       # 启动核心服务  
poetry run start-api        # 启动API服务
poetry run start-frontend   # 启动前端服务
```

### 方法二：手动安装

如果自动安装遇到问题，可以按以下步骤手动安装：

---

## 📋 详细安装步骤

### 1. 系统要求检查

```bash
# 检查Python版本
python3 --version  # 需要 >= 3.8

# 检查Node.js版本  
node --version     # 需要 >= 16

# 检查Docker版本
docker --version   # 需要支持docker-compose
```

### 2. 安装Poetry

#### Linux/WSL/macOS:
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
poetry --version
```

#### 使用pip安装（不推荐）:
```bash
pip3 install --user poetry
```

#### 使用包管理器:
```bash
# Ubuntu/Debian
sudo apt install python3-poetry

# macOS
brew install poetry

# CentOS/RHEL
sudo dnf install python3-poetry
```

### 3. 配置Poetry

```bash
# 在项目目录创建虚拟环境
poetry config virtualenvs.in-project true

# 配置并行安装
poetry config installer.max-workers 10

# 查看配置
poetry config --list
```

### 4. 安装Python依赖

```bash
# 进入项目目录
cd tianting/v1.0-intelligent-workflow

# 安装所有依赖（包括开发依赖）
poetry install --with dev,test,docs

# 或者仅安装生产依赖
poetry install --only main

# 验证安装
poetry run python -c "import fastapi, pydantic, uvicorn; print('✅ 依赖安装成功')"
```

### 5. 安装Node.js依赖

```bash
# Shared包 (TypeScript类型定义)
cd packages/shared
npm install
cd ../../

# Frontend包 (React应用)
cd packages/frontend  
npm install
cd ../../
```

### 6. 设置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 根据需要编辑配置
nano .env
```

### 7. 启动数据库服务

```bash
# 启动PostgreSQL和Redis
docker-compose up -d

# 检查服务状态
docker-compose ps

# 查看日志
docker-compose logs
```

---

## 🔧 故障排除

### 常见问题及解决方案

#### 1. Poetry安装失败

**错误**: `curl: command not found`
```bash
# Ubuntu/WSL
sudo apt update && sudo apt install curl

# CentOS/RHEL  
sudo dnf install curl
```

**错误**: Poetry命令未找到
```bash
# 添加到PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### 2. Python依赖冲突

**错误**: `Package 'xxx' has conflicting versions`
```bash
# 清理Poetry缓存
poetry cache clear pypi --all

# 删除虚拟环境重新创建
poetry env remove python
poetry install
```

**错误**: 全局包冲突
```bash
# 检查冲突包
poetry run pip list | grep -E "(fastapi|uvicorn|pydantic)"

# 解决方案：使用虚拟环境隔离
poetry shell  # 进入虚拟环境
```

#### 3. Node.js依赖问题

**错误**: `npm ERR! peer dep missing`
```bash
# 清理缓存重新安装
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**错误**: 权限问题
```bash
# 配置npm全局目录
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
```

#### 4. Docker服务问题

**错误**: `Cannot connect to Docker daemon`
```bash
# 启动Docker服务
sudo systemctl start docker

# WSL环境
# 确保Docker Desktop已启动
```

**错误**: 端口被占用
```bash
# 检查端口占用
sudo netstat -tulpn | grep :5432
sudo netstat -tulpn | grep :6379

# 关闭占用进程或修改docker-compose.yml端口
```

#### 5. WSL特殊问题

**问题**: 文件权限异常
```bash
# 修复脚本权限
chmod +x scripts/*.sh
chmod +x install.sh
```

**问题**: 路径问题
```bash
# 确保在WSL文件系统中工作
pwd  # 应该显示 /mnt/... 或 /home/...
```

---

## 🔍 验证安装

### 运行系统检查

```bash
# 运行安装脚本验证
./install.sh --help

# 检查Poetry环境
poetry env info

# 测试Python依赖
poetry run python -c "
import fastapi
import pydantic  
import uvicorn
import sqlalchemy
import redis
print('✅ 所有Python依赖正常')
"

# 测试Node.js依赖
cd packages/frontend && npm test
cd packages/shared && npm run type-check
```

### 健康检查

```bash
# 运行健康检查脚本
poetry run health-check

# 手动检查各服务
curl http://localhost:5432  # PostgreSQL
curl http://localhost:6379  # Redis  
poetry run start-core &     # Core服务
poetry run start-api &      # API服务
```

---

## 🎨 开发环境配置

### IDE设置

#### VS Code推荐配置

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["packages/"],
    "eslint.workingDirectories": ["packages/frontend", "packages/shared"]
}
```

#### PyCharm配置

1. 设置项目解释器：`.venv/bin/python`
2. 配置代码格式化：Black + isort
3. 设置测试运行器：pytest
4. 配置TypeScript：packages/shared, packages/frontend

### 开发工具命令

```bash
# 代码格式化
poetry run format        # Black + isort
poetry run lint          # Flake8检查

# 运行测试
poetry run test          # 所有测试
poetry run test-cov      # 带覆盖率报告

# 类型检查  
poetry run mypy packages/

# 启动开发服务
poetry run start-core    # Core服务 (端口8001)
poetry run start-api     # API服务 (端口8002)
poetry run start-frontend # 前端服务 (端口3001)
```

---

## 📈 性能优化

### Poetry加速

```bash
# 配置国内镜像（中国用户）
poetry config repositories.tsinghua https://pypi.tuna.tsinghua.edu.cn/simple/
poetry config repositories.aliyun https://mirrors.aliyun.com/pypi/simple/

# 并行安装
poetry config installer.max-workers 10

# 禁用虚拟环境（如果使用系统Python）
poetry config virtualenvs.create false
```

### NPM加速

```bash
# 设置国内镜像
npm config set registry https://registry.npmmirror.com/

# 或使用yarn
npm install -g yarn
yarn config set registry https://registry.npmmirror.com/
```

---

## 🚀 生产部署

### Docker部署

```bash
# 构建生产镜像
docker build -t tianting-system .

# 使用docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### 系统服务

```bash
# 创建systemd服务
sudo cp scripts/tianting.service /etc/systemd/system/
sudo systemctl enable tianting
sudo systemctl start tianting
```

---

## 📞 获取帮助

### 安装问题

1. **查看日志**: 安装脚本会输出详细日志
2. **检查文档**: 查看本文档故障排除部分
3. **重新安装**: 使用 `./install.sh --clean` 清理重装

### 技术支持

- **项目文档**: `README.md`
- **API文档**: 启动后访问 `http://localhost:8002/docs`
- **开发指南**: `docs/development/`
- **故障排除**: `docs/TROUBLESHOOTING.md`

### 社区资源

- **GitHub Issues**: 报告问题和获取帮助
- **文档站点**: https://tianting.ai/docs
- **示例项目**: examples/ 目录

---

## 🎉 安装完成

安装成功后，你将拥有：

✅ **完整的开发环境** - Python + Node.js + Poetry  
✅ **隔离的依赖管理** - 无版本冲突  
✅ **现代化工具链** - 代码格式化、测试、类型检查  
✅ **容器化服务** - PostgreSQL + Redis  
✅ **即用的脚本** - 一键启动各种服务  

**下一步**: 查看 `CURRENT-VERSION-STATUS.md` 了解项目状态，或运行 `poetry run test` 验证环境。

**开始使用**: 运行 `poetry run start-api` 启动API服务，访问 http://localhost:8002/docs 查看接口文档。

---

**🌟 天庭系统，让"言出法随"成为现实！**
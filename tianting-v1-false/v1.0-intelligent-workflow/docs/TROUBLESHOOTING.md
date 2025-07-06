# 🛠️ 天庭项目故障排除指南

## 🚨 紧急问题

### Claude API设计错误
**问题**: Core包错误设计了外部Claude API调用  
**解决方案**: 查看 [`CLAUDE-API-EMERGENCY-FIX.md`](./CLAUDE-API-EMERGENCY-FIX.md)  
**影响**: 仅Core包，其他包正常  

---

## 📦 依赖安装问题

### npm/pnpm安装超时
**症状**: 
```bash
npm install  # 超时或网络错误
pnpm install  # 进度停滞
```

**解决方案**:
```bash
# 方案1: 使用pnpm + 中国镜像
rm -rf node_modules package-lock.json
pnpm install --registry=https://registry.npmmirror.com

# 方案2: 设置超时时间
pnpm install --timeout=300000

# 方案3: 使用yarn
yarn install

# 方案4: 分步安装
pnpm install --no-frozen-lockfile
```

### Python依赖问题
**症状**: 
```bash
pip: command not found
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**:
```bash
# WSL2/Ubuntu环境
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# 虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔧 构建和编译问题

### TypeScript编译错误
**症状**:
```bash
error TS2307: Cannot find module 'xxx'
error TS2339: Property 'xxx' does not exist
```

**解决方案**:
```bash
# 1. 检查依赖安装
pnpm install

# 2. 清理缓存重新编译
rm -rf dist/ .tsbuildinfo
npx tsc --build --clean
npx tsc

# 3. 检查tsconfig.json配置
npx tsc --noEmit --listFiles
```

### React应用构建失败
**症状**:
```bash
Module not found: Error: Can't resolve './xxx'
```

**解决方案**:
```bash
# 1. 检查文件路径
ls -la src/

# 2. 创建缺失文件
touch src/styles/components.css

# 3. 重新启动开发服务器
pnpm start
```

---

## 🗄️ 数据库连接问题

### PostgreSQL连接失败
**症状**:
```bash
psql: could not connect to server
Connection refused
```

**解决方案**:
```bash
# 1. 启动Docker容器
docker-compose up -d postgres

# 2. 检查容器状态
docker ps | grep postgres

# 3. 检查连接配置
psql -h localhost -p 5432 -U tianting_user -d tianting_dev
```

### Redis连接问题
**症状**:
```bash
Redis connection failed
ECONNREFUSED 127.0.0.1:6379
```

**解决方案**:
```bash
# 1. 启动Redis容器
docker-compose up -d redis

# 2. 测试连接
docker exec -it <redis_container> redis-cli ping
```

---

## 🧪 测试相关问题

### Jest测试失败
**症状**:
```bash
Test suite failed to run
Cannot find module '@testing-library/jest-dom'
```

**解决方案**:
```bash
# 1. 安装测试依赖
pnpm add -D @testing-library/jest-dom

# 2. 检查setupTests.ts
cat src/setupTests.ts

# 3. 重新运行测试
pnpm test --passWithNoTests
```

### Python测试环境
**症状**:
```bash
pytest: command not found
No module named 'pytest'
```

**解决方案**:
```bash
# 1. 安装pytest
pip install pytest

# 2. 运行测试
python -m pytest tests/ -v

# 3. 检查测试配置
cat pytest.ini
```

---

## 🌐 网络和端口问题

### 端口冲突
**症状**:
```bash
Error: listen EADDRINUSE :::3001
Port 8002 is already in use
```

**解决方案**:
```bash
# 1. 查找占用进程
lsof -i :3001
netstat -tulpn | grep :8002

# 2. 终止进程
kill -9 <PID>

# 3. 使用其他端口
PORT=3002 pnpm start
```

### CORS跨域问题
**症状**:
```bash
Access to fetch blocked by CORS policy
```

**解决方案**:
```javascript
// 在API服务器中配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📁 文件和权限问题

### 文件权限错误
**症状**:
```bash
Permission denied
EACCES: permission denied
```

**解决方案**:
```bash
# 1. 修改文件权限
chmod +x scripts/setup.sh

# 2. 修改目录权限
sudo chown -R $USER:$USER node_modules/

# 3. 使用sudo（谨慎）
sudo pnpm install
```

### 缺失文件问题
**症状**:
```bash
ENOENT: no such file or directory
Module not found: Can't resolve
```

**解决方案**:
```bash
# 1. 检查文件是否存在
ls -la packages/shared/src/types/

# 2. 创建缺失文件
mkdir -p packages/shared/src/types/
touch packages/shared/src/types/domain.ts

# 3. 检查路径配置
cat tsconfig.json | grep "paths"
```

---

## 🐳 Docker相关问题

### Docker容器启动失败
**症状**:
```bash
docker-compose up failed
Error response from daemon
```

**解决方案**:
```bash
# 1. 检查Docker状态
docker --version
systemctl status docker

# 2. 清理Docker缓存
docker system prune -f

# 3. 重新构建容器
docker-compose down
docker-compose up --build -d
```

### 容器网络问题
**症状**:
```bash
Could not connect to the endpoint
Network tianting_default not found
```

**解决方案**:
```bash
# 1. 重新创建网络
docker network create tianting_default

# 2. 重启Docker服务
sudo systemctl restart docker

# 3. 重新启动容器
docker-compose down && docker-compose up -d
```

---

## 🔍 调试技巧

### 前端调试
```javascript
// 1. 使用React DevTools
console.log('组件状态:', state);

// 2. 网络请求调试
fetch('/api/test').then(res => console.log(res));

// 3. 样式调试
// 使用浏览器开发者工具检查CSS
```

### 后端调试
```python
# 1. 添加日志
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"处理请求: {request}")

# 2. 使用断点
import pdb; pdb.set_trace()

# 3. API测试
curl -X POST http://localhost:8002/api/test -H "Content-Type: application/json" -d '{"test": true}'
```

---

## 📞 寻求帮助

### 问题分类
1. **环境问题** → 查看本文档环境部分
2. **依赖问题** → 查看依赖安装部分  
3. **架构问题** → 查看对应的FIX文档
4. **集成问题** → 联系项目总控台

### 报告Bug步骤
1. **确认问题**: 重现问题并记录步骤
2. **收集信息**: 错误日志、环境信息、配置文件
3. **查阅文档**: 先查看本故障排除指南
4. **寻求帮助**: 提供详细的问题描述和环境信息

### 联系方式
- **紧急问题**: 直接找Frontend包负责人（项目总控台）
- **技术讨论**: 在对应包的开发者群组讨论
- **文档问题**: 提交到docs/目录的issue追踪

---

## 📚 参考资源

- [项目架构文档](../development/architecture/technical-architecture.md)
- [开发环境设置](../packages/common/environments/dev-environment-setup.md)
- [API契约规范](../packages/common/contracts/api-contracts.md)
- [Claude API修复指南](./CLAUDE-API-EMERGENCY-FIX.md)

---

**记住**: 大多数问题都有标准解决方案。先查文档，再寻求帮助！
# 天庭系统 TypeScript 类型定义 - 故障排除指南

## 📋 目录
- [TypeScript 编译问题](#typescript-编译问题)
- [测试相关问题](#测试相关问题)
- [工具链配置问题](#工具链配置问题)
- [包管理问题](#包管理问题)
- [IDE 集成问题](#ide-集成问题)

---

## 🔧 TypeScript 编译问题

### ❌ `TS1205: Re-exporting a type when 'isolatedModules' is enabled requires using 'export type'`

**问题描述**：
```
src/types/index.ts(9,3): error TS1205: Re-exporting a type when 'isolatedModules' is enabled requires using 'export type'.
```

**根本原因**：
- `tsconfig.json` 中启用了 `isolatedModules: true`
- 使用了普通的 `export { ... }` 导出类型定义
- TypeScript 5.0+ 严格模式要求类型导出必须明确区分

**解决方案**：
```typescript
// ❌ 错误写法
export {
  ID,
  Timestamp,
  ApiResponse,
  // ... 其他类型
} from './common';

// ✅ 正确写法
export type {
  ID,
  Timestamp,
  ApiResponse,
  // ... 其他类型
} from './common';

// 运行时值（函数、常量、类）仍使用普通 export
export {
  CommonErrorCodes,
  createApiError,
  TypeValidators,
  // ... 其他运行时值
} from './errors';
```

**验证修复**：
```bash
npm run type-check
```

---

### ❌ `TS2304: Cannot find name 'ApiResponse'`

**问题描述**：
在工具函数中引用类型时报找不到类型错误。

**根本原因**：
- `isolatedModules` 模式下，类型引用需要明确导入路径
- 循环依赖导致类型解析失败

**解决方案**：
```typescript
// ❌ 错误写法
validateApiResponse<T>(response: any): response is ApiResponse<T> {
  // ...
}

// ✅ 正确写法
validateApiResponse<T>(response: any): response is import('./common').ApiResponse<T> {
  // ...
}
```

---

## 🧪 测试相关问题

### ❌ 测试期望值与实际值不匹配

**问题描述**：
```
Expected: true
Received: {"test": "data"}
```

**根本原因**：
函数返回了错误的类型，通常是返回了对象而非布尔值。

**典型案例**：
```typescript
// ❌ 错误实现
isValidApiResponse(response: any): boolean {
  return response && response.success === true && response.data; // 返回 response.data 对象
}

// ✅ 正确实现
isValidApiResponse(response: any): boolean {
  return !!(response && response.success === true && response.data); // 强制转换为 boolean
}
```

**调试技巧**：
```typescript
// 添加调试日志
isValidApiResponse(response: any): boolean {
  const result = response && response.success === true && response.data;
  console.log('Debug result:', result, 'Type:', typeof result);
  return !!result;
}
```

---

### ❌ Jest 配置警告

**问题描述**：
```
Unknown option "moduleNameMapping" with value {...} was found.
```

**根本原因**：
Jest 配置选项名称拼写错误。

**解决方案**：
```javascript
// ❌ 错误配置
module.exports = {
  moduleNameMapping: {  // 错误的选项名
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};

// ✅ 正确配置
module.exports = {
  moduleNameMapper: {   // 正确的选项名
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};
```

---

## ⚙️ 工具链配置问题

### ❌ ESLint 无法找到配置文件

**问题描述**：
```
ESLint couldn't find a configuration file.
```

**解决方案**：
创建 `.eslintrc.js` 文件：
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint'],
  extends: ['eslint:recommended'],
  rules: {
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
  },
  env: {
    node: true,
    jest: true,
    es6: true,
  },
  ignorePatterns: ['dist/', 'node_modules/', '*.js'],
};
```

---

### ❌ ESLint 扩展配置无法找到

**问题描述**：
```
ESLint couldn't find the config "@typescript-eslint/recommended" to extend from.
```

**根本原因**：
缺少必要的 ESLint TypeScript 插件包。

**解决方案**：
```bash
# 安装必要依赖
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint

# 简化配置，避免复杂扩展
# 移除 '@typescript-eslint/recommended' 扩展，使用基础规则
```

---

### ❌ 未使用变量的 Lint 错误

**问题描述**：
```
'ID' is defined but never used @typescript-eslint/no-unused-vars
```

**解决方案**：
```typescript
// ❌ 导入了但未在当前文件使用的类型
import { 
  ID,           // 如果本文件不使用，应移除
  Timestamp, 
  ApiResponse
} from './common';

// ✅ 只导入实际使用的类型
import { 
  Timestamp, 
  ApiResponse
} from './common';
```

---

## 📦 包管理问题

### ❌ pnpm vs npm 兼容性

**问题现象**：
项目中同时存在 `package-lock.json` 和 `pnpm-lock.yaml`。

**建议解决方案**：
```bash
# 选择一种包管理器并保持一致
# 如果使用 npm：
rm pnpm-lock.yaml
npm install

# 如果使用 pnpm：
rm package-lock.json
pnpm install
```

---

### ❌ TypeScript 编译器找不到

**问题描述**：
```
sh: 1: tsc: not found
```

**解决方案**：
```bash
# 使用 npx 运行本地安装的 TypeScript
npx tsc --noEmit

# 或确保全局安装 TypeScript
npm install -g typescript
```

---

## 🎯 IDE 集成问题

### ❌ VS Code 类型提示不正确

**可能原因**：
1. TypeScript 服务器缓存问题
2. `tsconfig.json` 配置不正确
3. 工作区设置冲突

**解决步骤**：
1. 重启 TypeScript 服务器：`Ctrl+Shift+P` → "TypeScript: Restart TS Server"
2. 检查 `tsconfig.json` 路径配置
3. 验证 VS Code TypeScript 版本与项目版本兼容

---

## 🚀 快速诊断命令

### 完整验证流程：
```bash
# 1. 类型检查
npm run type-check

# 2. 测试验证  
npm test

# 3. 代码规范检查
npm run lint

# 4. 构建验证
npm run build

# 5. 类型覆盖率检查
npx type-coverage
```

### 常见问题快速检查：
```bash
# 检查是否有 export 类型问题
grep -r "export {" src/ --include="*.ts"

# 检查未使用的导入
npx ts-unused-exports tsconfig.json

# 检查循环依赖
npx madge --circular --extensions ts src/
```

---

## 📝 问题解决记录模板

遇到新问题时，请按以下格式记录：

```markdown
### ❌ [问题简述]

**问题描述**：
[详细的错误信息和现象]

**根本原因**：
[分析得出的问题根本原因]

**解决方案**：
[具体的修复代码或步骤]

**验证方法**：
[如何确认问题已解决]

**预防措施**：
[如何避免类似问题再次发生]
```

---

## 📞 获取帮助

如果遇到本文档未涵盖的问题：

1. **检查官方文档**：
   - [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
   - [Jest 配置文档](https://jestjs.io/docs/configuration)

2. **社区资源**：
   - [TypeScript GitHub Issues](https://github.com/microsoft/TypeScript/issues)
   - [Stack Overflow TypeScript 标签](https://stackoverflow.com/questions/tagged/typescript)

3. **项目内部**：
   - 检查 `docs/` 目录下的其他文档
   - 参考 `tests/` 目录下的测试用例
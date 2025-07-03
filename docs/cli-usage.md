# MemoryHub CLI 使用指南

MemoryHub 提供了命令行界面（CLI）用于管理和操作内存系统。

## 安装

CLI 工具随 MemoryHub 包一起安装：

```bash
pip install -e ./src
```

安装后，`memoryhub` 命令即可在系统中使用。

## 基本用法

```bash
memoryhub [--data-path PATH] <command> [options]
```

### 全局选项

- `--data-path, -d PATH`: 指定 MemoryHub 数据目录路径（默认：`./memoryhub_data`）

## 可用命令

### stats - 显示统计信息

显示 MemoryHub 的内存统计和性能指标：

```bash
memoryhub stats [--verbose]
```

**选项：**
- `--verbose, -v`: 显示详细统计信息

**示例输出：**
```
📊 MemoryHub Statistics: ./memoryhub_data
==================================================
📈 Memory Counts:
  Session: 0
  Core: 125
  Application: 2,450
  Archive: 890
  Total: 3,465

⚡ Performance:
  Avg Recall Latency: 18.32ms
  Max Recall Latency: 45.67ms
  Total Recalls: 1,234
```

### flush - 刷新待写入更新

将待写入的回忆计数更新刷新到磁盘：

```bash
memoryhub flush
```

此命令确保所有批量的回忆计数更新被写入 JSONL 文件。

### benchmark - 性能基准测试

运行 MemoryHub 性能基准测试：

```bash
memoryhub benchmark [--memories NUM] [--recalls NUM]
```

**选项：**
- `--memories, -m NUM`: 要存储的内存数量（默认：1000）
- `--recalls, -r NUM`: 要执行的回忆操作次数（默认：100）

**示例：**
```bash
# 轻量级测试
memoryhub benchmark -m 500 -r 50

# 完整性能测试
memoryhub benchmark -m 10000 -r 500
```

### build-index - 构建索引

构建或重建 JSONL 文件的索引以实现快速搜索：

```bash
memoryhub build-index [--layer LAYER] [--force]
```

**选项：**
- `--layer, -l LAYER`: 指定要构建的层（`application` 或 `archive`，默认：所有层）
- `--force, -f`: 即使索引是最新的也强制重建

**示例：**
```bash
# 构建所有层的索引
memoryhub build-index

# 只构建应用层索引
memoryhub build-index --layer application

# 强制重建所有索引
memoryhub build-index --force
```

### info - 显示文件信息

显示 MemoryHub 文件的详细信息和状态：

```bash
memoryhub info
```

**示例输出：**
```
📊 MemoryHub Information: ./memoryhub_data
==================================================

📁 APPLICATION Layer:
  📄 JSONL: 2,456,789 bytes (modified: 1672531200.0)
  🗂️  Index: 45,678 bytes, 2,450 entries (modified: 1672531201.0)
  ✅ Index is up to date

📁 ARCHIVE Layer:
  📄 JSONL: 890,123 bytes (modified: 1672530000.0)
  🗂️  Index: 12,345 bytes, 890 entries (modified: 1672530001.0)
  ✅ Index is up to date
```

## 常用工作流

### 日常维护

```bash
# 查看系统状态
memoryhub stats

# 刷新待写入的更新
memoryhub flush

# 检查文件状态
memoryhub info
```

### 性能优化

```bash
# 重建索引以优化搜索性能
memoryhub build-index --force

# 运行基准测试验证性能
memoryhub benchmark -m 5000 -r 250

# 查看详细性能统计
memoryhub stats --verbose
```

### 故障排除

```bash
# 检查索引是否过期
memoryhub info

# 强制重建所有索引
memoryhub build-index --force

# 刷新所有待写入更新
memoryhub flush

# 运行轻量级测试验证功能
memoryhub benchmark -m 100 -r 10
```

## 退出代码

- `0`: 成功
- `1`: 一般错误
- `130`: 用户中断（Ctrl+C）

## 注意事项

1. **资源管理**: CLI 工具会自动管理资源，在操作完成后释放文件句柄
2. **并发安全**: 避免在多个进程同时运行可能修改相同文件的命令
3. **性能**: 大型数据集的操作可能需要较长时间，请耐心等待
4. **备份**: 在运行 `build-index --force` 之前建议备份重要数据

## 环境变量

当前版本暂不支持环境变量配置，所有选项通过命令行参数指定。
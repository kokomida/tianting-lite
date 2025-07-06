# MemoryHub 资源管理

MemoryHub 实现了完善的资源管理机制，确保内存、文件句柄和数据库连接得到正确释放。

## 资源管理概述

### 管理的资源类型

1. **文件句柄**: JSONL 文件读写操作
2. **内存缓存**: 查询缓存、索引数组、标签索引
3. **数据库连接**: SQLite 连接（通过上下文管理器）
4. **待写入数据**: 批量的回忆计数更新

### 核心原则

- **自动清理**: 对象销毁时自动释放资源
- **显式关闭**: 提供 `close()` 方法手动释放资源
- **异常安全**: 即使发生异常也能正确清理资源
- **跨平台兼容**: 特别针对 Windows 文件句柄管理优化

## API 设计

### LayeredMemoryManager

```python
from memoryhub import LayeredMemoryManager

# 创建管理器
manager = LayeredMemoryManager(path="./data")

try:
    # 正常使用
    manager.remember("Some content", ["tag"], "/path")
    results = manager.recall("query")
finally:
    # 显式释放资源
    manager.close()
```

**`close()` 方法功能：**
- 刷新所有待写入的回忆计数更新
- 关闭 JSONL DAO 资源
- 关闭 SQLite DAO 连接
- 清理内存缓存

### JSONLMemoryDAO

```python
from memoryhub.jsonl_dao import JSONLMemoryDAO

dao = JSONLMemoryDAO(data_path="./data")

try:
    # 存储和搜索操作
    dao.store_memory(memory_record, "application")
    results = dao.search_memories("query", "application")
finally:
    # 释放资源
    dao.close()
```

**`close()` 方法功能：**
- 刷新所有待写入更新到磁盘
- 清理查询缓存
- 清空偏移量和长度数组
- 清理标签预索引

### MemoryHubDAO (SQLite)

```python
from memoryhub.sqlite_dao import MemoryHubDAO

dao = MemoryHubDAO(db_path="./data/memory.db")

try:
    # 数据库操作
    dao.store_memory(memory_record)
    results = dao.search_memories("query")
finally:
    # SQLite 使用上下文管理器，close() 为 no-op
    dao.close()
```

## 自动资源管理

### 析构函数清理

所有 DAO 类都实现了 `__del__` 方法，确保对象被垃圾回收时自动释放资源：

```python
def __del__(self):
    """Ensure resources are released when object is destroyed"""
    try:
        self.close()
    except Exception:
        pass  # Ignore errors during cleanup
```

### 异常安全

资源释放代码被包装在 try-except 块中，确保即使发生异常也能正确清理：

```python
def close(self):
    """Release all resources"""
    try:
        # Flush pending updates
        self.flush_all_pending_updates()
        # Clear caches
        self._query_cache.clear()
        # Clear arrays...
    except Exception as e:
        print(f"Warning: Error during close: {e}")
```

## Windows 兼容性

### 文件句柄问题

在 Windows 系统上，未正确关闭的文件句柄可能导致 `WinError 32`（文件被另一个进程使用）。MemoryHub 的解决方案：

1. **上下文管理器**: 所有文件操作使用 `with` 语句
2. **显式关闭**: 提供 `close()` 方法释放文件句柄
3. **测试验证**: 专门的 Windows 测试确保句柄正确释放

### 测试案例

```python
@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
def test_windows_file_handle_release(self):
    """Test that files can be deleted after close() on Windows"""
    manager = LayeredMemoryManager(path=self.test_dir)
    
    # 创建文件
    for i in range(5):
        manager.remember(f"Test memory {i}", ["test"], f"/test/path{i}")
    
    # 确保数据写入
    manager.flush_pending_updates()
    
    # 关闭管理器释放句柄
    manager.close()
    
    # Windows 上应该能删除文件
    try:
        app_logs_file.unlink()
        memory_db_file.unlink()
    except PermissionError as e:
        pytest.fail(f"File handles not properly released: {e}")
```

## 最佳实践

### 1. 使用上下文管理器模式

```python
# 推荐：显式管理生命周期
manager = LayeredMemoryManager(path="./data")
try:
    # 使用 manager
    manager.remember("content", ["tag"], "/path")
    results = manager.recall("query")
finally:
    manager.close()
```

### 2. 在异常处理中清理

```python
def process_memories():
    manager = None
    try:
        manager = LayeredMemoryManager(path="./data")
        # 处理逻辑
        return process_data(manager)
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if manager:
            manager.close()
```

### 3. 批量操作后刷新

```python
manager = LayeredMemoryManager(path="./data")
try:
    # 大量操作
    for i in range(1000):
        manager.remember(f"Memory {i}", ["batch"], f"/batch/{i}")
    
    # 确保数据写入
    manager.flush_pending_updates()
finally:
    manager.close()
```

### 4. 长期运行的应用

```python
class MemoryService:
    def __init__(self, data_path):
        self.manager = LayeredMemoryManager(path=data_path)
    
    def shutdown(self):
        """服务关闭时调用"""
        if self.manager:
            self.manager.close()
            self.manager = None
    
    def __del__(self):
        self.shutdown()
```

## 性能考虑

### 批量更新策略

MemoryHub 使用批量更新减少 I/O 操作：

- **批量大小**: 默认 10 个更新一批
- **自动刷新**: 达到批量大小时自动写入
- **显式刷新**: `flush_pending_updates()` 立即写入
- **关闭时刷新**: `close()` 确保所有数据写入

### 缓存管理

- **查询缓存**: 最多 500 个查询结果
- **索引缓存**: 内存中保持偏移量数组
- **标签索引**: 预建立的标签到记录映射

### 内存使用

调用 `close()` 后：
- 所有缓存被清理
- 数组被重置
- 内存使用降到最低

## 故障排除

### 常见问题

1. **文件无法删除**: 确保调用了 `close()` 方法
2. **内存泄漏**: 检查是否有未释放的对象引用
3. **数据丢失**: 确保在关闭前调用 `flush_pending_updates()`

### 调试技巧

```python
# 检查资源状态
print(f"Pending updates: {len(dao._pending_recall_updates)}")
print(f"Cache size: {len(dao._query_cache)}")
print(f"Index size: {len(dao._app_offsets)}")

# 强制清理
dao.close()

# 验证清理结果
assert len(dao._query_cache) == 0
assert len(dao._app_offsets) == 0
```

## 总结

MemoryHub 的资源管理确保：
- **跨平台兼容性**: 特别是 Windows 文件句柄管理
- **内存效率**: 适时清理缓存和临时数据
- **数据完整性**: 关闭前确保所有更新写入磁盘
- **异常安全**: 即使出错也能正确清理资源

通过遵循最佳实践和使用提供的 API，可以确保应用程序高效、安全地使用 MemoryHub。
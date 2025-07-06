# Python 并发文件锁定机制研究

## 概述

本 RFC 研究 Python 环境下的文件锁定机制，为 MemoryHub 多进程/多线程并发访问场景提供技术选型依据。重点分析 fcntl、file-lock 库和 SQLite WAL 模式的适用性。

## 背景与需求

### 当前挑战
- **并发写入**: 多个进程同时修改 JSONL 文件可能导致数据损坏
- **索引一致性**: 文件更新时需要同步重建索引
- **跨平台兼容**: Windows/Linux/macOS 文件锁机制差异
- **性能要求**: 锁定机制不应显著影响读写性能

### 应用场景
1. **JSONL 文件写入**: 多进程同时调用 `remember()` 
2. **索引重建**: 文件修改后的索引更新操作
3. **批量更新**: recall count 批量刷新到磁盘
4. **数据库访问**: SQLite 并发读写保护

## 技术方案对比

### 1. fcntl() 文件锁 (POSIX)

#### 机制说明
```python
import fcntl

def acquire_file_lock(file_path, exclusive=True):
    fd = os.open(file_path, os.O_RDWR | os.O_CREAT)
    lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
    fcntl.flock(fd, lock_type)
    return fd

def release_file_lock(fd):
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
```

#### 优势
- **标准库**: 无需额外依赖
- **性能**: 系统级锁定，开销低
- **灵活性**: 支持共享锁和排他锁

#### 劣势与风险
- **NFS 不兼容**: fcntl() 在多数 NFS 实现上损坏
- **锁归属问题**: 锁属于 (pid, inode) 对，而非文件描述符
- **意外释放**: 关闭任意 fd 会释放该 inode 上的所有锁
- **跨平台差异**: Windows 不支持 fcntl
- **静默损坏**: 文件锁失效时可能导致静默数据损坏

> ⚠️ **重要**: SQLite 使用 fcntl() 但避免共享锁，只使用排他锁随机字节范围

### 2. file-lock 库

#### 机制说明
```python
from filelock import FileLock

def safe_file_operation(file_path):
    lock_path = f"{file_path}.lock"
    lock = FileLock(lock_path)
    
    with lock:
        # 执行文件操作
        with open(file_path, 'a') as f:
            f.write("data\n")
```

#### 优势
- **跨平台**: 统一的 API，处理平台差异
- **简单易用**: 上下文管理器支持
- **超时控制**: 支持锁获取超时
- **进程间锁**: 基于锁文件的进程间同步

#### 劣势
- **外部依赖**: 需要安装第三方库
- **锁文件管理**: 需要清理残留锁文件
- **性能开销**: 相比 fcntl 有额外开销

### 3. SQLite WAL 模式 (推荐)

#### 机制说明
```sql
-- 启用 WAL 模式
PRAGMA journal_mode=WAL;

-- 检查当前模式
PRAGMA journal_mode;
```

#### 架构优势
- **读写并发**: 读操作不阻塞写操作，写操作不阻塞读操作
- **内置锁管理**: SQLite 自动处理锁定和事务
- **ACID 保证**: 完整的事务语义
- **检查点机制**: 自动合并 WAL 到主数据库

#### 工作原理
1. **写入 WAL**: 修改写入 write-ahead log 文件
2. **读取合并**: 读操作从主数据库 + WAL 合并结果
3. **检查点**: 定期将 WAL 内容合并到主数据库
4. **锁粒度**: 页级锁，减少锁竞争

#### 限制条件
- **本地文件系统**: 不支持网络文件系统 (NFS/SMB)
- **共享内存**: 所有进程必须在同一主机
- **VFS 限制**: 某些虚拟文件系统可能不兼容

## 推荐方案

### 主推荐: SQLite WAL + 应用层协调

```python
class ThreadSafeMemoryHub:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.db_path = self.data_path / "memory.db"
        
        # 启用 WAL 模式
        self._init_wal_mode()
        
        # 应用层锁保护 JSONL 操作
        self._jsonl_lock = threading.RLock()
    
    def _init_wal_mode(self):
        """初始化 SQLite WAL 模式"""
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")  # 平衡性能与安全性
            conn.execute("PRAGMA wal_autocheckpoint=1000")  # 自动检查点
    
    def remember(self, content: str, tags: List[str], context_path: str):
        """线程安全的记忆存储"""
        # SQLite 操作由 WAL 保护
        memory_id = self._dao.store_memory({
            "content": content,
            "tags": tags,
            "context_path": context_path
        })
        
        # JSONL 操作需要应用层锁
        with self._jsonl_lock:
            self._jsonl_dao.store_memory(memory_record, "application")
    
    def _rebuild_indices_locked(self, layer: str):
        """带锁的索引重建"""
        with self._jsonl_lock:
            self._jsonl_dao._rebuild_layer_indices(layer)
```

### 备选方案: file-lock + 细粒度锁

```python
from filelock import FileLock
import threading

class LockedJSONLDAO:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.app_lock = FileLock(self.data_path / "app_logs.lock")
        self.archive_lock = FileLock(self.data_path / "archive.lock")
        self._thread_lock = threading.RLock()
    
    def store_memory(self, memory_record: Dict, layer: str):
        """多级锁保护的存储操作"""
        file_lock = self.app_lock if layer == "application" else self.archive_lock
        
        with self._thread_lock:  # 线程级锁
            with file_lock:      # 进程级锁
                return self._unsafe_store_memory(memory_record, layer)
```

## 实施建议

### Phase 1: SQLite WAL 启用
```python
# 在 MemoryHubDAO.__init__ 中添加
def _ensure_wal_mode(self):
    """确保数据库使用 WAL 模式"""
    with self._get_connection() as conn:
        result = conn.execute("PRAGMA journal_mode=WAL").fetchone()
        if result[0].lower() != 'wal':
            raise RuntimeError("Failed to enable WAL mode")
```

### Phase 2: JSONL 保护机制
```python
# 选项 A: 使用 file-lock
from filelock import FileLock

# 选项 B: 使用线程锁 + 进程协调
import threading
import os

class SafeJSONLWriter:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.lock_path = file_path.with_suffix('.lock')
        self._local_lock = threading.RLock()
    
    def write_batch(self, records: List[Dict]):
        with self._local_lock:
            with FileLock(self.lock_path, timeout=30):
                self._unsafe_write_batch(records)
```

### Phase 3: 性能优化
- **批量操作**: 减少锁获取频率
- **读写分离**: 读操作尽量避免锁
- **锁超时**: 防止死锁和长时间等待

## 风险评估与缓解

### 高风险场景
1. **网络存储**: 如果数据存储在 NFS 上，fcntl/SQLite 都不可靠
2. **容器环境**: Docker 容器间文件锁可能失效
3. **进程异常**: 进程崩溃导致锁文件残留

### 缓解策略
```python
def safe_operation_with_timeout(func, timeout=30):
    """带超时的安全操作"""
    try:
        with FileLock(lock_path, timeout=timeout):
            return func()
    except filelock.Timeout:
        raise MemoryHubLockError(f"Failed to acquire lock within {timeout}s")
    except Exception as e:
        # 记录错误但继续运行
        logger.warning(f"Lock operation failed: {e}")
        return func()  # 降级为无锁操作
```

## 测试策略

### 并发测试
```python
import threading
import multiprocessing
import time

def test_concurrent_writes():
    """测试并发写入安全性"""
    def worker(worker_id):
        manager = LayeredMemoryManager(path="./test_data")
        for i in range(100):
            manager.remember(f"Worker {worker_id} - {i}", ["test"], f"/worker_{worker_id}")
        manager.close()
    
    # 多线程测试
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # 验证数据完整性
    assert_no_data_corruption()
```

## 监控与观测

### 关键指标
```python
class LockMetrics:
    def __init__(self):
        self.lock_wait_times = []
        self.lock_timeouts = 0
        self.lock_failures = 0
    
    def record_lock_wait(self, duration_ms: float):
        self.lock_wait_times.append(duration_ms)
    
    def get_metrics(self) -> Dict:
        return {
            "avg_lock_wait_ms": statistics.mean(self.lock_wait_times),
            "max_lock_wait_ms": max(self.lock_wait_times),
            "lock_timeout_rate": self.lock_timeouts / len(self.lock_wait_times),
            "lock_failure_rate": self.lock_failures / len(self.lock_wait_times)
        }
```

## 结论

**推荐使用 SQLite WAL + file-lock 混合方案**:

1. **SQLite WAL**: 处理数据库层面的并发访问
2. **file-lock**: 保护 JSONL 文件操作
3. **应用层协调**: 线程锁 + 进程锁的分层保护

这种方案在性能、可靠性和跨平台兼容性之间取得最佳平衡，适合 MemoryHub 的实际需求。

## 下一步行动

1. **创建 core-03b-concurrency-safety 任务卡**
2. **实施 SQLite WAL 模式启用**
3. **集成 file-lock 库到 pyproject.toml**
4. **编写并发安全测试套件**
5. **更新架构文档，说明锁定策略**
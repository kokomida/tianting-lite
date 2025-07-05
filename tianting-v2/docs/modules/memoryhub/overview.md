# MemoryHub – Overview

MemoryHub 是 Tianting 平台的混合记忆存储与检索子系统，提供：
1. 标签位图索引（RoaringBitmapTagIndex）
2. 分层 DAO：SQLite (Layer-1) + JSONL (Layer-0)
3. 统一 API：save_memory / search_memories / stats

> 详细架构见 design.md；性能演进见 changelog.md 
<execution>
  <constraint>
    ## 数据库管理限制条件
    - **性能约束**：数据库操作不得显著影响系统响应时间
    - **存储约束**：数据存储空间和索引大小有限制
    - **并发约束**：必须支持多用户并发访问
    - **一致性约束**：必须保证ACID事务特性
    - **安全约束**：敏感数据必须加密存储和传输
  </constraint>

  <rule>
    ## 数据库管理强制规则
    - **备份优先**：关键操作前必须备份数据
    - **事务完整性**：所有数据修改必须在事务中进行
    - **索引维护**：定期维护和优化数据库索引
    - **权限控制**：严格控制数据库访问权限
    - **日志记录**：所有重要操作必须记录日志
  </rule>

  <guideline>
    ## 数据库管理指导原则
    - **性能优先**：优化查询性能和存储效率
    - **安全第一**：确保数据安全和隐私保护
    - **可扩展性**：设计支持未来扩展的架构
    - **可维护性**：保持数据库结构清晰易维护
    - **标准化**：遵循数据库设计最佳实践
  </guideline>

  <process>
    ## 🗄️ 数据库管理工作流程

    ### 数据库架构设计
    ```mermaid
    graph TD
        A[需求分析] --> B[概念设计]
        B --> C[逻辑设计]
        C --> D[物理设计]
        D --> E[性能优化]
        E --> F[安全配置]
        F --> G[部署实施]
        
        B --> B1[实体关系建模]
        B --> B2[业务规则定义]
        
        C --> C1[表结构设计]
        C --> C2[关系定义]
        C --> C3[约束设计]
        
        D --> D1[索引策略]
        D --> D2[分区方案]
        D --> D3[存储优化]
        
        E --> E1[查询优化]
        E --> E2[缓存策略]
        E --> E3[连接池配置]
    ```

    ### 第一阶段：MemGPT数据库设计
    ```mermaid
    flowchart TD
        A[MemGPT需求] --> B[核心表设计]
        B --> C[记忆存储表]
        C --> D[关系映射表]
        D --> E[索引优化]
        E --> F[性能测试]
        
        C --> C1[memories表]
        C --> C2[memory_relations表]
        C --> C3[context_sessions表]
        C --> C4[user_profiles表]
        
        D --> D1[向量关系]
        D --> D2[语义关系]
        D --> D3[时序关系]
        
        E --> E1[向量索引]
        E --> E2[全文索引]
        E --> E3[复合索引]
    ```

    ### 第二阶段：数据库实施与优化
    ```mermaid
    graph TD
        A[数据库创建] --> B[表结构实施]
        B --> C[数据迁移]
        C --> D[性能调优]
        D --> E[监控部署]
        E --> F[维护计划]
        
        B --> B1[DDL执行]
        B --> B2[约束创建]
        B --> B3[索引建立]
        
        C --> C1[数据导入]
        C --> C2[数据验证]
        C --> C3[一致性检查]
        
        D --> D1[查询优化]
        D --> D2[索引调优]
        D --> D3[配置优化]
    ```

    ## 🛠️ SQLite MemGPT数据库实现

    ### 核心表结构设计
    ```sql
    -- 主记忆表
    CREATE TABLE memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        content_hash TEXT UNIQUE, -- 内容哈希，防重复
        memory_type TEXT NOT NULL CHECK (memory_type IN ('fact', 'event', 'preference', 'skill', 'context')),
        importance_score REAL DEFAULT 0.5 CHECK (importance_score >= 0 AND importance_score <= 1),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        access_count INTEGER DEFAULT 0,
        tags TEXT, -- JSON array of tags
        metadata JSON,
        embedding BLOB, -- 向量嵌入
        user_id TEXT,
        session_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    );

    -- 记忆关联表
    CREATE TABLE memory_relations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_memory_id INTEGER NOT NULL,
        target_memory_id INTEGER NOT NULL,
        relation_type TEXT NOT NULL CHECK (relation_type IN ('similar', 'causal', 'temporal', 'hierarchical', 'contradictory')),
        strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
        confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT DEFAULT 'system',
        FOREIGN KEY (source_memory_id) REFERENCES memories(id) ON DELETE CASCADE,
        FOREIGN KEY (target_memory_id) REFERENCES memories(id) ON DELETE CASCADE,
        UNIQUE(source_memory_id, target_memory_id, relation_type)
    );

    -- 用户会话表
    CREATE TABLE sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        context_data JSON,
        active_memories JSON, -- 当前激活的记忆ID列表
        session_summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    -- 用户配置表
    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        preferences JSON,
        memory_config JSON, -- 记忆管理配置
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 知识图谱节点表
    CREATE TABLE knowledge_nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concept TEXT NOT NULL,
        concept_type TEXT,
        description TEXT,
        properties JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(concept, concept_type)
    );

    -- 知识图谱边表
    CREATE TABLE knowledge_edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_node_id INTEGER NOT NULL,
        target_node_id INTEGER NOT NULL,
        relation_type TEXT NOT NULL,
        properties JSON,
        weight REAL DEFAULT 1.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (source_node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
        FOREIGN KEY (target_node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE
    );
    ```

    ### 索引优化策略
    ```sql
    -- 记忆表索引
    CREATE INDEX idx_memories_type_importance ON memories(memory_type, importance_score DESC);
    CREATE INDEX idx_memories_user_session ON memories(user_id, session_id);
    CREATE INDEX idx_memories_created_at ON memories(created_at DESC);
    CREATE INDEX idx_memories_last_accessed ON memories(last_accessed DESC);
    CREATE INDEX idx_memories_access_count ON memories(access_count DESC);
    CREATE INDEX idx_memories_content_hash ON memories(content_hash);

    -- 关系表索引
    CREATE INDEX idx_relations_source ON memory_relations(source_memory_id);
    CREATE INDEX idx_relations_target ON memory_relations(target_memory_id);
    CREATE INDEX idx_relations_type_strength ON memory_relations(relation_type, strength DESC);

    -- 会话表索引
    CREATE INDEX idx_sessions_user_created ON sessions(user_id, created_at DESC);
    CREATE INDEX idx_sessions_active ON sessions(user_id) WHERE ended_at IS NULL;

    -- 知识图谱索引
    CREATE INDEX idx_knowledge_nodes_concept ON knowledge_nodes(concept);
    CREATE INDEX idx_knowledge_nodes_type ON knowledge_nodes(concept_type);
    CREATE INDEX idx_knowledge_edges_source ON knowledge_edges(source_node_id);
    CREATE INDEX idx_knowledge_edges_target ON knowledge_edges(target_node_id);
    CREATE INDEX idx_knowledge_edges_relation ON knowledge_edges(relation_type);
    ```

    ### 数据库操作封装
    ```python
    import sqlite3
    import json
    import hashlib
    from datetime import datetime
    from typing import Dict, List, Any, Optional
    
    class MemGPTDatabase:
        def __init__(self, db_path: str = "memgpt.db"):
            self.db_path = db_path
            self.init_database()
        
        def init_database(self):
            """初始化数据库"""
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript("""
                    -- 启用外键约束
                    PRAGMA foreign_keys = ON;
                    
                    -- 设置WAL模式提高并发性能
                    PRAGMA journal_mode = WAL;
                    
                    -- 设置同步模式
                    PRAGMA synchronous = NORMAL;
                    
                    -- 设置缓存大小
                    PRAGMA cache_size = -64000; -- 64MB
                """)
        
        def store_memory(self, content: str, memory_type: str, user_id: str, 
                        session_id: str, importance: float = 0.5, 
                        tags: List[str] = None, metadata: Dict = None,
                        embedding: bytes = None) -> int:
            """存储记忆"""
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 检查是否已存在相同内容
                cursor.execute("SELECT id FROM memories WHERE content_hash = ?", (content_hash,))
                existing = cursor.fetchone()
                if existing:
                    return existing[0]
                
                # 插入新记忆
                cursor.execute("""
                    INSERT INTO memories (content, content_hash, memory_type, importance_score,
                                        tags, metadata, embedding, user_id, session_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (content, content_hash, memory_type, importance,
                      json.dumps(tags or []), json.dumps(metadata or {}),
                      embedding, user_id, session_id))
                
                return cursor.lastrowid
        
        def retrieve_memories(self, user_id: str, query_type: str = 'recent',
                            limit: int = 10, **kwargs) -> List[Dict]:
            """检索记忆"""
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if query_type == 'recent':
                    cursor.execute("""
                        SELECT * FROM memories 
                        WHERE user_id = ? 
                        ORDER BY last_accessed DESC 
                        LIMIT ?
                    """, (user_id, limit))
                
                elif query_type == 'important':
                    cursor.execute("""
                        SELECT * FROM memories 
                        WHERE user_id = ? 
                        ORDER BY importance_score DESC, access_count DESC 
                        LIMIT ?
                    """, (user_id, limit))
                
                elif query_type == 'by_type':
                    memory_type = kwargs.get('memory_type')
                    cursor.execute("""
                        SELECT * FROM memories 
                        WHERE user_id = ? AND memory_type = ?
                        ORDER BY importance_score DESC 
                        LIMIT ?
                    """, (user_id, memory_type, limit))
                
                return [dict(row) for row in cursor.fetchall()]
        
        def update_memory_access(self, memory_id: int):
            """更新记忆访问统计"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE memories 
                    SET last_accessed = CURRENT_TIMESTAMP, 
                        access_count = access_count + 1
                    WHERE id = ?
                """, (memory_id,))
        
        def create_memory_relation(self, source_id: int, target_id: int,
                                 relation_type: str, strength: float = 0.5):
            """创建记忆关联"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO memory_relations 
                    (source_memory_id, target_memory_id, relation_type, strength)
                    VALUES (?, ?, ?, ?)
                """, (source_id, target_id, relation_type, strength))
        
        def get_related_memories(self, memory_id: int, relation_types: List[str] = None) -> List[Dict]:
            """获取相关记忆"""
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if relation_types:
                    placeholders = ','.join('?' * len(relation_types))
                    cursor.execute(f"""
                        SELECT m.*, r.relation_type, r.strength
                        FROM memories m
                        JOIN memory_relations r ON m.id = r.target_memory_id
                        WHERE r.source_memory_id = ? AND r.relation_type IN ({placeholders})
                        ORDER BY r.strength DESC
                    """, [memory_id] + relation_types)
                else:
                    cursor.execute("""
                        SELECT m.*, r.relation_type, r.strength
                        FROM memories m
                        JOIN memory_relations r ON m.id = r.target_memory_id
                        WHERE r.source_memory_id = ?
                        ORDER BY r.strength DESC
                    """, (memory_id,))
                
                return [dict(row) for row in cursor.fetchall()]
    ```

    ## 📊 数据库性能监控

    ### 性能指标收集
    ```python
    class DatabaseMonitor:
        def __init__(self, db_path: str):
            self.db_path = db_path
        
        def get_performance_stats(self) -> Dict[str, Any]:
            """获取性能统计"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 数据库大小
                cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
                db_size = cursor.fetchone()[0]
                
                # 表统计
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                table_stats = {}
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_stats[table] = count
                
                # 索引使用统计
                cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index'")
                indexes = cursor.fetchall()
                
                return {
                    'database_size_bytes': db_size,
                    'table_counts': table_stats,
                    'index_count': len(indexes),
                    'indexes': [{'name': idx[0], 'table': idx[1]} for idx in indexes]
                }
        
        def analyze_query_performance(self, query: str) -> Dict[str, Any]:
            """分析查询性能"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 查询计划
                cursor.execute(f"EXPLAIN QUERY PLAN {query}")
                query_plan = cursor.fetchall()
                
                # 执行时间测试
                import time
                start_time = time.time()
                cursor.execute(query)
                results = cursor.fetchall()
                end_time = time.time()
                
                return {
                    'execution_time_ms': (end_time - start_time) * 1000,
                    'result_count': len(results),
                    'query_plan': query_plan
                }
    ```

    ## 🔄 数据库维护策略

    ### 自动维护任务
    ```mermaid
    graph TD
        A[定期维护] --> B[数据清理]
        A --> C[索引优化]
        A --> D[统计更新]
        A --> E[备份管理]
        
        B --> B1[过期记忆清理]
        B --> B2[重复数据去除]
        B --> B3[无效关系清理]
        
        C --> C1[索引重建]
        C --> C2[查询优化]
        C --> C3[碎片整理]
        
        D --> D1[表统计更新]
        D --> D2[性能指标收集]
        
        E --> E1[增量备份]
        E --> E2[完整备份]
        E --> E3[备份验证]
    ```

    ### 数据备份与恢复
    ```python
    def backup_database(source_db: str, backup_path: str):
        """备份数据库"""
        import shutil
        
        # 创建备份
        shutil.copy2(source_db, backup_path)
        
        # 验证备份
        with sqlite3.connect(backup_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            if result != 'ok':
                raise Exception(f"Backup verification failed: {result}")
    
    def restore_database(backup_path: str, target_db: str):
        """恢复数据库"""
        import shutil
        
        # 验证备份文件
        with sqlite3.connect(backup_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            if result != 'ok':
                raise Exception(f"Backup file is corrupted: {result}")
        
        # 恢复数据库
        shutil.copy2(backup_path, target_db)
    ```
  </process>

  <criteria>
    ## 数据库管理评价标准

    ### 性能指标
    - ✅ 查询响应时间 ≤ 100ms（简单查询）
    - ✅ 查询响应时间 ≤ 1s（复杂查询）
    - ✅ 并发连接支持 ≥ 100
    - ✅ 数据库大小增长合理

    ### 可靠性指标
    - ✅ 数据一致性 100%
    - ✅ 事务成功率 ≥ 99.9%
    - ✅ 备份成功率 100%
    - ✅ 恢复成功率 ≥ 99%

    ### 安全性指标
    - ✅ 访问控制有效
    - ✅ 数据加密完整
    - ✅ 审计日志完整
    - ✅ 权限管理规范

    ### 可维护性指标
    - ✅ 数据库结构清晰
    - ✅ 索引策略合理
    - ✅ 监控指标完善
    - ✅ 维护文档完整
  </criteria>
</execution>

<execution>
  <constraint>
    ## 记忆管理限制条件
    - **性能约束**：记忆操作不得显著影响系统响应时间
    - **存储约束**：记忆存储空间有限，需要智能管理
    - **隐私约束**：敏感信息的记忆和检索必须符合隐私保护要求
    - **一致性约束**：分布式记忆系统必须保证数据一致性
    - **可靠性约束**：关键记忆不得丢失，需要备份机制
  </constraint>

  <rule>
    ## 记忆管理强制规则
    - **分层存储**：记忆必须按重要性和访问频率分层存储
    - **版本控制**：记忆更新必须保留版本历史
    - **访问控制**：记忆访问必须有权限控制机制
    - **定期清理**：过期和低价值记忆必须定期清理
    - **备份恢复**：重要记忆必须有备份和恢复机制
  </rule>

  <guideline>
    ## 记忆管理指导原则
    - **智能分类**：根据内容类型和重要性智能分类存储
    - **语义关联**：建立记忆间的语义关联关系
    - **渐进遗忘**：模拟人类记忆的渐进遗忘机制
    - **上下文感知**：记忆检索要考虑当前上下文
    - **持续学习**：基于使用模式持续优化记忆策略
  </guideline>

  <process>
    ## 🧠 MemGPT记忆管理流程

    ### 记忆架构设计
    ```mermaid
    graph TD
        A[用户输入] --> B[上下文分析]
        B --> C[记忆检索]
        C --> D[主上下文构建]
        D --> E[AI处理]
        E --> F[响应生成]
        F --> G[记忆更新]
        G --> H[记忆优化]
        
        C --> C1[工作记忆]
        C --> C2[长期记忆]
        C --> C3[知识图谱]
        
        G --> G1[新记忆创建]
        G --> G2[现有记忆更新]
        G --> G3[关联关系建立]
        
        H --> H1[重要性评估]
        H --> H2[访问频率统计]
        H --> H3[存储优化]
    ```

    ### 第一阶段：记忆存储
    ```mermaid
    flowchart TD
        A[信息输入] --> B[内容分析]
        B --> C[重要性评估]
        C --> D[分类标记]
        D --> E[存储决策]
        E --> F{存储层级}
        F -->|高重要性| G[长期记忆]
        F -->|中重要性| H[工作记忆]
        F -->|低重要性| I[临时缓存]
        
        G --> J[持久化存储]
        H --> K[会话存储]
        I --> L[自动清理]
        
        J --> M[向量索引]
        K --> N[快速访问]
        L --> O[内存释放]
    ```

    ### 第二阶段：记忆检索
    ```mermaid
    graph TD
        A[检索请求] --> B[查询分析]
        B --> C[检索策略选择]
        C --> D[多路检索]
        D --> E[结果融合]
        E --> F[相关性排序]
        F --> G[上下文过滤]
        G --> H[结果返回]
        
        D --> D1[关键词检索]
        D --> D2[语义检索]
        D --> D3[时间检索]
        D --> D4[关联检索]
        
        E --> E1[权重计算]
        E --> E2[去重处理]
        E --> E3[质量评估]
    ```

    ### 第三阶段：记忆优化
    ```mermaid
    flowchart LR
        A[记忆优化] --> B[使用统计]
        B --> C[重要性重评估]
        C --> D[存储层级调整]
        D --> E[关联关系优化]
        E --> F[过期清理]
        F --> G[压缩存储]
        
        B --> B1[访问频率]
        B --> B2[最近访问时间]
        B --> B3[用户反馈]
        
        C --> C1[业务价值评估]
        C --> C2[时效性评估]
        C --> C3[关联度评估]
    ```

    ## 🔧 记忆管理技术实现

    ### SQLite记忆存储设计
    ```sql
    -- 主记忆表
    CREATE TABLE memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        memory_type TEXT NOT NULL, -- 'fact', 'event', 'preference', 'skill'
        importance_score REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        access_count INTEGER DEFAULT 0,
        tags TEXT, -- JSON array of tags
        metadata JSON,
        embedding BLOB -- 向量嵌入
    );

    -- 记忆关联表
    CREATE TABLE memory_relations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_memory_id INTEGER,
        target_memory_id INTEGER,
        relation_type TEXT, -- 'similar', 'causal', 'temporal', 'hierarchical'
        strength REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (source_memory_id) REFERENCES memories(id),
        FOREIGN KEY (target_memory_id) REFERENCES memories(id)
    );

    -- 上下文会话表
    CREATE TABLE context_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE NOT NULL,
        context_data JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

    ### Python记忆管理实现
    ```python
    import sqlite3
    import json
    import numpy as np
    from datetime import datetime, timedelta
    from sentence_transformers import SentenceTransformer
    
    class MemoryManager:
        def __init__(self, db_path="memory.db"):
            self.db_path = db_path
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            self.init_database()
        
        def store_memory(self, content, memory_type, importance=0.5, tags=None):
            """存储新记忆"""
            # 生成向量嵌入
            embedding = self.encoder.encode(content)
            
            # 存储到数据库
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO memories (content, memory_type, importance_score, tags, embedding)
                    VALUES (?, ?, ?, ?, ?)
                """, (content, memory_type, importance, json.dumps(tags or []), embedding.tobytes()))
                
                memory_id = cursor.lastrowid
                
            # 建立关联关系
            self.build_associations(memory_id, content)
            
            return memory_id
        
        def retrieve_memories(self, query, limit=10, threshold=0.7):
            """检索相关记忆"""
            # 生成查询向量
            query_embedding = self.encoder.encode(query)
            
            # 从数据库检索
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, content, embedding FROM memories")
                
                results = []
                for row in cursor.fetchall():
                    memory_id, content, embedding_bytes = row
                    embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
                    
                    # 计算相似度
                    similarity = np.dot(query_embedding, embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
                    )
                    
                    if similarity > threshold:
                        results.append((memory_id, content, similarity))
                
                # 按相似度排序
                results.sort(key=lambda x: x[2], reverse=True)
                
                # 更新访问统计
                for memory_id, _, _ in results[:limit]:
                    self.update_access_stats(memory_id)
                
                return results[:limit]
        
        def update_memory(self, memory_id, new_content=None, new_importance=None):
            """更新记忆"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if new_content:
                    new_embedding = self.encoder.encode(new_content)
                    cursor.execute("""
                        UPDATE memories 
                        SET content = ?, embedding = ?, updated_at = ?
                        WHERE id = ?
                    """, (new_content, new_embedding.tobytes(), datetime.now(), memory_id))
                
                if new_importance is not None:
                    cursor.execute("""
                        UPDATE memories 
                        SET importance_score = ?, updated_at = ?
                        WHERE id = ?
                    """, (new_importance, datetime.now(), memory_id))
        
        def cleanup_memories(self, days_threshold=30, importance_threshold=0.3):
            """清理过期和低价值记忆"""
            cutoff_date = datetime.now() - timedelta(days=days_threshold)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM memories 
                    WHERE last_accessed < ? AND importance_score < ?
                """, (cutoff_date, importance_threshold))
                
                deleted_count = cursor.rowcount
                
            return deleted_count
    ```

    ## 📊 记忆质量管理

    ### 记忆重要性评估
    ```python
    def calculate_importance(content, context, user_profile):
        """计算记忆重要性"""
        factors = {
            'frequency': calculate_frequency_score(content),
            'recency': calculate_recency_score(context),
            'relevance': calculate_relevance_score(content, user_profile),
            'uniqueness': calculate_uniqueness_score(content),
            'emotional_weight': calculate_emotional_score(content)
        }
        
        # 加权计算
        weights = {
            'frequency': 0.2,
            'recency': 0.15,
            'relevance': 0.3,
            'uniqueness': 0.2,
            'emotional_weight': 0.15
        }
        
        importance = sum(factors[key] * weights[key] for key in factors)
        return min(max(importance, 0.0), 1.0)  # 限制在[0,1]范围内
    ```

    ### 记忆关联建立
    ```mermaid
    graph TD
        A[新记忆] --> B[内容分析]
        B --> C[相似性计算]
        C --> D[时序关系分析]
        D --> E[因果关系识别]
        E --> F[层次关系判断]
        F --> G[关联强度计算]
        G --> H[关联关系存储]
        
        C --> C1[语义相似性]
        C --> C2[关键词重叠]
        
        D --> D1[时间邻近性]
        D --> D2[事件序列]
        
        E --> E1[逻辑因果]
        E --> E2[统计相关]
        
        F --> F1[概念层次]
        F --> F2[分类关系]
    ```

    ## 🔄 自适应记忆机制

    ### 记忆衰减模型
    ```python
    def memory_decay(initial_strength, time_elapsed, decay_rate=0.1):
        """记忆衰减模型（基于艾宾浩斯遗忘曲线）"""
        return initial_strength * np.exp(-decay_rate * time_elapsed)
    
    def adaptive_decay_rate(access_frequency, importance):
        """自适应衰减率"""
        base_rate = 0.1
        frequency_factor = 1.0 / (1.0 + access_frequency)
        importance_factor = 1.0 - importance
        
        return base_rate * frequency_factor * importance_factor
    ```

    ### 记忆强化机制
    ```python
    def reinforce_memory(memory_id, reinforcement_type='access'):
        """记忆强化机制"""
        reinforcement_values = {
            'access': 0.1,      # 访问强化
            'positive_feedback': 0.3,  # 正面反馈
            'repetition': 0.2,   # 重复强化
            'association': 0.15  # 关联强化
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 获取当前重要性
            cursor.execute("SELECT importance_score FROM memories WHERE id = ?", (memory_id,))
            current_importance = cursor.fetchone()[0]
            
            # 计算新的重要性
            reinforcement = reinforcement_values.get(reinforcement_type, 0.1)
            new_importance = min(current_importance + reinforcement, 1.0)
            
            # 更新记忆
            cursor.execute("""
                UPDATE memories 
                SET importance_score = ?, last_accessed = ?, access_count = access_count + 1
                WHERE id = ?
            """, (new_importance, datetime.now(), memory_id))
    ```
  </process>

  <criteria>
    ## 记忆管理评价标准

    ### 存储效率
    - ✅ 记忆存储时间 ≤ 100ms
    - ✅ 存储空间利用率 ≥ 85%
    - ✅ 数据压缩率 ≥ 60%
    - ✅ 并发存储支持 ≥ 100 ops/s

    ### 检索性能
    - ✅ 记忆检索时间 ≤ 200ms
    - ✅ 检索准确率 ≥ 90%
    - ✅ 相关性排序准确度 ≥ 85%
    - ✅ 检索覆盖率 ≥ 95%

    ### 记忆质量
    - ✅ 记忆保持率 ≥ 95%（重要记忆）
    - ✅ 关联准确性 ≥ 80%
    - ✅ 重要性评估准确度 ≥ 85%
    - ✅ 记忆一致性 ≥ 98%

    ### 系统可靠性
    - ✅ 数据丢失率 ≤ 0.01%
    - ✅ 系统可用性 ≥ 99.9%
    - ✅ 备份恢复成功率 ≥ 99%
    - ✅ 并发安全性 100%
  </criteria>
</execution>

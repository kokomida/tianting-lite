<execution>
  <constraint>
    ## 向量搜索限制条件
    - **性能约束**：搜索响应时间必须在毫秒级别
    - **内存约束**：向量索引的内存使用有限制
    - **精度约束**：搜索结果的相关性必须达到要求
    - **并发约束**：系统必须支持高并发搜索请求
    - **扩展性约束**：索引结构必须支持动态扩展
  </constraint>

  <rule>
    ## 向量搜索强制规则
    - **索引一致性**：向量索引必须与原始数据保持一致
    - **搜索准确性**：相似度计算必须准确可靠
    - **实时更新**：新增向量必须及时加入索引
    - **结果排序**：搜索结果必须按相似度正确排序
    - **错误处理**：搜索失败必须有明确的错误信息
  </rule>

  <guideline>
    ## 向量搜索指导原则
    - **效率优先**：优先选择高效的搜索算法
    - **精度平衡**：在速度和精度间找到最佳平衡
    - **资源优化**：合理使用计算和存储资源
    - **用户体验**：提供流畅的搜索体验
    - **可扩展性**：设计支持未来扩展的架构
  </guideline>

  <process>
    ## 🔍 向量搜索工作流程

    ### 搜索系统架构
    ```mermaid
    graph TD
        A[搜索请求] --> B[查询预处理]
        B --> C[向量编码]
        C --> D[索引检索]
        D --> E[相似度计算]
        E --> F[结果排序]
        F --> G[后处理]
        G --> H[结果返回]
        
        D --> D1[HNSW索引]
        D --> D2[IVF索引]
        D --> D3[LSH索引]
        
        E --> E1[余弦相似度]
        E --> E2[欧几里得距离]
        E --> E3[内积相似度]
        
        G --> G1[结果过滤]
        G --> G2[重排序]
        G --> G3[元数据补充]
    ```

    ### 第一阶段：查询预处理
    ```mermaid
    flowchart TD
        A[原始查询] --> B[文本清洗]
        B --> C[分词处理]
        C --> D[停用词过滤]
        D --> E[查询扩展]
        E --> F[查询向量化]
        
        B --> B1[去除特殊字符]
        B --> B2[统一编码格式]
        
        C --> C1[中文分词]
        C --> C2[英文分词]
        
        E --> E1[同义词扩展]
        E --> E2[相关词扩展]
        
        F --> F1[Embedding生成]
        F --> F2[向量标准化]
    ```

    ### 第二阶段：向量检索
    ```mermaid
    graph TD
        A[查询向量] --> B[索引选择]
        B --> C[粗排检索]
        C --> D[精排计算]
        D --> E[TopK选择]
        E --> F[结果聚合]
        
        B --> B1[HNSW图索引]
        B --> B2[IVF聚类索引]
        B --> B3[PQ量化索引]
        
        C --> C1[候选集生成]
        C --> C2[距离估算]
        
        D --> D1[精确距离计算]
        D --> D2[相似度评分]
        
        E --> E1[堆排序]
        E --> E2[阈值过滤]
    ```

    ### 第三阶段：结果优化
    ```mermaid
    flowchart LR
        A[初始结果] --> B[相关性评估]
        B --> C[多样性优化]
        C --> D[个性化调整]
        D --> E[结果重排]
        E --> F[最终输出]
        
        B --> B1[语义相关性]
        B --> B2[主题相关性]
        
        C --> C1[去重处理]
        C --> C2[多样性注入]
        
        D --> D1[用户偏好]
        D --> D2[历史行为]
        
        E --> E1[学习排序]
        E --> E2[规则调整]
    ```

    ## 🛠️ 技术实现框架

    ### Python向量搜索实现
    ```python
    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer
    import hnswlib
    
    class VectorSearchEngine:
        def __init__(self, dimension=384, index_type='hnsw'):
            self.dimension = dimension
            self.index_type = index_type
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            self.index = None
            self.documents = []
            self.init_index()
        
        def init_index(self):
            """初始化向量索引"""
            if self.index_type == 'hnsw':
                self.index = hnswlib.Index(space='cosine', dim=self.dimension)
                self.index.init_index(max_elements=1000000, ef_construction=200, M=16)
            elif self.index_type == 'faiss':
                self.index = faiss.IndexFlatIP(self.dimension)
            elif self.index_type == 'ivf':
                quantizer = faiss.IndexFlatIP(self.dimension)
                self.index = faiss.IndexIVFFlat(quantizer, self.dimension, 100)
        
        def add_documents(self, documents):
            """添加文档到索引"""
            # 生成向量
            vectors = self.encoder.encode(documents)
            vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
            
            # 添加到索引
            if self.index_type == 'hnsw':
                start_id = len(self.documents)
                ids = np.arange(start_id, start_id + len(documents))
                self.index.add_items(vectors, ids)
            else:
                self.index.add(vectors.astype('float32'))
            
            # 保存文档
            self.documents.extend(documents)
        
        def search(self, query, top_k=10, ef=50):
            """搜索相似文档"""
            # 查询向量化
            query_vector = self.encoder.encode([query])
            query_vector = query_vector / np.linalg.norm(query_vector)
            
            # 执行搜索
            if self.index_type == 'hnsw':
                self.index.set_ef(ef)
                labels, distances = self.index.knn_query(query_vector, k=top_k)
                results = []
                for i, (label, distance) in enumerate(zip(labels[0], distances[0])):
                    results.append({
                        'document': self.documents[label],
                        'score': 1 - distance,  # 转换为相似度
                        'rank': i + 1
                    })
            else:
                distances, indices = self.index.search(query_vector.astype('float32'), top_k)
                results = []
                for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
                    results.append({
                        'document': self.documents[idx],
                        'score': distance,
                        'rank': i + 1
                    })
            
            return results
        
        def update_document(self, doc_id, new_content):
            """更新文档"""
            if doc_id < len(self.documents):
                self.documents[doc_id] = new_content
                # 重新生成向量并更新索引
                new_vector = self.encoder.encode([new_content])
                new_vector = new_vector / np.linalg.norm(new_vector)
                
                if self.index_type == 'hnsw':
                    # HNSW需要重建索引来更新
                    self.rebuild_index()
                else:
                    # Faiss可以直接替换
                    self.index.reconstruct(doc_id, new_vector.astype('float32'))
        
        def rebuild_index(self):
            """重建索引"""
            if self.documents:
                self.init_index()
                self.add_documents(self.documents)
    ```

    ### 高级搜索功能
    ```python
    class AdvancedVectorSearch(VectorSearchEngine):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.metadata = []
        
        def add_documents_with_metadata(self, documents, metadata):
            """添加带元数据的文档"""
            self.add_documents(documents)
            self.metadata.extend(metadata)
        
        def filtered_search(self, query, filters=None, top_k=10):
            """带过滤条件的搜索"""
            # 先进行向量搜索
            initial_results = self.search(query, top_k * 3)  # 获取更多候选
            
            # 应用过滤条件
            filtered_results = []
            for result in initial_results:
                doc_idx = self.documents.index(result['document'])
                metadata = self.metadata[doc_idx] if doc_idx < len(self.metadata) else {}
                
                # 检查过滤条件
                if self._match_filters(metadata, filters):
                    result['metadata'] = metadata
                    filtered_results.append(result)
                
                if len(filtered_results) >= top_k:
                    break
            
            return filtered_results
        
        def _match_filters(self, metadata, filters):
            """检查元数据是否匹配过滤条件"""
            if not filters:
                return True
            
            for key, value in filters.items():
                if key not in metadata:
                    return False
                if isinstance(value, list):
                    if metadata[key] not in value:
                        return False
                else:
                    if metadata[key] != value:
                        return False
            
            return True
        
        def hybrid_search(self, query, text_weight=0.7, vector_weight=0.3, top_k=10):
            """混合搜索（文本+向量）"""
            # 向量搜索
            vector_results = self.search(query, top_k * 2)
            
            # 文本搜索（简单的关键词匹配）
            text_results = self._text_search(query, top_k * 2)
            
            # 结果融合
            combined_scores = {}
            
            # 向量搜索结果
            for result in vector_results:
                doc = result['document']
                combined_scores[doc] = vector_weight * result['score']
            
            # 文本搜索结果
            for result in text_results:
                doc = result['document']
                if doc in combined_scores:
                    combined_scores[doc] += text_weight * result['score']
                else:
                    combined_scores[doc] = text_weight * result['score']
            
            # 排序并返回
            sorted_results = sorted(combined_scores.items(), 
                                  key=lambda x: x[1], reverse=True)
            
            return [{'document': doc, 'score': score, 'rank': i+1} 
                   for i, (doc, score) in enumerate(sorted_results[:top_k])]
        
        def _text_search(self, query, top_k):
            """简单的文本搜索"""
            query_terms = query.lower().split()
            scores = []
            
            for doc in self.documents:
                doc_lower = doc.lower()
                score = sum(1 for term in query_terms if term in doc_lower)
                score = score / len(query_terms) if query_terms else 0
                scores.append({'document': doc, 'score': score})
            
            scores.sort(key=lambda x: x['score'], reverse=True)
            return scores[:top_k]
    ```

    ## 📊 搜索性能优化

    ### 索引优化策略
    ```mermaid
    graph TD
        A[索引优化] --> B[结构优化]
        A --> C[参数调优]
        A --> D[内存优化]
        A --> E[并发优化]
        
        B --> B1[HNSW图结构]
        B --> B2[IVF聚类数量]
        B --> B3[PQ量化参数]
        
        C --> C1[ef_construction]
        C --> C2[M连接数]
        C --> C3[ef搜索参数]
        
        D --> D1[向量压缩]
        D --> D2[批量加载]
        D --> D3[内存映射]
        
        E --> E1[读写分离]
        E --> E2[查询缓存]
        E --> E3[负载均衡]
    ```

    ### 搜索质量评估
    ```python
    def evaluate_search_quality(search_engine, test_queries, ground_truth):
        """评估搜索质量"""
        metrics = {
            'precision_at_k': [],
            'recall_at_k': [],
            'ndcg_at_k': [],
            'mrr': []
        }
        
        for query, relevant_docs in zip(test_queries, ground_truth):
            results = search_engine.search(query, top_k=10)
            retrieved_docs = [r['document'] for r in results]
            
            # 计算Precision@K
            precision = len(set(retrieved_docs) & set(relevant_docs)) / len(retrieved_docs)
            metrics['precision_at_k'].append(precision)
            
            # 计算Recall@K
            recall = len(set(retrieved_docs) & set(relevant_docs)) / len(relevant_docs)
            metrics['recall_at_k'].append(recall)
            
            # 计算NDCG@K
            ndcg = calculate_ndcg(retrieved_docs, relevant_docs)
            metrics['ndcg_at_k'].append(ndcg)
            
            # 计算MRR
            mrr = calculate_mrr(retrieved_docs, relevant_docs)
            metrics['mrr'].append(mrr)
        
        # 计算平均值
        for key in metrics:
            metrics[key] = np.mean(metrics[key])
        
        return metrics
    ```

    ## 🔄 动态索引管理

    ### 增量更新机制
    ```mermaid
    flowchart LR
        A[新文档] --> B[向量生成]
        B --> C[索引更新]
        C --> D[一致性检查]
        D --> E{更新成功?}
        E -->|是| F[索引优化]
        E -->|否| G[回滚操作]
        
        C --> C1[在线更新]
        C --> C2[批量更新]
        
        F --> F1[索引压缩]
        F --> F2[性能调优]
        
        G --> G1[错误日志]
        G --> G2[重试机制]
    ```

    ### 索引维护策略
    ```python
    def maintain_index(search_engine, maintenance_config):
        """索引维护"""
        # 定期重建索引
        if maintenance_config.get('rebuild_threshold', 0.1):
            fragmentation = calculate_index_fragmentation(search_engine)
            if fragmentation > maintenance_config['rebuild_threshold']:
                search_engine.rebuild_index()
        
        # 清理过期文档
        if maintenance_config.get('cleanup_enabled', False):
            expired_docs = find_expired_documents(search_engine)
            for doc_id in expired_docs:
                search_engine.remove_document(doc_id)
        
        # 性能监控
        performance_metrics = collect_performance_metrics(search_engine)
        if performance_metrics['avg_search_time'] > maintenance_config.get('max_search_time', 100):
            optimize_search_parameters(search_engine)
    ```
  </process>

  <criteria>
    ## 向量搜索评价标准

    ### 搜索性能
    - ✅ 搜索响应时间 ≤ 50ms
    - ✅ 并发查询支持 ≥ 1000 QPS
    - ✅ 索引构建时间合理
    - ✅ 内存使用效率 ≥ 80%

    ### 搜索质量
    - ✅ Top-10准确率 ≥ 85%
    - ✅ 召回率 ≥ 90%
    - ✅ NDCG@10 ≥ 0.8
    - ✅ 平均倒数排名 ≥ 0.75

    ### 系统可靠性
    - ✅ 索引一致性 ≥ 99.9%
    - ✅ 系统可用性 ≥ 99.5%
    - ✅ 数据完整性 100%
    - ✅ 错误恢复能力强

    ### 可扩展性
    - ✅ 支持向量数量 ≥ 10M
    - ✅ 水平扩展能力良好
    - ✅ 动态更新支持
    - ✅ 存储效率优化
  </criteria>
</execution>

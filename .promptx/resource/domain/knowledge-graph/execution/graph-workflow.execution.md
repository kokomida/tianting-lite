<execution>
  <constraint>
    ## 知识图谱构建限制条件
    - **计算资源约束**：图谱构建和查询的计算复杂度有限
    - **存储约束**：图数据存储空间和索引大小有限制
    - **实时性约束**：图谱更新和查询必须在可接受时间内完成
    - **准确性约束**：实体识别和关系抽取的准确率要求
    - **一致性约束**：图谱数据必须保持逻辑一致性
  </constraint>

  <rule>
    ## 知识图谱强制规则
    - **实体唯一性**：同一实体在图谱中必须唯一标识
    - **关系有向性**：所有关系必须明确方向和语义
    - **数据溯源**：所有实体和关系必须可追溯到原始数据源
    - **版本控制**：图谱变更必须有版本记录和回滚机制
    - **质量验证**：新增实体和关系必须通过质量检查
  </rule>

  <guideline>
    ## 知识图谱指导原则
    - **语义驱动**：图谱构建以语义理解为核心
    - **渐进构建**：从简单到复杂，逐步完善图谱
    - **多源融合**：整合多个数据源的知识
    - **动态更新**：支持知识的动态增加和修正
    - **可解释性**：图谱推理结果必须可解释
  </guideline>

  <process>
    ## 🕸️ 知识图谱构建流程

    ### 图谱构建架构
    ```mermaid
    graph TD
        A[文本输入] --> B[预处理]
        B --> C[实体识别]
        C --> D[关系抽取]
        D --> E[实体链接]
        E --> F[知识融合]
        F --> G[图谱存储]
        G --> H[质量验证]
        H --> I[图谱优化]
        
        C --> C1[命名实体识别]
        C --> C2[概念抽取]
        C --> C3[实体分类]
        
        D --> D1[句法分析]
        D --> D2[语义角色标注]
        D --> D3[关系分类]
        
        E --> E1[实体消歧]
        E --> E2[实体对齐]
        E --> E3[实体合并]
    ```

    ### 第一阶段：实体识别与抽取
    ```mermaid
    flowchart TD
        A[文本输入] --> B[分词处理]
        B --> C[词性标注]
        C --> D[命名实体识别]
        D --> E[实体分类]
        E --> F[实体标准化]
        F --> G[实体验证]
        
        D --> D1[人名识别]
        D --> D2[地名识别]
        D --> D3[机构名识别]
        D --> D4[概念识别]
        
        E --> E1[实体类型分类]
        E --> E2[实体属性提取]
        E --> E3[实体描述生成]
        
        F --> F1[名称标准化]
        F --> F2[格式统一]
        F --> F3[编码规范化]
    ```

    ### 第二阶段：关系抽取与建模
    ```mermaid
    graph TD
        A[实体对] --> B[上下文分析]
        B --> C[句法依存分析]
        C --> D[语义角色标注]
        D --> E[关系模式匹配]
        E --> F[关系分类]
        F --> G[关系验证]
        G --> H[关系存储]
        
        E --> E1[规则匹配]
        E --> E2[模板匹配]
        E --> E3[机器学习分类]
        
        F --> F1[因果关系]
        F --> F2[层次关系]
        F --> F3[时序关系]
        F --> F4[空间关系]
        F --> F5[属性关系]
    ```

    ### 第三阶段：知识融合与优化
    ```mermaid
    flowchart LR
        A[多源知识] --> B[实体对齐]
        B --> C[关系合并]
        C --> D[冲突检测]
        D --> E[冲突解决]
        E --> F[知识验证]
        F --> G[图谱更新]
        
        B --> B1[字符串匹配]
        B --> B2[语义相似度]
        B --> B3[结构相似度]
        
        D --> D1[逻辑冲突]
        D --> D2[数值冲突]
        D --> D3[时间冲突]
        
        E --> E1[置信度比较]
        E --> E2[来源权威性]
        E --> E3[时效性判断]
    ```

    ## 🛠️ 技术实现框架

    ### Python知识图谱构建
    ```python
    import spacy
    import networkx as nx
    from neo4j import GraphDatabase
    import pandas as pd
    
    class KnowledgeGraphBuilder:
        def __init__(self, neo4j_uri, username, password):
            self.nlp = spacy.load("zh_core_web_sm")
            self.driver = GraphDatabase.driver(neo4j_uri, auth=(username, password))
            self.graph = nx.DiGraph()
        
        def extract_entities(self, text):
            """实体抽取"""
            doc = self.nlp(text)
            entities = []
            
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'description': spacy.explain(ent.label_)
                })
            
            return entities
        
        def extract_relations(self, text):
            """关系抽取"""
            doc = self.nlp(text)
            relations = []
            
            # 基于依存句法的关系抽取
            for token in doc:
                if token.dep_ in ['nsubj', 'dobj', 'pobj']:
                    head = token.head
                    relations.append({
                        'subject': token.text,
                        'predicate': head.text,
                        'object': head.text if token.dep_ == 'nsubj' else token.text,
                        'relation_type': token.dep_
                    })
            
            return relations
        
        def build_graph(self, entities, relations):
            """构建图谱"""
            # 添加实体节点
            for entity in entities:
                self.graph.add_node(
                    entity['text'],
                    type=entity['label'],
                    description=entity.get('description', '')
                )
            
            # 添加关系边
            for relation in relations:
                if relation['subject'] in self.graph and relation['object'] in self.graph:
                    self.graph.add_edge(
                        relation['subject'],
                        relation['object'],
                        relation=relation['predicate'],
                        type=relation['relation_type']
                    )
        
        def save_to_neo4j(self):
            """保存到Neo4j数据库"""
            with self.driver.session() as session:
                # 创建节点
                for node, attrs in self.graph.nodes(data=True):
                    session.run(
                        "MERGE (n:Entity {name: $name, type: $type, description: $desc})",
                        name=node, type=attrs.get('type', ''), desc=attrs.get('description', '')
                    )
                
                # 创建关系
                for source, target, attrs in self.graph.edges(data=True):
                    session.run(
                        """
                        MATCH (a:Entity {name: $source}), (b:Entity {name: $target})
                        MERGE (a)-[r:RELATES {type: $rel_type, relation: $relation}]->(b)
                        """,
                        source=source, target=target, 
                        rel_type=attrs.get('type', ''), relation=attrs.get('relation', '')
                    )
    ```

    ### 图谱查询与推理
    ```python
    class GraphQueryEngine:
        def __init__(self, driver):
            self.driver = driver
        
        def find_shortest_path(self, start_entity, end_entity):
            """查找最短路径"""
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH path = shortestPath((start:Entity {name: $start})-[*]-(end:Entity {name: $end}))
                    RETURN path
                    """,
                    start=start_entity, end=end_entity
                )
                return result.single()
        
        def find_related_entities(self, entity, max_depth=2):
            """查找相关实体"""
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (start:Entity {name: $entity})-[*1..$depth]-(related:Entity)
                    RETURN DISTINCT related.name as name, related.type as type
                    """,
                    entity=entity, depth=max_depth
                )
                return [record for record in result]
        
        def semantic_search(self, query_concept):
            """语义搜索"""
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (n:Entity)
                    WHERE n.name CONTAINS $query OR n.description CONTAINS $query
                    RETURN n.name as name, n.type as type, n.description as description
                    ORDER BY n.name
                    """,
                    query=query_concept
                )
                return [record for record in result]
    ```

    ## 📊 图谱质量管理

    ### 实体质量评估
    ```python
    def evaluate_entity_quality(entity, context):
        """评估实体质量"""
        quality_factors = {
            'completeness': check_entity_completeness(entity),
            'accuracy': check_entity_accuracy(entity, context),
            'consistency': check_entity_consistency(entity),
            'uniqueness': check_entity_uniqueness(entity)
        }
        
        weights = {'completeness': 0.3, 'accuracy': 0.4, 'consistency': 0.2, 'uniqueness': 0.1}
        quality_score = sum(quality_factors[key] * weights[key] for key in quality_factors)
        
        return quality_score
    ```

    ### 关系质量验证
    ```mermaid
    graph TD
        A[关系验证] --> B[语法检查]
        A --> C[语义检查]
        A --> D[逻辑检查]
        A --> E[一致性检查]
        
        B --> B1[主谓宾结构]
        B --> B2[关系方向性]
        
        C --> C1[语义合理性]
        C --> C2[领域知识验证]
        
        D --> D1[逻辑矛盾检测]
        D --> D2[传递性验证]
        
        E --> E1[同类关系一致性]
        E --> E2[跨源一致性]
    ```

    ## 🔄 图谱动态更新

    ### 增量更新机制
    ```python
    def incremental_update(new_text, existing_graph):
        """增量更新图谱"""
        # 1. 抽取新知识
        new_entities = extract_entities(new_text)
        new_relations = extract_relations(new_text)
        
        # 2. 实体对齐
        aligned_entities = align_entities(new_entities, existing_graph)
        
        # 3. 冲突检测
        conflicts = detect_conflicts(new_relations, existing_graph)
        
        # 4. 冲突解决
        resolved_relations = resolve_conflicts(conflicts)
        
        # 5. 图谱更新
        update_graph(aligned_entities, resolved_relations, existing_graph)
        
        return existing_graph
    ```

    ### 图谱版本管理
    ```mermaid
    flowchart LR
        A[图谱V1.0] --> B[变更检测]
        B --> C[增量计算]
        C --> D[版本创建]
        D --> E[图谱V1.1]
        E --> F[质量验证]
        F --> G{验证通过?}
        G -->|是| H[版本发布]
        G -->|否| I[回滚到V1.0]
        
        D --> D1[变更日志]
        D --> D2[差异记录]
        D --> D3[元数据更新]
    ```
  </process>

  <criteria>
    ## 知识图谱评价标准

    ### 构建质量
    - ✅ 实体识别准确率 ≥ 90%
    - ✅ 关系抽取准确率 ≥ 85%
    - ✅ 实体链接准确率 ≥ 88%
    - ✅ 图谱完整性 ≥ 95%

    ### 查询性能
    - ✅ 简单查询响应时间 ≤ 100ms
    - ✅ 复杂查询响应时间 ≤ 1s
    - ✅ 并发查询支持 ≥ 100 qps
    - ✅ 查询准确率 ≥ 92%

    ### 系统可靠性
    - ✅ 图谱一致性 ≥ 98%
    - ✅ 数据完整性 ≥ 99%
    - ✅ 系统可用性 ≥ 99.5%
    - ✅ 更新成功率 ≥ 99%

    ### 可扩展性
    - ✅ 支持节点数 ≥ 1M
    - ✅ 支持关系数 ≥ 10M
    - ✅ 水平扩展能力良好
    - ✅ 存储效率 ≥ 80%
  </criteria>
</execution>

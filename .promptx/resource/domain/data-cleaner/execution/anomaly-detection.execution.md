<execution>
  <constraint>
    ## 异常检测限制条件
    - **实时性约束**：异常检测必须在可接受时间内完成
    - **准确性约束**：必须平衡检测精度和误报率
    - **计算资源约束**：检测算法的计算复杂度有限
    - **数据隐私约束**：检测过程不得泄露敏感信息
    - **可解释性约束**：检测结果必须可解释和可验证
  </constraint>

  <rule>
    ## 异常检测强制规则
    - **多方法验证**：重要异常必须通过多种方法验证
    - **阈值动态调整**：检测阈值必须根据数据特征动态调整
    - **异常分级处理**：不同级别异常采用不同处理策略
    - **检测结果记录**：所有异常检测结果必须详细记录
    - **人工复核机制**：关键异常必须经过人工复核
  </rule>

  <guideline>
    ## 异常检测指导原则
    - **业务导向**：异常定义必须符合业务理解
    - **统计与规则结合**：结合统计方法和业务规则
    - **渐进式检测**：从粗粒度到细粒度的渐进检测
    - **上下文感知**：考虑数据的时间和空间上下文
    - **持续学习**：基于反馈持续优化检测模型
  </guideline>

  <process>
    ## 🔍 异常检测执行流程

    ### 异常检测架构
    ```mermaid
    graph TD
        A[数据输入] --> B[预处理]
        B --> C[特征提取]
        C --> D[异常检测]
        D --> E[结果验证]
        E --> F[异常分级]
        F --> G[处理决策]
        G --> H[执行处理]
        H --> I[反馈学习]
        
        D --> D1[统计方法]
        D --> D2[机器学习]
        D --> D3[规则引擎]
        D --> D4[深度学习]
        
        style A fill:#e1f5fe
        style H fill:#e8f5e9
        style F fill:#fff3e0
    ```

    ### 第一层：统计异常检测
    ```mermaid
    flowchart LR
        A[统计检测] --> B[描述统计]
        A --> C[分布检测]
        A --> D[时序检测]
        A --> E[相关性检测]
        
        B --> B1[均值偏差]
        B --> B2[标准差检测]
        B --> B3[四分位数检测]
        B --> B4[Z-Score检测]
        
        C --> C1[正态性检验]
        C --> C2[分布拟合]
        C --> C3[KS检验]
        
        D --> D1[趋势异常]
        D --> D2[季节性异常]
        D --> D3[周期性异常]
        
        E --> E1[相关系数异常]
        E --> E2[协方差异常]
    ```

    ### 第二层：机器学习异常检测
    ```mermaid
    graph TD
        A[ML异常检测] --> B[无监督学习]
        A --> C[半监督学习]
        A --> D[监督学习]
        
        B --> B1[聚类方法]
        B --> B2[密度估计]
        B --> B3[降维方法]
        
        B1 --> B11[K-Means]
        B1 --> B12[DBSCAN]
        B1 --> B13[Isolation Forest]
        
        B2 --> B21[LOF]
        B2 --> B22[COPOD]
        B2 --> B23[KDE]
        
        B3 --> B31[PCA]
        B3 --> B32[Autoencoder]
        B3 --> B33[t-SNE]
        
        C --> C1[One-Class SVM]
        C --> C2[SVDD]
        
        D --> D1[分类方法]
        D --> D2[回归方法]
    ```

    ### 第三层：深度学习异常检测
    ```mermaid
    flowchart TD
        A[深度学习检测] --> B[自编码器]
        A --> C[循环神经网络]
        A --> D[生成对抗网络]
        A --> E[注意力机制]
        
        B --> B1[Vanilla AE]
        B --> B2[Variational AE]
        B --> B3[Denoising AE]
        
        C --> C1[LSTM]
        C --> C2[GRU]
        C --> C3[Transformer]
        
        D --> D1[AnoGAN]
        D --> D2[BiGAN]
        
        E --> E1[Self-Attention]
        E --> E2[Multi-Head Attention]
    ```

    ## 🎯 异常类型与检测策略

    ### 点异常检测
    ```python
    import numpy as np
    from sklearn.ensemble import IsolationForest
    from sklearn.svm import OneClassSVM
    
    def detect_point_anomalies(data, method='isolation_forest'):
        """点异常检测"""
        if method == 'isolation_forest':
            detector = IsolationForest(contamination=0.1, random_state=42)
        elif method == 'one_class_svm':
            detector = OneClassSVM(nu=0.1)
        
        # 训练和预测
        anomaly_labels = detector.fit_predict(data)
        anomaly_scores = detector.decision_function(data)
        
        return anomaly_labels, anomaly_scores
    
    # Z-Score方法
    def z_score_anomaly_detection(data, threshold=3):
        """基于Z-Score的异常检测"""
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        return z_scores > threshold
    ```

    ### 上下文异常检测
    ```python
    def detect_contextual_anomalies(data, context_features, behavioral_features):
        """上下文异常检测"""
        from sklearn.cluster import DBSCAN
        
        # 在上下文特征空间中聚类
        clustering = DBSCAN(eps=0.5, min_samples=5)
        context_clusters = clustering.fit_predict(context_features)
        
        anomalies = []
        for cluster_id in np.unique(context_clusters):
            if cluster_id == -1:  # 噪声点
                continue
                
            # 获取同一上下文的数据
            cluster_mask = context_clusters == cluster_id
            cluster_behavioral = behavioral_features[cluster_mask]
            
            # 在行为特征空间中检测异常
            cluster_anomalies = detect_point_anomalies(cluster_behavioral)
            anomalies.extend(cluster_anomalies)
        
        return anomalies
    ```

    ### 集体异常检测
    ```python
    def detect_collective_anomalies(time_series_data, window_size=10):
        """集体异常检测"""
        from sklearn.preprocessing import StandardScaler
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense
        
        # 数据预处理
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(time_series_data.reshape(-1, 1))
        
        # 创建时间窗口
        X, y = [], []
        for i in range(window_size, len(scaled_data)):
            X.append(scaled_data[i-window_size:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        
        # LSTM自编码器
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(window_size, 1)),
            LSTM(50, return_sequences=False),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse')
        model.fit(X.reshape(X.shape[0], X.shape[1], 1), y, epochs=100, verbose=0)
        
        # 预测和计算重构误差
        predictions = model.predict(X.reshape(X.shape[0], X.shape[1], 1))
        mse = np.mean(np.power(y - predictions.flatten(), 2), axis=1)
        
        # 异常检测
        threshold = np.percentile(mse, 95)
        anomalies = mse > threshold
        
        return anomalies, mse
    ```

    ## 📊 异常评估与处理

    ### 异常评分机制
    ```mermaid
    graph TD
        A[异常检测结果] --> B[多方法融合]
        B --> C[异常评分]
        C --> D[置信度计算]
        D --> E[异常排序]
        E --> F[阈值判断]
        F --> G[异常分级]
        
        B --> B1[投票机制]
        B --> B2[加权平均]
        B --> B3[集成学习]
        
        C --> C1[统计评分]
        C --> C2[距离评分]
        C --> C3[概率评分]
        
        G --> G1[严重异常]
        G --> G2[中等异常]
        G --> G3[轻微异常]
    ```

    ### 异常处理策略
    ```mermaid
    flowchart TD
        A[异常分级] --> B{异常级别}
        B -->|严重| C[立即处理]
        B -->|中等| D[计划处理]
        B -->|轻微| E[监控观察]
        
        C --> C1[数据隔离]
        C --> C2[告警通知]
        C --> C3[人工介入]
        C --> C4[自动修复]
        
        D --> D1[标记异常]
        D --> D2[延迟处理]
        D --> D3[批量处理]
        
        E --> E1[日志记录]
        E --> E2[趋势监控]
        E --> E3[定期复查]
    ```

    ## 🔄 检测模型优化

    ### 模型性能评估
    ```python
    def evaluate_anomaly_detection(y_true, y_pred, y_scores):
        """异常检测模型评估"""
        from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
        
        # 基础指标
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        auc = roc_auc_score(y_true, y_scores)
        
        # 异常检测特定指标
        true_positives = np.sum((y_true == 1) & (y_pred == 1))
        false_positives = np.sum((y_true == 0) & (y_pred == 1))
        false_negatives = np.sum((y_true == 1) & (y_pred == 0))
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'auc': auc,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives
        }
    ```

    ### 自适应阈值调整
    ```python
    def adaptive_threshold_adjustment(anomaly_scores, feedback_data):
        """自适应阈值调整"""
        from sklearn.metrics import precision_recall_curve
        
        # 基于历史反馈调整阈值
        if len(feedback_data) > 0:
            y_true = feedback_data['labels']
            y_scores = feedback_data['scores']
            
            # 计算最优阈值
            precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
            f1_scores = 2 * (precision * recall) / (precision + recall)
            optimal_threshold = thresholds[np.argmax(f1_scores)]
            
            return optimal_threshold
        else:
            # 使用统计方法设定初始阈值
            return np.percentile(anomaly_scores, 95)
    ```
  </process>

  <criteria>
    ## 异常检测评价标准

    ### 检测准确性
    - ✅ 检测精确率 ≥ 85%
    - ✅ 检测召回率 ≥ 80%
    - ✅ F1分数 ≥ 82%
    - ✅ AUC值 ≥ 0.9

    ### 检测效率
    - ✅ 检测时间 ≤ 业务要求
    - ✅ 内存使用合理
    - ✅ CPU使用率 ≤ 80%
    - ✅ 可扩展性良好

    ### 检测可用性
    - ✅ 误报率 ≤ 5%
    - ✅ 漏报率 ≤ 10%
    - ✅ 检测结果可解释
    - ✅ 处理策略有效
  </criteria>
</execution>

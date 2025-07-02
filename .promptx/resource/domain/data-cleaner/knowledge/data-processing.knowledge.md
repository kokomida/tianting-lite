<knowledge>
  ## 🔄 数据处理核心知识

  ### 数据处理生命周期
  - **数据采集**：从各种数据源获取原始数据
  - **数据存储**：将数据存储在合适的存储系统中
  - **数据清洗**：清理和预处理数据，提高数据质量
  - **数据转换**：将数据转换为适合分析的格式
  - **数据分析**：从数据中提取有价值的信息和洞察
  - **数据可视化**：以图表形式展示分析结果
  - **数据归档**：长期保存重要的历史数据

  ### 数据类型与特征
  ```mermaid
  graph TD
      A[数据类型] --> B[结构化数据]
      A --> C[半结构化数据]
      A --> D[非结构化数据]
      
      B --> B1[关系数据库]
      B --> B2[CSV文件]
      B --> B3[Excel表格]
      
      C --> C1[JSON数据]
      C --> C2[XML数据]
      C --> C3[日志文件]
      
      D --> D1[文本文档]
      D --> D2[图像数据]
      D --> D3[音频视频]
  ```

  ### 数据质量维度
  - **完整性（Completeness）**：数据是否完整，无缺失值
  - **准确性（Accuracy）**：数据是否正确反映现实
  - **一致性（Consistency）**：数据在不同地方是否一致
  - **时效性（Timeliness）**：数据是否及时更新
  - **有效性（Validity）**：数据是否符合定义的格式和规则
  - **唯一性（Uniqueness）**：数据是否存在重复

  ## 📊 数据清洗技术

  ### 缺失值处理方法
  ```mermaid
  mindmap
    root((缺失值处理))
      删除方法
        列表删除
        成对删除
        阈值删除
      填充方法
        均值填充
        中位数填充
        众数填充
        前向填充
        后向填充
      预测方法
        线性插值
        多项式插值
        机器学习预测
        时间序列预测
  ```

  ### 异常值检测与处理
  - **统计方法**：Z-Score、IQR、Grubbs检验
  - **可视化方法**：箱线图、散点图、直方图
  - **机器学习方法**：Isolation Forest、One-Class SVM、LOF
  - **处理策略**：删除、替换、变换、标记

  ### 重复数据处理
  ```python
  # 重复数据检测示例
  import pandas as pd
  
  # 完全重复
  duplicates = df.duplicated()
  
  # 基于特定列的重复
  duplicates = df.duplicated(subset=['name', 'email'])
  
  # 模糊匹配重复
  from fuzzywuzzy import fuzz
  
  def fuzzy_dedupe(df, column, threshold=80):
      """基于模糊匹配的去重"""
      to_remove = []
      for i in range(len(df)):
          for j in range(i+1, len(df)):
              similarity = fuzz.ratio(df.iloc[i][column], df.iloc[j][column])
              if similarity > threshold:
                  to_remove.append(j)
      
      return df.drop(df.index[to_remove])
  ```

  ## 🔧 数据转换技术

  ### 数据类型转换
  ```python
  # 常见数据类型转换
  import pandas as pd
  import numpy as np
  
  # 字符串转数值
  df['numeric_column'] = pd.to_numeric(df['string_column'], errors='coerce')
  
  # 日期时间转换
  df['datetime_column'] = pd.to_datetime(df['date_string'], format='%Y-%m-%d')
  
  # 分类数据编码
  from sklearn.preprocessing import LabelEncoder, OneHotEncoder
  
  # 标签编码
  le = LabelEncoder()
  df['category_encoded'] = le.fit_transform(df['category'])
  
  # 独热编码
  df_encoded = pd.get_dummies(df, columns=['category'])
  ```

  ### 数据标准化与归一化
  ```python
  from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
  
  # 标准化 (Z-score)
  scaler = StandardScaler()
  df_standardized = scaler.fit_transform(df[numeric_columns])
  
  # 归一化 (Min-Max)
  scaler = MinMaxScaler()
  df_normalized = scaler.fit_transform(df[numeric_columns])
  
  # 鲁棒缩放
  scaler = RobustScaler()
  df_robust = scaler.fit_transform(df[numeric_columns])
  ```

  ### 特征工程
  ```mermaid
  graph LR
      A[原始特征] --> B[特征选择]
      A --> C[特征构造]
      A --> D[特征变换]
      
      B --> B1[过滤法]
      B --> B2[包装法]
      B --> B3[嵌入法]
      
      C --> C1[组合特征]
      C --> C2[交互特征]
      C --> C3[聚合特征]
      
      D --> D1[多项式特征]
      D --> D2[对数变换]
      D --> D3[Box-Cox变换]
  ```

  ## 🛠️ 数据处理工具

  ### Python数据处理生态
  ```mermaid
  graph TD
      A[Python数据处理] --> B[核心库]
      A --> C[专业库]
      A --> D[可视化库]
      
      B --> B1[Pandas - 数据操作]
      B --> B2[NumPy - 数值计算]
      B --> B3[SciPy - 科学计算]
      
      C --> C1[Scikit-learn - 机器学习]
      C --> C2[Dask - 大数据处理]
      C --> C3[Modin - 并行Pandas]
      
      D --> D1[Matplotlib - 基础绘图]
      D --> D2[Seaborn - 统计绘图]
      D --> D3[Plotly - 交互绘图]
  ```

  ### 大数据处理框架
  - **Apache Spark**：分布式数据处理引擎
  - **Apache Flink**：流处理框架
  - **Apache Kafka**：分布式流平台
  - **Hadoop**：分布式存储和计算框架
  - **Dask**：Python并行计算库

  ### 数据质量工具
  ```python
  # Great Expectations - 数据验证
  import great_expectations as ge
  
  # 创建数据期望
  df_ge = ge.from_pandas(df)
  df_ge.expect_column_values_to_not_be_null('important_column')
  df_ge.expect_column_values_to_be_between('age', min_value=0, max_value=120)
  
  # Pandas Profiling - 数据概览
  from pandas_profiling import ProfileReport
  
  profile = ProfileReport(df, title="Data Quality Report")
  profile.to_file("data_quality_report.html")
  
  # PyJanitor - 数据清洗
  import janitor
  
  df_clean = (df
              .clean_names()  # 清理列名
              .remove_empty()  # 删除空行空列
              .dropna(subset=['important_column'])  # 删除特定列的空值
              )
  ```

  ## 📈 数据处理最佳实践

  ### 数据处理流水线设计
  ```python
  from sklearn.pipeline import Pipeline
  from sklearn.compose import ColumnTransformer
  from sklearn.preprocessing import StandardScaler, OneHotEncoder
  from sklearn.impute import SimpleImputer
  
  # 数值特征处理流水线
  numeric_pipeline = Pipeline([
      ('imputer', SimpleImputer(strategy='median')),
      ('scaler', StandardScaler())
  ])
  
  # 分类特征处理流水线
  categorical_pipeline = Pipeline([
      ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
      ('encoder', OneHotEncoder(handle_unknown='ignore'))
  ])
  
  # 组合处理流水线
  preprocessor = ColumnTransformer([
      ('num', numeric_pipeline, numeric_features),
      ('cat', categorical_pipeline, categorical_features)
  ])
  ```

  ### 数据版本控制
  - **DVC (Data Version Control)**：数据版本管理工具
  - **Git LFS**：大文件版本控制
  - **MLflow**：机器学习生命周期管理
  - **数据血缘追踪**：记录数据的来源和变换历史

  ### 数据安全与隐私
  ```python
  # 数据脱敏示例
  import hashlib
  
  def anonymize_data(df, sensitive_columns):
      """数据脱敏处理"""
      df_anonymized = df.copy()
      
      for column in sensitive_columns:
          # 哈希脱敏
          df_anonymized[column] = df_anonymized[column].apply(
              lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:10]
          )
      
      return df_anonymized
  
  # 差分隐私
  def add_noise(data, epsilon=1.0):
      """添加拉普拉斯噪声实现差分隐私"""
      sensitivity = 1.0  # 根据具体情况调整
      scale = sensitivity / epsilon
      noise = np.random.laplace(0, scale, data.shape)
      return data + noise
  ```

  ## 🎯 性能优化策略

  ### 内存优化
  ```python
  # 数据类型优化
  def optimize_dtypes(df):
      """优化数据类型以节省内存"""
      for col in df.columns:
          col_type = df[col].dtype
          
          if col_type != 'object':
              c_min = df[col].min()
              c_max = df[col].max()
              
              if str(col_type)[:3] == 'int':
                  if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                      df[col] = df[col].astype(np.int8)
                  elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                      df[col] = df[col].astype(np.int16)
                  elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                      df[col] = df[col].astype(np.int32)
              
              elif str(col_type)[:5] == 'float':
                  if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                      df[col] = df[col].astype(np.float32)
      
      return df
  
  # 分块处理大文件
  def process_large_file(filename, chunk_size=10000):
      """分块处理大文件"""
      results = []
      
      for chunk in pd.read_csv(filename, chunksize=chunk_size):
          # 处理每个块
          processed_chunk = process_chunk(chunk)
          results.append(processed_chunk)
      
      return pd.concat(results, ignore_index=True)
  ```

  ### 并行处理
  ```python
  from multiprocessing import Pool
  import dask.dataframe as dd
  
  # 使用Dask进行并行处理
  def parallel_processing_with_dask(df):
      """使用Dask进行并行数据处理"""
      # 转换为Dask DataFrame
      ddf = dd.from_pandas(df, npartitions=4)
      
      # 并行计算
      result = ddf.groupby('category').value.mean().compute()
      
      return result
  
  # 使用multiprocessing
  def parallel_apply(df, func, n_cores=4):
      """并行应用函数"""
      df_split = np.array_split(df, n_cores)
      
      with Pool(n_cores) as pool:
          results = pool.map(func, df_split)
      
      return pd.concat(results)
  ```
</knowledge>

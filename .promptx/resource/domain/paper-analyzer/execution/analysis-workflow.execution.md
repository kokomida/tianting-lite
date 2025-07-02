<execution>
  <constraint>
    ## 论文分析限制条件
    - **格式约束**：主要支持PDF格式，部分支持其他文档格式
    - **语言约束**：主要支持中英文，其他语言支持有限
    - **大小约束**：单个文件大小不超过100MB
    - **质量约束**：PDF质量影响文本提取准确性
    - **版权约束**：必须遵守学术论文的版权和使用规定
  </constraint>

  <rule>
    ## 论文分析强制规则
    - **完整性检查**：分析前必须验证文件完整性
    - **结构识别**：必须正确识别论文的基本结构
    - **引用保留**：必须保留原文的引用和参考信息
    - **质量标记**：必须标记提取内容的可信度
    - **版权声明**：必须保留原文的版权信息
  </rule>

  <guideline>
    ## 论文分析指导原则
    - **准确性优先**：确保提取信息的准确性
    - **结构化输出**：提供结构化的分析结果
    - **多层次分析**：从概览到细节的多层次分析
    - **上下文保持**：保持信息的上下文关系
    - **可追溯性**：确保分析结果可追溯到原文
  </guideline>

  <process>
    ## 📄 论文分析工作流程

    ### 论文分析架构
    ```mermaid
    graph TD
        A[PDF输入] --> B[文档预处理]
        B --> C[结构识别]
        C --> D[内容提取]
        D --> E[信息分析]
        E --> F[知识抽取]
        F --> G[结果输出]
        
        B --> B1[格式验证]
        B --> B2[OCR处理]
        B --> B3[文本清洗]
        
        C --> C1[标题识别]
        C --> C2[章节划分]
        C --> C3[图表定位]
        
        D --> D1[摘要提取]
        D --> D2[关键词提取]
        D --> D3[正文提取]
        D --> D4[参考文献提取]
        
        E --> E1[概念识别]
        E --> E2[方法分析]
        E --> E3[结果评估]
    ```

    ### 第一阶段：文档预处理
    ```mermaid
    flowchart TD
        A[PDF文件] --> B[文件验证]
        B --> C[格式检查]
        C --> D[文本提取]
        D --> E[OCR处理]
        E --> F[文本清洗]
        F --> G[编码标准化]
        
        B --> B1[文件完整性]
        B --> B2[文件大小]
        B --> B3[权限检查]
        
        C --> C1[PDF版本]
        C --> C2[页面数量]
        C --> C3[图文混合]
        
        D --> D1[直接文本提取]
        D --> D2[表格提取]
        D --> D3[图像识别]
        
        E --> E1[图像文字识别]
        E --> E2[手写文字识别]
        E --> E3[公式识别]
    ```

    ### 第二阶段：结构化分析
    ```mermaid
    graph TD
        A[预处理文本] --> B[文档结构分析]
        B --> C[内容分类]
        C --> D[关键信息提取]
        D --> E[关系识别]
        E --> F[质量评估]
        
        B --> B1[标题层次]
        B --> B2[段落结构]
        B --> B3[列表识别]
        
        C --> C1[摘要]
        C --> C2[引言]
        C --> C3[方法]
        C --> C4[结果]
        C --> C5[讨论]
        C --> C6[结论]
        
        D --> D1[研究问题]
        D --> D2[研究方法]
        D --> D3[主要发现]
        D --> D4[创新点]
        
        E --> E1[概念关系]
        E --> E2[因果关系]
        E --> E3[引用关系]
    ```

    ### 第三阶段：知识抽取与分析
    ```mermaid
    flowchart LR
        A[结构化内容] --> B[概念抽取]
        B --> C[方法识别]
        C --> D[结果分析]
        D --> E[价值评估]
        E --> F[知识图谱]
        F --> G[应用建议]
        
        B --> B1[核心概念]
        B --> B2[技术术语]
        B --> B3[理论框架]
        
        C --> C1[研究方法]
        C --> C2[实验设计]
        C --> C3[数据分析]
        
        D --> D1[定量结果]
        D --> D2[定性发现]
        D --> D3[统计显著性]
        
        E --> E1[学术价值]
        E --> E2[实用价值]
        E --> E3[创新程度]
    ```

    ## 🛠️ 论文分析技术实现

    ### PDF处理引擎
    ```python
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
    from PIL import Image
    import pytesseract
    import re
    from typing import Dict, List, Any, Optional
    import logging

    class PDFProcessor:
        def __init__(self):
            self.logger = logging.getLogger(__name__)
        
        def extract_text_pypdf2(self, pdf_path: str) -> str:
            """使用PyPDF2提取文本"""
            text = ""
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                self.logger.error(f"PyPDF2 extraction failed: {e}")
            return text
        
        def extract_text_pdfplumber(self, pdf_path: str) -> Dict[str, Any]:
            """使用pdfplumber提取文本和表格"""
            result = {"text": "", "tables": [], "metadata": {}}
            
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    result["metadata"] = pdf.metadata
                    
                    for page_num, page in enumerate(pdf.pages):
                        # 提取文本
                        page_text = page.extract_text()
                        if page_text:
                            result["text"] += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                        
                        # 提取表格
                        tables = page.extract_tables()
                        for table in tables:
                            result["tables"].append({
                                "page": page_num + 1,
                                "data": table
                            })
            
            except Exception as e:
                self.logger.error(f"pdfplumber extraction failed: {e}")
            
            return result
        
        def extract_text_pymupdf(self, pdf_path: str) -> Dict[str, Any]:
            """使用PyMuPDF提取文本和图像"""
            result = {"text": "", "images": [], "metadata": {}}
            
            try:
                doc = fitz.open(pdf_path)
                result["metadata"] = doc.metadata
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    
                    # 提取文本
                    text = page.get_text()
                    result["text"] += f"\n--- Page {page_num + 1} ---\n{text}\n"
                    
                    # 提取图像
                    image_list = page.get_images()
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        
                        if pix.n - pix.alpha < 4:  # GRAY or RGB
                            img_data = pix.tobytes("png")
                            result["images"].append({
                                "page": page_num + 1,
                                "index": img_index,
                                "data": img_data
                            })
                        pix = None
                
                doc.close()
            
            except Exception as e:
                self.logger.error(f"PyMuPDF extraction failed: {e}")
            
            return result
        
        def ocr_image(self, image_data: bytes) -> str:
            """OCR图像识别"""
            try:
                image = Image.open(io.BytesIO(image_data))
                text = pytesseract.image_to_string(image, lang='chi_sim+eng')
                return text
            except Exception as e:
                self.logger.error(f"OCR failed: {e}")
                return ""
        
        def extract_comprehensive(self, pdf_path: str) -> Dict[str, Any]:
            """综合提取方法"""
            result = {
                "text": "",
                "tables": [],
                "images": [],
                "metadata": {},
                "extraction_methods": []
            }
            
            # 尝试多种提取方法
            methods = [
                ("pdfplumber", self.extract_text_pdfplumber),
                ("pymupdf", self.extract_text_pymupdf),
                ("pypdf2", self.extract_text_pypdf2)
            ]
            
            for method_name, method_func in methods:
                try:
                    if method_name == "pypdf2":
                        text = method_func(pdf_path)
                        if text and len(text.strip()) > 100:
                            result["text"] = text
                            result["extraction_methods"].append(method_name)
                            break
                    else:
                        extracted = method_func(pdf_path)
                        if extracted["text"] and len(extracted["text"].strip()) > 100:
                            result.update(extracted)
                            result["extraction_methods"].append(method_name)
                            break
                
                except Exception as e:
                    self.logger.warning(f"Method {method_name} failed: {e}")
                    continue
            
            return result
    ```

    ### 学术论文结构识别
    ```python
    import re
    from dataclasses import dataclass
    from typing import List, Dict, Optional

    @dataclass
    class PaperSection:
        title: str
        content: str
        level: int
        start_pos: int
        end_pos: int

    class PaperStructureAnalyzer:
        def __init__(self):
            self.section_patterns = [
                r'(?i)^(abstract|摘要)',
                r'(?i)^(introduction|引言|1\.?\s*introduction)',
                r'(?i)^(related work|相关工作|literature review|文献综述)',
                r'(?i)^(method|methodology|方法|算法)',
                r'(?i)^(experiment|实验|evaluation|评估)',
                r'(?i)^(result|结果|findings|发现)',
                r'(?i)^(discussion|讨论|analysis|分析)',
                r'(?i)^(conclusion|结论|summary|总结)',
                r'(?i)^(reference|参考文献|bibliography)'
            ]
        
        def identify_sections(self, text: str) -> List[PaperSection]:
            """识别论文章节结构"""
            sections = []
            lines = text.split('\n')
            
            current_section = None
            content_buffer = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # 检查是否是章节标题
                section_match = self._is_section_title(line)
                if section_match:
                    # 保存前一个章节
                    if current_section:
                        current_section.content = '\n'.join(content_buffer)
                        current_section.end_pos = i
                        sections.append(current_section)
                    
                    # 开始新章节
                    current_section = PaperSection(
                        title=line,
                        content="",
                        level=self._get_section_level(line),
                        start_pos=i,
                        end_pos=0
                    )
                    content_buffer = []
                else:
                    content_buffer.append(line)
            
            # 保存最后一个章节
            if current_section:
                current_section.content = '\n'.join(content_buffer)
                current_section.end_pos = len(lines)
                sections.append(current_section)
            
            return sections
        
        def _is_section_title(self, line: str) -> bool:
            """判断是否是章节标题"""
            # 检查编号模式
            if re.match(r'^\d+\.?\s+[A-Za-z\u4e00-\u9fff]', line):
                return True
            
            # 检查关键词模式
            for pattern in self.section_patterns:
                if re.match(pattern, line):
                    return True
            
            # 检查格式特征（全大写、居中等）
            if line.isupper() and len(line.split()) <= 5:
                return True
            
            return False
        
        def _get_section_level(self, title: str) -> int:
            """获取章节层级"""
            # 基于编号判断层级
            match = re.match(r'^(\d+)\.', title)
            if match:
                return len(match.group(1))
            
            # 基于格式判断层级
            if title.isupper():
                return 1
            elif title.istitle():
                return 2
            else:
                return 3
        
        def extract_abstract(self, sections: List[PaperSection]) -> Optional[str]:
            """提取摘要"""
            for section in sections:
                if re.match(r'(?i)(abstract|摘要)', section.title):
                    return section.content
            return None
        
        def extract_keywords(self, text: str) -> List[str]:
            """提取关键词"""
            keywords = []
            
            # 查找关键词部分
            keyword_patterns = [
                r'(?i)keywords?[:\s]+(.*?)(?:\n|$)',
                r'(?i)关键词[:\s]+(.*?)(?:\n|$)',
                r'(?i)key words?[:\s]+(.*?)(?:\n|$)'
            ]
            
            for pattern in keyword_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    # 分割关键词
                    words = re.split(r'[,;，；]', match)
                    keywords.extend([word.strip() for word in words if word.strip()])
            
            return keywords
    ```

    ### 内容分析引擎
    ```python
    import spacy
    from collections import Counter
    from typing import Set

    class ContentAnalyzer:
        def __init__(self):
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                self.nlp = None
                logging.warning("spaCy English model not found")
        
        def extract_entities(self, text: str) -> Dict[str, List[str]]:
            """提取命名实体"""
            if not self.nlp:
                return {}
            
            doc = self.nlp(text)
            entities = {}
            
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)
            
            # 去重并排序
            for label in entities:
                entities[label] = list(set(entities[label]))
            
            return entities
        
        def extract_key_phrases(self, text: str, top_k: int = 20) -> List[str]:
            """提取关键短语"""
            if not self.nlp:
                return []
            
            doc = self.nlp(text)
            
            # 提取名词短语
            noun_phrases = []
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) >= 2:  # 至少两个词
                    noun_phrases.append(chunk.text.lower())
            
            # 统计频率
            phrase_counts = Counter(noun_phrases)
            
            # 返回最频繁的短语
            return [phrase for phrase, count in phrase_counts.most_common(top_k)]
        
        def analyze_methodology(self, text: str) -> Dict[str, Any]:
            """分析研究方法"""
            method_keywords = {
                'quantitative': ['survey', 'experiment', 'statistical', 'regression', 'correlation'],
                'qualitative': ['interview', 'case study', 'ethnography', 'grounded theory'],
                'mixed_methods': ['mixed method', 'triangulation', 'sequential', 'concurrent'],
                'machine_learning': ['neural network', 'deep learning', 'classification', 'clustering'],
                'statistical': ['t-test', 'anova', 'chi-square', 'regression', 'significance']
            }
            
            text_lower = text.lower()
            detected_methods = {}
            
            for method_type, keywords in method_keywords.items():
                count = sum(text_lower.count(keyword) for keyword in keywords)
                if count > 0:
                    detected_methods[method_type] = count
            
            return detected_methods
        
        def assess_paper_quality(self, sections: List[PaperSection], 
                               metadata: Dict[str, Any]) -> Dict[str, Any]:
            """评估论文质量"""
            quality_metrics = {
                'structure_completeness': 0,
                'content_depth': 0,
                'methodology_clarity': 0,
                'citation_quality': 0,
                'overall_score': 0
            }
            
            # 结构完整性评估
            required_sections = ['abstract', 'introduction', 'method', 'result', 'conclusion']
            found_sections = []
            
            for section in sections:
                title_lower = section.title.lower()
                for req_section in required_sections:
                    if req_section in title_lower:
                        found_sections.append(req_section)
                        break
            
            quality_metrics['structure_completeness'] = len(set(found_sections)) / len(required_sections)
            
            # 内容深度评估（基于长度和复杂性）
            total_length = sum(len(section.content) for section in sections)
            if total_length > 10000:  # 假设高质量论文至少10k字符
                quality_metrics['content_depth'] = min(total_length / 20000, 1.0)
            
            # 方法论清晰度（基于方法关键词）
            method_section = next((s for s in sections if 'method' in s.title.lower()), None)
            if method_section:
                method_analysis = self.analyze_methodology(method_section.content)
                quality_metrics['methodology_clarity'] = min(len(method_analysis) / 3, 1.0)
            
            # 引用质量（基于参考文献数量）
            ref_section = next((s for s in sections if 'reference' in s.title.lower()), None)
            if ref_section:
                ref_count = len(re.findall(r'\[\d+\]', ref_section.content))
                quality_metrics['citation_quality'] = min(ref_count / 50, 1.0)
            
            # 计算总分
            quality_metrics['overall_score'] = sum(quality_metrics.values()) / 4
            
            return quality_metrics
    ```

    ## 📊 分析结果输出

    ### 结构化报告生成
    ```python
    class PaperAnalysisReport:
        def __init__(self, paper_path: str):
            self.paper_path = paper_path
            self.processor = PDFProcessor()
            self.structure_analyzer = PaperStructureAnalyzer()
            self.content_analyzer = ContentAnalyzer()
        
        def generate_full_report(self) -> Dict[str, Any]:
            """生成完整分析报告"""
            # 1. 提取文档内容
            extracted_data = self.processor.extract_comprehensive(self.paper_path)
            
            # 2. 分析文档结构
            sections = self.structure_analyzer.identify_sections(extracted_data["text"])
            
            # 3. 提取关键信息
            abstract = self.structure_analyzer.extract_abstract(sections)
            keywords = self.structure_analyzer.extract_keywords(extracted_data["text"])
            
            # 4. 内容分析
            entities = self.content_analyzer.extract_entities(extracted_data["text"])
            key_phrases = self.content_analyzer.extract_key_phrases(extracted_data["text"])
            methodology = self.content_analyzer.analyze_methodology(extracted_data["text"])
            
            # 5. 质量评估
            quality_assessment = self.content_analyzer.assess_paper_quality(
                sections, extracted_data["metadata"]
            )
            
            # 6. 生成报告
            report = {
                "paper_info": {
                    "file_path": self.paper_path,
                    "metadata": extracted_data["metadata"],
                    "extraction_methods": extracted_data["extraction_methods"]
                },
                "structure": {
                    "sections": [
                        {
                            "title": section.title,
                            "level": section.level,
                            "word_count": len(section.content.split())
                        } for section in sections
                    ],
                    "total_sections": len(sections)
                },
                "content": {
                    "abstract": abstract,
                    "keywords": keywords,
                    "key_phrases": key_phrases,
                    "entities": entities,
                    "methodology": methodology
                },
                "quality": quality_assessment,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return report
        
        def generate_summary(self, report: Dict[str, Any]) -> str:
            """生成分析摘要"""
            summary = f"""
            论文分析报告摘要
            ==================
            
            文件: {report['paper_info']['file_path']}
            分析时间: {report['analysis_timestamp']}
            
            结构分析:
            - 章节数量: {report['structure']['total_sections']}
            - 主要章节: {', '.join([s['title'] for s in report['structure']['sections'][:5]])}
            
            内容分析:
            - 关键词: {', '.join(report['content']['keywords'][:10])}
            - 研究方法: {', '.join(report['content']['methodology'].keys())}
            
            质量评估:
            - 结构完整性: {report['quality']['structure_completeness']:.2%}
            - 内容深度: {report['quality']['content_depth']:.2%}
            - 总体评分: {report['quality']['overall_score']:.2%}
            """
            
            return summary
    ```
  </process>

  <criteria>
    ## 论文分析评价标准

    ### 提取准确性
    - ✅ 文本提取准确率 ≥ 95%
    - ✅ 结构识别准确率 ≥ 90%
    - ✅ 关键信息提取完整性 ≥ 85%
    - ✅ 表格图像识别率 ≥ 80%

    ### 分析深度
    - ✅ 概念识别覆盖率 ≥ 90%
    - ✅ 方法论分析准确性 ≥ 85%
    - ✅ 质量评估合理性 ≥ 80%
    - ✅ 知识抽取有效性 ≥ 85%

    ### 处理效率
    - ✅ 单篇论文处理时间 ≤ 5分钟
    - ✅ 批量处理能力 ≥ 10篇/小时
    - ✅ 内存使用合理
    - ✅ 错误恢复能力强

    ### 输出质量
    - ✅ 报告结构清晰
    - ✅ 信息组织合理
    - ✅ 可读性强
    - ✅ 可操作性高
  </criteria>
</execution>

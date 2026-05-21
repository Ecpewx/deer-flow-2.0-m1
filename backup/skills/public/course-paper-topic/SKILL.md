---
name: course-paper-topic
description: Use this skill when the user requests to generate, design, or brainstorm course paper topics, thesis titles, essay prompts, research project ideas, or assignment topics for academic courses. Supports input from PPT slides, textbooks, mind maps, past exams, exercise banks, existing course assignments, course papers, student essays, and outstanding student work examples. Trigger on requests like "generate paper topics", "design course essay prompts", "出论文题目", "设计课程大作业", "课程论文选题", "生成研究课题", "大作业题目推荐", or "帮我设计课程论文方向".
---

# Course Paper Topic Generation Skill

## Overview

This skill generates high-quality, academically rigorous course paper topics, essay prompts, and research project ideas based on user-provided course materials. It analyzes source materials to identify key themes, knowledge gaps, and research-worthy intersections, then produces structured topic proposals with clear scope, methodology guidance, and evaluation criteria.

The output includes a set of well-defined paper topics with varying difficulty levels, each accompanied by a topic description, suggested research direction, key references, and grading rubric — ready for direct use in course syllabi or assignment sheets.

## Core Capabilities

- Parse and comprehend diverse course materials (PPT, PDF, DOCX, Markdown, images)
- Analyze existing course assignments, papers, and outstanding student work to identify successful patterns
- Generate paper topics spanning multiple cognitive levels (descriptive, analytical, critical, creative)
- Calibrate topic difficulty and scope to course level (undergraduate / graduate / professional)
- Provide structured topic proposals with research direction, methodology hints, and scope boundaries
- Ensure topics are non-overlapping and cover the breadth of course content
- Generate topics in batch (e.g., 10-20 topics for a class to choose from)
- Support both Chinese and English academic contexts

## When to Use This Skill

**Always load this skill when:**

- User asks to generate course paper topics, essay prompts, or thesis titles
- User wants to design course assignments (大作业) or research projects
- User asks for "论文选题", "课程论文题目", "大作业设计", "research topic ideas"
- User uploads course materials and asks for paper/essay topic suggestions
- User wants to create a topic list for students to choose from
- User requests to improve or expand an existing set of paper topics
- User provides past student work and wants new, non-overlapping topics

## Source Material Types

This skill can work with the following input types:

| Source Type | Description | How It's Used |
|-------------|-------------|---------------|
| **课件 PPT** | Lecture slides | Extract core concepts, theoretical frameworks, and key themes |
| **教材章节** | Textbook chapters | Identify depth of coverage, formal definitions, and advanced topics |
| **思维导图** | Mind maps | Understand topic hierarchy and cross-topic connections |
| **历年真题** | Past exam papers | Identify high-weight knowledge areas and exam-level expectations |
| **习题库** | Exercise banks | Understand computational and applied dimensions |
| **课程大作业** | Existing course assignments | Learn assignment format, scope expectations, and past topic patterns |
| **课程论文** | Existing course papers/essays | Understand expected depth, structure, and academic rigor |
| **优秀作业案例** | Outstanding student work | Identify what makes a topic successful — scope, methodology, innovation |
| **课程大纲** | Course syllabus | Understand learning objectives, grading weights, and topic sequencing |
| **参考文献列表** | Reading lists / bibliography | Identify recommended sources and research directions |

## Topic Generation Workflow

### Phase 1: Material Analysis

#### Step 1.1: Catalog All Source Materials

For each provided material, record:

```
Source: [filename / description]
Type: [PPT / textbook / mind map / past exam / assignment / student paper / ...]
Coverage: [chapters, topics, or themes covered]
Key Insights: [what this source uniquely contributes to topic design]
```

#### Step 1.2: Extract Knowledge Architecture

Build a hierarchical map of the course content:

```
Course: [Course Name]
├── Module 1: [Theme]
│   ├── Core Concepts: [list]
│   ├── Key Theories/Models: [list]
│   ├── Applied Dimensions: [list]
│   └── Open Questions: [areas where research is ongoing or debated]
├── Module 2: [Theme]
│   └── ...
└── Cross-Module Connections: [interdisciplinary links, synthesis opportunities]
```

#### Step 1.3: Analyze Existing Assignments and Student Work

When past assignments or student papers are provided:

1. **Topic Pattern Analysis** — What topics have been assigned before? What themes recur?
2. **Scope Calibration** — How broad/narrow were successful topics? What's the expected page count / word count?
3. **Methodology Patterns** — What research methods did successful papers use? (literature review, case study, data analysis, model building, comparative analysis, etc.)
4. **Quality Signals** — What distinguishes outstanding work from average work? (depth of analysis, originality, use of primary sources, quantitative rigor, etc.)
5. **Gap Identification** — What themes or angles have NOT been explored yet?

#### Step 1.4: 优秀作业深度分析（如有优秀案例）

对每篇优秀学生作品进行结构化拆解：

```
优秀论文分析卡片
├── 选题特征
│   ├── 题目范围：宽泛 / 适中 / 聚焦
│   ├── 创新点类型：理论 / 方法 / 应用 / 数据
│   └── 与课程内容的关联度：核心概念 / 延伸应用 / 跨学科
├── 结构特征
│   ├── 正文章节数：N 章
│   ├── 文献综述占比：约 X%
│   ├── 核心论证占比：约 Y%
│   └── 案例/数据分析占比：约 Z%
├── 方法论特征
│   ├── 主要方法：[列举]
│   ├── 数据来源：[公开数据 / 问卷 / 企业数据 / 仿真]
│   └── 分析工具：[Excel / Python / R / SPSS / 手工推导]
├── 质量信号
│   ├── 得分/等级：[如有]
│   ├── 参考文献数量和质量：X 篇，含 Y 篇英文
│   └── 教师评语关键词：[如有]
└── 可复用元素
    ├── 选题角度是否可变形？→ [具体方向]
    └── 方法论是否可迁移到新主题？→ [是/否]
```

#### Step 1.5: Identify Topic-Worthy Dimensions

From the analyzed materials, identify potential topic angles:

| Dimension | Description | Example |
|-----------|-------------|---------|
| **理论辨析** | Theoretical comparison or critique | Compare two competing models and evaluate their assumptions |
| **案例应用** | Apply theory to a real-world case | Use model X to analyze a specific industry/company/scenario |
| **数据实证** | Empirical data analysis | Collect data and test hypothesis using methods from the course |
| **模型拓展** | Extend or modify a course model | Relax an assumption in model X and derive new results |
| **综述评价** | Literature review and critical evaluation | Survey recent developments in sub-field Y |
| **跨学科交叉** | Interdisciplinary synthesis | Connect concepts from this course with another field |
| **历史演变** | Historical development analysis | Trace the evolution of concept X and its modern implications |
| **政策分析** | Policy or regulation analysis | Evaluate how policy Z impacts the domain studied in this course |
| **方法论比较** | Methodological comparison | Compare different approaches to solving problem type P |
| **前沿探索** | Frontier/cutting-edge topics | Explore emerging trends that extend beyond the textbook |

### Phase 2: Topic Design

#### Step 2.1: Determine Design Parameters

Confirm with the user or use intelligent defaults:

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Topic Count** | Number of topics to generate | 10-15 |
| **Course Level** | Undergraduate / Graduate / Professional | Infer from materials |
| **Paper Length** | Expected word count or page count | 3000-5000 words |
| **Difficulty Distribution** | Basic : Intermediate : Advanced ratio | 3 : 5 : 2 |
| **Topic Type Mix** | Theoretical / Applied / Empirical / Review | Balanced mix |
| **Overlap Policy** | Whether topics may share sub-themes | Minimal overlap |
| **Language** | Chinese / English / Bilingual | Same as source materials |
| **Deadline Context** | Time available for students | Semester-long |
| **Group or Individual** | Solo paper or group project | Individual |

#### Step 2.2: Topic Composition Principles

Each topic should:

1. **Be specific enough** to be actionable — avoid overly broad titles like "论XX的发展" without scoping
2. **Be open enough** to allow student creativity — don't prescribe the conclusion
3. **Match course level** — undergraduate topics should be more guided; graduate topics more exploratory
4. **Have clear boundaries** — students should understand what is in-scope and out-of-scope
5. **Be researchable** — sufficient source materials must exist for students to complete the paper
6. **Not duplicate past assignments** — if past topics are provided, generate fresh angles

#### Step 2.3: Design Topic Difficulty Tiers

**Tier 1 — 基础型 (Descriptive/Analytical)**:
- Explain, summarize, compare, or classify concepts from the course
- Students demonstrate understanding of course content
- Suitable for students aiming for a passing to good grade

**Tier 2 — 提高型 (Applied/Critical)**:
- Apply course theories to real cases, critique existing models, or conduct empirical analysis
- Students demonstrate ability to transfer knowledge to new contexts
- Suitable for students aiming for good to excellent grades

**Tier 3 — 拓展型 (Creative/Research-oriented)**:
- Extend models, propose new frameworks, conduct original data analysis, or explore frontier topics
- Students demonstrate research capability and original thinking
- Suitable for top students or graduate-level work

### Phase 3: Output Generation

#### Step 3.1: Topic Proposal Format

Each topic should be presented in this structure:

```markdown
### 题目 [N]：[Paper Title]

**难度等级**：★☆☆ 基础型 / ★★☆ 提高型 / ★★★ 拓展型

**题目类型**：理论辨析 / 案例应用 / 数据实证 / 模型拓展 / 综述评价 / 跨学科交叉

**题目描述**：
[2-4 sentences describing the topic, its significance, and what the paper should address]

**研究方向提示**：
1. [Suggested angle or sub-question 1]
2. [Suggested angle or sub-question 2]
3. [Suggested angle or sub-question 3]

**建议方法论**：
- [Methodology 1: e.g., 文献综述法]
- [Methodology 2: e.g., 案例分析法]

**知识点来源**：
> ⚠️ **必填项** — 必须注明该题目所依据的具体课件文件名及页码，格式如下：
- `[文件名] 第[N]页（[知识点简述]）`
- `[文件名] 第[X]-[Y]页（[知识点简述]）`

示例：
- `精算学第三章生命表.pptx 第12页（生命表基本假设）`
- `精算学第三章生命表.pptx 第18-21页（Makeham模型参数估计）`

**参考切入点**：
- [Reference to specific course material: e.g., 课件第X章 / 教材§Y.Z]
- [Relevant real-world context or data source]

**预期篇幅**：[word count] 字

**评分要点**：
- [ ] [Key evaluation criterion 1]
- [ ] [Key evaluation criterion 2]
- [ ] [Key evaluation criterion 3]
- [ ] [Key evaluation criterion 4]
```

#### Step 3.2: Full Output Structure

```markdown
# [课程名称] · 课程论文选题指南

> **适用课程**：[Course Name]
> **适用层次**：本科 / 研究生 / 专业认证
> **参考材料**：[List all source materials used]
> **生成题目数量**：[N] 个
> **难度分布**：基础型 [A] 个 / 提高型 [B] 个 / 拓展型 [C] 个

---

## 选题总览

| 序号 | 题目 | 难度 | 类型 | 关键词 |
|------|------|------|------|--------|
| 1 | [Title] | ★☆☆ | 理论辨析 | keyword1, keyword2 |
| 2 | [Title] | ★★☆ | 案例应用 | keyword1, keyword2 |
| ... | ... | ... | ... | ... |

---

## 详细题目说明

### 题目 1：[Title]
[Full topic proposal as per Step 3.1 format]

---

### 题目 2：[Title]
...

---

## 选题建议

### 如何选择适合自己的题目
1. **根据兴趣选择** — [guidance]
2. **根据能力选择** — [guidance]
3. **根据资源选择** — [guidance]

### 写作建议
1. [General writing tip 1]
2. [General writing tip 2]
3. [General writing tip 3]

### 评分标准说明
| 评分维度 | 权重 | 说明 |
|----------|------|------|
| 选题与内容相关性 | 15% | ... |
| 文献综述质量 | 20% | ... |
| 分析深度与逻辑性 | 25% | ... |
| 创新性与独立思考 | 20% | ... |
| 写作规范与格式 | 10% | ... |
| 参考文献引用 | 10% | ... |
```

#### Step 3.3: Quality Checklist

Before delivering the topic list, verify:

- [ ] All topics are specific, actionable, and have clear scope
- [ ] No two topics have excessive overlap (students choosing different topics should produce distinct papers)
- [ ] Difficulty distribution matches the specified ratio
- [ ] All major course modules/chapters are represented across the topic set
- [ ] If past assignments were provided, new topics do not duplicate them
- [ ] Topic descriptions are in the correct language (matching source materials)
- [ ] Each topic's suggested methodology is appropriate for the course level
- [ ] Evaluation criteria are fair and measurable
- [ ] Topics are ordered logically (e.g., by module, by difficulty, or by type)

### Phase 4: Refinement (Optional)

#### Step 4.1: User Feedback Iteration

After presenting the initial topic list:

1. **Add/Remove topics** based on user preferences
2. **Adjust difficulty** — make topics easier or harder
3. **Narrow/Broaden scope** — for topics that are too vague or too specific
4. **Cross-reference** — ensure topics align with the user's grading rubric if provided
5. **Generate variants** — create alternative phrasings or angles for selected topics

#### Step 4.2: Anti-Plagiarism Considerations

When generating topics:

- Avoid topics that can be answered by copying a single source
- Design topics that require synthesis of multiple materials or original analysis
- Include requirements for personal opinion, case-specific data, or original argumentation
- Where possible, embed constraints that make each student's paper unique (e.g., "choose a company/country/scenario of your choice")

## Important Notes

1. **Source fidelity** — Topics must be rooted in the provided course materials; do not introduce concepts far beyond the course scope
2. **Level appropriateness** — Undergraduate topics should be manageable within one semester; graduate topics can be more ambitious
3. **Diversity** — Ensure a mix of topic types (theory, application, empirical, review) to accommodate different student strengths
4. **Freshness** — When past assignments are provided, actively avoid recycling old topics
5. **Cultural context** — For Chinese university courses, follow conventions like 中文标题 + 英文副标题, 摘要/关键词 requirements, etc.
6. **File output** — Save the generated topic guide to `/mnt/user-data/workspace/` as a `.md` file for easy download

## 学术深度强化

### 文献综述要求嵌入

每个选题应包含文献检索指引，帮助学生快速进入研究状态：

```markdown
**推荐文献检索路径**：
1. 知网（CNKI）：关键词 "[关键词1]" + "[关键词2]"，限定期刊来源为 CSSCI/北大核心
2. Web of Science / Scopus：检索 "[English keyword]"，限定近5年
3. 课程教材参考文献章节：[教材名] 第X章参考文献 [编号范围]
4. Google Scholar：引用量 > 50 的综述类文献优先

**建议参考文献数量**：
- 基础型选题：8-12 篇（中文为主）
- 提高型选题：12-18 篇（中英文各半）
- 拓展型选题：15-25 篇（英文为主，含最新发表）
```

### 研究方法论深度

为不同类型的选题提供方法论指导：

| 选题类型 | 推荐研究方法 | 方法论要点 |
|----------|-------------|-----------|
| 理论辨析 | 文献研究法、比较分析法 | 需构建分析框架，明确比较维度 |
| 案例应用 | 案例研究法、定性分析 | 需说明案例选择理由，避免以偏概全 |
| 数据实证 | 统计分析法、计量经济学 | 需说明数据来源、样本量、显著性检验 |
| 模型拓展 | 数学建模、仿真模拟 | 需给出模型假设、推导过程、数值验证 |
| 综述评价 | 系统性文献综述（SLR） | 需说明检索策略、纳入/排除标准、文献数量 |
| 跨学科交叉 | 混合研究法 | 需说明各学科视角的整合逻辑 |

### 学术创新点引导

每个选题应提示可能的创新方向：

1. **理论创新** — 是否能对已有理论提出修正或补充？
2. **方法创新** — 是否能用新方法研究旧问题？
3. **应用创新** — 是否能将理论应用到新场景？
4. **数据创新** — 是否能使用新数据源或更大样本？
5. **视角创新** — 是否能从新的学科交叉角度切入？

## 中国高校课程论文规范

### 论文格式要求

生成选题指南时，附带以下中国高校通用论文格式要求：

```markdown
### 论文格式规范

**基本结构**：
1. 封面（题目、姓名、学号、专业、指导教师、日期）
2. 中文摘要（200-300字）+ 关键词（3-5个）
3. 英文摘要（Abstract）+ Keywords
4. 目录
5. 正文（引言 → 文献综述 → 主体内容 → 结论）
6. 参考文献
7. 附录（如有）

**排版规范**：
- 标题：黑体/小二号，居中
- 正文：宋体/小四号，1.5倍行距
- 英文/数字：Times New Roman
- 页边距：上下 2.54cm，左右 3.17cm
- 页码：底部居中，阿拉伯数字

**参考文献格式（GB/T 7714-2015）**：
- 期刊：[序号] 作者. 题名[J]. 刊名, 年, 卷(期): 页码.
- 专著：[序号] 作者. 书名[M]. 出版地: 出版社, 年.
- 学位论文：[序号] 作者. 题名[D]. 保存地: 保存单位, 年.
- 网络文献：[序号] 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
```

### 字数与篇幅要求

| 课程层次 | 建议字数 | 参考文献数量 | 完成周期 |
|----------|----------|-------------|---------|
| 本科低年级 | 3000-5000字 | 8-12篇 | 4-6周 |
| 本科高年级 | 5000-8000字 | 12-18篇 | 6-10周 |
| 硕士课程论文 | 8000-12000字 | 20-30篇 | 8-12周 |
| 博士课程论文 | 12000字以上 | 30篇以上 | 一学期 |

### 查重与学术诚信

选题设计时内置防抄袭考量：
- 每个选题要求"选择你感兴趣的具体案例/数据/场景"，使每位学生论文具有唯一性
- 建议查重率要求：本科 < 30%，硕士 < 20%，博士 < 10%
- 引用格式必须规范，区分直接引用（加引号）和间接引用（改写）

## 导出为 Word / PDF

生成 Markdown 选题指南后，可使用内置脚本导出为 .docx 或 .pdf 格式：

```bash
# 导出为 Word 文档
python /mnt/skills/public/course-paper-topic/scripts/export.py \
  --input /mnt/user-data/workspace/选题指南.md \
  --format docx \
  --output /mnt/user-data/workspace/选题指南.docx

# 导出为 PDF
python /mnt/skills/public/course-paper-topic/scripts/export.py \
  --input /mnt/user-data/workspace/选题指南.md \
  --format pdf \
  --output /mnt/user-data/workspace/选题指南.pdf

# 同时导出 Word 和 PDF
python /mnt/skills/public/course-paper-topic/scripts/export.py \
  --input /mnt/user-data/workspace/选题指南.md \
  --format both \
  --output-dir /mnt/user-data/workspace/
```

导出脚本功能：
- **DOCX**：宋体正文、标准页边距（上下 2.54cm、左右 3.17cm）、表格自动排版
- **PDF**：中文衬线字体、打印友好排版
- **LaTeX 公式**：自动将 `$...$` 和 `$$...$$` 转换为可渲染格式

## Example Interaction

**User**: 我上传了精算学原理的课件、习题库、去年的大作业题目和几篇优秀论文，帮我设计15个课程论文选题

**Assistant workflow**:
1. Read and analyze all uploaded materials → build course knowledge architecture
2. Analyze past assignment topics and outstanding papers → identify patterns, gaps, and quality signals
3. Design 15 topics: 5 basic + 7 intermediate + 3 advanced, covering all core modules
4. Compose full topic proposals with descriptions, methodology suggestions, and evaluation criteria
5. Generate summary table and writing guidance
6. Save to `/mnt/user-data/workspace/精算学原理_课程论文选题指南.md`

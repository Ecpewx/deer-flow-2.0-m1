---
name: exam-generation
description: Use this skill when the user requests to generate, create, or draft exam papers, test questions, quizzes, practice problems, mock exams, or homework assignments from course materials. Supports generating questions from uploaded PPT slides, textbooks, mind maps, past exam papers, and exercise banks. Covers multiple question types including multiple choice, fill-in-the-blank, true/false, short answer, calculation, and proof. Supports LaTeX math rendering. Trigger on requests like "generate an exam", "create test questions", "make a quiz from this PPT", "出题", "期末试卷", "随堂测试试卷", "生成试卷", "出一套测试题", "根据课件出题", or "生成练习题".
---

# Exam Generation Skill

## Overview

This skill generates professional, academically rigorous exam papers and practice questions from user-provided course materials. It analyzes source materials (PPT slides, textbooks, mind maps, past exam papers, exercise banks) to extract key knowledge points, then composes structured exam papers with multiple question types, proper difficulty distribution, and complete answer keys.

The output is a complete, ready-to-use exam paper in Markdown format with LaTeX math support, suitable for direct use in teaching, self-study, or assessment.

## Core Capabilities

- Parse and comprehend course materials from uploaded files (PPT, PDF, DOCX, Markdown, images)
- Extract knowledge points, formulas, theorems, and definitions from source materials
- Generate multiple question types: single-choice, multiple-choice, true/false, fill-in-the-blank, short answer, calculation, and proof
- Control difficulty distribution (easy / medium / hard) and total score allocation
- Trace each question back to its source material with explicit citations（来源标注仅放在答案卷）
- Generate complete answer keys with step-by-step solutions
- Support mathematical notation via LaTeX ($...$ and $$...$$)
- Support multi-language exam generation (Chinese / English / other languages)
- Generate multiple variant papers from the same source materials for A/B testing or anti-cheating

## When to Use This Skill

**Always load this skill when:**

- User uploads course materials (PPT, PDF, textbook chapters) and asks for exam questions
- User asks to "generate an exam", "create a test", "make quiz questions", "出题", "生成试卷"
- User wants practice problems based on specific chapters or topics
- User requests mock exams that mimic past exam styles
- User asks to create homework assignments from lecture content
- User wants to generate question banks from course materials
- User requests comparative exam papers using different source combinations

## Exam Generation Workflow

### Phase 0: Confirm Output Format（首次必问）

**在开始分析材料之前，必须先询问用户所需的输出格式。**

> 您好！在开始出题之前，请问您需要将试卷导出为哪种格式？
> 1. **Word（.docx）**
> 2. **PDF（.pdf）**
> 3. **Word + PDF 两者都要**

记录用户的选择（`docx` / `pdf` / `both`），在后续导出阶段按此格式执行。  
**若用户在出卷请求中已明确提及输出格式（如"导出 Word"、"要 PDF"、"docx 和 pdf 都要"），则直接使用该格式，跳过询问步骤。**

> ⚠️ **分卷规则**：试卷（题目卷）和答案卷**必须分开生成为独立文件**，不得合并在同一文件中。  
> - 题目卷文件名示例：`[课程]_[章节]_试题卷.docx / .pdf`  
> - 答案卷文件名示例：`[课程]_[章节]_答案及评分标准.docx / .pdf`

---

### Phase 1: Material Analysis

#### Step 1.1: Identify and Catalog Source Materials

When the user provides materials, catalog each source:

| Field | Description |
|-------|-------------|
| **Source Type** | PPT slides, textbook chapter, mind map, past exam, exercise bank |
| **Subject** | Course name and specific topic/chapter |
| **Coverage** | Key topics and knowledge points covered |
| **Depth** | Surface-level overview vs. detailed derivations |
| **Language** | Primary language of the material |

#### Step 1.2: Source Coverage Requirement

> ⚠️ **当用户同时提供多种来源（PPT课件、知识图谱、习题集、往年真题、教材等），生成的试卷必须从所有来源中出题，不能只使用其中一两份文件。** 出题前请确认：
>
> - 每一份上传文件至少对应一道题目
> - 单一来源占比不超过 60%（除非仅提供了一种来源）
> - 往年真题、习题集、PPT课件、知识图谱各按内容体量按比例贡献题目

#### Step 1.3: Knowledge Point Extraction

Systematically extract from each source:

1. **Definitions & Concepts** — Key terms, definitions, classifications, and their relationships
2. **Formulas & Theorems** — Mathematical formulas, theorems, lemmas, and their conditions
3. **Derivations & Proofs** — Important proof techniques, derivation steps
4. **Examples & Applications** — Worked examples, typical application scenarios
5. **Common Pitfalls** — Frequently confused concepts, common mistakes

Organize extracted knowledge points into a structured knowledge map:

```
Chapter/Topic: [Name]
├── Core Concept 1
│   ├── Definition: [...]
│   ├── Key Formula: $formula$
│   ├── Conditions/Constraints: [...]
│   └── Related Concepts: [...]
├── Core Concept 2
│   └── ...
└── Cross-topic Connections: [...]
```

#### Step 1.4: Analyze Past Exam Patterns (if available)

When past exams are provided, analyze:

- **Question type distribution** — ratio of MC, fill-in, calculation, proof, etc.
- **Score allocation** — points per question type
- **Difficulty distribution** — easy : medium : hard ratio
- **High-frequency topics** — concepts that appear repeatedly across exams
- **Question style** — typical phrasing, level of detail, expected answer format

### Phase 2: Exam Design

#### Step 2.1: Determine Exam Parameters

Confirm with the user or use intelligent defaults:

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Total Score** | Total points for the exam | 100 |
| **Duration** | Suggested exam duration | 120 minutes |
| **Difficulty** | Easy : Medium : Hard ratio | 3 : 5 : 2 |
| **Question Types** | Which types to include | All applicable types |
| **Coverage** | Specific chapters/topics to cover | All provided materials |
| **Source Constraint** | Which sources to use for question derivation | All provided sources |
| **Language** | Exam language | Same as source materials |
| **Answer Key** | Whether to include answers | Yes, with solutions |
| **Variants** | Number of exam variants to generate | 1 |

#### Step 2.2: Design Question Type Distribution

Based on the subject and available materials, design the exam structure. Here is a recommended template (adjustable):

**Quantitative/Science Subjects (e.g., Actuarial Science, Mathematics, Physics)**:

| Question Type | Count | Points Each | Total | Purpose |
|--------------|-------|-------------|-------|---------|
| Single Choice | 4-6 | 4-5 | 20-25 | Test concept understanding |
| Multiple Choice | 2-3 | 5-6 | 10-15 | Test comprehensive understanding |
| True/False | 2-4 | 3-4 | 8-12 | Test common misconceptions |
| Fill-in-the-Blank | 2-4 | 4-5 | 10-15 | Test formula recall and calculation |
| Short Answer | 2-3 | 8-10 | 16-20 | Test explanation and reasoning |
| Calculation/Proof | 2-3 | 10-15 | 25-35 | Test problem-solving and rigor |

**Humanities/Social Science Subjects**:

| Question Type | Count | Points Each | Total | Purpose |
|--------------|-------|-------------|-------|---------|
| Single Choice | 5-8 | 3-4 | 20-25 | Test factual knowledge |
| Multiple Choice | 3-4 | 5 | 15-20 | Test comprehensive understanding |
| True/False | 3-5 | 3 | 9-15 | Test common misconceptions |
| Short Answer | 3-4 | 8-10 | 25-35 | Test analysis and explanation |
| Essay | 1-2 | 15-20 | 20-30 | Test critical thinking and synthesis |

#### Step 2.3: Map Questions to Knowledge Points

Create a coverage matrix ensuring:

- Every major knowledge point has at least one question
- High-frequency exam topics (from past exam analysis) are adequately represented
- Difficulty is distributed across topics, not concentrated
- Questions progress from basic to advanced within each section

```
Knowledge Point Matrix:
| Knowledge Point        | Q1 | Q2 | Q3 | ... | Coverage |
|------------------------|----|----|----|----|----------|
| Concept A              | ★  |    |    |    | ✓        |
| Formula B              |    | ★  | ★  |    | ✓        |
| Derivation C           |    |    |    | ★  | ✓        |
```

### Phase 3: Question Composition

#### Step 3.1: Question Writing Guidelines

Follow these principles for each question:

**Single/Multiple Choice Questions**:
- Stem must be clear and unambiguous
- All options must be plausible (avoid obviously wrong distractors)
- For math questions, include common computational errors as distractors
- Clearly mark "(多选)" for multiple-choice questions
- Each option should test a specific misconception or knowledge gap

**True/False Questions**:
- Statement must be definitively true or false, not debatable
- Include subtle modifications of correct statements to test precision
- Require brief justification (not just T/F marking)

**Fill-in-the-Blank Questions**:
- Blank should test a key formula component or critical concept
- Provide sufficient context/equations so the blank is uniquely determined
- For numerical answers, specify precision requirements

**Short Answer Questions**:
- Ask for explanation of concepts, comparison of methods, or analysis
- Provide clear scope: "from the following N aspects" if applicable
- Should require 100-300 words to answer adequately

**Calculation/Proof Questions**:
- State all given conditions explicitly
- Break complex problems into sub-parts (a), (b), (c)
- Ensure intermediate results can be verified
- Include point allocation for each sub-part

#### Step 3.2: Source Citation（仅答案卷显示）

Every question MUST have a source citation record. **This is mandatory — never omit it.**
However, **source citations must be written in the answer sheet only**, not in the exam paper.

The citation must specify:
1. The **exact filename** of the source material (e.g., `精算学第三章生命表.pptx`)
2. The **specific slide/page number(s)** where the knowledge point appears
3. A brief description of the knowledge point covered

**Required format:**
```
> *来源：[文件名] 第[N]页（[知识点简述]）*
```

**Examples (follow these exactly):**
- `> *来源：精算学第三章生命表.pptx 第15页（死亡力 $\mu_x$ 的定义与推导）*`
- `> *来源：精算学第三章生命表.pptx 第8-10页（Balducci假设与UDD假设对比）*`
- `> *来源：利息理论第五章.pptx 第22页（年金现值公式）+ 习题集4.2改编*`
- `> *来源：教材第5章 §5.3 第187页（定理5.3.2）*`
- `> *来源：2023年期末真题 第3题（改编自课件第三章生命表.pptx 第20页）*`

**If the exact page number cannot be determined** from the converted Markdown, write the nearest identifiable section heading:
- `> *来源：精算学第三章生命表.pptx「第三节 完全未来寿命」（具体幻灯片页码待确认）*`

> ⚠️ **Do NOT write vague citations like `来源：课件` or `来源：第三章`. Always include filename and page number.**

> ⚠️ **Placement rule**：
> - 题目卷：不得出现任何“来源”字段或来源脚注。
> - 答案卷：每题答案后必须附来源标注（按上述格式）。

#### Step 3.3: Math Formatting

Use proper LaTeX notation throughout:

- Inline math: `$formula$`
- Display math: `$$formula$$`
- Aligned equations:
  ```
  $$\begin{aligned}
  step_1 &= expression_1 \\
  step_2 &= expression_2
  \end{aligned}$$
  ```
- Common actuarial/math notations:
  - Life table functions: `$l_x$`, `$d_x$`, `$q_x$`, `$p_x$`, `$\mu_x$`, `$e_x$`, `$\bar{e}_x$`
  - Conditional probabilities: `${}_{n}p_x$`, `${}_{n}q_x$`, `${}_{n|m}q_x$`
  - Integrals: `$\int_0^\infty$`, `$\sum_{k=0}^{n}$`
  - Fractions: `$\dfrac{a}{b}$` (display) or `$\tfrac{a}{b}$` (inline)

### Phase 4: Assembly and Output

#### Step 4.1: Exam Paper Format

Assemble the final exam paper in this Markdown structure:

> **⚠️ 编号规则：每个题型大题内部序号从 1 重新开始，禁止跨题型连续编号。**
> ✅ 正确：一、单选题 **1.**2.3.4.5　二、判断题 **1.**2.3　三、填空题 **1.**2.3.4
> ❌ 错误：一、单选题 1.2.3.4.5　二、判断题 **6.**7.8　三、填空题 **9.**10.11.12

```markdown
# [课程名称] · [章节/主题] · 测试卷

> **总分：[X] 分　　建议用时：[Y] 分钟**
> **难度分布：基础 [A]% / 中等 [B]% / 综合 [C]%**

---

## 一、单项选择题（每题 X 分，共 Y 分）

**1.** [题目内容]

A. [选项A]　　B. [选项B]　　C. [选项C]　　D. [选项D]

**2.** [题目内容]　← 每个大题内部从 1 开始，依次递增

---

## 二、多项选择题（每题 X 分，共 Y 分，多选、少选均不得分）

**1.** [题目内容]　← 重新从 1 开始

...

## 三、判断题（每题 X 分，共 Y 分，判断正误并简述理由）

**1.** [题目内容]　← 重新从 1 开始

...

## 四、填空题（每题 X 分，共 Y 分）

**1.** [题目内容]　← 重新从 1 开始

...

## 五、简答题（每题 X 分，共 Y 分）

**1.** [题目内容]　← 重新从 1 开始

...

## 六、计算/证明题（每题 X 分，共 Y 分）

**1.** [题目内容]　← 重新从 1 开始

...

---

## 参考答案速查（仅答案，不含解释）

> 用于快速批改，禁止写“要点/过程/公式推导”。

### 客观题答案汇总

- 单选：1.A，2.B，3.A，...
- 多选：1.ABD，2.BC，...
- 判断：1.对，2.错，...
- 填空：1.[答案]，2.[答案]，...

## 参考答案明细（含详细解答与评分标准）

### 详细解答

**单选题 第1题**

[完整解题步骤，包含公式推导]

**判断题 第1题**

...
```

#### Step 4.2: Answer Key Guidelines

The answer key must include:

1. **Quick Reference Section（置于答案卷开头）** — One-line answers for objective questions only, no explanation
2. **Detailed Solutions** — Full step-by-step solutions for calculation/proof questions
3. **Scoring Rubric** — For subjective questions, list key answer points and their scores
4. **Common Mistakes** — Note typical errors students may make
5. **Source Statistics（来源统计）** — The answer key **must** include the following statistics block:

> ⚠️ **Quick Reference Section constraints**:
> - 仅保留题号与最终答案（如 `1.A`、`2.BD`、`3.对`）。
> - 不要出现“要点”“过程”“公式推导”或长文本说明。
> - 禁止在速查区放置 LaTeX 公式，避免出现未渲染的 `$$...$$`。

```
### 📊 来源统计

| 指标 | 数值 |
|------|------|
| 📌 历年真题重复率 | X / M × 100% = __% （X：与历年真题完全相同或高度相似的题目数；M：本次试卷总题目数） |
| 📝 习题原题率 | Y / N × 100% = __% （Y：直接来自习题库的原题数；N：本次试卷总题目数） |
| 📂 文件覆盖率 | K / T × 100% = __% （K：至少有一道题来源于该文件的文件数；T：上传参考文件总数） |

**各文件出题数量：**

| 文件名 | 出题数量 | 占总题数比例 |
|--------|----------|-------------|
| [文件1] | [n] 题 | [x]% |
| [文件2] | [n] 题 | [x]% |
| ...    | ...      | ...   |
```

> **计算规则**：
> - 同一道题若与历年真题"相同知识点但改写表述"，计为**重复**（相似度 ≥ 70%）。
> - 做到文件覆盖率 = 100%（每个上传文件至少有 1 道题使用它作为来源）。
> - 如有文件覆盖率 < 100%，必须在此处说明原因。

#### Step 4.3: Quality Checklist

Before delivering the exam paper, verify:

- [ ] Total score sums correctly to the stated total
- [ ] **每个题型大题内部序号从 1 重新开始，禁止跨题型连续编号**
- [ ] 题目卷不显示来源；答案卷每题均有来源标注
- [ ] Math notation renders correctly (balanced `$` signs, proper LaTeX)
- [ ] Difficulty distribution matches the stated ratio
- [ ] **All major knowledge points are covered AND every uploaded file is represented by at least one question**
- [ ] Answer key matches all questions
- [ ] No duplicate or near-duplicate questions
- [ ] Language is consistent throughout (no mixed Chinese/English unless intentional)
- [ ] Questions are ordered from easy to hard within each section
- [ ] **答案卷包含"来源统计"表格**（历年真题重复率 + 习题原题率 + 文件覆盖率，且文件覆盖率达到 100%）

### Phase 5: Variants and Comparisons (Optional)

#### Step 5.1: Generate Exam Variants

When asked to create multiple variants:

1. **Same structure, different numbers** — Change numerical values in calculation questions
2. **Same knowledge points, different question angles** — Test the same concept from a different perspective
3. **Different source combinations** — Use different subsets of source materials (e.g., PPT-only vs. PPT+exercise bank)

#### Step 5.2: Comparative Analysis

When generating multiple papers from different sources, provide a comparison table:

```markdown
## 各卷对比分析

| 维度 | 试卷一 | 试卷二 | 试卷三 |
|------|--------|--------|--------|
| 参考来源 | [sources] | [sources] | [sources] |
| 知识覆盖率 | X% | Y% | Z% |
| 计算题占比 | A% | B% | C% |
| 与历年真题重合度 | ... | ... | ... |
| 综合评价 | ... | ... | ... |
```

## Important Notes

1. **Never fabricate questions** — Every question must be derivable from the provided source materials
2. **Respect source boundaries** — When the user specifies which sources to use, strictly limit question derivation to those sources only
3. **Academic integrity** — Do not reproduce entire past exam papers verbatim; adapt, modify, and create original variations
4. **Difficulty calibration** — If past exams are available, calibrate difficulty to match the historical level
5. **Subject sensitivity** — Adapt question types and scoring to the specific subject domain (STEM vs. humanities vs. professional exams)
6. **Progressive complexity** — Within each question type section, arrange questions from easier to harder
7. **File output** — Save the generated exam paper to `/mnt/user-data/workspace/` as a `.md` file for easy download

## 中国高校试卷规范适配

### 试卷头部格式

中国高校正式考试试卷应遵循以下格式规范：

```markdown
# XX大学 20XX—20XX 学年第 X 学期期末考试试卷

**课程名称**：[课程名]　　**课程代码**：[代码]
**考试时间**：[120] 分钟　　**试卷总分**：[100] 分
**考试形式**：闭卷 / 开卷　　**适用专业/年级**：[专业年级]

| 题型 | 一 | 二 | 三 | 四 | 五 | 六 | 总分 |
|------|----|----|----|----|----|----|------|
| 分值 | XX | XX | XX | XX | XX | XX | 100  |
| 得分 |    |    |    |    |    |    |      |

**注意事项**：
1. 请在答题纸上作答，写在试卷上无效
2. 考试结束后请将试卷和答题纸一并交回
```

### 题型中文标准称谓

| 英文 | 中文标准称谓 | 备注 |
|------|-------------|------|
| Single Choice | 单项选择题 | 每小题只有一个正确答案 |
| Multiple Choice | 多项选择题 | 注明"多选、少选均不得分" |
| True/False | 判断题 | 可要求"判断并简述理由" |
| Fill-in-the-Blank | 填空题 | 注明精度要求（如"保留4位小数"） |
| Short Answer | 简答题 | — |
| Calculation | 计算题 | 注明"要求写出计算过程" |
| Proof | 证明题 | — |
| Essay | 论述题 | 人文社科类常用 |
| Case Analysis | 案例分析题 | 商科/法学常用 |

### 分数合计校验

生成试卷后自动执行：
1. 各大题小题分数之和 = 该大题标注总分
2. 所有大题总分之和 = 试卷标注总分（通常 100 分）
3. 客观题（选择+判断+填空）占比建议 30%-50%
4. 主观题（简答+计算+证明）占比建议 50%-70%

## 试卷格式模板

`/mnt/skills/public/exam-generation/templates/` 目录下提供了两份官方出卷模板，出卷时应参照这些模板的版式和格式要求：

| 文件名 | 用途 |
|--------|------|
| `浙江财经大学出卷模板.doc` | **题目卷模板**：包含标准封面（课程名称、班级、姓名、学号栏）、各题型版式、分数栏、注意事项等 |
| `试卷答案及评分标准模板.doc` | **答案卷模板**：包含每题参考答案、评分标准、分值分配说明等 |

### 模板使用规范

1. **封面信息**：题目卷需包含"课程名称""考试时间""总分""班级/姓名/学号"填写栏
2. **题型顺序**：按照模板顺序排列（单选题 → 判断题/填空题 → 简答题 → 计算题/证明题）
3. **分值标注**：每大题在括号内注明"（每题 X 分，共 X 分）"
4. **答案卷**：每题答案后附评分细则，明确各步骤得分点
5. **页眉页脚**：课程名称和"第 X 页 / 共 X 页"标注（仅 DOCX 导出时有效）

导出 DOCX 时，脚本会自动应用与模板一致的字体（宋体 12pt）和页边距设置。

## 导出为 Word / PDF

> ⚠️ **分卷强制要求**：每次出卷必须将**题目卷**和**答案卷**分别保存为独立的 Markdown 文件，再分别导出。禁止将两者合并到同一个文件中。

生成 Markdown 试卷后，根据用户在 Phase 0 确认的格式，使用内置脚本导出。**题目卷和答案卷各自单独执行导出命令。**

```bash
# ── 导出题目卷（以 docx 为例）──
python /mnt/skills/public/exam-generation/scripts/export.py \
  --input /mnt/user-data/workspace/[课程]_试题卷.md \
  --format docx \
  --output /mnt/user-data/workspace/[课程]_试题卷.docx

# ── 导出答案卷（以 docx 为例）──
python /mnt/skills/public/exam-generation/scripts/export.py \
  --input /mnt/user-data/workspace/[课程]_答案及评分标准.md \
  --format docx \
  --output /mnt/user-data/workspace/[课程]_答案及评分标准.docx

# ── 若用户选择 PDF ──
python /mnt/skills/public/exam-generation/scripts/export.py \
  --input /mnt/user-data/workspace/[课程]_试题卷.md \
  --format pdf \
  --output /mnt/user-data/workspace/[课程]_试题卷.pdf

python /mnt/skills/public/exam-generation/scripts/export.py \
  --input /mnt/user-data/workspace/[课程]_答案及评分标准.md \
  --format pdf \
  --output /mnt/user-data/workspace/[课程]_答案及评分标准.pdf

# ── 若用户选择 both（docx + pdf）──
# 对题目卷和答案卷各运行两次，format 分别为 docx 和 pdf
```

**输出文件清单**（每次出卷后必须交付所有对应文件）：

| 用户选择 | 题目卷 | 答案卷 |
|----------|--------|--------|
| docx     | `[课程]_试题卷.docx` | `[课程]_答案及评分标准.docx` |
| pdf      | `[课程]_试题卷.pdf`  | `[课程]_答案及评分标准.pdf`  |
| both     | `[课程]_试题卷.docx` + `.pdf` | `[课程]_答案及评分标准.docx` + `.pdf` |

导出脚本功能：
- **DOCX**：宋体正文、标准页边距（上下 2.54cm、左右 3.17cm）、表格自动排版
- **PDF**：中文衬线字体、打印友好排版
- **LaTeX 公式**：使用 `matplotlib` 将 `$...$`（行内）和 `$$...$$`（独行）自动渲染为高清 PNG 图片嵌入文档，Word 和 PDF 均可正确显示公式

## Example Interaction

**User**: 我上传了精算学原理第三章的课件PPT和习题库，请帮我出一套100分的测试卷

**Assistant workflow**:
1. **Ask output format** → "请问需要导出 Word、PDF 还是两者都要？" → user replies "docx"
2. Read and analyze the uploaded PPT slides → extract knowledge points (life tables, survival functions, mortality assumptions, etc.)
3. Read and analyze the exercise bank → identify question patterns and key formulas
4. Design exam structure with 6 question types totaling 100 points
5. Compose questions with proper LaTeX math and source citations
6. Generate complete answer key with detailed solutions
7. Save **题目卷** to `/mnt/user-data/workspace/精算学原理_第三章_试题卷.md`
8. Save **答案卷** to `/mnt/user-data/workspace/精算学原理_第三章_答案及评分标准.md`
9. Export 题目卷 → `精算学原理_第三章_试题卷.docx`
10. Export 答案卷 → `精算学原理_第三章_答案及评分标准.docx`
11. Deliver both files to the user

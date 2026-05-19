# Content Overview Generator

## Core Mission

After source content is processed and project is initialized, generate a **slide-by-slide content script** — showing exactly what text, data, and structure will appear on each slide — and present it to the user for confirmation. This is the first BLOCKING checkpoint after project creation.

> 💡 **Think of this as writing the slide script**: The user should be able to read through the overview and visualize each slide's content — titles, bullet points, figures referenced, key numbers, and conclusions — just like reading a finished PPT slide by slide. Design (colors, fonts, layout) comes later.

## Pipeline Context

| Previous Step | Current | Next Step |
|--------------|---------|-----------|
| Project Initialization (Step 2) | **Content Overview** (Step 3) ⛔ BLOCKING | Template Selection (Step 4) |

---

## Process

### 1. Analyze Source Content

Read the converted Markdown source file(s) from `<project_path>/sources/`. Understand:

- **Main theme**: What is the presentation about?
- **Structure**: Natural section breaks, chapter divisions
- **Key points**: Extract specific statements, data, quotes — not just topics
- **Data elements**: Charts, statistics, comparisons, tables
- **Narrative flow**: Hook → background → problem → solution → results → conclusion
- **Figures & tables**: What visuals from the source should appear on which slides

### 2. Generate Slide Script Format

Each slide should be written as a **mini script** showing the actual content. Use this format:

```
Slide N: [Slide Title]
[Content blocks as they would appear on the slide]
```

Content blocks can include:
- **Headings / subheadings**
- **Bullet points** with real text
- **Data and metrics**
- **Figure/table references** (e.g., "[图：产品架构图]", "[表1：预算分配]")
- **Key conclusions** (bold or highlighted)
- **Structure hints** when helpful

### 3. Complete Slide Script Example (Generic)

Here is what a complete content overview should look like when presented to the user. **Every slide must read like real slide content, not abstract descriptions.** This example uses a generic business/product launch scenario to show the format:

```markdown
## 📋 内容设计概览

根据您提供的素材，我建议将演示文稿设计为以下 **12页** 内容：

---

**Slide 1: 封面**
2025 年度产品战略发布
—— 智慧赋能，重塑未来

汇报人：张伟 | 产品战略部
日期：2025 年 3 月

---

**Slide 2: 目录**
1. 行业趋势与市场洞察
2. 现有产品体系回顾
3. 核心战略方向
4. 新一代产品矩阵
5. 技术架构升级
6. 路线图与里程碑
7. Q&A

---

**Slide 3: 行业趋势与市场洞察**
• 全球市场规模达 580 亿美元，年复合增长率 23%
• 客户需求从"功能完整"转向"智能化、个性化"
• 竞争对手布局：A 公司已推出 AI 原生方案，B 公司收购了 3 家初创

**关键结论**：窗口期还有 12-18 个月，必须加速产品升级

---

**Slide 4: 现有产品体系回顾**
[图：现有产品架构图]

核心产品线：
• 数据分析平台（市场份额 18%，行业第三）
• 智能推荐引擎（年收入 ¥3.2亿，同比增长 47%）
• 自动化运营系统（客户数 1200+，续费率 91%）

**优势**：推荐引擎技术领先，NLP 准确率 96%
**短板**：产品矩阵分散，缺乏统一 AI 底座

---

**Slide 5: 三大核心战略方向**
方向一：统一 AI 底座
• 构建跨产品的共享推理引擎
• 推理成本降低 60%，上线速度提升 3 倍

方向二：场景化产品组合
• 按行业打包解决方案（零售 / 金融 / 医疗）
• 客单价预计提升 2.5 倍

方向三：开放生态
• 开放 API 和低代码平台
• 目标：12 个月内接入 500+ 合作伙伴

---

**Slide 6: 新一代产品矩阵**
[图：产品矩阵布局图]

四大核心产品：
• **AI洞察平台** —— 数据 → 洞察 → 行动 全链路
• **智能决策引擎** —— 实时 AI 决策，支持因果推断
• **自适应推荐系统** —— 多模态融合，冷启动提升 40%
• **自动化工作流** —— 低代码配置 + AI 编排

**定价策略**：SaaS 订阅制，按数据量分层

---

**Slide 7: 技术架构升级**
[图：新旧架构对比图]

旧架构：烟囱式，各产品独立部署
新架构：统一 AI 底座 + 微服务

关键技术升级：
• 大模型推理引擎（延迟 < 200ms）
• 多模态融合层（文本 / 图像 / 行为）
• 实时特征平台（支持毫秒级更新）

---

**Slide 8: 路线图与里程碑**
[图：时间线路线图]

Q2 2025：AI 底座 V1.0 上线，首批 3 个客户试点
Q3 2025：四大产品完成 AI 底座迁移
Q4 2025：开放平台公测，目标 50 个合作伙伴
Q1 2026：行业解决方案发布（零售 / 金融首发）
Q2 2026：海外市场拓展（东南亚优先）

---

**Slide 9: 资源投入与预算**
[表1：预算分配表]

总预算：¥1.8 亿

• 研发投入：¥1.1 亿（61%）
  - 大模型底座：¥5,000 万
  - 产品开发：¥4,000 万
  - 基础设施：¥2,000 万
• 市场推广：¥4,000 万（22%）
• 生态建设：¥3,000 万（17%）

团队规模：从 120 人扩至 200 人

---

**Slide 10: 预期收益与 KPI**
[图：收益增长预测曲线]

| 指标 | 2025（预估） | 2026（目标）|
|------|------------|------------|
| 总收入 | ¥8.5 亿 | ¥15 亿 |
| 新客户 | 300+ | 800+ |
| 客单价 | ¥85 万 | ¥120 万 |
| 市场份额 | 22% | 35% |
| NPS 评分 | 65 | 75+ |

ROI 预计：18 个月回本

---

**Slide 11: 风险与应对**
风险 1：技术落地不及预期
• 应对：分阶段上线，关键节点设置决策 checkpoint

风险 2：市场推广滞后
• 应对：提前锁定 5 个种子客户，打造标杆案例

风险 3：人才竞争激烈
• 应对：启动"AI 英才计划"，与 3 所高校合作

---

**Slide 12: Thank You!**
联系方式：
张伟 | 产品战略部
Email: zhangwei@company.com

欢迎各位提出宝贵意见！
Q&A

---

**以上内容设计是否符合您的预期？** 您可以：
- ✅ **确认** — 进入下一步，选择风格和模板
- ✏️ **编辑** — 告诉我哪些页需要调整
- 🔄 **调整结构** — 增删、合并、排序页面

> ⛔ **BLOCKING**：等待用户确认或修改后再继续。
```

### 4. Content Design Rules

#### Rule 1: Every slide must read like real slide content

✅ **GOOD** (user can visualize the slide):
```
**Slide 3: 行业趋势与市场洞察**
• 全球市场规模达 580 亿美元，年复合增长率 23%
• 客户需求从"功能完整"转向"智能化、个性化"
• 竞争对手布局：A 公司已推出 AI 原生方案

**关键结论**：窗口期还有 12-18 个月，必须加速产品升级
```

❌ **BAD** (too vague, can't visualize):
```
**Slide 3: Market Trends**
Type: Content
• Talk about market size
• Talk about competitors
• Draw conclusion
```

#### Rule 2: Include figure/table references where content needs visuals

When the content needs a figure, chart, or table, note it with brackets: `[图：产品架构图]`, `[表1：预算分配表]`, `[图：收益增长预测曲线]`. This tells the user "there will be a visual here showing X."

#### Rule 3: Use natural content hierarchy
- **Main headings**: Bold and clear
- **Bullet points**: Use `•` for slide-style bullets
- **Sub-bullets**: Indent for secondary points
- **Conclusions**: Highlight with `**结论**` or similar
- **Data**: Include actual numbers, not placeholders

#### Rule 4: Separate slides clearly
Use `---` between slides for visual separation.

#### Rule 5: NO design decisions in this step
- No colors, no fonts, no layout modes
- No template choices
- No icon selections
- No image generation prompts

All of those come in Steps 4 & 5.

### 5. Slide Types Reference

| Slide Type | Description | Typical Content |
|-----------|-------------|-----------------|
| **Cover** | Title page | Title, subtitle, author, date, affiliation |
| **TOC / Agenda** | Table of contents | Section list with page numbers |
| **Background / Context** | Problem setting | Industry trends, market data, pain points |
| **Challenge** | Problem statement | Specific issues, why they matter |
| **Insight / Observation** | Key finding | Data analysis, charts, key takeaways |
| **Overview / Framework** | High-level picture | Architecture diagram, pipeline, roadmap |
| **Method / Approach** | Specific solution | Steps, components, logic |
| **Data / Results** | Key numbers | Tables, metrics, comparisons |
| **Comparison** | Side-by-side | Before/after, competitor comparison |
| **Timeline / Roadmap** | Time-based | Milestones, phases, schedules |
| **Conclusion** | Summary | Key takeaways, next steps |
| **Ending** | Thank you / Q&A | Contact info, links, Q&A |

### 6. Output File

Save the confirmed content design to `<project_path>/content_overview.md` in the same script format:

```markdown
# Content Overview — {project_name}

- **Source**: {source_description}
- **Total Slides**: {slide_count}
- **Generated**: {date}

---

**Slide 1: {Slide Title}**
{Actual content as it would appear on the slide}

---

**Slide 2: {Slide Title}**
{Actual content as it would appear on the slide}

---
...
```

### 7. After User Confirmation

1. Save confirmed version to `<project_path>/content_overview.md`
2. Page structure is now **locked for content**
3. Proceed to **Step 4: Template Selection** (style comes next)

> The confirmed content script becomes the **Content Outline** foundation when the Strategist generates `design_spec.md`. The Strategist inherits every slide's content verbatim and wraps it with design annotations (layout modes, visual types, typography).

### 8. User Requests Changes

If user requests changes:
1. Modify specific slides accordingly
2. Re-present the updated version
3. Once confirmed, save and proceed

### Relationship with Strategist's Content Outline

- **Content Overview (Step 3)**: The complete slide-by-slide content script — every word, data point, and figure reference. **This is what the slides SAY.**
- **Strategist's design_spec.md (Step 5)**: Adds Section IX (Content Outline) which **preserves the content script verbatim**, then layers on design decisions (layout mode, visual types, typography annotations)

The content in `content_overview.md` MUST be preserved word-for-word in the Strategist's Content Outline. The Strategist only adds design annotations, never changes the content itself.

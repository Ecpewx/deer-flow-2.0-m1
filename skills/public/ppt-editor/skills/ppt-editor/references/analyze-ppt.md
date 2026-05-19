# Analyze Existing PPT

## Core Mission

When a user provides an existing PPTX for modification, first analyze it thoroughly to understand its current state before suggesting or making any changes.

## Process

### 1. Extract Content

Use ppt-master's PPTX-to-Markdown conversion:

```bash
python3 /mnt/skills/public/ppt-master/skills/ppt-master/scripts/source_to_md/ppt_to_md.py <project_path>/source.pptx -o <project_path>/source_content.md
```

Read the output to understand:
- Total slide count
- Each slide's title hierarchy
- Body text content per slide
- Any tables, charts, or image references detected

### 2. Identify Slide Types

After reading the content, classify each slide:

| Slide Type | Clues |
|-----------|-------|
| **Cover** | First slide, large title, author/date info |
| **TOC / Agenda** | List of section names, numbered items |
| **Section Divider** | Short text, large font, between sections |
| **Content** | Bullet points, paragraphs |
| **Data / Chart** | Numbers, percentages, comparisons |
| **Table** | Structured rows/columns |
| **Image-heavy** | Image descriptions, minimal text |
| **Quote / Callout** | Single emphasized statement |
| **Ending** | Thank you, Q&A, contact info |

### 3. Build Slide Map

Present a clear map to the user:

```markdown
📊 PPT 分析报告

总页数：15 页

| 页码 | 标题 | 类型 | 要点数 |
|------|------|------|--------|
| 1 | 2025产品战略发布 | 封面 | - |
| 2 | 目录 | TOC | 6 章节 |
| 3 | 市场趋势分析 | 内容 | 4 要点 |
| 4 | 产品路线图 | 时间线 | 5 节点 |
| ... | ... | ... | ... |
| 15 | Thank You | 结尾 | - |

当前设计概况：
- 配色：蓝色系（主色 #1A5276）
- 字体：微软雅黑
- 风格：商务正式

请问您想从哪开始修改？
```

### 4. Note Design Characteristics

When analyzing, note what design elements are observable:
- Color scheme (dominant colors)
- Font usage (title vs body fonts)
- Layout patterns (single column, two-column, etc.)
- Use of images or icons
- Footer/header patterns
- Page number placement

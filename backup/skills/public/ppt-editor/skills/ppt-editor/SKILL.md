---
name: ppt-editor
description: >
  AI-driven PPT modification system. Takes an existing PPTX and performs
  user-guided modifications — content changes, design updates, restructuring,
  restyling. Each modification step requires explicit user input and confirmation.
  Use when user asks to "modify PPT", "edit presentation", "修改PPT", "改PPT",
  "帮我改一下这个PPT", or mentions "change my PPT".
---

# PPT Editor Skill

> AI-driven PPT modification system. Takes existing PPTX files and performs step-by-step user-guided modifications.

**Core Pipeline**: `Input PPT → Analyze → Understand State → [Modification Loop: Ask → Specify → Modify → Confirm] → Export Modified PPTX`

> [!CAUTION]
> ## 🚨 Global Execution Discipline (MANDATORY)
>
> **This workflow is an interactive modification loop. Each modification is a user-guided step:**
>
> 1. **INTERACTIVE**: Every modification requires user input — never assume what to change
> 2. **⛔ BLOCKING PER MODIFICATION**: Each individual modification step is BLOCKING. Wait for user to specify details, apply the change, then wait for confirmation before next modification
> 3. **ASK STEP BY STEP**: Never bundle multiple modification questions into one question. Ask one modification at a time
> 4. **UNDERSTAND BEFORE MODIFY**: Always analyze the current state of the PPT first. Don't suggest modifications without understanding what exists
> 5. **SHOW WHAT CHANGED**: After each modification, show the user what was changed before asking for confirmation
> 6. **NO UNREQUESTED CHANGES**: Only make changes the user explicitly requests. Don't add "improvements" they didn't ask for
> 7. **PRESERVE UNTOUCHED CONTENT**: Content the user doesn't ask to change must stay exactly as-is

> [!IMPORTANT]
> ## 🌐 Language & Communication Rule
>
> - **Response language**: Match the user's input language
> - **Always ask for specifics**: When user says "change this slide", ask what exactly to change. When user says "make it blue", ask which blue.
> - **Confirm understanding**: Before applying changes, summarize what you understood the user wants

---

## Workflow

### Step 1: Receive PPT and Initialize Project

🚧 **GATE**: User has provided or pointed to an existing PPTX file.

> ⛔ **BLOCKING**: Ask the user which PPT they want to modify, and what general scope of changes they're thinking about (don't dive into details yet — just understand the scope).

**Process**:

1. If user hasn't provided a PPTX yet, ask them to upload or specify the file path
2. Create a project workspace:
   ```bash
   python3 /mnt/skills/public/ppt-master/skills/ppt-master/scripts/project_manager.py init <project_name> --format ppt169 --dir /mnt/user-data/projects
   ```
3. Copy the input PPTX into the project:
   ```bash
   cp <input_pptx_path> <project_path>/source.pptx
   ```
4. Ask the user about the general scope:
   ```
   📋 我已经收到了您的PPT。在开始修改之前，请您先告诉我大致想改哪些方面？例如：
   
   - ✏️ **内容修改** — 修改文字、更新数据、增删要点
   - 🎨 **设计修改** — 改颜色、字体、整体风格
   - 📐 **结构调整** — 增删页面、调整顺序
   - 🖼️ **图片修改** — 替换图片、添加新图
   - 🔄 **整体刷新** — 保留内容，换个全新风格
   
   或者您可以先告诉我具体想改哪一页？
   ```

**✅ Checkpoint — User has described scope. Proceed to Step 2.**

---

### Step 2: Analyze Current PPT

🚧 **GATE**: PPTX received and project initialized.

> ⛔ **BLOCKING**: Analyze the PPT and present findings to user. Ask if they want to proceed with modifications based on this understanding.

**Process**:

1. Extract PPT content to understand structure:
   ```bash
   python3 /mnt/skills/public/ppt-master/skills/ppt-master/scripts/source_to_md/ppt_to_md.py <project_path>/source.pptx -o <project_path>/source_content.md
   ```

2. Read the extracted content to understand:
   - Total slide count
   - Each slide's title and content
   - Current design characteristics (colors, layout types if detectable)

3. Present analysis to user:
   ```
   📊 **PPT 分析结果**
   
   总页数：{N} 页
   结构概览：
   | 页码 | 标题 | 类型 |
   |------|------|------|
   | 1 | {title} | 封面 |
   | 2 | {title} | {type} |
   | ... | ... | ... |
   
   当前设计概况：{简要描述可识别的设计特征}
   
   请问您想从哪一页开始修改？或者想做什么类型的修改？
   ```

**✅ Checkpoint — User has seen analysis and is ready to specify modifications.**

---

### Step 3: Modification Loop (⛔ BLOCKING per iteration)

🚧 **GATE**: PPT analyzed and user is ready.

> ⛔ **BLOCKING — EACH MODIFICATION**: This is a loop. For EACH modification:
> 1. Ask user what to modify (which slide? what aspect?)
> 2. Ask for specific details (what text? what color? what layout?)
> 3. Ask follow-up questions until you have enough detail
> 4. Apply the modification
> 5. Show the result and ask for confirmation
> 6. Ask "Do you want to make another modification?"
> 7. If yes → loop; if no → proceed to Step 4

**Critical Rule**: Never bundle multiple modifications. One question → one answer → one change → one confirmation → next.

#### 3.1 Modification Type Identification

When user tells you what they want to modify, identify the type and ask appropriate follow-ups:

| User Says | Type | Ask For |
|-----------|------|---------|
| "改一下第3页的文字" | Content Change | Which text? New text content? Formatting? |
| "把配色换成蓝色的" | Design Change | Which blue? Exact color? All slides or specific? |
| "加一页新的" | Structure Add | Where to insert? What content? |
| "删掉第5页" | Structure Remove | Confirm deletion |
| "换张图片" | Image Change | Which image? New image source? Position/size? |
| "整体风格改一下" | Style Refresh | Which style direction? Reference examples? |

#### 3.2 Content Modification Sub-flow

When user wants to change text/content on a slide:

```
您想修改第3页的文字，请问具体要改哪里？

当前第3页的内容：
标题：市场趋势分析
正文：
• 2024年市场规模达到420亿
• 年增长率15%
• 主要竞争对手：A公司、B公司

您想：
1️⃣ 改标题 → 新标题是什么？
2️⃣ 改某个要点 → 改哪个？改成什么？
3️⃣ 新增一个要点 → 内容是什么？插在哪里？
4️⃣ 删除某个要点 → 删哪个？
5️⃣ 全部替换 → 新内容是什么？

或者您可以直接告诉我：把"420亿"改成"580亿"，把"15%"改成"23%"
```

#### 3.3 Design Modification Sub-flow

When user wants to change design/colors/fonts:

```
您想修改配色方案，请问具体要：

1️⃣ 改主色 → 想要什么颜色？（可提供 HEX 值、颜色名称、或参考图片）
2️⃣ 改字体 → 标题字体？正文字体？
3️⃣ 改背景 → 纯色？渐变？图片？
4️⃣ 参考已有风格 → 是否有参考的PPT或品牌指南？

或者您可以说：\"我想要科技蓝色系，主色#1565C0，字体用微软雅黑\"
```

#### 3.4 Structure Modification Sub-flow

When user wants to add/reorder slides:

```
您想新增一页，请问：

1️⃣ 插在哪一页后面？
2️⃣ 这页的标题是什么？
3️⃣ 主要内容是什么？
4️⃣ 需要什么特殊格式？（图表、图片、对比等）
```

#### 3.5 Style Refresh Sub-flow

When user wants to refresh the overall style:

```
好的，您想整体刷新风格。请问：

1️⃣ 想要什么风格方向？
   - 科技感（蓝色系、简洁现代）
   - 商务专业（深蓝/深灰、稳重）
   - 创意活力（亮色、动感）
   - 简约清新（浅色、留白多）
   - 其他（请描述）

2️⃣ 有没有参考的PPT或图片风格？
3️⃣ 需要保留现有配色中的哪些元素吗？
4️⃣ 字体是否需要更换？
```

#### 3.6 Image Modification Sub-flow

When user wants to change images:

```
您想更换图片，请问：

1️⃣ 要换第几页的哪张图？
2️⃣ 新图片是您提供，还是需要我生成？
   - 您提供 → 请上传图片文件
   - AI生成 → 请描述想要的图片内容（场景、风格、色调）
3️⃣ 图片的位置和大小需要调整吗？
```

### 3.7 Applying Modifications

Once user has provided sufficient detail:

1. **For content changes**: Update the extracted Markdown content, then regenerate the affected SVG pages
2. **For design changes**: Update spec_lock.md and regenerate affected SVGs
3. **For structural changes**: Add/remove SVG pages and update numbering
4. **For style refresh**: Create new design spec, regenerate all SVGs with new style

Use ppt-master's executor and scripts to apply changes:
```bash
# Read current spec_lock for reference
read_file <project_path>/spec_lock.md

# Read current SVG for the slide being modified
read_file <project_path>/svg_output/03_content.svg

# After determining changes, regenerate the modified SVG
# (use the same SVG generation approach as ppt-master executor)
```

**After applying**: Show the user what changed and ask for confirmation:

```
✅ 修改完成！

第3页已更新：
- 标题：市场趋势分析 ✅（保持不变）
- 数据更新："420亿" → "580亿" ✅
- 数据更新："15%" → "23%" ✅
- 新增："• 海外业务占比提升至35%" ✅

您还满意吗？需要继续修改其他内容吗？
```

**✅ Checkpoint — User confirms this modification. Ready for next modification or export.**

---

### Step 4: Finalize and Export

🚧 **GATE**: User confirms no more modifications needed.

**Process**:

1. Run SVG post-processing:
   ```bash
   python3 /mnt/skills/public/ppt-master/skills/ppt-master/scripts/finalize_svg.py <project_path>
   ```

2. Export to PPTX:
   ```bash
   python3 /mnt/skills/public/ppt-master/skills/ppt-master/scripts/svg_to_pptx.py <project_path> -s final
   ```

3. Deliver to user:
   ```
   ✅ 修改完成！您的PPT已导出：
   
   文件路径：{project_path}/exports/{filename}.pptx
   
   修改总结：
   - 共修改了 {N} 处内容
   - 更新了 {M} 页设计
   - {其他修改概要}
   
   您还有什么需要吗？
   ```

**✅ Checkpoint — PPT exported and delivered to user.**

---

## Key Principles

### 1. One Change at a Time

✅ **GOOD**:
```
User: "我想改第3页的颜色"
AI: "好的，第3页想改成什么颜色？"

User: "蓝色"
AI: "哪种蓝色？比如：#1565C0（亮蓝）、#003366（深蓝）、还是您有其他偏好？"
```

❌ **BAD**:
```
User: "我想改一下PPT"
AI: "请问您想改第3页的颜色、第5页的文字、加一页新的、换字体、改背景...（一次性列了10个问题）"
```

### 2. Always Ask for Specifics

When user gives vague instructions, ask clarifying questions:

| User Says | Instead of Assuming | Ask |
|-----------|-------------------|-----|
| "把这段文字改一下" | Changing random text | "改成什么内容？" |
| "换个好看的颜色" | Picking any color | "您想要什么色系的？有参考颜色吗？" |
| "这里加个图表" | Adding any chart | "加什么类型的图表？数据是什么？" |
| "整体调一下" | Making random adjustments | "具体想调哪些方面？" |

### 3. Preserve Context

- When modifying one slide, keep all other slides exactly as they were
- When changing colors, only change what the user specified
- When updating text, preserve formatting unless asked to change it
- Show the user what stayed the same AND what changed after each modification

### 4. Use ppt-master Infrastructure

ppt-editor leverages ppt-master's existing scripts and SVG pipeline:

| Need | Use |
|------|-----|
| Extract PPT content | `ppt_to_md.py` |
| Analyze images | `analyze_images.py` |
| Generate new images | `image_gen.py` |
| Post-process SVGs | `finalize_svg.py` |
| Export PPTX | `svg_to_pptx.py` |
| SVG format constraints | `shared-standards.md` |
| Canvas formats | `canvas-formats.md` |

---

## Interaction Example

Here's a complete example interaction flow:

```
User: "帮我改一下这个PPT，第3页的数据要更新"

AI: 📊 已收到您的PPT！让我先分析一下...
    (analyzes PPT, presents structure)
    
    总页数：12页
    第3页当前内容：市场趋势分析
    • 2024年市场规模达到420亿
    • 年增长率15%
    
    请问您具体要更新哪些数据？

User: "把420亿改成580亿，15%改成23%"

AI: 好的，我来修改第3页：
    • "420亿" → "580亿" ✅
    • "15%" → "23%" ✅
    
    还需要加其他内容吗？比如加一个关于海外市场的要点？

User: "加一个：海外业务占比提升至35%"

AI: 已添加 ✅
    第3页最新内容：
    • 2024年市场规模达到580亿
    • 年增长率23%
    • 海外业务占比提升至35%
    
    还需要修改其他地方吗？

User: "第3页改好了，接下来想改一下配色"

AI: 好的！您想要什么色系的配色方案？
    ...
```

---

## Reference Resources

| Resource | Path |
|----------|------|
| ppt-master scripts | `/mnt/skills/public/ppt-master/skills/ppt-master/scripts/` |
| ppt-master SVG standards | `/mnt/skills/public/ppt-master/skills/ppt-master/references/shared-standards.md` |
| ppt-master canvas formats | `/mnt/skills/public/ppt-master/skills/ppt-master/references/canvas-formats.md` |
| ppt-master image layout | `/mnt/skills/public/ppt-master/skills/ppt-master/references/image-layout-spec.md` |

---
name: ppt-master
description: >
  AI-driven multi-format SVG content generation system. Converts source documents
  (PDF/DOCX/URL/Markdown) into high-quality SVG pages and exports to PPTX through
  multi-role collaboration. Use when user asks to "create PPT", "make presentation",
  "生成PPT", "做PPT", "制作演示文稿", or mentions "ppt-master".
---

# PPT Master Skill

> AI-driven multi-format SVG content generation system. Converts source documents into high-quality SVG pages through multi-role collaboration and exports to PPTX.

**Core Pipeline**: `Source Document → Create Project → Content Overview (⛔) → Template Option (⛔) → Strategist (⛔) → [Image_Generator] → Executor → Post-processing → Export`

> **Three BLOCKING checkpoints**: Content confirmation → Template selection → Style/design confirmation. Each must wait for explicit user approval.

> [!CAUTION]
> ## 🚨 Global Execution Discipline (MANDATORY)
>
> **This workflow is a strict serial pipeline. Violating any rule below constitutes execution failure:**
>
> 1. **SERIAL**: Steps in order; non-BLOCKING adjacent steps proceed continuously without waiting
> 2. **⛔ BLOCKING = HARD STOP**: Must wait for explicit user response
> 3. **NO CROSS-PHASE BUNDLING**: Once Step 5 (Eight Confirmations ⛔) user confirms, all subsequent non-BLOCKING steps auto-proceed
> 4. **GATE BEFORE ENTRY**: Verify prerequisites before each Step
> 5. **NO SPECULATIVE EXECUTION**: Don't pre-prepare content for later Steps
> 6. **NO SUB-AGENT SVG**: Step 7 SVG generation by main agent only
> 7. **SEQUENTIAL PAGES ONLY**: One page at a time, one continuous pass
> 8. **SPEC_LOCK RE-READ PER PAGE**: `read_file <project_path>/spec_lock.md` before each page — no memory values

> [!IMPORTANT]
> ## 🌐 Language & Communication Rule
>
> - **Response language**: Match user's input language. Explicit override takes priority.
> - **Template format**: `design_spec.md` headings/field names always in English; content values may be in user's language.

> [!IMPORTANT]
> ## 🔌 Compatibility With Generic Coding Skills
>
> - Repository-specific skill, not a general scaffold. Follow this skill's workflow over generic coding conventions unless user explicitly says otherwise.

> [!IMPORTANT]
> ## 📦 Environment
>
> **SKILL_DIR**=`/mnt/skills/public/ppt-master/skills/ppt-master`
> **USER_DATA**=`/mnt/user-data`
>
> Install: `pip install -r /mnt/skills/public/ppt-master/requirements.txt`
> See `${SKILL_DIR}/references/setup.md` for full dependency details and env vars.

## Main Pipeline Scripts

All scripts under `${SKILL_DIR}/scripts/`. Key ones used in workflow:

| Script | Purpose |
|--------|---------|
| `source_to_md/pdf_to_md.py` | PDF → Markdown |
| `source_to_md/doc_to_md.py` | DOCX/HTML/EPUB → Markdown |
| `source_to_md/ppt_to_md.py` | PPTX → Markdown |
| `source_to_md/web_to_md.py` | URL → Markdown |
| `project_manager.py` | Init / import / validate |
| `analyze_images.py` | Image analysis |
| `image_gen.py` | AI image generation |
| `svg_quality_checker.py` | SVG quality check |
| `total_md_split.py` | Split speaker notes |
| `finalize_svg.py` | SVG post-processing |
| `svg_to_pptx.py` | Export to PPTX |
| `update_spec.py` | Bulk spec_lock color/font update |

Full docs: `${SKILL_DIR}/scripts/README.md`

## Template Index

| Index | Path |
|-------|------|
| Layouts | `templates/layouts/layouts_index.json` |
| Charts | `templates/charts/charts_index.json` |
| Icons | `templates/icons/` (libraries: `chunk/`, `tabler-filled/`, `tabler-outline/`) |

## Standalone Workflow

| Workflow | Path |
|----------|------|
| Create template | `workflows/create-template.md` |

---

## Workflow

### Step 1: Source Content Processing

🚧 **GATE**: User has provided source material (any format).

Convert non-Markdown content:

| Type | Command |
|------|---------|
| PDF | `python3 ${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py <file>` |
| DOCX/Office | `python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py <file>` |
| PPTX | `python3 ${SKILL_DIR}/scripts/source_to_md/ppt_to_md.py <file>` |
| EPUB/HTML/etc | `python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py <file>` |
| URL | `python3 ${SKILL_DIR}/scripts/source_to_md/web_to_md.py <URL>` |
| WeChat | `python3 ${SKILL_DIR}/scripts/source_to_md/web_to_md.py <URL>` (curl_cffi) |
| Markdown | Read directly |

**✅ Checkpoint — Confirm source content ready, proceed to Step 2.**

---

### Step 2: Project Initialization

🚧 **GATE**: Step 1 complete; source content is ready (Markdown file, user-provided text, or requirements described in conversation are all valid).

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py init <project_name> --format <format>
```

Format options: `ppt169` (default), `ppt43`, `xhs`, `story`, etc. For the full format list, see `${SKILL_DIR}/references/canvas-formats.md`.

> Add `--dir /mnt/user-data/projects` to place projects there.

**Auto-import sources** (AI MUST do this automatically, no user input needed):
```bash
# AI auto-discovers & imports:
python3 ${SKILL_DIR}/scripts/project_manager.py import-sources <project_path> /mnt/user-data/uploads/* --move
```
> ⚠️ **MUST use `--move`** — all source files moved (not copied) into `sources/` for archiving. Uploads dir is cleared.

**✅ Checkpoint — Project structure ready. Proceed to Step 3.**

---

### Step 3: Content Overview Generation (NEW — ⛔ BLOCKING)

🚧 **GATE**: Project structure ready. Read `${SKILL_DIR}/references/content-overview.md`.

> ⛔ **BLOCKING**: This is the **first of three** user confirmation checkpoints. Generate a **slide-by-slide content script** — every slide shows its actual text, bullet points, data, figures, and conclusions. Present to user and wait for explicit confirmation.

**Process**:
1. Read source content from `<project_path>/sources/`
2. Write each slide as a **mini script** — real titles, real bullet points, real data, figure references
3. **NO design decisions** — no colors, fonts, templates, or layout modes yet
4. Present inline with `---` separators between slides

**Output**:
- Present the full slide script inline to user for review
- Save confirmed version to `<project_path>/content_overview.md`

**After user confirms**: Proceed to Step 4 (Template Selection).

**If user requests changes**: Modify specific slides, re-present, re-confirm, then proceed.

**✅ Checkpoint — Content confirmed. Proceed to Step 4.**

---

### Step 4: Template Selection

🚧 **GATE**: Content overview confirmed. ⛔ **BLOCKING** (wait for user response).

**Early-exit**: If user already stated "no template" / "自由设计", skip to Step 5.

**Recommendation flow** (only when undecided):
1. Query `templates/layouts/layouts_index.json`
2. Recommend (lean toward free design unless content benefits from fixed preset)
3. Present options:

> 💡 I recommend **[template / free design]** because...
> **A) Use template** (validated structure+style preset)
> **B) Free design (recommended)** — AI tailors to your content

If A: `cp ${SKILL_DIR}/templates/layouts/<name>/*.{svg,md,png,jpg} <project_path>/templates/ 2>/dev/null; cp .../images/`
If B: proceed directly.

**✅ Checkpoint — Template confirmed. Proceed to Step 5.**

---

### Step 5: Strategist Phase (MANDATORY)

🚧 **GATE**: Template confirmed. Read `${SKILL_DIR}/references/strategist.md`.

> 💡 **Note**: Content structure has already been confirmed in Step 3 (see `<project_path>/content_overview.md`). The Strategist should inherit the confirmed page structure and focus on **design/style decisions**. The content outline in `design_spec.md` Section IX must preserve the confirmed page structure.

> ⚠️ Before writing `design_spec.md`, MUST `read_file ${SKILL_DIR}/templates/design_spec_reference.md` and follow its I–XI structure.

**⛔ BLOCKING — Eight Confirmations** (present as bundled set, wait for user):
1. Canvas format
2. Page count range (should align with confirmed content overview)
3. Target audience
4. Style objective
5. Color scheme
6. Icon usage approach
7. Typography plan
8. Image usage approach

If user provided images: `python3 ${SKILL_DIR}/scripts/analyze_images.py <project_path>/images` (NEVER read image files directly)

**Output**:
- `<project_path>/design_spec.md` — human-readable design narrative (Section IX inherits confirmed content structure)
- `<project_path>/spec_lock.md` — machine-readable contract (Executor re-reads before each page). See `templates/spec_lock_reference.md`

**✅ Checkpoint — Auto-proceed to next step.**

---

### Step 6: Image_Generator Phase (Conditional)

🚧 **GATE**: Strategist phase complete. **Skip** if image approach ≠ "AI generation".

Read `${SKILL_DIR}/references/image-generator.md`

1. Extract pending images from design spec → `images/image_prompts.md`
2. Generate: `python3 ${SKILL_DIR}/scripts/image_gen.py "prompt" --aspect_ratio 16:9 --image_size 1K -o <project_path>/images`

**✅ Checkpoint — Proceed to Step 7.**

---

### Step 7: Executor Phase

🚧 **GATE**: Steps 5 (and 6 if applicable) complete.

Read role definition (executor-base + one style):
```
Read ${SKILL_DIR}/references/executor-base.md          # REQUIRED
Read ${SKILL_DIR}/references/executor-general.md       # General
Read ${SKILL_DIR}/references/executor-consultant.md    # Consulting
Read ${SKILL_DIR}/references/executor-consultant-top.md # Top consulting
```

**Mandatory**:
1. Before first SVG: review & output key design params (canvas, colors, fonts, body font size)
2. Before **each** page: `read_file <project_path>/spec_lock.md` — resist context drift

> ⚠️ **Main-agent only**: SVG generation MUST stay with current main agent (full upstream context).
> ⚠️ **Sequential**: Pages one at a time, one continuous pass. No batching.

**Visual**: Generate SVGs → `svg_output/`
**Logic**: Generate speaker notes → `notes/total.md`

**✅ Checkpoint — Proceed to Step 8.**

---

### Step 8: Post-processing & Export

🚧 **GATE**: Step 7 complete.

> ⚠️ Execute **one at a time** (NEVER in one code block):

**7.1** — Split notes: `python3 ${SKILL_DIR}/scripts/total_md_split.py <project_path>`
**7.2** — Post-process SVGs: `python3 ${SKILL_DIR}/scripts/finalize_svg.py <project_path>`
**7.3** — Export PPTX: `python3 ${SKILL_DIR}/scripts/svg_to_pptx.py <project_path> -s final`

> 🔄 **Auto-retry 机制**: 如果某些页面在转换中出错，脚本会自动重试。
> 1. 先重试原生转换（Native DrawingML）
> 2. 如果仍失败，自动降级为 SVG 图片嵌入模式（页面内容保留，但不可直接编辑）
> 3. 生成完毕后会报告每页的状态：`✅ 成功` / `⚠️ 降级` / `❌ 失败`
> 4. 最终 PPTX **始终包含所有页面**，不会因部分页面出错而缺少内容
>
> ❌ NEVER use `cp` as substitute for `finalize_svg.py`
> ❌ NEVER export from `svg_output/` — use `-s final`
> ❌ NEVER add extra flags like `--only`

---

## Role Switching Protocol

Before switching roles, **read** the corresponding reference file, then output:
```
## [Role Switch: <Role Name>]
📖 Reading: ${SKILL_DIR}/references/<filename>.md
📋 Task: <brief description>
```

## Reference Resources

| Resource | Path |
|----------|------|
| Shared technical constraints | `references/shared-standards.md` |
| Canvas formats | `references/canvas-formats.md` |
| Image layout | `references/image-layout-spec.md` |
| SVG embedding | `references/svg-image-embedding.md` |
| Full setup/deps | `references/setup.md` |

## Notes

- Local preview: `python3 -m http.server -d <project_path>/svg_final 8000`
- Troubleshooting: check `docs/faq.md` for known issues

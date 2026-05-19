#!/usr/bin/env python3
"""生成 PPT Master 功能介绍 Word 文档"""
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os

doc = Document()

# ── 全局默认样式 ──
style = doc.styles['Normal']
font = style.font
font.name = 'Microsoft YaHei'
font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

# ── 辅助函数 ──
def add_heading_styled(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'Microsoft YaHei'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    return h

def add_para(text, bold=False, size=None, align=None, space_after=Pt(6)):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    if bold:
        run.bold = True
    if size:
        run.font.size = size
    if align:
        p.alignment = align
    p.paragraph_format.space_after = space_after
    return p

def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        for p in hdr_cells[i].paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(10)
                r.font.name = 'Microsoft YaHei'
                r.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    # Data rows
    for row_data in rows:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = str(val)
            for p in row_cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
                    r.font.name = 'Microsoft YaHei'
                    r.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    return table

# ═══════════════════════════════════════════
# 封面标题
# ═══════════════════════════════════════════
doc.add_paragraph()  # 空行
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('PPT Master\nAI 驱动智能演示文稿生成系统')
run.bold = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
run.font.name = 'Microsoft YaHei'
run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('功能特性与技术架构概述')
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
run.font.name = 'Microsoft YaHei'
run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

doc.add_paragraph()  # 空行

# ═══════════════════════════════════════════
# 目录提示
# ═══════════════════════════════════════════
toc = doc.add_paragraph()
toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = toc.add_run('（建议目录：插入 → 引用 → 目录 → 自动目录）')
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
run.font.name = 'Microsoft YaHei'
run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

doc.add_page_break()

# ═══════════════════════════════════════════
# 一、系统概述
# ═══════════════════════════════════════════
add_heading_styled('一、系统概述', level=1)

add_para(
    'PPT Master 是一个基于人工智能多角色协作的智能演示文稿生成系统。'
    '它能够将用户的源文档（PDF、DOCX、网页链接、Markdown 等）自动转化为'
    '原生可编辑的 PPTX 文件，输出采用 PowerPoint 标准 DrawingML 格式，'
    '绝非图片式 PPT，可在 PowerPoint 或 WPS 中自由编辑。'
)

add_para('核心价值：', bold=True)
add_table(
    ['特性', '说明'],
    [
        ['原生可编辑', '生成的 PPTX 使用标准 DrawingML 形状（Shape/TextBox/Chart），可在 PowerPoint/WPS 中任意编辑文字、颜色、布局'],
        ['AI 驱动', '多角色 AI 协作（策略师 → 图片生成 → 执行器），无需人工设计能力'],
        ['多画布格式', '支持 16:9、4:3、小红书、微信朋友圈、Story 等多种画布格式'],
        ['专业模板库', '内置 21 套专业模板，覆盖 McKinsey、Google、政府、学术等多种场景'],
        ['零依赖核心', '项目管理等核心功能仅依赖 Python 标准库，可选依赖按需安装'],
    ]
)

# ═══════════════════════════════════════════
# 二、系统架构
# ═══════════════════════════════════════════
add_heading_styled('二、系统架构', level=1)

add_heading_styled('2.1 整体处理流程', level=2)
add_para(
    '源文档 → 创建项目 → 模板选择 → 策略师八项确认 → [图片生成] → 执行器生成 SVG → 后处理 → 导出 PPTX'
)

add_heading_styled('2.2 多角色协作模型', level=2)
add_para('系统采用四角色流水线架构，每个角色独立且严格串行执行：')

add_table(
    ['角色', '职责', '关键产出'],
    [
        ['策略师 (Strategist)', '分析源文档、与用户完成八项确认、制定设计规范', 'design_spec.md（设计规范）、spec_lock.md（执行锁定文件）'],
        ['图片生成器 (Image_Generator)', '根据设计规范 AI 生成所需图片（可选阶段）', '图片资源、image_prompts.md'],
        ['执行器 (Executor)', '逐页生成 SVG、编写演讲备注、保证跨页一致性', 'svg_output/ 目录下的 SVG 页面、notes/total.md'],
        ['后处理流水线', '备注拆分、SVG 优化、PPTX 导出', '最终 PPTX 文件'],
    ]
)

add_heading_styled('2.3 技术栈', level=2)
add_table(
    ['层级', '核心技术'],
    [
        ['SVG 生成', '手工 SVG 绘制（viewBox 坐标系统），遵循严格 PPT 兼容性约束'],
        ['PPTX 导出', 'python-pptx + DrawingML（原生形状，非图片）'],
        ['PDF 转换', 'PyMuPDF（文本、图片、表格提取）'],
        ['文档转换', 'mammoth（DOCX）、markdownify（HTML）、ebooklib（EPUB）'],
        ['网页抓取', 'requests / curl_cffi（支持微信公众号等 TLS 指纹限制站点）'],
        ['图片生成', '12+ AI 后端：Gemini / OpenAI / SiliconFlow / 智谱 / Minimax 等'],
        ['图标库', '6700+ 内置矢量图标（Tabler Icons 三套风格）'],
        ['图表模板', '50+ 可视化图表 SVG 模板（柱状图、饼图、雷达图、桑基图等）'],
    ]
)

# ═══════════════════════════════════════════
# 三、核心工作流程
# ═══════════════════════════════════════════
add_heading_styled('三、核心工作流程', level=1)

# Step 1
add_heading_styled('Step 1：源内容处理', level=2)
add_para('将用户提供的源文档自动转换为 Markdown 格式：')
add_table(
    ['输入类型', '工具', '输出'],
    [
        ['PDF 文件', 'pdf_to_md.py（PyMuPDF）', 'Markdown + 图片提取'],
        ['DOCX / Word', 'doc_to_md.py（mammoth）', 'Markdown'],
        ['PPTX', 'ppt_to_md.py', 'Markdown'],
        ['网页链接', 'web_to_md.py（curl_cffi）', 'Markdown'],
        ['EPUB / HTML', 'doc_to_md.py', 'Markdown'],
    ]
)

# Step 2
add_heading_styled('Step 2：项目初始化与源文件导入', level=2)
add_para('自动创建项目目录结构，并导入源文件：')
add_para('项目目录结构：', bold=True)
add_para(
    'my_project_ppt169_20250418/\n'
    '├── sources/          ← 源文件 & 转换后的 Markdown（自动导入）\n'
    '├── svg_output/       ← 执行器生成的原始 SVG\n'
    '├── svg_final/        ← 后处理优化后的 SVG\n'
    '├── images/           ← 图片资源\n'
    '├── notes/            ← 演讲备注\n'
    '├── templates/        ← 选中模板文件\n'
    '├── exports/          ← 最终导出的 PPTX\n'
    '├── design_spec.md    ← 设计规范（人类可读）\n'
    '└── spec_lock.md      ← 执行锁定文件（机器可读）',
    size=Pt(9)
)

# Step 3
add_heading_styled('Step 3：模板选择', level=2)
add_para('内置 21 套专业模板，覆盖多种场景。AI 根据内容主题提供专业推荐。')
add_para('推荐策略：默认倾向自由设计（AI 根据内容定制），仅在内容明显适合固定结构（如咨询报告、年报）时推荐模板。')

add_table(
    ['类别', '模板示例', '适用场景'],
    [
        ['品牌风格', 'McKinsey、Google Style、Anthropic、中国电信、招商银行', '企业级专业演示'],
        ['通用风格', 'Exhibit、科技蓝商务、Smart Red', '日常商务汇报'],
        ['学术场景', '学术答辩、重庆大学、医学院', '论文答辩、学术报告'],
        ['政府风格', '政府红、政府蓝、AI Ops', '政务汇报、党建'],
        ['创意风格', 'Pixel Retro', '技术分享、创意展示'],
    ]
)

# Step 4
add_heading_styled('Step 4：策略师阶段（八项确认）', level=2)
add_para('这是系统的核心决策环节。AI 策略师与用户进行八项确认，确保设计方向完全符合需求后，方可继续执行。这是两个阻塞点之一，必须等待用户明确确认。')

add_table(
    ['#', '确认项', '说明'],
    [
        ['1', '画布格式', '16:9 / 4:3 / 小红书 / 朋友圈 / Story'],
        ['2', '页数范围', '建议页数区间'],
        ['3', '目标受众', '谁来看这个 PPT'],
        ['4', '风格目标', '专业 / 科技 / 温暖 / 权威 等'],
        ['5', '配色方案', '主色 / 辅色 / 背景色系统'],
        ['6', '图标使用', '图标风格与密度'],
        ['7', '字体排版', '中英文字体搭配与字号层级'],
        ['8', '图片使用', 'AI 生成 / 现有图片 / 占位符'],
    ]
)

add_para('确认后自动生成两份核心文件：')
add_para('• design_spec.md — 人类可读的设计叙事文档（11 个章节：项目信息、画布规格、视觉主题、字体系统、布局原则、图标规范、可视化引用、图片资源、内容大纲、演讲备注要求、技术约束）')
add_para('• spec_lock.md — 机器可读的执行锁定文件（执行器在生成每个 SVG 页面之前都要重新读取，以防止长文上下文压缩导致的风格漂移）')

# Step 5
add_heading_styled('Step 5：图片生成（可选）', level=2)
add_para('如果设计规范中的图片方案包含"AI 生成"，则进入此阶段。支持 12+ AI 图片生成后端，根据设计规范生成配图。')

# Step 6
add_heading_styled('Step 6：执行器阶段（SVG 生成）', level=2)
add_para('这是技术含量最高的环节：')
add_para('1. 设计参数确认 — 生成首个 SVG 前审查画布尺寸、配色、字体等全局参数', size=Pt(10))
add_para('2. 每页重读锁定文件 — 生成每个 SVG 前重新读取 spec_lock.md，确保颜色/字体/图标来源一致，抵抗长文上下文压缩漂移', size=Pt(10))
add_para('3. 逐页连续生成 — 确认全局参数后，逐页连续生成所有 SVG，禁止分批或并行', size=Pt(10))
add_para('4. 生成演讲备注 — 为每页编写演讲备注，保存到 notes/total.md', size=Pt(10))

add_para('关键技术约束（确保 PPTX 兼容性）：', bold=True)
add_table(
    ['规则', '说明'],
    [
        ['禁止使用', 'mask、&lt;style&gt;、class、foreignObject、textPath、rgba()、&lt;g opacity&gt;'],
        ['推荐使用', 'fill-opacity、stroke-opacity、内联样式、&lt;tspan&gt; 文本换行'],
        ['条件允许', 'clipPath（仅用于图片裁剪）、marker（箭头，需符合特定约束）'],
    ]
)

# Step 7
add_heading_styled('Step 7：后处理与导出', level=2)
add_para('三个子步骤必须严格串行执行，每个命令完成后确认成功再执行下一个：')

add_table(
    ['步骤', '工具', '功能', '说明'],
    [
        ['7.1', 'total_md_split.py', '拆分演讲备注到各页面', '将 total.md 按页面拆分为独立备注文件'],
        ['7.2', 'finalize_svg.py', 'SVG 后处理', '图标嵌入、图片裁剪嵌入、文本展平、圆角矩形转路径等多个关键处理'],
        ['7.3', 'svg_to_pptx.py', '导出 PPTX', '最终生成原生 DrawingML 格式 PPTX（⚠️ 必须通过工具调用执行）'],
    ]
)

add_para('导出产物：')
add_para('• <项目名>_<时间戳>.pptx — 原生 DrawingML 形状（可在 PowerPoint 中自由编辑）', size=Pt(10))
add_para('• <项目名>_<时间戳>_svg.pptx — SVG 引用版本', size=Pt(10))

# ═══════════════════════════════════════════
# 四、核心设计原则
# ═══════════════════════════════════════════
add_heading_styled('四、核心设计原则', level=1)

add_heading_styled('4.1 严格串行执行', level=2)
add_para('每一步骤的输入是上一步的输出，禁止跨步骤批处理、并行执行或提前准备后续步骤内容。两个阻塞点（模板选择、八项确认）必须等待用户明确确认。')

add_heading_styled('4.2 跨页一致性保障', level=2)
add_para('spec_lock.md 机制：执行器在生成每个 SVG 页面之前都重新读取该文件，所有颜色、字体、图标、图片来源必须来自锁定文件，有效防止长文档生成过程中的风格漂移。')

add_heading_styled('4.3 最终导出必须调用工具', level=2)
add_para('最后一步 PPTX 导出（svg_to_pptx.py）必须通过 Tool Call 方式执行，不能手动在终端运行。导出完成后通过工具返回生成的 PPTX 文件路径和结果信息。')

# ═══════════════════════════════════════════
# 五、模板与可视化资源
# ═══════════════════════════════════════════
add_heading_styled('五、模板与可视化资源', level=1)

add_table(
    ['资源类型', '路径', '数量', '说明'],
    [
        ['布局模板', 'templates/layouts/', '21 套', '品牌/通用/学术/政府/创意五类'],
        ['图表模板', 'templates/charts/', '50+', '柱状图、饼图、雷达图、桑基图、甘特图等'],
        ['图标库', 'templates/icons/', '6700+', 'Tabler Icons（chunk/filled/outline 三套风格）'],
    ]
)

# ═══════════════════════════════════════════
# 六、系统依赖
# ═══════════════════════════════════════════
add_heading_styled('六、系统依赖', level=1)
add_para('核心功能（项目管理、文件操作等）仅依赖 Python 标准库，无需安装任何额外包即可运行。以下为可选依赖：')

add_table(
    ['功能组', '依赖包', '使用阶段'],
    [
        ['PPTX 导出', 'python-pptx >= 0.6.21、svglib >= 1.5.0、reportlab >= 4.0.0', '后处理 Step 7.3'],
        ['PDF 转 Markdown', 'PyMuPDF >= 1.23.0', '源内容处理 Step 1'],
        ['DOCX/HTML/EPUB 转换', 'mammoth >= 1.6.0、markdownify >= 0.11.6、ebooklib >= 0.18', '源内容处理 Step 1'],
        ['网页抓取', 'requests >= 2.31.0、beautifulsoup4 >= 4.12.0、curl_cffi >= 0.7.0', '源内容处理 Step 1'],
        ['图片处理', 'Pillow >= 9.0.0、numpy >= 1.20.0', '图片分析/水印去除'],
        ['AI 图片生成', 'google-genai >= 1.0.0、openai >= 1.0.0', '图片生成 Step 5'],
    ]
)

# ═══════════════════════════════════════════
# 七、应用场景
# ═══════════════════════════════════════════
add_heading_styled('七、应用场景', level=1)

add_table(
    ['场景', '典型用途'],
    [
        ['学术答辩', '论文答辩 PPT、科研汇报、学术会议演示'],
        ['企业汇报', '季度报告、项目方案、战略汇报、年度总结'],
        ['数据分析', '数据看板、趋势分析、对比报告、可视化呈现'],
        ['教学课件', '课程讲义、培训材料、教学演示'],
        ['政务汇报', '政府工作报告、党建汇报、城市治理'],
        ['营销方案', '产品发布会、方案提案、商业计划书'],
    ]
)

# ═══════════════════════════════════════════
# 八、与同类方案对比
# ═══════════════════════════════════════════
add_heading_styled('八、与同类方案对比', level=1)

add_table(
    ['对比维度', 'PPT Master', '传统 PPT 工具', '在线 PPT 生成'],
    [
        ['输出格式', '原生 PPTX（可编辑 DrawingML）', '原生 PPTX', '网页 / PDF / 图片'],
        ['设计质量', 'AI 多角色深度协作', '人工设计（依赖个人能力）', '模板填充（样式固定）'],
        ['定制程度', '八项确认 + 自由设计', '完全自由（需设计能力）', '固定模板选项'],
        ['内容理解', 'AI 深度理解源文档内容', '人工复制粘贴', '简单关键词提取'],
        ['画布格式', '支持多种格式（16:9/4:3/小红书等）', '固定画布', '固定画布'],
        ['图标图表', '内置 6700+ 图标 + 50+ 图表模板', '需手动插入', '有限模板'],
        ['技术门槛', '零门槛', '需设计/排版能力', '零门槛'],
    ]
)

# ═══════════════════════════════════════════
# 九、快速开始
# ═══════════════════════════════════════════
add_heading_styled('九、快速开始', level=1)

add_para('以下为在 Docker 环境中的完整使用流程：')
add_para(
    '# 1. 设置环境变量\n'
    'SKILL_DIR=/mnt/skills/public/ppt-master/skills/ppt-master\n\n'
    '# 2. 安装依赖（可选，按需安装）\n'
    'pip install -r /mnt/skills/public/ppt-master/requirements.txt\n\n'
    '# 3. 创建项目\n'
    'python3 ${SKILL_DIR}/scripts/project_manager.py init my_ppt --format ppt169 --dir /mnt/user-data/projects\n\n'
    '# 4. 项目创建后，AI 自动发现并导入上传的源文件\n'
    '#    （自动执行 import-sources <project_path> /mnt/user-data/uploads/* --move）\n\n'
    '# 5. 后续流程由 AI 自动完成：模板选择 → 八项确认 → SVG 生成 → 后处理 → 导出 PPTX\n'
    '#    最终导出时通过 Tool Call 调用 svg_to_pptx.py 完成',
    size=Pt(9)
)

# ═══════════════════════════════════════════
# 页脚
# ═══════════════════════════════════════════
doc.add_paragraph()
footer = doc.add_paragraph()
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer.add_run('— 本文档由 deer-flow 2.0 ppt-master skill 自动生成 —')
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
run.font.name = 'Microsoft YaHei'
run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

# ── 保存 ──
output_path = '/home/student2/deer-flow-2.0-m1/skills/public/ppt-master/PPT-Master-功能介绍.docx'
doc.save(output_path)
print(f'Document saved to: {output_path}')

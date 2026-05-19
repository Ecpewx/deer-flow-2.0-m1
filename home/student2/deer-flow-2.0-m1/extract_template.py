#!/usr/bin/env python3
"""Extract structure of the template docx"""
import zipfile
import xml.etree.ElementTree as ET

docx_path = '/home/student2/deer-flow-2.0-m1/skills/old/mentor-recommendation-report.docx'

zf = zipfile.ZipFile(docx_path)
tree = ET.parse(zf.open('word/document.xml'))
root = tree.getroot()
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

output = []
output.append("=== DOCUMENT STRUCTURE ===\n")

for i, para in enumerate(root.findall('.//w:p', ns)):
    texts = []
    for t in para.findall('.//w:t', ns):
        if t.text:
            texts.append(t.text)
    full_text = ''.join(texts)
    if full_text.strip():
        # Style
        style_el = para.find('.//w:pStyle', ns)
        style_name = style_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if style_el is not None else 'Normal'
        # Bold check
        bolds = para.findall('.//w:b', ns)
        is_bold = len(bolds) > 0
        # Font size
        sz_els = para.findall('.//w:sz', ns)
        sz = sz_els[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if sz_els else None
        
        prefix = ""
        if is_bold:
            prefix = "[BOLD] "
        if sz:
            prefix += f"[{sz}pt] "
        output.append(f'P{i}: style={style_name} | {prefix}{full_text[:300]}')

output.append("\n=== TABLES ===\n")
for ti, tbl in enumerate(root.findall('.//w:tbl', ns)):
    rows = tbl.findall('.//w:tr', ns)
    output.append(f'Table {ti}: {len(rows)} rows')
    for ri, row in enumerate(rows):
        cells = row.findall('.//w:tc', ns)
        for ci, cell in enumerate(cells):
            texts = []
            for t in cell.findall('.//w:t', ns):
                if t.text:
                    texts.append(t.text)
            txt = ''.join(texts)
            if txt.strip():
                output.append(f'  [{ri},{ci}] {txt[:200]}')

with open('/home/student2/deer-flow-2.0-m1/template_structure.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

zf.close()
print("Done - wrote to template_structure.txt")

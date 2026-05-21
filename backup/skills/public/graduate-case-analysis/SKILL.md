---
name: graduate-case-analysis
description: 当教师需要生成研究生/博士层次案例分析题与详细参考答案时使用；默认课堂作业场景，输出为三段式（案例材料、问题、参考答案）。
---

# 研究生案例分析技能（优化版）

## 1. 适用范围
本技能用于生成高校研究生/博士层次案例分析题，默认用于课堂作业。  
默认输出聚焦三部分（主体）：
- `【案例材料】`
- `【问题】`（默认4题，含分值）
- `【参考答案】`（逐题详细、含分值拆解）

若正文引用了检索或上传文件中的可核验内容，须在全文末尾**额外**增加一节 `【参考文献】`（仅此一节为扩展；无引用时可省略）。

不用于以下任务：
- 学生答案批改/评分（应路由 `student-case-questions-grading`）
- 客观题出题（选择/判断）
- 论文评审（应路由 `academic-paper-review`）

## 2. 触发规则（路由意图）
满足“案例关键词 + 生成意图”时优先触发本技能：
- 案例关键词：`案例`、`案例分析`、`案例题`、`课堂案例`、`案例作业`、`综合案例`
- 生成意图词：`生成`、`出题`、`设计`、`编写`、`拟题`、`重写`
- 排除词：`批改`、`评分`、`打分`、`评阅`、`判卷`

## 3. 输入策略（先生成后追问）
不强制用户逐项填写字段。用户只给主题时也必须先产出可用初稿。

可选输入字段（缺失可自动补全）：

```yaml
discipline: string | null
course_topic: string | null
graduate_level: master-year-1 | master-year-2 | phd-coursework | mixed-graduate   # default phd-coursework
difficulty: advanced | challenge   # default challenge
learning_objectives: string[] | null
case_source: string | null
answer_length: medium | long   # default long
course_type: assignment | seminar | exam   # default assignment
knowledge_point: string | null
grade: string | null
RAG_template: string | object | null
teacher_background: string | null
conversation_history: string | null
constraints: string[] | null
```

追问规则：
- 仅在“关键缺口严重影响可用性”时，允许追加 **1个可选优化问题**
- 不允许因信息不足拒绝生成
- 不允许多轮连环追问

## 4. 上传资料与目录使用规则

### 4.0 资料读取优先级（强制）
按顺序使用事实来源：**上一条已足够支撑生成时，不得跳过更高优先级去用更低优先级**；仅当更高优先级无命中或明显不足时，才进入下一级。

1) **用户上传文件（最高）**  
   - 路径：`/mnt/user-data/uploads`（或当前会话映射的上传目录；与 thread 隔离目录等价时以实际可访问路径为准）。  
   - 触发：用户声明已上传、或该目录下存在与本轮主题相关的文件。  
   - 必须先读取/检索上传内容；不得在未检查上传的情况下直接用技能包内知识库覆盖用户材料。

2) **技能包内 Markdown**  
   - 路径：`/mnt/skills/public/graduate-case-analysis/case-kb/*.md`  
   - 用途：直接 `read_file` 读取相关 `.md`。

3) **技能包内 PDF / DOC / DOCX**  
   - 路径：`/mnt/skills/public/graduate-case-analysis/case-kb/` 下 `.pdf`、`.doc`、`.docx`  
   - 用途：仅在前两级仍不足时使用；须经项目既有文档转换链或等价工具解析为可用文本后再引用。

4) **技能包内全文索引库（最后）**  
   - 路径：`/mnt/skills/public/graduate-case-analysis/case-kb/index.sqlite`  
   - 用途：段落级检索召回；**禁止**用 `read_file` 打开该文件。

**本地开发等价路径**（仓库内、非 `/mnt/skills` 挂载时）：将上文 `/mnt/skills/public/graduate-case-analysis/case-kb` 替换为  
`/T20050026/deer-flow/skills/public/graduate-case-analysis/case-kb`（含其中 `index.sqlite` 与 md/pdf）。

默认提示语（可按场景改写）：  
`请先使用我上传的资料；若无或未命中，再检索技能包内 case-kb 索引与 md/pdf。`

若上传资料不足以支撑具体数据，在答案中明确标注：  
`请教师根据实际教学补充具体数据`

- 关于“目录是否为空/是否命中”的判断，必须基于真实读取或检索结果，不得凭推断描述。
- 若已检索到相关文件，正文中须用 `[1]`、`[2]` … 角标标出引用处，并在文末 `【参考文献】` 中列出对应条目（见第 5 节引用规范）。

### 4.1 `index.sqlite` 读取方式（禁止误用 read_file）
- `index.sqlite` 为二进制 SQLite 库，**禁止**用 `read_file`、按行文本等方式打开。
- **优先**：在项目根执行（`--db` 与当前环境一致即可）：
  - 容器技能挂载：`python scripts/case_kb.py search --db "/mnt/skills/public/graduate-case-analysis/case-kb/index.sqlite" --query "你的检索词" --top-k 5`
  - 仓库内副本：`--db "/T20050026/deer-flow/skills/public/graduate-case-analysis/case-kb/index.sqlite"`
  - 权威主库（与 `ingest/index` 流水线一致时）：`--db "/T20050026/deer-flow/data/case-kb/index.sqlite"`
- **备选**：`sqlite3 "<db路径>" "..."` 或 `python -c 'import sqlite3; ...'` 查询 `documents` / `chunks` / `chunks_fts`。

### 4.2 知识库检索执行顺序（强制）
1. 若有上传：先读完/检索上传，再进入技能包 `case-kb`；  
2. 再对 `index.sqlite` 做检索（先检索后生成）；  
3. 必要时再读 `case-kb` 下 `.md`；  
4. 仍不足再处理 `case-kb` 下 `.pdf` / `.doc` / `.docx`；  
5. 若声明“基于知识库/资料”，必须在正文中给出 `[1]`、`[2]` … 角标，并在文末 `【参考文献】` 列出对应文件名。

执行前证据检查（二选一成功即可，禁止先整目录枚举）：  
`ls -l /mnt/skills/public/graduate-case-analysis/case-kb/index.sqlite`  
或（本地仓库）：`ls -l /T20050026/deer-flow/skills/public/graduate-case-analysis/case-kb/index.sqlite`  
若对应命令成功，不得再说“权限被拒绝”；应直接基于该 `index.sqlite` 检索并返回命中的 `source_name` 与前 3 条片段。

### 4.3 无新上传时的更新规则
- 若没有新增上传文件，仅需刷新索引，不必执行 ingest：
  - `python scripts/case_kb.py index --source "/T20050026/deer-flow/data/case-kb" --db "/T20050026/deer-flow/data/case-kb/index.sqlite"`
- 若需与技能包内副本一致，索引更新后可同步复制到：  
  `/T20050026/deer-flow/skills/public/graduate-case-analysis/case-kb/`（或部署流程中同步到 `/mnt/skills/.../case-kb/`）。

### 4.4 检索失败降级策略
- 若 `/mnt/skills/.../case-kb/index.sqlite` 不可访问，依次尝试：
  1) 仓库内同路径：`/T20050026/deer-flow/skills/public/graduate-case-analysis/case-kb/index.sqlite`
  2) 主库：`/T20050026/deer-flow/data/case-kb/index.sqlite`
  3) 镜像：`/mnt/user-data/uploads/index.sqlite`
- 若仍失败，明确说明“本轮未命中知识库资料”，再生成“低证据草稿版”；低证据草稿版必须提示教师复核，不得伪造来源。
- 当目录访问受限但某一路径的 `index.sqlite` 可读时，不要求先列目录；可直接基于可读库检索。
- 若出现“Permission denied/权限被拒绝”，不得直接判定“目录不存在”或“无资料”；应判定为环境权限受限并换用上述降级路径之一，且在输出中简短说明所用路径。

## 5. 事实与质量约束
- 以 RAG/上传资料为主要事实依据，不杜撰可核验事实
- 保留知识骨架，去除噪声细节（信息瓶颈原则）
- 案例必须有清晰因果链：`冲突/压力 -> 创新实践 -> 定量评价 -> 教学启示`
- 至少一题要求 3 个以上视角分析
- 融入 1-2 处课程思政元素（自然、不过度）
- **引用与角标（强制）**：凡引用上传资料、检索命中片段或 `case-kb` 内文件中的可核验表述，须在对应句末使用 **编号角标** `[1]`、`[2]` …（全篇连续编号、不跳号、不重复占用同一编号指代不同文件）。
  - 角标写法二选一、全篇一致：  
    - 紧接句末：`……结论成立[1]。`  
    - 或 HTML 上标：`……结论成立<sup>[1]</sup>。`
  - 文末必须增加一节 `【参考文献】`，与正文角标一一对应，每行一条，格式示例：  
    `[1]27-驭风而行，智领未来：运达股份的“数智+绿色”服务化之路.md`  
    （即：`[` + 编号 + `]` + 完整 `source_name` 或实际文件名，含扩展名；上传文件写原始文件名即可。）
  - `【参考文献】` 仅列本轮正文中实际出现过的编号；不得虚构未引用文献。

## 6. 输出协议（最高优先级）
以下规则高于其他所有说明：

1. 最终输出必须包含三个一级标题（顺序固定）：
   - `【案例材料】`
   - `【问题】`
   - `【参考答案】`
2. 当且仅当正文出现 `[1]`、`[2]` … 等文献角标时，在 `【参考答案】` **之后** 增加第四个一级标题 `【参考文献】`；无角标时不得单独输出该节。
3. 禁止输出其他附加章节（除非用户明确要求）：
   - 教学说明、评分标准、案例编号、附录、备注等
4. 禁止输出思考过程、检索过程、计划草稿
5. `【问题】` 必须格式化：
   - 默认4题，序号 `(1)(2)(3)(4)`
   - 每题单独成行，题间空一行
   - 每题末尾有分值（建议 8/8/7/7）
6. `【参考答案】` 必须逐题对应，含分值拆解与评分要点
7. 若标注“基于知识库/资料”生成，正文中须含 `[1]`… 角标且文末有 `【参考文献】`；若无命中，必须显式声明“未命中知识库资料”（此时不输出 `【参考文献】`）。

## 7. 课程类型预设
- `assignment`（默认）：课堂作业导向，强调可执行与可评分
- `seminar`：强化课堂追问、辩论与反思
- `exam`：强化区分度与结构严谨性

## 8. 标准模板（示意）
```text
【案例材料】
[研究生/博士层次案例叙述，建议 1500-2200 字]

【问题】
(1) ...（8分）

(2) ...（8分）

(3) ...（7分）

(4) ...（7分）

【参考答案】
(1) [结论 + 推理链 + 评分要点分值]

(2) [结论 + 推理链 + 评分要点分值]

(3) [结论 + 推理链 + 评分要点分值]

(4) [结论 + 推理链 + 定量方法 + 分层方案 + 评分要点分值]

【参考文献】
（仅在有引用时输出；与正文角标对应）
[1]27-驭风而行，智领未来：运达股份的“数智+绿色”服务化之路.md
[2]…（如有）
```

## 9. 重生成模式
- `rewrite-question`：仅重写问题
- `rewrite-answer`：仅重写参考答案
- `rewrite-all`：整体重写

默认保持主题一致，除非用户明确要求改题。

## 10. 最终自检清单
- [ ] 三段式输出是否严格满足
- [ ] 研究生/博士难度是否达标
- [ ] 四题是否高阶且格式合规（换行、空行、分值）
- [ ] 答案是否逐题对应并可评分
- [ ] 是否使用上传资料/RAG信息（若用户要求）
- [ ] 若使用了上传资料/RAG信息，是否已在句末使用 `[1]`… 角标，并在文末列出 `【参考文献】` 且与角标一一对应
- [ ] 是否避免了思考过程外显

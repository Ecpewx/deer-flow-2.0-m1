# PPT Master Integration into DeerFlow

> 将 [ppt-master](https://github.com/your-repo/ppt-master) 集成到 DeerFlow 框架中，使其能够通过 AI 对话生成可编辑的 PPTX 演示文稿。

---

## 目录

1. [背景与动机](#1-背景与动机)
2. [架构设计](#2-架构设计)
3. [集成方案对比](#3-集成方案对比)
4. [最终方案：社区工具 + Volume 挂载](#4-最终方案社区工具--volume-挂载)
5. [文件变更清单](#5-文件变更清单)
6. [详细实现说明](#6-详细实现说明)
7. [配置步骤](#7-配置步骤)
8. [使用方式](#8-使用方式)
9. [故障排查](#9-故障排查)
10. [附录：备选方案](#10-附录备选方案)

---

## 1. 背景与动机

### 1.1 问题

DeerFlow 框架内置了 `pptx` 技能（位于 `skills/public/pptx/`），但存在以下问题：

- **调用内置 skills 报错**：原生 DeerFlow 框架调用内置 skills 时会出现错误，原因可能包括路径解析、依赖缺失或技能加载机制的问题
- **功能受限**：内置的 pptx 技能功能较为基础，只能生成简单的幻灯片

### 1.2 为什么选择 ppt-master

[ppt-master](https://github.com/topics/ppt-master) 是一个功能强大的 AI 驱动 PPT 生成系统，具有以下特点：

- **多格式输入**：支持 PDF/DOCX/PPTX/URL/Markdown 等多种源文件
- **AI 驱动的设计**：自动分析内容，生成设计规范
- **高质量输出**：生成可编辑的 PPTX 文件，支持自定义模板
- **完整流水线**：源文件处理 → 项目初始化 → 策略设计 → SVG 生成 → 后处理 → 导出

### 1.3 集成目标

- 将 ppt-master 的核心功能以 **社区工具（Community Tool）** 的形式注册到 DeerFlow
- AI 可以通过对话直接调用这些工具，无需手动编写代码
- 支持 Docker 部署环境
- 保持 ppt-master 的独立性，便于后续更新

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────┐
│                   DeerFlow                       │
│  ┌───────────────────────────────────────────┐  │
│  │            AI Agent (LLM)                  │  │
│  └──────────────┬────────────────────────────┘  │
│                 │ 调用工具                        │
│                 ▼                                │
│  ┌───────────────────────────────────────────┐  │
│  │         Tool Registry (config.yaml)        │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │ ppt_create_presentation              │  │  │
│  │  │ ppt_convert_to_markdown              │  │  │
│  │  │ ppt_analyze_presentation             │  │  │
│  │  └──────────────┬──────────────────────┘  │  │
│  └─────────────────┼─────────────────────────┘  │
│                    │                              │
│                    ▼                              │
│  ┌───────────────────────────────────────────┐  │
│  │  deerflow.community.ppt_master.tools       │  │
│  │  (Python subprocess → ppt-master scripts)  │  │
│  └──────────────────┬────────────────────────┘  │
└─────────────────────┼───────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│           ppt-master (独立项目)             │
│  ┌─────────┬──────────┬───────────────┐  │
│  │ scripts │ templates │ references    │  │
│  │         │           │               │  │
│  │ pdf_to_md│ layout   │ strategist.md │  │
│  │ project  │ charts   │ executor.md   │  │
│  │ svg_to   │ icons    │ image_gen.md  │  │
│  │ _pptx    │          │               │  │
│  └─────────┴──────────┴───────────────┘  │
└───────────────────────────────────────────┘
```

### 2.2 为什么不使用 MCP（Model Context Protocol）

我们最初设计了 **方案B（MCP 服务器）**，但最终选择了社区工具方式，原因如下：

| 对比维度 | MCP 服务器 | 社区工具（方案A） |
|----------|-----------|------------------|
| **进程数** | 额外进程 | 同一进程 |
| **通信开销** | stdio/HTTP 通信 | 直接 Python 调用 |
| **Docker 兼容性** | 需额外配置网络 | Volume 挂载即可 |
| **调试难度** | 需排查 MCP 协议问题 | 直接 Python 调试 |
| **依赖管理** | 独立环境 | 共享 DeerFlow 环境 |
| **可靠性** | 依赖 MCP 协议稳定性 | 直接 subprocess 调用 |

**关键决策点**：在 Docker 环境下，MCP 服务器需要额外处理 conda 环境路径、容器网络等问题，而社区工具方式只需 volume 挂载 + pip install 即可。

---

## 3. 集成方案对比

### 3.1 方案A：社区工具 + Volume 挂载（✅ 最终选择）

**原理**：将 ppt-master 包装为 DeerFlow 的社区工具（`deerflow.community.ppt_master.tools`），通过 subprocess 调用 ppt-master 的 Python 脚本。

**优点**：
- 无需额外进程
- 配置简单（仅需添加 volume 和修改 config.yaml）
- 不修改 Docker 镜像
- 易于调试

**缺点**：
- 启动时需安装依赖（约 10 秒）
- 依赖通过 volume 挂载

### 3.2 方案B：MCP 服务器（备选）

**原理**：将 ppt-master 包装为 MCP 服务器，DeerFlow 通过 MCP 协议调用。

**优点**：
- 标准化协议
- 独立进程，隔离性好

**缺点**：
- Docker 环境下配置复杂
- 需额外维护 MCP 服务进程
- 增加通信延迟

### 3.3 方案C：构建到 Docker 镜像

**原理**：修改 Dockerfile，在构建镜像时安装 ppt-master 及其依赖。

**优点**：
- 一劳永逸
- 无需启动时安装依赖

**缺点**：
- 每次修改 ppt-master 需重建镜像
- 构建时间长

---

## 4. 最终方案：社区工具 + Volume 挂载

### 4.1 核心实现

```
backend/packages/harness/deerflow/community/ppt_master/
├── __init__.py       # 模块初始化 + 智能路径查找
├── tools.py          # 6 个社区工具函数
├── mcp_server.py     # MCP 服务器（已禁用，备选）
└── README.md         # 集成说明文档
```

### 4.2 路径查找策略

为了解决 Docker 容器内 `__file__` 指向虚拟环境路径（site-packages）而非源文件路径的问题，实现了多级路径查找：

```python
def _find_ppt_master_root() -> Path | None:
    # 1. 环境变量 DEER_FLOW_PPT_MASTER_ROOT（最高优先级）
    # 2. 相对 __file__ 的源码目录路径
    # 3. Docker 固定路径 /app/backend/packages/harness/ppt-master
    # 4. 相对 $PWD 的项目路径
    # 5. 其他常见位置
```

### 4.3 依赖安装策略

在 `docker-compose.yaml` 的 `command` 中，启动前自动安装 ppt-master 所需的 Python 包：

```
pip install --quiet python-pptx PyMuPDF svglib reportlab mammoth ebooklib nbconvert curl_cffi mcp
```

这些包包括：
| 包名 | 用途 | 来源 |
|------|------|------|
| `python-pptx` | PPTX 文件生成 | ppt-master 核心依赖 |
| `PyMuPDF` | PDF 转 Markdown | ppt-master 脚本 |
| `svglib` + `reportlab` | SVG 转 PNG（Office 兼容） | ppt-master 导出 |
| `mammoth` | DOCX 转 Markdown | ppt-master 脚本 |
| `ebooklib` | EPUB 解析 | ppt-master 脚本 |
| `nbconvert` | Jupyter Notebook 解析 | ppt-master 脚本 |
| `curl_cffi` | 网页抓取（微信等 TLS 网站） | ppt-master 脚本 |
| `mcp` | MCP 协议支持（备选） | 可选 |

> **注意**：`markdownify`、`Pillow`、`numpy`、`requests`、`beautifulsoup4`、`openai`、`google-genai` 等包已在 DeerFlow 的 `pyproject.toml` 中存在，无需重复安装。

---

## 5. 文件变更清单

### 5.1 新建文件（4 个）

| 文件 | 行数 | 说明 |
|------|------|------|
| `backend/packages/harness/deerflow/community/ppt_master/__init__.py` | ~45 | 模块初始化，智能路径查找 |
| `backend/packages/harness/deerflow/community/ppt_master/tools.py` | ~180 | 6 个社区工具函数 |
| `backend/packages/harness/deerflow/community/ppt_master/mcp_server.py` | ~250 | MCP 服务器（已禁用） |
| `backend/packages/harness/deerflow/community/ppt_master/README.md` | ~120 | 集成说明文档 |

### 5.2 修改文件（2 个）

| 文件 | 变更内容 |
|------|----------|
| `docker/docker-compose.yaml` | gateway + langgraph 容器：添加 volume 挂载 + 修改 command 安装依赖 |
| `extensions_config.json` | ppt-master MCP 服务器 → `enabled: false`（改用社区工具） |

### 5.3 需要用户手动修改（1 个）

| 文件 | 原因 |
|------|------|
| `config.yaml` | 受 DeerFlow 保护，无法自动编辑，需手动添加工具配置 |

---

## 6. 详细实现说明

### 6.1 `__init__.py` — 智能路径查找

```python
def _find_ppt_master_root() -> Path | None:
    """
    按优先级查找 ppt-master 根目录：
    
    1. 环境变量 DEER_FLOW_PPT_MASTER_ROOT
       - 可用于手动指定路径
       - 适用于自定义部署场景
    
    2. 相对 __file__ 的源码路径
       - 开发环境：__file__ 指向源文件
       - PPT_MASTER_ROOT = .../harness/ppt-master
    
    3. Docker 固定路径 /app/backend/packages/harness/ppt-master
       - 生产环境：__file__ 指向 site-packages
       - 需要通过 volume 挂载或镜像构建提供
    
    4. 相对 $PWD 的路径
       - 当从项目根目录运行时的回退方案
    
    5. 其他常见位置
       - 作为最后的回退
    """
```

### 6.2 `tools.py` — 工具函数

提供了 6 个工具函数，每个函数都是一个 LangChain `@tool`：

```python
@tool("ppt_create_presentation", parse_docstring=True)
def ppt_create_presentation_tool(source_file, project_name, format="ppt169", template=None):
    """从源文件创建 PPTX 演示文稿"""
    # 1. project_manager.py init 初始化项目
    # 2. project_manager.py import-sources 导入源文件
    # 3. 返回项目信息和下一步指引

@tool("ppt_convert_to_markdown", parse_docstring=True)
def ppt_convert_to_markdown_tool(source_file, output_file=None):
    """将文档转换为 Markdown"""
    # 根据文件后缀自动选择转换脚本

@tool("ppt_analyze_presentation", parse_docstring=True)
def ppt_analyze_presentation_tool(pptx_file):
    """分析 PPTX 文件内容"""
    # 使用 markitdown 提取文本内容

@tool("ppt_generate_images", parse_docstring=True)
def ppt_generate_images_tool(prompt, aspect_ratio="16:9", ...):
    """使用 AI 生成图片"""
    # 调用 image_gen.py

@tool("ppt_validate_project", parse_docstring=True)
def ppt_validate_project_tool(project_path):
    """验证项目结构"""

@tool("ppt_get_project_info", parse_docstring=True)
def ppt_get_project_info_tool(project_path):
    """获取项目信息"""
```

所有工具通过 `_run_ppt_master_script()` 统一调用 ppt-master 的 Python 脚本：

```python
def _run_ppt_master_script(script_name, args, cwd=None):
    script_path = SKILLS_DIR / "scripts" / script_name
    cmd = [sys.executable, str(script_path)] + args
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout
```

### 6.3 Docker 集成要点

**为什么需要 volume 挂载？**

虽然 Docker 构建时已经通过 `COPY backend ./backend` 将整个 `backend/` 目录复制到镜像中，但 ppt-master 是一个独立项目，可能由用户单独更新。Volume 挂载可以：

1. **热更新**：修改 ppt-master 代码后无需重建镜像
2. **一致性**：确保容器内使用的 ppt-master 版本与宿主机一致
3. **减少镜像大小**：避免将大型模板文件打包到镜像中

**为什么在 command 中安装依赖？**

- 不改 Dockerfile，避免重建镜像
- 只在启动时安装一次，之后容器重启无需重复安装（因为 `pip install` 会缓存已安装的包）
- 便于调试：可以在 command 中临时调整依赖

**启动流程：**

```
容器启动
  │
  ├── pip install python-pptx PyMuPDF ... (首次约 10-15 秒)
  │
  ├── uv run uvicorn (启动 DeerFlow 服务)
  │
  └── AI 调用 ppt_create_presentation 工具
        │
        └── subprocess.run → python project_manager.py init ...
              │
              └── 生成项目目录 → SVG 幻灯片 → PPTX 导出
```

---

## 7. 配置步骤

### 7.1 前提条件

- DeerFlow 项目已正常运行（Docker 或本地）
- ppt-master 已存在于 `backend/packages/harness/ppt-master/`
- 已安装 Docker（如果是 Docker 部署）

### 7.2 安装依赖（宿主机，可选）

```bash
# 在宿主机上安装 ppt-master 依赖（用于本地测试）
conda activate /home/student2/envs/deer-flow/
cd backend/packages/harness/ppt-master
pip install -r requirements.txt
pip install mcp
```

### 7.3 Docker 部署配置

**步骤 1：确认 docker-compose.yaml 已更新**

检查 `docker/docker-compose.yaml` 中 gateway 和 langgraph 容器是否包含：

```yaml
# Volume 挂载
volumes:
  - ../backend/packages/harness/ppt-master:/app/backend/packages/harness/ppt-master:ro

# Command 依赖安装
command: sh -c "
  cd backend &&
  pip install --quiet python-pptx PyMuPDF ... &&
  PYTHONPATH=. uv run uvicorn ..."
```

**步骤 2：修改 config.yaml**

在 `config.yaml` 的 `tools` 部分添加：

```yaml
tools:
  - name: ppt_create_presentation
    group: file:write
    use: deerflow.community.ppt_master.tools:ppt_create_presentation_tool
  
  - name: ppt_convert_to_markdown
    group: file:read
    use: deerflow.community.ppt_master.tools:ppt_convert_to_markdown_tool
  
  - name: ppt_analyze_presentation
    group: file:read
    use: deerflow.community.ppt_master.tools:ppt_analyze_presentation_tool
```

**步骤 3：重启 Docker**

```bash
cd docker
docker compose down
docker compose up -d

# 查看日志确认依赖安装成功
docker compose logs gateway | grep "ppt-master"
# 应输出: ppt-master dependencies installed.
```

### 7.4 非 Docker 部署（本地开发）

如果 DeerFlow 直接在宿主机上运行（非 Docker），无需修改 `docker-compose.yaml`，只需：

1. 安装 ppt-master 依赖：
   ```bash
   cd backend/packages/harness/ppt-master
   pip install -r requirements.txt
   ```

2. 在 `config.yaml` 中添加工具配置（同上）

3. 设置环境变量（可选，如果路径自动查找失败）：
   ```bash
   export DEER_FLOW_PPT_MASTER_ROOT=/path/to/ppt-master
   ```

4. 重启 DeerFlow

---

## 8. 使用方式

### 8.1 AI 对话示例

集成后，用户可以通过自然语言与 AI 对话来生成 PPT：

**示例 1：转换文档**
```
用户：帮我把这份PDF转成Markdown
AI：好的，正在使用 ppt_convert_to_markdown 工具...
```

**示例 2：创建 PPT**
```
用户：根据这份文档帮我创建一个PPT
AI：正在使用 ppt_create_presentation 工具...
1. 初始化项目
2. 导入源文件
3. 分析内容生成设计规范
4. 创建 SVG 幻灯片
5. 导出为 PPTX
```

**示例 3：分析 PPT**
```
用户：帮我看看这个PPT里有什么内容
AI：正在使用 ppt_analyze_presentation 工具...
```

### 8.2 工具调用流程

```
用户请求 → AI 理解意图 → 选择工具 → 填充参数
                                            │
                                            ▼
                                  _run_ppt_master_script()
                                            │
                                            ▼
                                subprocess.run(script.py args)
                                            │
                                            ▼
                                  ppt-master 脚本执行
                                            │
                                            ▼
                                  返回结果 → AI 呈现给用户
```

### 8.3 生成的文件结构

每次调用 `ppt_create_presentation` 会在 `backend/packages/harness/ppt-master/projects/` 下生成一个项目目录：

```
projects/{project_name}_{format}_{YYYYMMDD}/
├── sources/          # 源文件（PDF/MD 等）
├── images/           # 图片资源
├── templates/        # 模板文件（如使用模板）
├── design_spec.md    # 设计规范
├── spec_lock.md      # 执行锁定文件
├── svg_output/       # 原始 SVG 幻灯片
├── svg_final/        # 最终 SVG（后处理后）
├── notes/            # 演讲者备注
└── exports/          # 最终 PPTX 文件
```

---

## 9. 故障排查

### 9.1 工具找不到

**症状**：AI 说 "I don't have a tool for that"

**原因**：工具未在 `config.yaml` 中注册

**解决**：检查 `config.yaml` 的 `tools` 部分是否包含 ppt 相关工具配置

### 9.2 ppt-master 路径找不到

**症状**：调用工具返回 `Error: ppt-master not found`

**原因**：`_find_ppt_master_root()` 未能找到 ppt-master 目录

**解决**：
```bash
# 方案1：设置环境变量
export DEER_FLOW_PPT_MASTER_ROOT=/app/backend/packages/harness/ppt-master

# 方案2：检查 volume 挂载
docker compose exec gateway ls /app/backend/packages/harness/ppt-master
```

### 9.3 依赖未安装

**症状**：调用工具返回 `ModuleNotFoundError` 或 `ImportError`

**原因**：ppt-master 依赖未安装

**解决**：
```bash
# Docker 环境
docker compose exec gateway pip install python-pptx PyMuPDF svglib reportlab mammoth ebooklib nbconvert curl_cffi

# 本地环境
cd backend/packages/harness/ppt-master
pip install -r requirements.txt
```

### 9.4 脚本执行失败

**症状**：返回 `Error: ...`

**原因**：ppt-master 脚本执行出错

**解决**：
```bash
# 直接运行脚本查看详细错误
docker compose exec gateway python /app/backend/packages/harness/ppt-master/skills/ppt-master/scripts/project_manager.py init test_project
```

### 9.5 性能问题

**症状**：容器启动慢

**原因**：每次启动都要 `pip install`

**解决**：修改 Dockerfile，将依赖安装到镜像中（方案C），或使用 Docker 缓存层。

---

## 10. 附录：备选方案

### 10.1 MCP 服务器方案

如果未来需要将 ppt-master 作为独立服务运行（例如提供给多个 DeerFlow 实例使用），可以启用 MCP 服务器：

```json
// extensions_config.json
"ppt-master": {
  "enabled": true,
  "type": "stdio",
  "command": "/home/student2/envs/deer-flow/bin/python",
  "args": ["-m", "deerflow.community.ppt_master.mcp_server"],
  "env": {
    "PYTHONPATH": "$PWD/backend/packages/harness:$PWD:$PYTHONPATH"
  }
}
```

### 10.2 构建到 Docker 镜像

修改 `backend/Dockerfile`，在构建时安装依赖：

```dockerfile
# 在 builder 阶段添加
RUN pip install python-pptx PyMuPDF svglib reportlab mammoth ebooklib nbconvert curl_cffi mcp

# 在 runtime 阶段同样添加
RUN pip install python-pptx PyMuPDF svglib reportlab mammoth ebooklib nbconvert curl_cffi mcp
```

### 10.3 HTTP MCP 服务器

在宿主机上运行 HTTP 模式的 MCP 服务器，容器通过网络连接：

```bash
# 宿主机
conda activate /home/student2/envs/deer-flow/
cd backend/packages/harness
python -c "
from deerflow.community.ppt_master.http_server import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8002)
"
```

```json
// extensions_config.json
"ppt-master": {
  "enabled": true,
  "type": "http",
  "url": "http://host.docker.internal:8002/sse"
}
```

---

## 修订历史

| 日期 | 版本 | 说明 | 作者 |
|------|------|------|------|
| 2024-01 | v1.0 | 初稿，方案B（MCP 服务器） | - |
| 2024-01 | v2.0 | 改为方案A（社区工具 + Volume 挂载） | - |

---

> **文档维护者**：DeerFlow Team
> **最后更新**：2024-01

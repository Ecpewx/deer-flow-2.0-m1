#!/usr/bin/env python3
"""
DeerFlow 出卷/论文选题测试工具
================================
通过 Gateway API 完成以下流程：
  1. 创建对话线程
  2. 上传课件（PPT/PDF/DOCX，自动转 Markdown）
  3. 调用 DeepSeek Reasoner 生成试卷或论文选题
  4. 从 SSE 流中提取生成的文件
  5. 可选：用 export.py 导出 DOCX

用法：
  # 基本用法（使用默认课件和提示词）
  python3 scripts/test_exam.py

  # 自定义课件和输出目录
  python3 scripts/test_exam.py --file /path/to/课件.pptx --output ~/Desktop/outputs

  # 自定义提示词
  python3 scripts/test_exam.py --prompt "根据课件出10道选择题"

  # 跳过上传（使用已有线程）
  python3 scripts/test_exam.py --thread <thread_id>

  # 导出为 DOCX（需要已安装 python-docx）
  python3 scripts/test_exam.py --export-docx
"""

import argparse
import json
import os
import sys
import time
import urllib.request

# ─── 默认配置 ───────────────────────────────────────────────
GATEWAY = "http://localhost:8001"
DEFAULT_COURSEFILE = os.path.expanduser(
    "~/Desktop/精算学原理/A2 完整课件/第三章-生命表.pptx"
)
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Desktop/精算学原理/试卷输出")
DEFAULT_PROMPT = (
    "根据我上传的课件，帮我出一套100分的测试卷。"
    "要求包含：选择题（每题2分x10=20分），判断题（每题1分x10=10分），"
    "填空题（每题2分x5=10分），简答题（每题10分x3=30分），"
    "计算题（每题15分x2=30分）。"
    "请确保题目覆盖课件的核心概念。"
)

# ─── 工具函数 ───────────────────────────────────────────────

def api_post(path, json_data=None):
    """发送 POST 请求到 Gateway。"""
    url = f"{GATEWAY}{path}"
    body = json.dumps(json_data or {}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def upload_file(thread_id: str, filepath: str) -> dict:
    """上传文件到指定线程。"""
    import mimetypes

    boundary = "----DeerFlowBoundary"
    filename = os.path.basename(filepath)
    ctype = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    with open(filepath, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="files"; filename="{filename}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"{GATEWAY}/api/threads/{thread_id}/uploads"
    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def stream_run(thread_id: str, message: str):
    """发送 run/stream 请求，实时显示进度，返回 (thread_id, events)。

    events 是原始 SSE data 字段的 JSON 列表。
    """
    body = {
        "input": {"messages": [{"role": "user", "content": message}]},
        "config": {"configurable": {"model_name": "deepseek-v3"}},
        "stream_mode": ["values", "messages-tuple", "custom"],
    }
    url = f"{GATEWAY}/api/threads/{thread_id}/runs/stream"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )

    events = []
    start = time.time()
    thinking_chars = 0
    content_chars = 0
    tool_call_count = 0

    print("  等待 DeepSeek Reasoner 响应...", flush=True)

    with urllib.request.urlopen(req, timeout=600) as resp:
        buf = ""
        while True:
            chunk = resp.read(4096)
            if not chunk:
                break
            buf += chunk.decode("utf-8", errors="replace")

            while "\n\n" in buf:
                raw_event, buf = buf.split("\n\n", 1)
                for line in raw_event.split("\n"):
                    if not line.startswith("data: "):
                        continue
                    try:
                        ev = json.loads(line[6:])
                    except json.JSONDecodeError:
                        continue
                    events.append(ev)

                    # ── 实时进度 ──
                    if isinstance(ev, list) and len(ev) >= 1:
                        msg = ev[0]
                        if not isinstance(msg, dict):
                            continue
                        # 思考内容
                        rc = msg.get("additional_kwargs", {}).get(
                            "reasoning_content", ""
                        )
                        if rc:
                            thinking_chars += len(rc)
                        # 正文内容
                        c = msg.get("content", "")
                        if c:
                            content_chars += len(c)
                        # 工具调用
                        tc = msg.get("tool_calls", [])
                        if tc:
                            tool_call_count += len(tc)
                            for t in tc:
                                name = t.get("name", "?")
                                print(f"  🔧 工具调用: {name}", flush=True)

                    # 每 10 秒打印一次总进度
                    elapsed = time.time() - start
                    if len(events) % 200 == 0:
                        print(
                            f"  [{elapsed:.0f}s] 思考 {thinking_chars} 字 | "
                            f"内容 {content_chars} 字 | "
                            f"工具 {tool_call_count} 次 | "
                            f"事件 {len(events)}",
                            flush=True,
                        )

    elapsed = time.time() - start
    print(
        f"  ✅ 完成! 耗时 {elapsed:.1f}s, "
        f"思考 {thinking_chars} 字, 内容 {content_chars} 字, "
        f"工具 {tool_call_count} 次, 共 {len(events)} 事件"
    )
    return events


def extract_outputs(events: list, thread_id: str, output_dir: str):
    """从 SSE 事件中提取 AI 生成的文件，并复制到 output_dir。

    DeepSeek 通常使用 write_file 工具将试卷写入
    backend/.deer-flow/threads/{thread_id}/user-data/outputs/
    """
    # 方案 A：直接从线程的 outputs 目录读取文件
    base = os.path.join(
        os.path.dirname(__file__),
        "..",
        "backend",
        ".deer-flow",
        "threads",
        thread_id,
        "user-data",
        "outputs",
    )
    base = os.path.normpath(base)

    found_files = []
    if os.path.isdir(base):
        for fname in os.listdir(base):
            src = os.path.join(base, fname)
            dst = os.path.join(output_dir, fname)
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            with open(dst, "w", encoding="utf-8") as f:
                f.write(content)
            found_files.append((fname, len(content)))
            print(f"  📄 {fname} ({len(content)} 字符)")

    if not found_files:
        # 方案 B：从最终 AI 消息中提取内容
        print("  ⚠️  outputs 目录为空，尝试从 SSE 事件提取...")
        ai_content = _extract_ai_content(events)
        if ai_content:
            fname = "生成结果.md"
            dst = os.path.join(output_dir, fname)
            with open(dst, "w", encoding="utf-8") as f:
                f.write(ai_content)
            found_files.append((fname, len(ai_content)))
            print(f"  📄 {fname} ({len(ai_content)} 字符)")

    return found_files


def _extract_ai_content(events: list) -> str:
    """从 SSE 事件中提取最终的 AI 回复文本。"""
    # 先尝试从最终 values 状态中取
    for ev in reversed(events):
        if isinstance(ev, dict):
            for msg in ev.get("messages", []):
                if isinstance(msg, dict) and msg.get("type") == "ai":
                    c = msg.get("content", "")
                    if c and len(c) > 200:
                        return c

    # 再尝试从流式 chunks 拼接（ev[0] 是消息数据）
    parts = []
    for ev in events:
        if isinstance(ev, list) and len(ev) >= 1:
            msg = ev[0]
            if isinstance(msg, dict) and msg.get("type") == "AIMessageChunk":
                c = msg.get("content", "")
                if c:
                    parts.append(c)
    return "".join(parts)


def export_docx(md_files: list, output_dir: str):
    """调用 export.py 将 Markdown 转为 DOCX。"""
    export_script = os.path.join(
        os.path.dirname(__file__),
        "..",
        "skills",
        "public",
        "exam-generation",
        "scripts",
        "export.py",
    )
    export_script = os.path.normpath(export_script)
    venv_python = os.path.join(
        os.path.dirname(__file__), "..", "backend", ".venv", "bin", "python"
    )
    venv_python = os.path.normpath(venv_python)

    if not os.path.exists(export_script):
        print(f"  ⚠️  export.py 不存在: {export_script}")
        return

    python_cmd = venv_python if os.path.exists(venv_python) else sys.executable

    import subprocess

    for md_name, _ in md_files:
        if not md_name.endswith(".md"):
            continue
        md_path = os.path.join(output_dir, md_name)
        docx_path = md_path.rsplit(".", 1)[0] + ".docx"
        print(f"  📝 导出: {md_name} → {os.path.basename(docx_path)}")
        try:
            subprocess.run(
                [python_cmd, export_script, "--input", md_path,
                 "--format", "docx", "--output", docx_path],
                check=True, capture_output=True, text=True,
            )
            print(f"     ✅ {docx_path}")
        except subprocess.CalledProcessError as e:
            print(f"     ❌ 导出失败: {e.stderr[:200]}")


# ─── 主流程 ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="DeerFlow 出卷/论文选题测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--file", "-f", nargs="+", default=None,
        help="要上传的文件路径，支持多个（PPT/PDF/DOCX/MD/TXT/PNG/JPG）。"
             "例如：-f 课件.pptx 知识图谱.pdf 习题1.docx 习题2.docx",
    )
    parser.add_argument(
        "--output", "-o", default=DEFAULT_OUTPUT_DIR,
        help="输出目录",
    )
    parser.add_argument(
        "--prompt", "-p", default=DEFAULT_PROMPT,
        help="发送给 AI 的提示词",
    )
    parser.add_argument(
        "--thread", "-t", default=None,
        help="使用已有的 Thread ID（跳过创建和上传）",
    )
    parser.add_argument(
        "--gateway", "-g", default=GATEWAY,
        help=f"Gateway 地址（默认 {GATEWAY}）",
    )
    parser.add_argument(
        "--export-docx", action="store_true",
        help="自动导出为 DOCX",
    )
    args = parser.parse_args()

    # 默认文件列表
    files_to_upload = args.file or [DEFAULT_COURSEFILE]

    global GATEWAY
    GATEWAY = args.gateway

    os.makedirs(args.output, exist_ok=True)

    # Step 1 & 2: 创建线程并上传
    if args.thread:
        thread_id = args.thread
        print(f"[1/4] 使用已有 Thread: {thread_id}")
    else:
        print("[1/4] 创建 Thread...")
        result = api_post("/api/threads")
        thread_id = result["thread_id"]
        print(f"  Thread ID: {thread_id}")

        print(f"[2/4] 上传 {len(files_to_upload)} 个文件...")
        total_uploaded = 0
        for filepath in files_to_upload:
            filepath = os.path.expanduser(filepath)
            fname = os.path.basename(filepath)
            if not os.path.exists(filepath):
                print(f"  ❌ 文件不存在，跳过: {filepath}")
                continue
            fsize = os.path.getsize(filepath)
            print(f"  📎 上传: {fname} ({fsize/1024:.0f} KB)...", end="", flush=True)
            upload_result = upload_file(thread_id, filepath)
            n = len(upload_result.get("files", []))
            total_uploaded += n
            # 显示转换信息
            for f_info in upload_result.get("files", []):
                md_file = f_info.get("markdown_file", "")
                if md_file:
                    print(f" → {md_file}", end="")
            print(" ✅")
        print(f"  共上传 {total_uploaded} 个文件")

    # Step 3: 发送请求
    print("[3/4] 发送请求到 DeepSeek Reasoner...")
    print(f"  提示词: {args.prompt[:80]}...")
    events = stream_run(thread_id, args.prompt)

    # Step 4: 提取输出
    print("[4/4] 提取生成文件...")
    md_files = extract_outputs(events, thread_id, args.output)

    if not md_files:
        print("\n⚠️  未找到生成的文件。可能 DeepSeek 直接回复了内容而未写入文件。")
        print("   你可以查看 SSE 事件了解详情。")
    else:
        print(f"\n📁 输出目录: {args.output}")
        for fname, size in md_files:
            print(f"   {fname} ({size} 字符)")

    # 可选：DOCX 导出
    if args.export_docx and md_files:
        print("\n[额外] 导出 DOCX...")
        export_docx(md_files, args.output)

    print(f"\n🔗 Thread ID: {thread_id}")
    print("   (可用 --thread 参数在同一线程中继续对话)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹  用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

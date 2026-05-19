"""Chroma knowledge base retrieval tool for DeerFlow.

Queries the local ChromaDB knowledge base (mounted at /app/chroma_db)
to retrieve relevant course material chunks.

NOTE: The Chroma database was built with pre-computed embeddings using
Qwen/Qwen3-Embedding-4B (2560-dim vectors) via SiliconFlow API.
This tool computes query embeddings using the same API for compatibility.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any

import requests
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Chroma database path inside the container (set via docker-compose volume mount)
CHROMA_DIR = Path(os.environ.get("CHROMA_DB_PATH", "/app/chroma_db"))
COLLECTION_NAME = "course_material_chunks"

# Embedding configuration — same as build_kb.py for SiliconFlow compatibility
EMBEDDING_ENDPOINT = os.environ.get("EMBEDDING_ENDPOINT", "https://api.siliconflow.cn/v1/embeddings")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-4B")


def _get_embedding(text: str) -> list[float]:
    """Compute embedding vector using the configured embedding API."""
    # Try SILICONFLOW_API_KEY first, then OPENAI_API_KEY as fallback
    api_key = (
        os.environ.get("SILICONFLOW_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    )

    try:
        import certifi
        verify = certifi.where()
    except ImportError:
        verify = True

    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(
        EMBEDDING_ENDPOINT,
        headers=headers,
        json={"model": EMBEDDING_MODEL, "input": text, "encoding_format": "float"},
        timeout=30,
        verify=verify,
    )
    if response.status_code == 401:
        raise ValueError("API Key 无效或已过期，无法计算 embedding。")
    response.raise_for_status()
    body = response.json()
    return body["data"][0]["embedding"]


@tool
def chroma_retrieve(
    query: str,
    course_id: str | None = None,
    top_k: int = 5,
) -> str:
    """【强制优先顺序】必须首先使用此工具检索本地课程知识库！

    ===== 执行规则（请严格遵守） =====
    第1步：当用户询问课程知识点、概念、案例分析、出题等教学内容时，必须先调用此工具检索知识库。
    第2步：仅当本工具返回"知识库中未找到相关内容"时，才考虑使用web_search等联网搜索工具。
    第3步：如果知识库找到了相关内容但不够充分，可以先用找到的内容回答，再补充说明。

    ===== 为什么必须优先使用 =====
    此知识库存储了本校所有课程的PPT、教材、案例等教学资料，比网络搜索更准确、权威、针对性更强。

    ===== 使用示例 =====
    - 直接问知识点：chroma_retrieve(query="生态保护红线")
    - 指定课程：chroma_retrieve(query="供求关系", course_id="经济学原理")
    - 检索多个概念：可以多次调用，每次查一个概念

    Args:
        query: 搜索的关键词或问题，如课程名称、知识点概念等
        course_id: 课程ID（可选），限定搜索范围到某门课程。例如"管理学原理"、"经济学"等
        top_k: 返回的最相关片段数量，默认5条

    Returns:
        检索到的文本片段列表。如果未找到相关结果会明确提示。
    """
    logger.info(f"Chroma retrieve: query='{query}', course_id={course_id}, top_k={top_k}")

    try:
        import chromadb
    except ImportError:
        return "检索失败: chromadb 未安装。请联系管理员安装: pip install chromadb"

    if not CHROMA_DIR.exists():
        return f"检索失败: 知识库路径不存在 ({CHROMA_DIR})。请确认知识库已正确挂载。"

    try:
        # Step 1: Compute query embedding
        logger.info("Computing query embedding via embedding API...")
        query_embedding = _get_embedding(query)
        logger.info(f"Query embedding computed, dimension={len(query_embedding)}")

        # Step 2: Query Chroma with the computed embedding
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collections = client.list_collections()
        logger.info(f"Chroma opened DB at {CHROMA_DIR}, collections: {[c.name for c in collections]}")

        collection = client.get_collection(COLLECTION_NAME)
        count = collection.count()
        logger.info(f"Chroma collection '{COLLECTION_NAME}' has {count} items")

        # Build filters
        where: dict[str, Any] = {}
        if course_id:
            where["course_id"] = course_id

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where or None,
            include=["documents", "metadatas", "distances"],
        )

        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        logger.info(f"Chroma query returned {len(ids)} results")

        if not ids:
            filter_info = f" (course_id='{course_id}')" if course_id else ""
            return f"知识库中未找到与「{query}」相关的内容{filter_info}。"

        output_lines = [f"从知识库中找到 {len(ids)} 条相关结果:\n"]
        for i, (chunk_id, text, meta, distance) in enumerate(zip(ids, documents, metadatas, distances), 1):
            source = meta.get("source_path", meta.get("source", "未知来源"))
            chunk_idx = meta.get("chunk_index", "")
            course = meta.get("course_id", "")
            similarity = 1 - distance
            output_lines.append(f"[{i}] 课程: {course} | 来源: {source} | 片段#{chunk_idx} (相似度: {similarity:.3f})")
            output_lines.append(f"    内容: {text[:500]}")
            output_lines.append("")

        return "\n".join(output_lines)

    except requests.exceptions.ConnectionError as e:
        logger.error(f"Chroma 检索失败: 无法连接到 embedding 服务 ({EMBEDDING_ENDPOINT}): {e}")
        return (
            f"检索失败: 无法连接到 embedding 服务 ({EMBEDDING_ENDPOINT})。"
            f"请检查网络连接或环境变量配置。"
        )
    except ValueError as e:
        logger.error(f"Chroma 检索参数错误: {e}")
        return f"检索失败: {e}"
    except Exception as e:
        logger.error(f"Chroma 检索异常: {e}", exc_info=True)
        return f"检索失败: {e}"

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


@dataclass
class TutorRecommendation:
    teacher: str
    title: str
    school: str
    research: str
    email: str
    url: str
    score: float
    reason: str
    papers_count: int
    projects_count: int
    tags: list[str]
    webpage_excerpt: str
    web_fetch_status: str


class TutorRecommenderService:
    """Lightweight recommender service with optional LLM-style reasoning."""

    def __init__(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        data_root = repo_root / "tutor_recommender_deepflow" / "data"
        self.tutors_path = data_root / "tutors_354.json"
        self.academic_path = data_root / "tutors_academic_full.json"
        self._tutors: list[dict[str, Any]] = []
        self._academic_map: dict[str, dict[str, Any]] = {}
        self._web_excerpt_cache: dict[str, str] = {}
        self._web_cache_updated_at: dict[str, float] = {}
        self._empty_cache_ttl_seconds = 300
        self._ready = False
        self._load()

    def _load(self) -> None:
        if not self.tutors_path.exists():
            logger.warning("Tutor data file not found: %s", self.tutors_path)
            return
        with self.tutors_path.open("r", encoding="utf-8") as f:
            self._tutors = json.load(f)
        if self.academic_path.exists():
            with self.academic_path.open("r", encoding="utf-8") as f:
                academic_list = json.load(f)
                self._academic_map = {item.get("teacher", ""): item for item in academic_list}
        self._ready = True
        logger.info("Tutor recommender loaded %s tutors", len(self._tutors))

    def health(self) -> dict[str, Any]:
        return {
            "ready": self._ready,
            "tutors_path": str(self.tutors_path),
            "academic_path": str(self.academic_path),
            "tutors_count": len(self._tutors),
        }

    @staticmethod
    def _normalize(text: str) -> str:
        return (text or "").strip().lower()

    def _build_tutor_text(self, tutor: dict[str, Any]) -> str:
        courses = tutor.get("courses", [])
        course_texts: list[str] = []
        for c in courses:
            if isinstance(c, dict):
                course_texts.append(str(c.get("course_name", "")))
            else:
                course_texts.append(str(c))
        return " ".join(
            [
                str(tutor.get("teacher", "")),
                str(tutor.get("title", "")),
                str(tutor.get("school", "")),
                str(tutor.get("research", "")),
                " ".join(course_texts),
            ]
        ).lower()

    def _match_score(self, query: str, tutor_text: str) -> float:
        query_tokens = [t for t in self._normalize(query).split() if t]
        if not query_tokens:
            return 0.0
        hit = 0
        for token in query_tokens:
            if token in tutor_text:
                hit += 1
        return hit / max(len(query_tokens), 1)

    def _passes_filters(self, tutor: dict[str, Any], filters: dict[str, Any] | None) -> bool:
        if not filters:
            return True
        school = str(tutor.get("school", ""))
        title = str(tutor.get("title", ""))
        teacher = str(tutor.get("teacher", ""))
        academic = self._academic_map.get(teacher, {})
        if filters.get("school") and filters["school"] not in school:
            return False
        if filters.get("title") and filters["title"] not in title:
            return False
        if filters.get("has_papers") and not academic.get("papers"):
            return False
        if filters.get("has_projects") and not academic.get("projects"):
            return False
        return True

    def _reason(self, query: str, tutor: dict[str, Any], score: float, llm_optional: bool) -> tuple[str, bool]:
        level = "高度匹配" if score >= 0.66 else ("较为匹配" if score >= 0.33 else "具备相关性")
        reason = f"该导师与“{query}”{level}，研究方向为：{tutor.get('research', '暂无公开研究方向')}。"
        # Placeholder for future LLM enhancement while keeping stable fallback behavior.
        used_llm = False
        if llm_optional:
            used_llm = False
        return reason, used_llm

    def _extract_text_excerpt(self, html: str, max_chars: int = 180) -> str:
        no_script = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
        no_style = re.sub(r"<style[\s\S]*?</style>", " ", no_script, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", no_style)
        text = re.sub(r"&nbsp;|&amp;|&lt;|&gt;|&quot;", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars]

    def _fetch_webpage_excerpt(self, url: str, refresh: bool = False) -> tuple[str, str]:
        if not url:
            return "", "no_url"
        if refresh:
            self._web_excerpt_cache.pop(url, None)
            self._web_cache_updated_at.pop(url, None)
        if url in self._web_excerpt_cache:
            cached = self._web_excerpt_cache[url]
            cached_at = self._web_cache_updated_at.get(url, 0.0)
            if not cached and (time.time() - cached_at > self._empty_cache_ttl_seconds):
                self._web_excerpt_cache.pop(url, None)
                self._web_cache_updated_at.pop(url, None)
            else:
                return cached, "cached_success" if cached else "cached_empty"
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; DeerFlowTutorRecommender/1.0)",
                },
            )
            with urlopen(req, timeout=3) as resp:
                content_type = resp.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    self._web_excerpt_cache[url] = ""
                    self._web_cache_updated_at[url] = time.time()
                    return "", "non_html"
                html = resp.read(65536).decode("utf-8", errors="ignore")
            excerpt = self._extract_text_excerpt(html)
            self._web_excerpt_cache[url] = excerpt
            self._web_cache_updated_at[url] = time.time()
            return excerpt, "success"
        except (URLError, TimeoutError, ValueError) as e:
            logger.info("Failed to fetch tutor page %s: %s", url, e)
            self._web_excerpt_cache[url] = ""
            self._web_cache_updated_at[url] = time.time()
            message = str(e).lower()
            if "timed out" in message or "timeout" in message:
                return "", "timeout"
            return "", "fetch_error"

    def recommend(
        self,
        query: str,
        k: int = 5,
        filters: dict[str, Any] | None = None,
        llm_optional: bool = True,
        fetch_web_content: bool = True,
        refresh_web_content: bool = False,
    ) -> tuple[list[TutorRecommendation], dict[str, Any]]:
        if not self._ready:
            raise RuntimeError("Tutor recommender is not ready. Please check data files.")
        start = time.perf_counter()
        scored: list[tuple[float, dict[str, Any]]] = []
        for tutor in self._tutors:
            if not self._passes_filters(tutor, filters):
                continue
            tutor_text = self._build_tutor_text(tutor)
            score = self._match_score(query, tutor_text)
            if score <= 0:
                continue
            scored.append((score, tutor))
        scored.sort(key=lambda item: item[0], reverse=True)
        selected = scored[: max(1, min(k, 20))]
        used_llm = False
        results: list[TutorRecommendation] = []
        for score, tutor in selected:
            teacher = str(tutor.get("teacher", ""))
            academic = self._academic_map.get(teacher, {})
            reason, used_llm_one = self._reason(query, tutor, score, llm_optional)
            used_llm = used_llm or used_llm_one
            webpage_excerpt = ""
            web_fetch_status = "skipped"
            if fetch_web_content:
                webpage_excerpt, web_fetch_status = self._fetch_webpage_excerpt(
                    str(tutor.get("url", "")),
                    refresh=refresh_web_content,
                )
            results.append(
                TutorRecommendation(
                    teacher=teacher,
                    title=str(tutor.get("title", "")),
                    school=str(tutor.get("school", "")),
                    research=str(tutor.get("research", "")),
                    email=str(tutor.get("email", "")),
                    url=str(tutor.get("url", "")),
                    score=round(float(score), 4),
                    reason=reason,
                    papers_count=len(academic.get("papers", []) or []),
                    projects_count=len(academic.get("projects", []) or []),
                    tags=[str(t) for t in (tutor.get("keywords", []) or []) if str(t).strip()],
                    webpage_excerpt=webpage_excerpt,
                    web_fetch_status=web_fetch_status,
                )
            )
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        debug = {
            "query": query,
            "requested_k": k,
            "matched_count": len(scored),
            "returned_count": len(results),
            "used_llm": used_llm,
            "fallback_used": not used_llm,
            "elapsed_ms": elapsed_ms,
            "fetch_web_content": fetch_web_content,
            "refresh_web_content": refresh_web_content,
            "empty_cache_ttl_seconds": self._empty_cache_ttl_seconds,
        }
        return results, debug


tutor_recommender_service = TutorRecommenderService()

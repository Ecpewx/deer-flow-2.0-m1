import argparse
import json
import math
import re
from datetime import datetime
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from textwrap import wrap


PERSON_SITE = "person.zufe.edu.cn"
INFO_SITE = "info.zufe.edu.cn"


@dataclass
class MentorDoc:
    mentor_name: str
    college_name: str
    program: str
    url: str
    site_type: str
    profile: dict
    raw_sections: dict
    text: str


def normalize_major(major: str) -> str:
    return normalize_text(major).replace(" ", "")


def safe_excerpt(value: str, max_len: int = 160) -> str:
    text = normalize_text(str(value))
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def extract_recent_lines(text: str, *, years: tuple[str, ...], limit: int = 5) -> list[str]:
    lines = [normalize_text(line) for line in str(text).splitlines()]
    lines = [line for line in lines if line]
    picked: list[str] = []
    for line in lines:
        if any(y in line for y in years):
            picked.append(line)
        if len(picked) >= limit:
            break
    return picked


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def sanitize_narrative_text(text: str) -> str:
    """Remove ranking/comparison style wording for user-facing text."""
    cleaned = normalize_text(text)
    banned_patterns = (
        r"排名第[一二三四五六七八九十0-9]+",
        r"第[一二三四五六七八九十0-9]+名",
        r"TOP\s*[0-9]+",
        r"top\s*[0-9]+",
        r"明显优于",
        r"不如某导师",
        r"优于",
        r"不如",
        r"碾压",
        r"吊打",
        r"拉踩",
    )
    for pattern in banned_patterns:
        cleaned = re.sub(pattern, "更匹配当前条件", cleaned, flags=re.IGNORECASE)
    return cleaned


def normalize_homepage_url(url: str) -> str:
    raw = normalize_text(url)
    if not raw:
        return "未提供"
    lowered = raw.lower().rstrip("/")
    # Reject portal/home roots; only keep concrete teacher profile pages.
    blocked = {
        "https://person.zufe.edu.cn",
        "http://person.zufe.edu.cn",
        "https://info.zufe.edu.cn/szdw/fjs",
        "http://info.zufe.edu.cn/szdw/fjs",
        "https://info.zufe.edu.cn",
        "http://info.zufe.edu.cn",
    }
    if lowered in blocked:
        return "未提供"
    return raw


def tokenize(text: str) -> list[str]:
    text = normalize_text(text).lower()
    zh_chunks = re.findall(r"[\u4e00-\u9fff]+", text)
    en_chunks = re.findall(r"[a-z0-9_+-]+", text)
    tokens: list[str] = []
    for chunk in zh_chunks:
        tokens.append(chunk)
        if len(chunk) > 1:
            tokens.extend(chunk[i : i + 2] for i in range(len(chunk) - 1))
    tokens.extend(en_chunks)
    return [tok for tok in tokens if tok]


def collect_person_site_sections(url_details: dict) -> tuple[dict, dict]:
    profile = url_details.get("个人信息", {}) or {}
    filtered_profile = {
        "学科教学所属单位": profile.get("学科教学所属单位", ""),
        "办公地点": profile.get("办公地点", ""),
        "最高学位": profile.get("最高学位", ""),
        "教师拼音名称": profile.get("教师拼音名称", profile.get("教师英文名称", "")),
        "最高学历": profile.get("最高学历", ""),
        "性别": profile.get("性别", ""),
        "职务": profile.get("职务", ""),
        "电子邮箱": profile.get("电子邮箱", ""),
    }
    sections = {
        "基本信息": url_details.get("基本信息", ""),
        "科学研究": url_details.get("科学研究", ""),
        "教学研究": url_details.get("教学研究", ""),
        "招生与就业": url_details.get("招生与就业", ""),
    }
    return filtered_profile, sections


def collect_info_site_sections(url_details: dict) -> tuple[dict, dict]:
    profile = url_details.get("个人信息", {}) or {}
    filtered_profile = {
        "性别": profile.get("性别", ""),
        "学历": profile.get("学历", ""),
        "学位": profile.get("学位", ""),
        "联系方式": profile.get("联系方式", ""),
        "办公地点": profile.get("办公地点", ""),
        "所在系部": profile.get("所在系部", ""),
        "研究方向": profile.get("研究方向", ""),
    }
    sections = {
        "个人简介": url_details.get("个人简介", ""),
        "教学与育人": url_details.get("教学与育人", ""),
        "论文与专著": url_details.get("论文与专著", ""),
        "课题与社会服务": url_details.get("课题与社会服务", ""),
        "奖励与荣誉": url_details.get("奖励与荣誉", ""),
    }
    return filtered_profile, sections


def build_doc_text(mentor_name: str, college_name: str, program: str, profile: dict, sections: dict) -> str:
    profile_text = " ".join(f"{k}:{v}" for k, v in profile.items() if v)
    section_text = " ".join(f"{k}:{normalize_text(str(v))}" for k, v in sections.items() if v)
    return normalize_text(f"导师:{mentor_name} 学院:{college_name} 项目:{program} {profile_text} {section_text}")


def flatten_mentors(payload: dict) -> list[MentorDoc]:
    docs: list[MentorDoc] = []
    college_map = payload.get("college_name", {}) or {}
    for college_name, college_value in college_map.items():
        by_program = (college_value or {}).get("mentors_by_program", {}) or {}
        for program, mentors in by_program.items():
            for mentor_name, mentor_info in (mentors or {}).items():
                url = normalize_homepage_url((mentor_info or {}).get("url", ""))
                url_details = (mentor_info or {}).get("url_details", {}) or {}
                if PERSON_SITE in url:
                    site_type = "person"
                    profile, sections = collect_person_site_sections(url_details)
                elif INFO_SITE in url:
                    site_type = "info"
                    profile, sections = collect_info_site_sections(url_details)
                else:
                    site_type = "other"
                    profile = (url_details.get("个人信息", {}) or {}) if isinstance(url_details, dict) else {}
                    sections = {k: v for k, v in (url_details or {}).items() if k != "个人信息"}

                text = build_doc_text(mentor_name, college_name, program, profile, sections)
                docs.append(
                    MentorDoc(
                        mentor_name=mentor_name,
                        college_name=college_name,
                        program=program,
                        url=url,
                        site_type=site_type,
                        profile=profile,
                        raw_sections=sections,
                        text=text,
                    )
                )
    return docs


def compute_bm25(tokenized_docs: list[list[str]], query_tokens: list[str], k1: float = 1.5, b: float = 0.75) -> list[float]:
    doc_count = len(tokenized_docs)
    doc_lens = [len(doc) for doc in tokenized_docs]
    avg_len = sum(doc_lens) / max(1, doc_count)

    df = defaultdict(int)
    for doc in tokenized_docs:
        for t in set(doc):
            df[t] += 1

    idf = {}
    for t, freq in df.items():
        idf[t] = math.log(1 + (doc_count - freq + 0.5) / (freq + 0.5))

    scores = []
    for i, doc in enumerate(tokenized_docs):
        tf = Counter(doc)
        score = 0.0
        for q in query_tokens:
            if q not in tf:
                continue
            freq = tf[q]
            numerator = freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * doc_lens[i] / max(1e-6, avg_len))
            score += idf.get(q, 0.0) * (numerator / denominator)
        scores.append(score)
    return scores


def build_tfidf_vectors(tokenized_texts: list[list[str]]) -> tuple[list[dict[str, float]], dict[str, float]]:
    doc_count = len(tokenized_texts)
    df = defaultdict(int)
    for doc in tokenized_texts:
        for t in set(doc):
            df[t] += 1
    idf = {t: math.log((doc_count + 1) / (freq + 1)) + 1.0 for t, freq in df.items()}

    vectors = []
    for doc in tokenized_texts:
        tf = Counter(doc)
        total = sum(tf.values()) or 1
        vec = {t: (c / total) * idf.get(t, 1.0) for t, c in tf.items()}
        vectors.append(vec)
    return vectors, idf


def cosine_sim(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    keys = set(a.keys()) & set(b.keys())
    dot = sum(a[k] * b[k] for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def query_vector(tokens: Iterable[str], idf: dict[str, float]) -> dict[str, float]:
    cnt = Counter(tokens)
    total = sum(cnt.values()) or 1
    return {t: (c / total) * idf.get(t, 1.0) for t, c in cnt.items()}


def min_max_norm(values: list[float]) -> list[float]:
    if not values:
        return values
    lo, hi = min(values), max(values)
    if hi - lo < 1e-12:
        return [0.0 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]


def build_reason(doc: MentorDoc, hit_terms: list[str], *, baseline_major_only: bool = False) -> str:
    area = doc.profile.get("研究方向", "") or doc.raw_sections.get("科学研究", "") or doc.raw_sections.get("个人简介", "")
    area = normalize_text(str(area))[:120]
    if baseline_major_only:
        reason = f"匹配依据：已在该专业导师池内完成匹配；科研/论文/项目等学术信息较完整。研究内容片段：{area if area else '该导师主页信息显示方向相关。'}"
        return sanitize_narrative_text(reason)
    hit_text = "、".join(hit_terms[:5]) if hit_terms else "研究方向语义匹配"
    reason = f"匹配依据：命中关键词（{hit_text}）；研究内容片段：{area if area else '该导师主页信息显示方向相关。'}"
    return sanitize_narrative_text(reason)


def build_unified_profile(doc: MentorDoc) -> dict:
    if doc.site_type == "info":
        return {
            "性别": doc.profile.get("性别", "") or "未提供",
            "学历": doc.profile.get("学历", "") or "未提供",
            "学位": doc.profile.get("学位", "") or "未提供",
            "联系方式": doc.profile.get("联系方式", "") or "未提供",
            "办公地点": doc.profile.get("办公地点", "") or "未提供",
            "所在系部": doc.profile.get("所在系部", "") or "未提供",
            "研究方向": doc.profile.get("研究方向", "") or "未提供",
        }

    return {
        "性别": doc.profile.get("性别", "") or "未提供",
        "学历": doc.profile.get("最高学历", "") or "未提供",
        "学位": doc.profile.get("最高学位", "") or "未提供",
        "联系方式": doc.profile.get("电子邮箱", "") or "未提供",
        "办公地点": doc.profile.get("办公地点", "") or "未提供",
        "所在系部": doc.profile.get("学科教学所属单位", "") or "未提供",
        "研究方向": safe_excerpt(
            doc.raw_sections.get("科学研究", "")
            or doc.raw_sections.get("个人简介", "")
            or doc.raw_sections.get("基本信息", "")
            or ""
        )
        or "未提供",
    }


def build_recent_highlights(doc: MentorDoc) -> dict:
    years = ("2025", "2026")
    papers_source = doc.raw_sections.get("论文与专著", "") or doc.raw_sections.get("基本信息", "")
    project_source = doc.raw_sections.get("课题与社会服务", "") or doc.raw_sections.get("科学研究", "") or doc.raw_sections.get("基本信息", "")
    progression_source = (
        doc.raw_sections.get("招生与就业", "")
        or doc.raw_sections.get("教学与育人", "")
        or doc.raw_sections.get("基本信息", "")
    )

    papers = extract_recent_lines(papers_source, years=years, limit=5)
    projects = extract_recent_lines(project_source, years=years, limit=5)
    progression = [line for line in extract_recent_lines(progression_source, years=years, limit=8) if any(k in line for k in ("读博", "升博", "毕业生", "985", "211", "去向"))]

    return {
        "recent_representative_works_2025_2026": papers if papers else ["未提供"],
        "recent_research_projects_2025_2026": projects if projects else ["未提供"],
        "student_progression": progression if progression else ["未提供"],
    }


def build_structured_sections(doc: MentorDoc) -> dict:
    if doc.site_type == "person":
        return {
            "个人信息": doc.profile,
            "基本信息": safe_excerpt(doc.raw_sections.get("基本信息", "")),
            "科学研究": safe_excerpt(doc.raw_sections.get("科学研究", "")),
            "教学研究": safe_excerpt(doc.raw_sections.get("教学研究", "")),
            "招生与就业": safe_excerpt(doc.raw_sections.get("招生与就业", "")),
        }
    if doc.site_type == "info":
        return {
            "个人信息": doc.profile,
            "个人简介": safe_excerpt(doc.raw_sections.get("个人简介", "")),
            "教学与育人": safe_excerpt(doc.raw_sections.get("教学与育人", "")),
            "论文与专著": safe_excerpt(doc.raw_sections.get("论文与专著", "")),
            "课题与社会服务": safe_excerpt(doc.raw_sections.get("课题与社会服务", "")),
            "奖励与荣誉": safe_excerpt(doc.raw_sections.get("奖励与荣誉", "")),
        }
    generic = {"个人信息": doc.profile}
    for k, v in doc.raw_sections.items():
        generic[k] = safe_excerpt(v)
    return generic


def filter_docs_by_major(docs: list[MentorDoc], major: str) -> list[MentorDoc]:
    major_norm = normalize_major(major).lower()
    if not major_norm:
        return []
    matched: list[MentorDoc] = []
    for doc in docs:
        # Enforce major ownership: only keep entries whose program label belongs to the major.
        program_norm = normalize_major(doc.program).lower()
        if major_norm in program_norm:
            matched.append(doc)
    return matched


def count_term_hits(text_l: str, terms: list[str]) -> int:
    hits = 0
    for term in terms:
        term_l = term.lower()
        if term_l and term_l in text_l:
            hits += 1
    return hits


def gender_bucket(doc: MentorDoc) -> str:
    gender = normalize_text(
        str(
            doc.profile.get("性别", "")
            or doc.profile.get("gender", "")
        )
    )
    if "男" in gender:
        return "male"
    if "女" in gender:
        return "female"
    return "missing"


def apply_gender_preference(docs: list[MentorDoc], must_have: list[str], avoid: list[str]) -> list[MentorDoc]:
    must_text = normalize_text(" ".join(must_have))
    avoid_text = normalize_text(" ".join(avoid))

    # Rule:
    # - want male -> male + missing
    # - avoid male -> female + missing
    if "男" in must_text:
        return [d for d in docs if gender_bucket(d) in {"male", "missing"}]
    if "男" in avoid_text:
        return [d for d in docs if gender_bucket(d) in {"female", "missing"}]
    if "女" in must_text:
        return [d for d in docs if gender_bucket(d) in {"female", "missing"}]
    if "女" in avoid_text:
        return [d for d in docs if gender_bucket(d) in {"male", "missing"}]
    return docs


def academic_strength_signal(doc: MentorDoc) -> float:
    weights = (
        # In major-only mode, prioritize objective research outputs over direction wording.
        ("科学研究", 0.30),
        ("论文与专著", 0.40),
        ("课题与社会服务", 0.15),
        ("招生与就业", 0.10),
        ("研究方向", 0.06),
        ("教学研究", 0.04),
    )
    score = 0.0
    text = doc.text.lower()
    for term, weight in weights:
        if term.lower() in text:
            score += weight
    # In major-only mode, prioritize recent 3-year research outputs by current year.
    current_year = datetime.now().year
    recent_years = tuple(str(y) for y in range(current_year - 2, current_year + 1))
    research_sections = (
        doc.raw_sections.get("科学研究", ""),
        doc.raw_sections.get("论文与专著", ""),
        doc.raw_sections.get("课题与社会服务", ""),
    )
    recent_hits = 0
    for section in research_sections:
        section_text = normalize_text(str(section))
        if section_text and any(y in section_text for y in recent_years):
            recent_hits += 1
    if recent_hits > 0:
        # up to +0.24 bonus when all three high-value sections include recent-year evidence
        score += min(0.08 * recent_hits, 0.24)
    return min(score, 1.0)


def recent_research_evidence_strength(doc: MentorDoc) -> float:
    """Return recent 3-year evidence strength in key research sections.

    0.0 means no recent evidence in key sections; 1.0 means all key sections include recent evidence.
    """
    current_year = datetime.now().year
    recent_years = tuple(str(y) for y in range(current_year - 2, current_year + 1))
    key_sections = (
        doc.raw_sections.get("科学研究", ""),
        doc.raw_sections.get("论文与专著", ""),
        doc.raw_sections.get("课题与社会服务", ""),
    )
    hits = 0
    for section in key_sections:
        section_text = normalize_text(str(section))
        if section_text and any(y in section_text for y in recent_years):
            hits += 1
    return hits / 3.0


def recent_output_count(doc: MentorDoc) -> int:
    """Count recent 3-year outputs in research/paper/project sections."""
    current_year = datetime.now().year
    recent_years = tuple(str(y) for y in range(current_year - 2, current_year + 1))
    sections = (
        doc.raw_sections.get("科学研究", ""),
        doc.raw_sections.get("论文与专著", ""),
        doc.raw_sections.get("课题与社会服务", ""),
    )
    count = 0
    for section in sections:
        lines = [normalize_text(line) for line in str(section).splitlines()]
        for line in lines:
            if line and any(y in line for y in recent_years):
                count += 1
    return count


def run_search(
    docs: list[MentorDoc],
    query: str,
    must_have: list[str],
    avoid: list[str],
    top_k: int,
    *,
    show_similarity: bool,
    baseline_major_only: bool,
) -> list[dict]:
    if baseline_major_only:
        # Strict recency gate for major-only mode:
        # if there are mentors with recent 3-year research evidence, rank only within that subset.
        recent_docs = [d for d in docs if recent_research_evidence_strength(d) > 0.0]
        if recent_docs:
            docs = recent_docs

    expanded_query = " ".join([query] + must_have)
    doc_tokens = [tokenize(d.text) for d in docs]
    query_tokens = tokenize(expanded_query)

    bm25 = compute_bm25(doc_tokens, query_tokens)
    bm25_norm = min_max_norm(bm25)

    tfidf_docs, idf = build_tfidf_vectors(doc_tokens)
    q_vec = query_vector(query_tokens, idf)
    vec_scores = [cosine_sim(v, q_vec) for v in tfidf_docs]
    vec_norm = min_max_norm(vec_scores)

    avoid_terms = [a.strip() for a in avoid if a.strip()]
    must_have_terms = [m.strip() for m in must_have if m.strip()]
    results = []
    for idx, doc in enumerate(docs):
        text_l = doc.text.lower()
        avoid_penalty = 0.12 * count_term_hits(text_l, avoid_terms)
        # Soft preference re-ranking keeps TopK stable across multi-turn updates.
        must_boost = 0.12 * count_term_hits(text_l, must_have_terms)
        if baseline_major_only:
            # Major-only mode: reduce generic keyword influence, emphasize academic density.
            score = 0.15 * bm25_norm[idx] + 0.20 * vec_norm[idx] + 0.65 * academic_strength_signal(doc)
            # Strongly down-rank mentors without recent 3-year research evidence.
            if recent_research_evidence_strength(doc) <= 0.0:
                score -= 0.28
        else:
            score = 0.45 * bm25_norm[idx] + 0.55 * vec_norm[idx]
        score = score + min(must_boost, 0.36) - min(avoid_penalty, 0.36)
        hits = [qt for qt in query_tokens if qt in doc_tokens[idx]]
        if baseline_major_only:
            # Avoid low-information hit terms like "管理/科学/工程" in major-only explanations.
            hits = []
        item = {
            "mentor_name": doc.mentor_name,
            "college_name": doc.college_name,
            "program": doc.program,
            "url": doc.url,
            "site_type": doc.site_type,
            "hit_terms": list(dict.fromkeys(hits))[:10],
            "unified_profile": build_unified_profile(doc),
            "recent_highlights": build_recent_highlights(doc),
            "structured_sections": build_structured_sections(doc),
            "reason": build_reason(doc, list(dict.fromkeys(hits)), baseline_major_only=baseline_major_only),
        }
        # Sort is always similarity-based; this switch only controls visibility.
        if show_similarity:
            item["similarity_score"] = round(score, 6)
        item["_rank_score"] = score
        item["_recent_output_count"] = recent_output_count(doc) if baseline_major_only else 0
        results.append(item)

    if baseline_major_only:
        # Primary key: recent 3-year output count (desc); secondary: model score (desc).
        results.sort(key=lambda x: (x["_recent_output_count"], x["_rank_score"]), reverse=True)
    else:
        results.sort(key=lambda x: x["_rank_score"], reverse=True)
    for item in results:
        item.pop("_rank_score", None)
        item.pop("_recent_output_count", None)
    if len(results) <= top_k:
        return results
    return results[:top_k]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mentor recommendation retrieval (hybrid BM25 + vector rerank)")
    parser.add_argument("--data", default=str(Path(__file__).resolve().parents[1] / "data" / "zufe_mentors.json"), help="Path to zufe_mentors.json")
    parser.add_argument("--research-direction-en", default="", help="Research direction in English (optional, preferred)")
    parser.add_argument("--query", default="", help="Legacy query text (optional)")
    parser.add_argument("--major", default="", help="User major/professional direction (required for recommendation)")
    parser.add_argument("--must-have", default="", help="Comma separated constraints that should be included")
    parser.add_argument("--avoid", default="", help="Comma separated constraints to avoid")
    parser.add_argument("--history-query", default="", help="Previous round query/constraints text for multi-turn merge")
    parser.add_argument("--top-k", type=int, default=5, help="Top-k mentors")
    parser.add_argument("--show-similarity", action="store_true", help="Show similarity score in output (ranking always uses similarity)")
    parser.add_argument(
        "--export-format",
        choices=("none", "auto", "word", "doc", "docx", "pdf", "md"),
        default="none",
        help="Optional report export format for current recommendation result",
    )
    parser.add_argument(
        "--export-path",
        default="",
        help="Optional output path for exported report file",
    )
    return parser.parse_args()


def build_export_markdown(output: dict) -> str:
    lines: list[str] = []
    major = output.get("major", "未提供")
    lines.append(f"# 导师推荐结果（{major}）")
    lines.append("")
    lines.append(
        f"- 共匹配 {output.get('returned_count', 0)} 人（条件：{output.get('merged_query', '未提供')}）"
    )
    lines.append(f"- must-have：{', '.join(output.get('must_have', [])) or '未提供'}")
    lines.append(f"- avoid：{', '.join(output.get('avoid', [])) or '未提供'}")
    lines.append("")
    lines.append("## 导师详情")
    lines.append("")
    for item in output.get("results", []):
        lines.append(f"### {item.get('mentor_name', '未提供')}")
        lines.append(f"- 学院：{item.get('college_name', '未提供')}")
        lines.append(f"- 项目类型：{item.get('program', '未提供')}")
        lines.append(f"- 主页：{item.get('url', '未提供')}")
        profile = item.get("unified_profile", {}) or {}
        lines.append("- 个人信息：")
        for key in ("性别", "学历", "学位", "联系方式", "办公地点", "所在系部", "研究方向"):
            lines.append(f"  - {key}：{profile.get(key, '未提供') or '未提供'}")
        lines.append(f"- AI推荐理由：{sanitize_narrative_text(item.get('reason', '未提供'))}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def _build_default_export_path(report_dir: Path, export_format: str, ts: str) -> Path:
    suffix_map = {
        "word": ".docx",
        "doc": ".docx",
        "docx": ".docx",
        "pdf": ".pdf",
        "md": ".md",
    }
    suffix = suffix_map.get(export_format, ".txt")
    return report_dir / f"mentor-recommendation-{ts}{suffix}"


def _export_word(output: dict, export_path: Path) -> str:
    from docx import Document  # type: ignore

    doc = Document()
    doc.add_heading(f"导师推荐结果（{output.get('major', '未提供')}）", level=1)
    doc.add_paragraph(f"查询条件：{output.get('merged_query', '未提供')}")
    doc.add_paragraph(f"返回人数：{output.get('returned_count', 0)}")
    for item in output.get("results", []):
        doc.add_heading(item.get("mentor_name", "未提供"), level=2)
        doc.add_paragraph(f"学院：{item.get('college_name', '未提供')}")
        doc.add_paragraph(f"项目类型：{item.get('program', '未提供')}")
        doc.add_paragraph(f"主页：{item.get('url', '未提供')}")
        profile = item.get("unified_profile", {}) or {}
        info_text = "；".join(
            f"{key}：{profile.get(key, '未提供') or '未提供'}"
            for key in ("性别", "学历", "学位", "联系方式", "办公地点", "所在系部", "研究方向")
        )
        doc.add_paragraph(f"个人信息：{info_text}")
        doc.add_paragraph(f"AI推荐理由：{sanitize_narrative_text(item.get('reason', '未提供'))}")
    doc.save(export_path)
    return str(export_path)


def _export_pdf(output: dict, export_path: Path) -> str:
    content = build_export_markdown(output)
    lines = content.splitlines()

    # Prefer reportlab CID font to avoid matplotlib CJK glyph-missing warnings.
    try:
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.pdfbase import pdfmetrics  # type: ignore
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont  # type: ignore
        from reportlab.pdfgen import canvas  # type: ignore

        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        c = canvas.Canvas(str(export_path), pagesize=A4)
        page_width, page_height = A4
        left = 36
        top = page_height - 40
        bottom = 40
        line_height = 15
        c.setFont("STSong-Light", 11)

        y = top
        for line in lines:
            wrapped_lines = wrap(line, width=54) or [""]
            for wrapped in wrapped_lines:
                if y < bottom:
                    c.showPage()
                    c.setFont("STSong-Light", 11)
                    y = top
                c.drawString(left, y, wrapped)
                y -= line_height
        c.save()
        return str(export_path)
    except Exception as exc:
        raise RuntimeError(
            "PDF 导出失败：当前环境受限，需通过 reportlab 直接注册字体（如 STSong-Light），"
            "且不可依赖 /usr/share/fonts/ 路径访问。"
        ) from exc


def _export_md(output: dict, export_path: Path) -> str:
    export_path.write_text(build_export_markdown(output), encoding="utf-8")
    return str(export_path)


def export_recommendation(output: dict, export_format: str, export_path: str) -> str:
    report_dir = Path(__file__).resolve().parents[2] / "exports"
    report_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    normalized_format = export_format
    if export_format == "auto":
        # Unspecified format defaults to Word export.
        normalized_format = "word"
    if export_format in {"doc", "docx"}:
        normalized_format = "word"

    if normalized_format in {"word", "pdf", "md"}:
        file_path = Path(export_path) if export_path else _build_default_export_path(report_dir, normalized_format, ts)
        if normalized_format == "word":
            return _export_word(output, file_path)
        if normalized_format == "pdf":
            return _export_pdf(output, file_path)
        return _export_md(output, file_path)

    raise ValueError(f"unsupported export format: {export_format}")


def build_latest_response_snapshot(output: dict) -> dict:
    """Build sanitized snapshot from current in-memory output for export."""
    snapshot = dict(output)
    snapshot["results"] = [dict(item) for item in output.get("results", [])]
    for item in snapshot["results"]:
        item["reason"] = sanitize_narrative_text(item.get("reason", "未提供"))
    return snapshot


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    docs = flatten_mentors(payload)
    major = normalize_text(args.major)
    if not major:
        output = {
            "query": args.query,
            "error": "missing_major",
            "message": "请先提供专业信息（例如：图书情报、电子信息、管理科学与工程）。提供专业后才能推荐导师。",
            "results": [],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    major_docs = filter_docs_by_major(docs, major)
    if not major_docs:
        output = {
            "query": args.query,
            "major": major,
            "error": "major_not_found",
            "message": f"未检索到与专业“{major}”相关的导师，请确认专业名称或换一种表达。",
            "results": [],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    must_have = [s.strip() for s in args.must_have.split(",") if s.strip()]
    avoid = [s.strip() for s in args.avoid.split(",") if s.strip()]
    major_docs = apply_gender_preference(major_docs, must_have, avoid)
    history_query = normalize_text(args.history_query)
    direction_query = normalize_text(args.research_direction_en)
    legacy_query = normalize_text(args.query)
    current_query = normalize_text(" ".join([direction_query, legacy_query]))
    merged_query = normalize_text(" ".join([history_query, current_query]))
    baseline_major_only = False
    if not merged_query:
        # Only major is provided: run a baseline recommendation within the major.
        baseline_major_only = True
        merged_query = major
    results = run_search(
        major_docs,
        merged_query,
        must_have,
        avoid,
        args.top_k,
        show_similarity=args.show_similarity,
        baseline_major_only=baseline_major_only,
    )

    output = {
        "query": current_query,
        "major": major,
        "history_query": history_query,
        "merged_query": merged_query,
        "must_have": must_have,
        "avoid": avoid,
        "total_docs": len(docs),
        "major_matched_docs": len(major_docs),
        "top_k": args.top_k,
        "show_similarity": bool(args.show_similarity),
        "returned_count": len(results),
        "results": results,
    }
    if args.export_format != "none":
        try:
            latest_snapshot = build_latest_response_snapshot(output)
            export_file = export_recommendation(latest_snapshot, args.export_format, args.export_path)
            output["export"] = {
                "requested": args.export_format,
                "file": export_file,
                "status": "success",
                "source": "latest_response_snapshot",
            }
        except Exception as exc:
            output["export"] = {
                "requested": args.export_format,
                "status": "failed",
                "error": str(exc),
            }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

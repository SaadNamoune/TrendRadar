from __future__ import annotations
from typing import Any

_INTEREST_KEYWORDS = {
    "ai": ["llm", "gpt", "transformer", "diffusion", "embedding", "ml", "deep learning", "neural", "nlp", "rag"],
    "security": ["pentest", "cve", "exploit", "malware", "siem", "firewall", "ctf", "vulnerability", "threat"],
    "systems": ["kernel", "cuda", "gpu", "distributed", "database", "storage", "runtime", "compiler", "wasm"],
    "devops": ["kubernetes", "docker", "terraform", "ansible", "ci/cd", "gitops", "helm", "observability"],
    "web": ["react", "nextjs", "svelte", "tailwind", "graphql", "api", "serverless"],
    "research": ["paper", "arxiv", "benchmark", "dataset", "survey", "framework"],
}


def _description_quality(desc: str) -> float:
    if not desc or len(desc) < 10:
        return 0.5
    if len(desc) > 100:
        return 1.2
    return 1.0


def _category_boost(title: str, desc: str, categories: list[str]) -> float:
    if "all" in categories:
        return 1.0
    text = (title + " " + (desc or "")).lower()
    for cat in categories:
        keywords = _INTEREST_KEYWORDS.get(cat, [])
        if any(kw in text for kw in keywords):
            return 1.5
    return 1.0


def score(repo: dict[str, Any], interest_categories: list[str] | None = None) -> float:
    interest_categories = interest_categories or ["all"]
    new_stars = repo.get("new_star", 0) or 0
    stars = repo.get("star", 0) or 0
    forks = repo.get("fork", 0) or 0
    desc = repo.get("description", "") or ""
    title = repo.get("title", "") or ""

    raw = (new_stars * 3.0) + (stars * 0.001) + (forks * 0.5)
    boost = _category_boost(title, desc, interest_categories)
    quality = _description_quality(desc)
    return round(raw * boost * quality, 2)


def rank(repos: list[dict[str, Any]], interest_categories: list[str] | None = None, top_k: int = 10) -> list[dict[str, Any]]:
    scored = [{**r, "score": score(r, interest_categories)} for r in repos]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

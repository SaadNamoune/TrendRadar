from __future__ import annotations
from typing import Any

_CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("AI/ML",     ["llm", "gpt", "transformer", "diffusion", "bert", "neural", "embedding", "nlp", "ml", "deep learning", "rag", "agent"]),
    ("Security",  ["exploit", "cve", "pentest", "ctf", "vulnerability", "malware", "siem", "threat", "fuzzer", "reverse"]),
    ("Systems",   ["kernel", "cuda", "gpu", "compiler", "runtime", "database", "storage", "os", "hypervisor", "wasm", "distributed"]),
    ("DevOps",    ["kubernetes", "docker", "terraform", "helm", "ci/cd", "gitops", "ansible", "observability", "monitoring"]),
    ("Web",       ["react", "nextjs", "vue", "svelte", "tailwind", "graphql", "api", "frontend", "fullstack"]),
    ("Research",  ["paper", "arxiv", "benchmark", "dataset", "survey", "replication"]),
]


def classify(repo: dict[str, Any]) -> str:
    text = ((repo.get("title") or "") + " " + (repo.get("description") or "")).lower()
    for category, keywords in _CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return category
    return "General"

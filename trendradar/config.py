from __future__ import annotations
import os
from dataclasses import dataclass, field


@dataclass
class Config:
    languages: list[str] = field(default_factory=lambda: ["", "python", "java", "javascript", "go", "rust", "c++"])
    top_k: int = 10
    interest_categories: list[str] = field(default_factory=lambda: ["all"])
    min_new_stars: int = 0
    webhook_url: str = ""
    notify_threshold: int = 200
    output_dir: str = "markdowns"
    reports_dir: str = "reports"
    request_timeout: int = 15
    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    @classmethod
    def from_env(cls) -> "Config":
        langs = os.getenv("LANGUAGES", "")
        return cls(
            languages=langs.split(",") if langs else cls.__dataclass_fields__["languages"].default_factory(),
            top_k=int(os.getenv("TOP_K", "10")),
            min_new_stars=int(os.getenv("MIN_NEW_STARS", "0")),
            webhook_url=os.getenv("WEBHOOK_URL", ""),
            notify_threshold=int(os.getenv("NOTIFY_THRESHOLD", "200")),
            output_dir=os.getenv("OUTPUT_DIR", "markdowns"),
            reports_dir=os.getenv("REPORTS_DIR", "reports"),
        )

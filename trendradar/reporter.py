from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Any


def _md_row(repo: dict[str, Any]) -> str:
    return (
        f"* [{repo['title']}]({repo['url']}): {repo.get('description','')}"
        f" ***★{repo['star']:,} ⑂{repo['fork']:,} +{repo['new_star']:,} today***"
        f"  `{repo.get('category','General')}` score={repo.get('score',0)}\n"
    )


def write_markdown(data: dict[str, list[dict[str, Any]]], date_str: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{date_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"## {date_str} GitHub Trending\n\n")
        for lang, repos in data.items():
            f.write(f"\n### {lang or 'All'}\n")
            for repo in repos:
                f.write(_md_row(repo))
    return path


def write_json(data: dict[str, list[dict[str, Any]]], date_str: str, reports_dir: str) -> str:
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, f"{date_str}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"date": date_str, "data": data}, f, ensure_ascii=False, indent=2)
    return path

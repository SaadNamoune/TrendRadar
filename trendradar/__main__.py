from __future__ import annotations
import argparse
from datetime import datetime

from .config import Config
from .crawler import scrape_all
from .scoring import rank
from .categories import classify
from .reporter import write_markdown, write_json
from .notifier import notify_webhook


def main() -> None:
    parser = argparse.ArgumentParser(description="TrendRadar — GitHub trending tracker")
    parser.add_argument("--languages", default="", help="Comma-separated languages (empty=all)")
    parser.add_argument("--topk", type=int, default=10)
    parser.add_argument("--categories", default="all", help="Filter: ai,security,systems,devops,web,research")
    parser.add_argument("--min-stars", type=int, default=0)
    args = parser.parse_args()

    cfg = Config.from_env()
    if args.languages:
        cfg.languages = [""] + args.languages.split(",")
    cfg.top_k = args.topk
    cfg.interest_categories = args.categories.split(",")
    cfg.min_new_stars = args.min_stars

    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"[TrendRadar] Crawling GitHub trending for {date_str}...")

    raw = scrape_all(cfg)
    processed: dict = {}
    for lang, repos in raw.items():
        repos = [r for r in repos if r.get("new_star", 0) >= cfg.min_new_stars]
        for r in repos:
            r["category"] = classify(r)
        repos = rank(repos, cfg.interest_categories, cfg.top_k)
        processed[lang] = repos

    md_path = write_markdown(processed, date_str, cfg.output_dir)
    json_path = write_json(processed, date_str, cfg.reports_dir)
    print(f"[TrendRadar] Markdown: {md_path}")
    print(f"[TrendRadar] JSON    : {json_path}")

    all_repos = [r for repos in processed.values() for r in repos]
    notify_webhook(all_repos, cfg.webhook_url, cfg.notify_threshold)


if __name__ == "__main__":
    main()

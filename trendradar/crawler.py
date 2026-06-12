from __future__ import annotations
import time
from typing import Any

try:
    import requests
    from pyquery import PyQuery
    _HAS_DEPS = True
except ImportError:
    _HAS_DEPS = False

from .config import Config


_BASE_URL = "https://github.com/trending/{language}"


def _fetch(url: str, cfg: Config) -> bytes:
    headers = {
        "User-Agent": cfg.user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=cfg.request_timeout)
    resp.raise_for_status()
    return resp.content


def _parse_int(value: str) -> int:
    try:
        return int(value.replace(",", "").replace("k", "000").strip())
    except (ValueError, AttributeError):
        return 0


def scrape_language(language: str, cfg: Config) -> list[dict[str, Any]]:
    if not _HAS_DEPS:
        raise RuntimeError("requests and pyquery are required: pip install requests pyquery")
    url = _BASE_URL.format(language=language)
    content = _fetch(url, cfg)
    d = PyQuery(content)
    repos = []
    for item in d("div.Box article.Box-row"):
        i = PyQuery(item)
        title = i(".lh-condensed a").text().strip()
        href = i(".lh-condensed a").attr("href") or ""
        url_full = "https://github.com" + href
        description = i("p.col-9").text().strip()
        star_text = i(".f6 a").eq(0).text().strip()
        fork_text = i(".f6 a").eq(1).text().strip()
        new_star_el = i(".f6 svg.octicon-star").parent().text().strip()
        new_star_parts = new_star_el.split()
        repos.append({
            "title": title,
            "url": url_full,
            "description": description,
            "star": _parse_int(star_text),
            "fork": _parse_int(fork_text),
            "new_star": _parse_int(new_star_parts[1]) if len(new_star_parts) > 1 else 0,
            "language": language or "all",
        })
    return repos


def scrape_all(cfg: Config) -> dict[str, list[dict[str, Any]]]:
    results: dict[str, list[dict[str, Any]]] = {}
    for lang in cfg.languages:
        try:
            repos = scrape_language(lang, cfg)
            results[lang or "all"] = repos
            time.sleep(0.5)
        except Exception as exc:
            results[lang or "all"] = []
            print(f"[TrendRadar] Failed to scrape '{lang}': {exc}")
    return results

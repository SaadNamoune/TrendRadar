from __future__ import annotations
import json
from typing import Any
try:
    import requests as _requests
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False


def notify_webhook(repos: list[dict[str, Any]], webhook_url: str, threshold: int = 200) -> int:
    if not webhook_url or not _HAS_REQUESTS:
        return 0
    hot = [r for r in repos if (r.get("new_star") or 0) >= threshold]
    if not hot:
        return 0
    lines = [f"• [{r['title']}]({r['url']}) — +{r['new_star']} stars today | {r.get('category','')}" for r in hot[:5]]
    payload = {"text": "🔥 *TrendRadar — Hot repos today*\n" + "\n".join(lines)}
    try:
        resp = _requests.post(webhook_url, json=payload, timeout=10)
        return resp.status_code
    except Exception:
        return 0

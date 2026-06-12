# Changelog

## [2.0.0] — 2024-06-12

### Added
- `trendradar/` package — modular rewrite replacing single `crawler.py`
- `scoring.py` — composite relevance score (velocity × category boost × description quality)
- `categories.py` — domain classifier: AI/ML, Security, Systems, DevOps, Web, Research
- `notifier.py` — Slack/Discord webhook alerts for high-velocity repos
- `reporter.py` — Markdown + JSON digest writer
- `config.py` — `Config` dataclass with env-var override support
- `__main__.py` — CLI: `python -m trendradar --languages python,go --categories ai,security`
- `tests/test_scoring.py` — unit tests for scoring and classification
- GitHub Actions CI — pytest + scheduled daily crawl with auto-commit

### Changed
- Crawler rewritten with robust int parser, rate-limit sleep, error isolation per language
- README rewritten with architecture diagram and scoring formula documentation

## [1.0.0] — 2023-07-19

Initial release — single-file GitHub trending scraper with Markdown output.

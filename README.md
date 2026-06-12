# TrendRadar

**GitHub Trending Intelligence Tracker** — automated daily crawler with ML relevance scoring, category filtering, and multi-language digest generation.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/SaadNamoune/TrendRadar/actions/workflows/ci.yml/badge.svg)](https://github.com/SaadNamoune/TrendRadar/actions)

---

## What It Does

TrendRadar scrapes GitHub Trending daily across multiple languages and domains, then:

1. **Scores** each repo with a composite relevance formula (stars velocity, forks, description quality)
2. **Categorizes** repos into domains: AI/ML, Security, DevOps, Systems, Web, Research
3. **Filters** by configurable interest profiles
4. **Generates** a structured Markdown + JSON digest per day
5. **Notifies** via webhook or email when high-interest repos appear

---

## Architecture

```
GitHub Trending (HTML)
       │
       ▼ crawler.py::scrape()
  raw repo list [{title, url, desc, stars, forks, new_stars}]
       │
       ▼ scoring.py::score()
  scored + ranked repos
       │
       ▼ categories.py::classify()
  repos with domain labels
       │
       ├──► markdown digest  (markdowns/YYYY-MM-DD.md)
       ├──► JSON export       (reports/YYYY-MM-DD.json)
       └──► notifier.py       → webhook / email alerts
```

---

## Quick Start

```bash
git clone https://github.com/SaadNamoune/TrendRadar.git
cd TrendRadar
pip install -r requirements.txt

# Run one crawl
python -m trendradar

# With filters
python -m trendradar --languages python,go,rust --topk 10 --categories security,ai
```

---

## Scoring Formula

```
score = (new_stars × 3.0) + (total_stars × 0.001) + (forks × 0.5)
      × category_boost × description_quality_factor
```

`category_boost` is 1.5× for repos matching AI/Security/Systems interest keywords.

---

## Sample Output

```markdown
## 2024-06-12 GitHub Trending — AI/Security Focus

### Python  (top 5 by score)
* facebookresearch/segment-anything ★89.2k ⑂10.8k +2341 today
  Category: AI/ML | Score: 7024.1
```

---

## Author

**Saad Namoune** — ESI Alger  
[GitHub](https://github.com/SaadNamoune) · [Email](mailto:saad.namoune28@gmail.com)

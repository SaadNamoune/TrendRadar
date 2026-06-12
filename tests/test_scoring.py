from trendradar.scoring import score, rank
from trendradar.categories import classify


def test_score_higher_for_more_new_stars():
    r1 = {"new_star": 500, "star": 1000, "fork": 200, "description": "A great ML tool", "title": "ml-tool"}
    r2 = {"new_star": 50, "star": 1000, "fork": 200, "description": "A great ML tool", "title": "ml-tool"}
    assert score(r1) > score(r2)


def test_score_category_boost():
    base = {"new_star": 100, "star": 1000, "fork": 100, "description": "gpt llm transformer", "title": "ai-lib"}
    boosted = score(base, interest_categories=["ai"])
    unboosted = score(base, interest_categories=["devops"])
    assert boosted > unboosted


def test_rank_returns_top_k():
    repos = [{"new_star": i, "star": i * 10, "fork": i, "description": "", "title": f"r{i}"} for i in range(20)]
    result = rank(repos, top_k=5)
    assert len(result) == 5
    assert result[0]["new_star"] == 19


def test_classify_security():
    repo = {"title": "exploit-framework", "description": "pentest and cve scanner"}
    assert classify(repo) == "Security"


def test_classify_ai():
    repo = {"title": "llm-agent", "description": "transformer based neural network"}
    assert classify(repo) == "AI/ML"


def test_classify_general():
    repo = {"title": "my-project", "description": "a simple utility"}
    assert classify(repo) == "General"

from pathlib import Path
from cv_evaluator.checks import evaluate_file


def test_evaluate_file_basic(tmp_path: Path):
    p = tmp_path / "cv.txt"
    p.write_text(
        """
John Doe
john@example.com
Summary: Software engineer
Experience: Developer at X
Skills: Python, SQL
Education: BSc
        """.strip(),
        encoding="utf-8",
    )
    res = evaluate_file(p, keywords=["python", "sql", "docker"])
    assert res["checks"]["has_text"] is True
    assert res["checks"]["has_contact_info"] is True
    assert res["score"] >= 60
    assert "docker" in res["missing_keywords"]

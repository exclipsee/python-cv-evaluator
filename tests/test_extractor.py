from pathlib import Path
from cv_evaluator.extractor import extract_text


def test_extract_txt(tmp_path: Path):
    p = tmp_path / "cv.txt"
    p.write_text("John Doe\njohn@example.com\nExperience: Developer\nSkills: Python, SQL\nEducation: BSc", encoding="utf-8")
    ext = extract_text(p)
    assert "john@example.com" in ext.text
    assert ext.file_type == "txt"

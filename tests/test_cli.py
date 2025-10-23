import json
import sys
from pathlib import Path
from click.testing import CliRunner

from cv_evaluator.cli import main


def test_cli_runs_text(tmp_path: Path):
    p = tmp_path / "cv.txt"
    p.write_text("John Doe\n+123456789\nSkills: Python", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, [str(p), "--keywords", "python,sql", "--format", "text", "--fail-under", "0"])
    assert result.exit_code == 0
    assert "Score:" in result.output


def test_cli_runs_json(tmp_path: Path):
    p = tmp_path / "cv.txt"
    p.write_text("John Doe\njohn@example.com\nSkills: Python", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, [str(p), "--format", "json", "--fail-under", "0"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, dict)
    assert "score" in data


def test_cli_show_text(tmp_path: Path):
    p = tmp_path / "cv.txt"
    p.write_text("John Doe\njohn@example.com\nSkills: Python", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, [str(p), "--show-text", "--fail-under", "0"])
    assert result.exit_code == 0
    assert "john@example.com" in result.output


def test_cli_markdown_output(tmp_path: Path):
    p = tmp_path / "cv.txt"
    p.write_text("John Doe\njohn@example.com\nSkills: Python", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, [str(p), "--format", "md", "--fail-under", "0"])
    assert result.exit_code == 0
    assert "## CV Evaluation Report" in result.output

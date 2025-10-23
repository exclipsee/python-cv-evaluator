import json
from pathlib import Path
import sys
import click

from .checks import evaluate_file
from .extractor import extract_text
from .utils import tokenize_words, STOPWORDS


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("cv_path", type=click.Path(exists=True, path_type=Path))
@click.option("--job", "job_file", type=click.Path(exists=True, path_type=Path), help="Path to a job description text file for keyword extraction")
@click.option("--keywords", type=str, help="Comma-separated keywords to check for")
@click.option("--format", "out_format", type=click.Choice(["text", "json"], case_sensitive=False), default="text", show_default=True)
@click.option("--fail-under", type=int, default=70, show_default=True, help="Exit non-zero if score is below this threshold")
@click.option("--show-text", is_flag=True, help="Print the raw extracted text to stdout (debug)")
def main(cv_path: Path, job_file: Path | None, keywords: str | None, out_format: str, fail_under: int, show_text: bool) -> None:
    """Evaluate a CV/Resume file for ATS compatibility.

    CV_PATH: Path to the CV file (pdf, docx, txt)
    """
    kw_list: list[str] | None = None
    if job_file and job_file.exists():
        try:
            text = job_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            text = job_file.read_text(errors="ignore")
        # improved keyword extraction: filter stopwords and short tokens
        from collections import Counter

        words = [w.lower() for w in tokenize_words(text) if len(w) >= 3 and w.lower() not in STOPWORDS]
        common = [w for w, _ in Counter(words).most_common(40)]
        kw_list = common
    if keywords:
        parts = [p.strip() for p in keywords.split(",") if p.strip()]
        kw_list = (kw_list or []) + parts

    if show_text:
        ext = extract_text(cv_path)
        click.echo(ext.text)
        # Continue to evaluation afterwards
    result = evaluate_file(cv_path, kw_list)

    if out_format.lower() == "json":
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo(f"Score: {result['score']} / 100")
        click.echo("Checks:")
        for name, ok in result["checks"].items():
            click.echo(f"  {'✓' if ok else '✗'} {name}")
        if result.get("missing_keywords"):
            click.echo("Missing keywords:")
            for kw in result["missing_keywords"]:
                click.echo(f"  - {kw}")
        if result.get("suggestions"):
            click.echo("Suggestions:")
            for s in result["suggestions"]:
                click.echo(f"  - {s}")

    if result.get("score", 0) < fail_under:
        sys.exit(2)

# Python CV Evaluator

Minimal CLI to check if a CV/Resume is ATS‑friendly (extractable text, key sections, contact info, layout pitfalls, and keyword coverage).

## Quick start

Requirements: Python 3.10+

```powershell
# From the project root
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Usage

```powershell
# Basic evaluation (text output)
ats-eval "C:\\path\\to\\YourCV.pdf"

# JSON output
ats-eval "C:\\path\\to\\YourCV.pdf" --format json

# Use a job description to derive keywords
ats-eval "C:\\path\\to\\YourCV.pdf" --job "C:\\path\\to\\job.txt"

# Provide explicit keywords and a fail threshold
ats-eval "C:\\path\\to\\YourCV.pdf" --keywords "python,sql,azure" --fail-under 75
```

Notes:
- For scanned PDFs, export a text-based PDF or DOCX first.
- Prefer a single-column layout; avoid tables for critical content.

## License
MIT

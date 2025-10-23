# Python CV Evaluator

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Type](https://img.shields.io/badge/type-CLI-success)

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

### Debug options

```powershell
# Show exactly what the extractor reads (useful for ATS parsing checks)
ats-eval "C:\\path\\to\\YourCV.pdf" --show-text | more
```

## Why ATS‑friendly?

Applicant Tracking Systems parse your CV to extract text and structure. Common pitfalls reduce what the system can “see.” This tool focuses on:

- Text extraction: Confirms your file contains selectable text (not just an image scan).
- Key sections: Summary, Experience, Education, Skills, Projects — headings ATS/recruiters expect.
- Contact info: Ensures email/phone are detectable.
- Layout risks: Warns about tables/columns and overly wide spacing that can break parsers.
- Keywords: Checks coverage against your provided list or a job description.

These are practical, vendor‑agnostic heuristics based on common ATS behavior — not any single vendor’s private scoring. Use them to de‑risk parsing and keep content machine‑readable.

Notes:
- For scanned PDFs, export a text-based PDF or DOCX first.
- Prefer a single-column layout; avoid tables for critical content.

## License
MIT

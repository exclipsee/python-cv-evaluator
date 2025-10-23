from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable

from .extractor import extract_text
from .scoring import weighted_score
from .utils import normalize_text
import tldextract


SECTION_KEYWORDS = {
    "summary": ["summary", "objective", "profile"],
    "experience": ["experience", "work history", "employment"],
    "education": ["education", "academics"],
    "skills": ["skills", "technical skills", "core competencies"],
    "projects": ["projects", "portfolio"],
}


def _has_contact_info(text: str) -> bool:
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.search(r"(?:\+?\d[\s-]?){7,}\d", text)
    return bool(email or phone)


def _section_presence(text: str) -> dict[str, bool]:
    t = text.lower()
    present: dict[str, bool] = {}
    for key, kws in SECTION_KEYWORDS.items():
        present[key] = any(kw in t for kw in kws)
    return present


def _formatting_pitfalls(notes: list[str] | None, text: str) -> list[str]:
    issues: list[str] = []
    if notes:
        for n in notes:
            if "table" in n:
                issues.append("Document contains tables; some ATS may not parse table content reliably.")
            if "image" in n:
                issues.append("Document contains images; avoid embedding headshots or text in images.")
    # Heuristic: many consecutive spaces can imply columns
    if re.search(r"\S\s{4,}\S", text):
        issues.append("Detected wide spacing that may indicate columns; consider single-column layout.")
    return issues


def _keyword_coverage(text: str, keywords: Iterable[str] | None) -> tuple[list[str], int]:
    if not keywords:
        return ([], 0)
    t = normalize_text(text)
    toks = set(t.split())
    missing: list[str] = []
    hit = 0
    for kw in keywords:
        for alt in {kw, kw.lower()}:
            if alt.replace(" ", "") in toks or alt in toks:
                hit += 1
                break
        else:
            missing.append(kw)
    return (missing, hit)


def _profile_links(text: str) -> dict[str, bool]:
    urls = re.findall(r"https?://[^\s)]+", text)
    found = {"linkedin": False, "github": False}
    for u in urls:
        ext = tldextract.extract(u)
        domain = ".".join(p for p in [ext.domain, ext.suffix] if p)
        if domain.lower().startswith("linkedin.") or domain.lower() == "linkedin.com":
            found["linkedin"] = True
        if domain.lower().startswith("github.") or domain.lower() == "github.com":
            found["github"] = True
    return found


def evaluate_file(path: Path, keywords: Iterable[str] | None = None) -> dict:
    ext = extract_text(path)
    text = ext.text or ""
    sections = _section_presence(text)
    has_contact = _has_contact_info(text)
    pitfalls = _formatting_pitfalls(ext.notes or [], text)
    links = _profile_links(text)
    missing, hits = _keyword_coverage(text, keywords)

    checks = {
        "has_text": bool(text.strip()),
        "has_contact_info": has_contact,
        **{f"section_{k}": v for k, v in sections.items()},
        "no_table_layout": not any("tables" in p for p in pitfalls),
        "reasonable_length": (50 <= len(text.split()) <= 1200),
        "has_profile_links": (links["linkedin"] or links["github"]),
    }

    # Weights sum to 1.0
    score = weighted_score({
        "has_text": (1.0 if checks["has_text"] else 0.0, 0.25),
        "contact": (1.0 if has_contact else 0.0, 0.15),
        "sections": (
            sum(1.0 for v in sections.values() if v) / max(1, len(sections)),
            0.30,
        ),
        "length": (1.0 if checks["reasonable_length"] else 0.0, 0.15),
        "pitfalls": (1.0 if not pitfalls else 0.0, 0.05),
        "keywords": (0.0 if not keywords else (hits / max(1, len(list(keywords)))), 0.08),
        "profile_links": (1.0 if checks["has_profile_links"] else 0.0, 0.02),
    })

    suggestions: list[str] = []
    if not has_contact:
        suggestions.append("Add a professional email and a phone number.")
    for k, present in sections.items():
        if not present:
            suggestions.append(f"Consider adding a '{k.title()}' section.")
    suggestions.extend(pitfalls)
    if ext.file_type == "pdf" and not text.strip():
        suggestions.append("PDF text extraction failed; export to PDF as text (not scanned) or use DOCX.")
    if not checks["has_profile_links"]:
        suggestions.append("Add a LinkedIn and/or GitHub URL in contact info.")

    return {
        "path": str(path),
        "file_type": ext.file_type,
        "pages": ext.pages,
        "checks": checks,
        "score": int(round(score * 100)),
        "missing_keywords": missing,
        "suggestions": suggestions,
    }

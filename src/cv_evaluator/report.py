from __future__ import annotations

from typing import Dict, Any


def render_markdown(result: Dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("## CV Evaluation Report")
    lines.append("")
    lines.append(f"Path: `{result.get('path','')}`  ")
    if result.get("file_type"):
        lines.append(f"Type: `{result['file_type']}`  ")
    if result.get("pages") is not None:
        lines.append(f"Pages: {result['pages']}  ")
    if result.get("file_size_kb") is not None:
        lines.append(f"Size: {result['file_size_kb']} KB  ")
    lines.append("")

    lines.append("### Score")
    lines.append(f"Overall: **{result.get('score', 0)} / 100**")
    if isinstance(result.get("scores"), dict):
        lines.append("")
        lines.append("Details:")
        for k, comp in result["scores"].items():
            val = comp.get("value", 0)
            wt = comp.get("weight", 0)
            lines.append(f"- {k}: {val:.2f} (weight {wt:.2f})")
    lines.append("")

    lines.append("### Checks")
    checks = result.get("checks", {})
    for name in sorted(checks.keys()):
        ok = checks[name]
        lines.append(f"- {'✅' if ok else '❌'} {name}")
    lines.append("")

    if result.get("missing_keywords"):
        lines.append("### Missing Keywords")
        for kw in result["missing_keywords"]:
            lines.append(f"- {kw}")
        lines.append("")

    if result.get("suggestions"):
        lines.append("### Suggestions")
        for s in result["suggestions"]:
            lines.append(f"- {s}")
        lines.append("")

    return "\n".join(lines)

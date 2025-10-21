from __future__ import annotations

import re


def normalize_text(t: str) -> str:
    t = t.lower()
    # Replace non-word separators with space
    t = re.sub(r"[^a-z0-9+#/.-]+", " ", t)
    # Collapse spaces
    t = re.sub(r"\s+", " ", t).strip()
    return t

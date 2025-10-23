from __future__ import annotations

import re


def normalize_text(t: str) -> str:
    t = t.lower()
    # Replace non-word separators with space
    t = re.sub(r"[^a-z0-9+#/.-]+", " ", t)
    # Collapse spaces
    t = re.sub(r"\s+", " ", t).strip()
    return t


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "into",
    "your",
    "you",
    "are",
    "our",
    "we",
    "will",
    "have",
    "has",
    "use",
    "using",
    "on",
    "in",
    "to",
    "of",
    "a",
    "an",
    "as",
    "by",
    "or",
    "be",
    "is",
    "it",
    "at",
}


def tokenize_words(text: str) -> list[str]:
    # keep tech separators +/-# and dots for things like C++, C#, Node.js
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#./-]{1,}", text)
    return words


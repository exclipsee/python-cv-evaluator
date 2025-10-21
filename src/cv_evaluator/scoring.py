from __future__ import annotations

def weighted_score(parts: dict[str, tuple[float, float]]) -> float:
    """Compute a weighted score from (value, weight) pairs.

    Values should be in [0,1], weights will be normalized to sum to 1.
    """
    total_w = sum(w for _, w in parts.values()) or 1.0
    score = 0.0
    for (v, w) in parts.values():
        v = max(0.0, min(1.0, v))
        score += v * (w / total_w)
    return score

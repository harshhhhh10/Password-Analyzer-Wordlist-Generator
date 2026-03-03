"""
password_analyzer.py
--------------------
Analyse a password with:
  1. Common password database (1000+ passwords + mutations)
  2. zxcvbn (dictionary / pattern matching)
  3. Custom entropy-based scorer

Returns a rich result dict that the CLI and GUI can display.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    import zxcvbn as _zxcvbn

    HAS_ZXCVBN = True
except ImportError:
    HAS_ZXCVBN = False

from utils import (
    STRENGTH_LABELS,
    calculate_entropy,
    detect_patterns,
    unique_chars_ratio,
)

from common_passwords import (
    is_common_password,
    get_common_match,
    get_password_rank,
    get_total_count,
    get_extended_count,
)


@dataclass
class AnalysisResult:
    """Container for every metric the analyser produces."""

    password: str
    length: int = 0
    entropy: float = 0.0
    unique_ratio: float = 0.0
    charset_flags: Dict[str, bool] = field(default_factory=dict)
    patterns_found: List[str] = field(default_factory=list)
    custom_score: int = 0
    custom_label: str = ""
    zxcvbn_score: int = -1
    zxcvbn_label: str = ""
    zxcvbn_feedback: Dict[str, Any] = field(default_factory=dict)
    zxcvbn_crack_time: str = ""
    suggestions: List[str] = field(default_factory=list)
    overall_score: int = 0
    overall_label: str = ""
    # Common password fields
    is_common: bool = False
    common_match: Optional[str] = None
    common_rank: Optional[int] = None
    common_db_size: int = 0
    common_extended_size: int = 0


def _custom_score(
    entropy: float,
    length: int,
    unique_ratio: float,
    patterns: List[str],
    is_common: bool,
) -> int:
    """Map entropy + heuristic penalties into a 0-4 score."""
    # INSTANT FAIL if common password
    if is_common:
        return 0

    score = 0
    if entropy >= 28:
        score = 1
    if entropy >= 36:
        score = 2
    if entropy >= 50:
        score = 3
    if entropy >= 60:
        score = 4

    # Penalties
    if length < 8:
        score = max(score - 2, 0)
    if unique_ratio < 0.4:
        score = max(score - 1, 0)
    if patterns:
        score = max(score - 1, 0)

    return min(max(score, 0), 4)


def _build_suggestions(result: AnalysisResult) -> List[str]:
    """Build list of improvement suggestions."""
    tips: List[str] = []

    # Common password warning
    if result.is_common:
        tips.append("THIS IS A COMMONLY USED PASSWORD - CHANGE IT IMMEDIATELY!")
        if result.common_match:
            tips.append(f"   Matched common password: '{result.common_match}'")
        tips.append("   It can be cracked in less than 1 second.")
        tips.append("   Use a unique passphrase with 4+ random words.")
        return tips

    if result.length < 12:
        tips.append("Increase length to at least 12 characters.")
    if not result.charset_flags.get("uppercase"):
        tips.append("Add UPPERCASE letters.")
    if not result.charset_flags.get("lowercase"):
        tips.append("Add lowercase letters.")
    if not result.charset_flags.get("digits"):
        tips.append("Include digits (0-9).")
    if not result.charset_flags.get("symbols"):
        tips.append("Include symbols (!@#$%...).")
    if result.unique_ratio < 0.5:
        tips.append("Use more unique characters; avoid repetition.")
    if result.entropy < 50:
        tips.append("Overall entropy is low - consider a longer passphrase.")
    return tips


def analyse(password: str) -> AnalysisResult:
    """Run full analysis and return an AnalysisResult."""
    r = AnalysisResult(password=password)
    r.length = len(password)
    r.entropy = round(calculate_entropy(password), 2)
    r.unique_ratio = round(unique_chars_ratio(password), 2)

    r.charset_flags = {
        "lowercase": any(c.islower() for c in password),
        "uppercase": any(c.isupper() for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(not c.isalnum() for c in password),
    }

    r.patterns_found = detect_patterns(password)

    # Common password check
    r.is_common = is_common_password(password)
    r.common_match = get_common_match(password)
    r.common_rank = get_password_rank(password)
    r.common_db_size = get_total_count()
    r.common_extended_size = get_extended_count()

    # Custom scorer
    r.custom_score = _custom_score(
        r.entropy, r.length, r.unique_ratio, r.patterns_found, r.is_common
    )
    r.custom_label = STRENGTH_LABELS.get(r.custom_score, "")

    # zxcvbn scorer
    if HAS_ZXCVBN:
        z = _zxcvbn.zxcvbn(password)
        r.zxcvbn_score = z["score"]
        r.zxcvbn_label = STRENGTH_LABELS.get(z["score"], "")
        r.zxcvbn_feedback = z.get("feedback", {})
        ct = z.get("crack_times_display", {})
        r.zxcvbn_crack_time = ct.get("offline_slow_hashing_1e4_per_second", "N/A")

    # Overall = minimum of scores (conservative)
    if r.zxcvbn_score >= 0:
        r.overall_score = min(r.custom_score, r.zxcvbn_score)
    else:
        r.overall_score = r.custom_score

    # Force score to 0 if common
    if r.is_common:
        r.overall_score = 0

    r.overall_label = STRENGTH_LABELS.get(r.overall_score, "")
    r.suggestions = _build_suggestions(r)
    return r


def result_to_text(r: AnalysisResult) -> str:
    """Pretty-print the analysis for terminal or text widget."""
    lines = [
        "=" * 60,
        "         PASSWORD STRENGTH ANALYSIS REPORT",
        "=" * 60,
        f"  Password       : {r.password}",
        f"  Length          : {r.length}",
        f"  Entropy (bits)  : {r.entropy}",
        f"  Unique ratio    : {r.unique_ratio:.0%}",
        f"  Charsets used   : {', '.join(k for k, v in r.charset_flags.items() if v)}",
        "",
    ]

    # Common password section
    lines.append("-" * 60)
    lines.append("  COMMON PASSWORD DATABASE CHECK")
    lines.append(f"     Database size : {r.common_db_size:,} base passwords")
    lines.append(f"     With mutations: {r.common_extended_size:,} total entries")

    if r.is_common:
        lines.append("")
        lines.append("  +==================================================+")
        lines.append("  |  WARNING: THIS IS A COMMON PASSWORD!             |")
        lines.append("  +==================================================+")
        if r.common_match:
            lines.append(f"     Matched       : '{r.common_match}'")
        if r.common_rank:
            lines.append(f"     Approx rank   : #{r.common_rank} most common")
        lines.append("     Crack time    : < 1 second (dictionary attack)")
        lines.append("")
    else:
        lines.append("     Status        : NOT found in common password list")
        lines.append("")

    lines.append("-" * 60)

    # Scores
    lines.append(f"  Custom Score    : {r.custom_score}/4  {r.custom_label}")

    if r.zxcvbn_score >= 0:
        lines.append(f"  zxcvbn Score    : {r.zxcvbn_score}/4  {r.zxcvbn_label}")
        lines.append(f"  Crack time      : {r.zxcvbn_crack_time}")

    lines.append("")
    lines.append(f"  * OVERALL       : {r.overall_score}/4  {r.overall_label}")
    lines.append("-" * 60)

    if r.patterns_found:
        lines.append("  Patterns detected:")
        for p in r.patterns_found:
            lines.append(f"      - {p}")

    if r.suggestions:
        lines.append("  Suggestions:")
        for s in r.suggestions:
            lines.append(f"      - {s}")

    if r.zxcvbn_feedback and not r.is_common:
        warn = r.zxcvbn_feedback.get("warning")
        if warn:
            lines.append(f"  zxcvbn warning: {warn}")
        for s in r.zxcvbn_feedback.get("suggestions", []):
            lines.append(f"      - {s}")

    lines.append("=" * 60)
    return "\n".join(lines)

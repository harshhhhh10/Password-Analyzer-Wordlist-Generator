"""
utils.py
--------
Shared constants, leetspeak maps, and helper functions used by both
the analyzer and the wordlist generator.
"""

import math
import string
from typing import Dict, List, Set


# Leetspeak substitution map (char -> list of replacements)
LEET_MAP: Dict[str, List[str]] = {
    "a": ["@", "4"],
    "b": ["8"],
    "c": ["(", "{"],
    "e": ["3"],
    "g": ["9", "6"],
    "h": ["#"],
    "i": ["1", "!"],
    "l": ["1", "|"],
    "o": ["0"],
    "s": ["$", "5"],
    "t": ["7", "+"],
    "z": ["2"],
}

# Common suffixes appended to base words
COMMON_SUFFIXES: List[str] = [
    "",
    "1",
    "12",
    "123",
    "1234",
    "12345",
    "!",
    "!!",
    "!!!",
    "@",
    "#",
    "$",
    ".",
    "*",
    "01",
    "69",
    "007",
    "abc",
    "qwerty",
]

# Years that are commonly appended
COMMON_YEARS: List[int] = list(range(1970, 2030))

# Separators people place between tokens
SEPARATORS: List[str] = ["", "_", "-", ".", "@", "#"]

# Character-set definitions for entropy calculation
CHARSETS: List[tuple] = [
    (string.ascii_lowercase, 26),
    (string.ascii_uppercase, 26),
    (string.digits, 10),
    (string.punctuation, 32),
]

# Strength labels mapped to zxcvbn scores 0-4
STRENGTH_LABELS: Dict[int, str] = {
    0: "Very Weak",
    1: "Weak",
    2: "Fair",
    3: "Strong",
    4: "Very Strong",
}

STRENGTH_COLORS: Dict[int, str] = {
    0: "#e74c3c",
    1: "#e67e22",
    2: "#f1c40f",
    3: "#2ecc71",
    4: "#27ae60",
}


def calculate_entropy(password: str) -> float:
    """
    Calculate Shannon entropy of password based on the character-pool
    size it draws from.
    Pool size = sum of charset sizes for every charset that contains at
    least one character in the password.
    """
    if not password:
        return 0.0
    pool = 0
    for charset, size in CHARSETS:
        if any(ch in charset for ch in password):
            pool += size
    # Include any characters outside known charsets (unicode etc.)
    extra = set(password) - set(
        string.ascii_letters + string.digits + string.punctuation
    )
    if extra:
        pool += len(extra) * 10
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def unique_chars_ratio(password: str) -> float:
    """Return the ratio of unique characters to total length."""
    if not password:
        return 0.0
    return len(set(password)) / len(password)


def detect_patterns(password: str) -> List[str]:
    """Detect common weak patterns inside the password."""
    findings: List[str] = []
    low = password.lower()

    # Keyboard walks
    walks = [
        "qwerty",
        "asdfgh",
        "zxcvbn",
        "qazwsx",
        "123456",
        "abcdef",
        "password",
        "letmein",
    ]
    for w in walks:
        if w in low:
            findings.append(f"Contains keyboard walk / common sequence: '{w}'")

    # Repeated characters
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            findings.append(f"Repeated character run: '{password[i] * 3}'")
            break

    # All same case
    if password.isalpha():
        if password.islower():
            findings.append("All lowercase letters - add uppercase and symbols")
        elif password.isupper():
            findings.append("All uppercase letters - mix in lowercase and symbols")

    # Only digits
    if password.isdigit():
        findings.append("Digits only - extremely limited character pool")

    return findings

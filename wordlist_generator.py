"""
wordlist_generator.py
---------------------
Generate attack-oriented wordlists from personal tokens (name,
birthday, pet, favourite team, etc).

Mutation strategies:
  1. Case variants         : hello -> Hello, HELLO, hELLO
  2. Leetspeak             : hello -> h3ll0, H3LL0
  3. Reverse               : hello -> olleh
  4. Year / number append  : hello2024, hello99
  5. Suffix append         : hello!, hello123
  6. Token combination     : johnfluffy, fluffyjohn
  7. Separator insertion   : john_fluffy, john.2024
  8. Truncation / initials : John Smith -> js, JS, j.smith
"""

from __future__ import annotations

import itertools
from datetime import datetime
from typing import Iterable, List, Optional, Set

from utils import COMMON_SUFFIXES, COMMON_YEARS, LEET_MAP, SEPARATORS


class WordlistGenerator:
    """Build a wordlist from personal information tokens."""

    def __init__(self) -> None:
        self.tokens: List[str] = []
        self.dates: List[str] = []
        self._extras: List[str] = []
        self._results: Set[str] = set()

    # -- public API --

    def add_token(self, token: str) -> None:
        """Add a personal token (name, pet, team, etc)."""
        token = token.strip()
        if token:
            self.tokens.append(token)

    def add_tokens(self, tokens: Iterable[str]) -> None:
        """Add multiple tokens at once."""
        for t in tokens:
            self.add_token(t)

    def add_date(self, date_str: str) -> None:
        """Add a date string (flexible formats accepted)."""
        date_str = date_str.strip()
        if date_str:
            self.dates.append(date_str)

    def add_extra(self, word: str) -> None:
        """Add an arbitrary word directly into the candidate pool."""
        if word.strip():
            self._extras.append(word.strip())

    def generate(
        self,
        max_length: int = 64,
        min_length: int = 4,
        enable_leet: bool = True,
        enable_years: bool = True,
        enable_combos: bool = True,
        combo_depth: int = 2,
    ) -> List[str]:
        """
        Generate the full wordlist and return it sorted.

        Parameters
        ----------
        max_length    : reject candidates longer than this
        min_length    : reject candidates shorter than this
        enable_leet   : apply leetspeak mutations
        enable_years  : append year numbers
        enable_combos : combine tokens pairwise
        combo_depth   : how many tokens to join (2 or 3)
        """
        self._results.clear()
        bases = self._build_base_words()

        for word in bases:
            self._add(word)

            # Case variants
            for v in self._case_variants(word):
                self._add(v)
                self._add_suffixes(v)
                if enable_years:
                    self._add_years(v)

            # Leetspeak
            if enable_leet:
                for leet in self._leetspeak(word):
                    self._add(leet)
                    self._add_suffixes(leet)

            # Reverse
            self._add(word[::-1])
            self._add(word[::-1].title())

            # Suffixes on base
            self._add_suffixes(word)
            if enable_years:
                self._add_years(word)

        # Token combinations
        if enable_combos and len(bases) > 1:
            self._combine_tokens(bases, combo_depth, enable_leet)

        # Add extras verbatim
        for e in self._extras:
            self._add(e)

        # Date-derived numbers
        self._add_date_fragments()

        # Filter by length
        filtered = sorted(
            w for w in self._results if min_length <= len(w) <= max_length
        )
        return filtered

    def export(self, path: str, wordlist: Optional[List[str]] = None) -> int:
        """Write wordlist to path. Returns the number of words written."""
        if wordlist is None:
            wordlist = self.generate()
        with open(path, "w", encoding="utf-8") as fp:
            for word in wordlist:
                fp.write(word + "\n")
        return len(wordlist)

    # -- internal helpers --

    def _add(self, word: str) -> None:
        """Add a word to results set."""
        if word:
            self._results.add(word)

    def _build_base_words(self) -> List[str]:
        """Create the first round of base words from tokens and dates."""
        bases: List[str] = []
        for tok in self.tokens:
            bases.append(tok.lower())
            # If multi-word, also add individual parts and initials
            parts = tok.split()
            if len(parts) > 1:
                for p in parts:
                    bases.append(p.lower())
                initials = "".join(p[0] for p in parts)
                bases.append(initials.lower())
                bases.append(initials.upper())
        # De-dup while preserving order
        seen: Set[str] = set()
        unique: List[str] = []
        for b in bases:
            if b not in seen:
                seen.add(b)
                unique.append(b)
        return unique

    @staticmethod
    def _case_variants(word: str) -> List[str]:
        """Generate case variants of a word."""
        return list(
            {
                word.lower(),
                word.upper(),
                word.title(),
                word.swapcase(),
                word.capitalize(),
                word[0].upper() + word[1:] if len(word) > 1 else word.upper(),
            }
        )

    @staticmethod
    def _leetspeak(word: str, max_variants: int = 50) -> List[str]:
        """Generate up to max_variants leetspeak mutations."""
        positions = []
        for i, ch in enumerate(word.lower()):
            if ch in LEET_MAP:
                positions.append((i, LEET_MAP[ch]))

        if not positions:
            return []

        # Limit combinatorial explosion
        if len(positions) > 6:
            positions = positions[:6]

        results: List[str] = []
        chars = list(word.lower())

        # Generate combinations
        options_per_pos = []
        for idx, replacements in positions:
            options_per_pos.append(
                [(idx, chars[idx])] + [(idx, r) for r in replacements]
            )

        count = 0
        for combo in itertools.product(*options_per_pos):
            if count >= max_variants:
                break
            mutated = chars[:]
            for idx, replacement in combo:
                mutated[idx] = replacement
            candidate = "".join(mutated)
            if candidate != word.lower():
                results.append(candidate)
            count += 1

        return results

    def _add_suffixes(self, word: str) -> None:
        """Append common suffixes to a word."""
        for sfx in COMMON_SUFFIXES:
            self._add(word + sfx)

    def _add_years(self, word: str) -> None:
        """Append years to a word."""
        # Full years
        for y in COMMON_YEARS:
            self._add(f"{word}{y}")
        # Two-digit years
        for y in range(0, 100):
            self._add(f"{word}{y:02d}")

    def _combine_tokens(self, bases: List[str], depth: int, enable_leet: bool) -> None:
        """Combine pairs or triples of base tokens with separators."""
        depth = min(depth, 3)
        for combo in itertools.permutations(bases, min(depth, len(bases))):
            for sep in SEPARATORS:
                merged = sep.join(combo)
                self._add(merged)
                self._add(merged.title())
                self._add(merged.upper())
                self._add_suffixes(merged)
                if enable_leet:
                    for leet in self._leetspeak(merged, max_variants=10):
                        self._add(leet)

    def _add_date_fragments(self) -> None:
        """Extract useful numeric fragments from every supplied date."""
        for raw in self.dates:
            # Try common date formats
            for fmt in (
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
                "%d-%m-%Y",
                "%m-%d-%Y",
                "%Y/%m/%d",
                "%d.%m.%Y",
                "%B %d, %Y",
                "%b %d, %Y",
                "%Y%m%d",
                "%d%m%Y",
                "%m%d%Y",
            ):
                try:
                    dt = datetime.strptime(raw, fmt)
                    self._add(dt.strftime("%Y"))
                    self._add(dt.strftime("%y"))
                    self._add(dt.strftime("%m%d"))
                    self._add(dt.strftime("%d%m"))
                    self._add(dt.strftime("%m%d%Y"))
                    self._add(dt.strftime("%d%m%Y"))
                    self._add(dt.strftime("%m%d%y"))
                    self._add(dt.strftime("%Y%m%d"))
                    self._add(dt.strftime("%d%m%y"))
                    # Also append fragments to every token
                    for tok in self.tokens:
                        low = tok.lower()
                        self._add(low + dt.strftime("%Y"))
                        self._add(low + dt.strftime("%y"))
                        self._add(low + dt.strftime("%m%d"))
                        self._add(low + dt.strftime("%d%m"))
                        self._add(low.title() + dt.strftime("%Y"))
                        self._add(low.title() + dt.strftime("%y"))
                    break  # parsed successfully
                except ValueError:
                    continue

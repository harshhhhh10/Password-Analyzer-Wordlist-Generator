#!/usr/bin/env python3
"""
cli_app.py
----------
Full-featured command-line interface for the password tool.

Usage examples:
  python main.py cli analyse --password "P@ssw0rd123"

  python main.py cli generate --name "John Smith" --pet "Fluffy" --dob "1990-03-15" --output wordlist.txt

  python main.py cli both --password "Fluffy1990!" --name "John Smith" --pet "Fluffy" --dob "1990-03-15" --output wordlist.txt
"""

from __future__ import annotations

import argparse
import sys
import time

from password_analyzer import analyse, result_to_text
from wordlist_generator import WordlistGenerator


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with all sub-commands."""
    parser = argparse.ArgumentParser(
        prog="PassTool CLI",
        description="Password Strength Analyser & Custom Wordlist Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # analyse command
    p_analyse = sub.add_parser(
        "analyse", aliases=["analyze"], help="Analyse password strength"
    )
    p_analyse.add_argument(
        "-p", "--password", required=True, help="The password to analyse"
    )

    # generate command
    p_gen = sub.add_parser("generate", help="Generate a custom wordlist")
    _add_gen_args(p_gen)

    # both command
    p_both = sub.add_parser("both", help="Analyse a password AND generate a wordlist")
    p_both.add_argument("-p", "--password", required=True)
    _add_gen_args(p_both)

    return parser


def _add_gen_args(p: argparse.ArgumentParser) -> None:
    """Add wordlist-generation arguments to a sub-parser."""
    p.add_argument("-n", "--name", nargs="+", default=[], help="Full name(s) of target")
    p.add_argument("--pet", nargs="+", default=[], help="Pet name(s)")
    p.add_argument(
        "--dob",
        nargs="+",
        default=[],
        help="Date(s) of birth (YYYY-MM-DD or DD/MM/YYYY)",
    )
    p.add_argument(
        "--extra", nargs="+", default=[], help="Any extra keywords (team, city, hobby)"
    )
    p.add_argument(
        "-o",
        "--output",
        default="wordlist.txt",
        help="Output file path [default: wordlist.txt]",
    )
    p.add_argument(
        "--min-len", type=int, default=4, help="Minimum word length [default: 4]"
    )
    p.add_argument(
        "--max-len", type=int, default=64, help="Maximum word length [default: 64]"
    )
    p.add_argument("--no-leet", action="store_true", help="Disable leetspeak mutations")
    p.add_argument("--no-years", action="store_true", help="Disable year appending")
    p.add_argument(
        "--no-combos", action="store_true", help="Disable token combinations"
    )
    p.add_argument(
        "--combo-depth",
        type=int,
        default=2,
        choices=[2, 3],
        help="Max tokens to combine [default: 2]",
    )


def _run_generate(args) -> None:
    """Execute the wordlist generation."""
    gen = WordlistGenerator()

    for n in args.name:
        gen.add_token(n)
    for p in args.pet:
        gen.add_token(p)
    for d in args.dob:
        gen.add_date(d)
    for e in args.extra:
        gen.add_token(e)

    if not gen.tokens and not gen.dates:
        print("[!] No tokens supplied. Use --name, --pet, --dob, or --extra.")
        sys.exit(1)

    print(
        f"\n[*] Generating wordlist with {len(gen.tokens)} token(s) "
        f"and {len(gen.dates)} date(s) ..."
    )
    start = time.time()

    wordlist = gen.generate(
        min_length=args.min_len,
        max_length=args.max_len,
        enable_leet=not args.no_leet,
        enable_years=not args.no_years,
        enable_combos=not args.no_combos,
        combo_depth=args.combo_depth,
    )

    count = gen.export(args.output, wordlist)
    elapsed = time.time() - start

    print(
        f"[+] {count:,} candidates written to '{args.output}' " f"in {elapsed:.2f}s\n"
    )


def run_cli(argv=None) -> None:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command in ("analyse", "analyze"):
        result = analyse(args.password)
        print(result_to_text(result))

    elif args.command == "generate":
        _run_generate(args)

    elif args.command == "both":
        result = analyse(args.password)
        print(result_to_text(result))
        _run_generate(args)


if __name__ == "__main__":
    run_cli()

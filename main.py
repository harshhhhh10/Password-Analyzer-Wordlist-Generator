#!/usr/bin/env python3
"""
main.py
-------
Unified entry point.

  python main.py gui            -> launch Tkinter GUI
  python main.py cli <command>  -> use the CLI (see --help)
  python main.py                -> default to GUI
"""

from __future__ import annotations

import sys


def main() -> None:
    """Dispatch to GUI or CLI based on first argument."""
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        from cli_app import run_cli

        run_cli(sys.argv[2:])
    else:
        # Strip "gui" argument if present
        if len(sys.argv) > 1 and sys.argv[1].lower() == "gui":
            sys.argv.pop(1)
        from gui_app import run_gui

        run_gui()


if __name__ == "__main__":
    main()

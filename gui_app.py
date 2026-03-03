#!/usr/bin/env python3
"""
gui_app.py
----------
Tkinter GUI for the Password Strength Analyser &
Custom Wordlist Generator.
"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional, List

from password_analyzer import analyse, result_to_text
from wordlist_generator import WordlistGenerator
from utils import STRENGTH_COLORS, STRENGTH_LABELS


# Colour palette
BG = "#1e1e2e"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
ENTRY_BG = "#313244"
BTN_BG = "#585b70"
BTN_FG = "#cdd6f4"


class PasswordToolGUI:
    """Main application window."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Password Strength Analyser & Wordlist Generator")
        self.root.geometry("820x660")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        style = ttk.Style()
        style.theme_use("clam")
        self._configure_styles(style)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_analyser_tab()
        self._build_generator_tab()

        self._last_wordlist: Optional[List[str]] = None

    # ── styles ──

    @staticmethod
    def _configure_styles(style: ttk.Style) -> None:
        """Configure ttk widget styles."""
        style.configure("TNotebook", background=BG)
        style.configure(
            "TNotebook.Tab", background=BTN_BG, foreground=FG, padding=[14, 6]
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", ACCENT)],
            foreground=[("selected", "#1e1e2e")],
        )
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 10))
        style.configure(
            "TButton",
            background=BTN_BG,
            foreground=BTN_FG,
            font=("Segoe UI", 10, "bold"),
            padding=6,
        )
        style.map(
            "TButton",
            background=[("active", ACCENT)],
            foreground=[("active", "#1e1e2e")],
        )
        style.configure(
            "TCheckbutton", background=BG, foreground=FG, font=("Segoe UI", 10)
        )
        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 13, "bold"),
            foreground=ACCENT,
            background=BG,
        )

    # ══════════════════════════════════════════════
    #  TAB 1: PASSWORD ANALYSER
    # ══════════════════════════════════════════════

    def _build_analyser_tab(self) -> None:
        """Build the password analyser tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="  Password Analyser  ")

        ttk.Label(tab, text="Enter Password to Analyse", style="Header.TLabel").pack(
            pady=(16, 6)
        )

        # Password entry row
        entry_frame = ttk.Frame(tab)
        entry_frame.pack(fill="x", padx=20)

        self.pw_var = tk.StringVar()
        self.pw_entry = tk.Entry(
            entry_frame,
            textvariable=self.pw_var,
            font=("Consolas", 13),
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            show="*",
        )
        self.pw_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        self.show_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            entry_frame, text="Show", variable=self.show_var, command=self._toggle_show
        ).pack(side="left", padx=(0, 8))

        ttk.Button(entry_frame, text="Analyse", command=self._on_analyse).pack(
            side="left"
        )

        # Strength bar
        self.bar_canvas = tk.Canvas(tab, height=28, bg=BG, highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=20, pady=(10, 0))

        # Score label
        self.score_label = ttk.Label(tab, text="", font=("Segoe UI", 12, "bold"))
        self.score_label.pack(pady=(2, 6))

        # Report area
        self.report_text = scrolledtext.ScrolledText(
            tab,
            font=("Consolas", 10),
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            wrap="word",
            height=18,
        )
        self.report_text.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    def _toggle_show(self) -> None:
        """Toggle password visibility."""
        if self.show_var.get():
            self.pw_entry.config(show="")
        else:
            self.pw_entry.config(show="*")

    def _on_analyse(self) -> None:
        """Handle the Analyse button click."""
        pw = self.pw_var.get()
        if not pw:
            messagebox.showwarning("Input needed", "Please enter a password.")
            return

        result = analyse(pw)
        self._draw_bar(result.overall_score)

        # Show common password warning in red
        if result.is_common:
            self.score_label.config(
                text="COMMON PASSWORD - CHANGE IMMEDIATELY!", foreground="#e74c3c"
            )
        else:
            self.score_label.config(
                text=result.overall_label,
                foreground=STRENGTH_COLORS.get(result.overall_score, FG),
            )

        # Display the full report
        self.report_text.delete("1.0", "end")
        self.report_text.insert("1.0", result_to_text(result))

        # Highlight warning lines in red
        if result.is_common:
            self._highlight_warning()

    def _highlight_warning(self) -> None:
        """Highlight WARNING lines in red inside the report text."""
        self.report_text.tag_configure(
            "warning", foreground="#e74c3c", font=("Consolas", 11, "bold")
        )
        start = "1.0"
        while True:
            pos = self.report_text.search("WARNING", start, stopindex="end")
            if not pos:
                break
            line_num = pos.split(".")[0]
            line_end = f"{line_num}.end"
            self.report_text.tag_add("warning", f"{line_num}.0", line_end)
            start = line_end

    def _draw_bar(self, score: int) -> None:
        """Draw the strength meter bar on canvas."""
        self.bar_canvas.delete("all")
        w = self.bar_canvas.winfo_width()
        if w < 10:
            w = 760
        h = 28
        segments = 5
        gap = 4
        seg_w = (w - gap * (segments - 1)) / segments

        for i in range(segments):
            x0 = i * (seg_w + gap)
            if i <= score:
                color = STRENGTH_COLORS.get(i, "#555")
            else:
                color = "#44475a"
            self.bar_canvas.create_rectangle(
                x0, 2, x0 + seg_w, h - 2, fill=color, outline=""
            )

    # ══════════════════════════════════════════════
    #  TAB 2: WORDLIST GENERATOR
    # ══════════════════════════════════════════════

    def _build_generator_tab(self) -> None:
        """Build the wordlist generator tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="  Wordlist Generator  ")

        ttk.Label(tab, text="Personal Information Tokens", style="Header.TLabel").pack(
            pady=(16, 8)
        )

        # Input form
        form = ttk.Frame(tab)
        form.pack(fill="x", padx=20)

        # Row builder helper
        def make_row(parent, label_text, row_num):
            ttk.Label(parent, text=label_text, width=14, anchor="e").grid(
                row=row_num, column=0, sticky="e", padx=(0, 6), pady=4
            )
            entry = tk.Entry(
                parent,
                font=("Segoe UI", 10),
                bg=ENTRY_BG,
                fg=FG,
                insertbackground=FG,
                relief="flat",
                width=36,
            )
            entry.grid(row=row_num, column=1, sticky="ew", pady=4, ipady=3)
            return entry

        self.gen_name = make_row(form, "Name(s):", 0)
        self.gen_pet = make_row(form, "Pet name(s):", 1)
        self.gen_dob = make_row(form, "DOB (date):", 2)
        self.gen_extra = make_row(form, "Extra tokens:", 3)

        form.columnconfigure(1, weight=1)

        # Hint labels
        hints = [
            "e.g. John Smith, Jane",
            "e.g. Fluffy, Rex",
            "e.g. 1990-03-15, 05/12/2000",
            "e.g. Yankees, pizza, NYC",
        ]
        for row_idx, hint_text in enumerate(hints):
            ttk.Label(
                form, text=hint_text, font=("Segoe UI", 8), foreground="#6c7086"
            ).grid(row=row_idx, column=2, sticky="w", padx=8)

        # Options frame
        opts = ttk.Frame(tab)
        opts.pack(fill="x", padx=20, pady=(10, 0))

        self.opt_leet = tk.BooleanVar(value=True)
        self.opt_years = tk.BooleanVar(value=True)
        self.opt_combo = tk.BooleanVar(value=True)

        ttk.Checkbutton(opts, text="Leetspeak", variable=self.opt_leet).grid(
            row=0, column=0, padx=8
        )
        ttk.Checkbutton(opts, text="Append years", variable=self.opt_years).grid(
            row=0, column=1, padx=8
        )
        ttk.Checkbutton(opts, text="Combine tokens", variable=self.opt_combo).grid(
            row=0, column=2, padx=8
        )

        ttk.Label(opts, text="Min len:").grid(row=0, column=3, padx=(16, 2))
        self.min_len_var = tk.StringVar(value="4")
        tk.Spinbox(
            opts,
            from_=1,
            to=32,
            width=4,
            textvariable=self.min_len_var,
            bg=ENTRY_BG,
            fg=FG,
            relief="flat",
        ).grid(row=0, column=4)

        ttk.Label(opts, text="Max len:").grid(row=0, column=5, padx=(12, 2))
        self.max_len_var = tk.StringVar(value="64")
        tk.Spinbox(
            opts,
            from_=8,
            to=128,
            width=4,
            textvariable=self.max_len_var,
            bg=ENTRY_BG,
            fg=FG,
            relief="flat",
        ).grid(row=0, column=6)

        # Buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=12)

        ttk.Button(btn_frame, text="Generate Wordlist", command=self._on_generate).pack(
            side="left", padx=6
        )
        ttk.Button(btn_frame, text="Export .txt", command=self._on_export).pack(
            side="left", padx=6
        )

        # Status label
        self.gen_status = ttk.Label(tab, text="Status: idle", font=("Segoe UI", 10))
        self.gen_status.pack()

        # Preview area
        ttk.Label(tab, text="Preview (first 200 entries)", style="Header.TLabel").pack(
            pady=(8, 4)
        )
        self.preview_text = scrolledtext.ScrolledText(
            tab,
            font=("Consolas", 10),
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            wrap="word",
            height=12,
        )
        self.preview_text.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    def _parse_csv(self, entry: tk.Entry) -> List[str]:
        """Split comma or semicolon separated entry text into a list."""
        raw = entry.get().strip()
        if not raw:
            return []
        for sep in (",", ";"):
            if sep in raw:
                return [t.strip() for t in raw.split(sep) if t.strip()]
        return [raw]

    def _on_generate(self) -> None:
        """Handle the Generate Wordlist button click."""
        names = self._parse_csv(self.gen_name)
        pets = self._parse_csv(self.gen_pet)
        dobs = self._parse_csv(self.gen_dob)
        extras = self._parse_csv(self.gen_extra)

        if not any([names, pets, dobs, extras]):
            messagebox.showwarning(
                "No input", "Enter at least one token (name, pet, DOB, or extra)."
            )
            return

        self.gen_status.config(text="Status: generating ...")
        self.root.update_idletasks()

        def worker():
            gen = WordlistGenerator()
            gen.add_tokens(names)
            gen.add_tokens(pets)
            gen.add_tokens(extras)
            for d in dobs:
                gen.add_date(d)

            wordlist = gen.generate(
                min_length=int(self.min_len_var.get()),
                max_length=int(self.max_len_var.get()),
                enable_leet=self.opt_leet.get(),
                enable_years=self.opt_years.get(),
                enable_combos=self.opt_combo.get(),
            )
            self._last_wordlist = wordlist
            self.root.after(0, lambda: self._show_preview(wordlist))

        threading.Thread(target=worker, daemon=True).start()

    def _show_preview(self, wordlist: List[str]) -> None:
        """Display generated wordlist preview."""
        self.gen_status.config(text=f"Status: {len(wordlist):,} candidates generated")
        self.preview_text.delete("1.0", "end")
        preview = "\n".join(wordlist[:200])
        if len(wordlist) > 200:
            preview += f"\n\n... and {len(wordlist) - 200:,} more"
        self.preview_text.insert("1.0", preview)

    def _on_export(self) -> None:
        """Handle the Export button click."""
        if not self._last_wordlist:
            messagebox.showinfo("Nothing to export", "Generate a wordlist first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="wordlist.txt",
        )
        if not path:
            return
        gen = WordlistGenerator()
        count = gen.export(path, self._last_wordlist)
        messagebox.showinfo("Export complete", f"{count:,} words written to:\n{path}")

    # ── Run ──

    def run(self) -> None:
        """Start the Tkinter main loop."""
        self.root.mainloop()


def run_gui() -> None:
    """Entry point for GUI mode."""
    app = PasswordToolGUI()
    app.run()


if __name__ == "__main__":
    run_gui()

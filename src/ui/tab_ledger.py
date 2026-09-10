"""
Modular Incident Audit Ledger View Component (Tab 2) for SwarSatya Application.
"""

import tkinter as tk
from tkinter import ttk
from config import (
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_ORANGE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_BG_DARK,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED
)


def build_tab_ledger(tab_frame: tk.Widget, app: tk.Tk) -> None:
    """
    Builds Tab 2 (Incident Audit Ledger) UI layout.
    """
    top_bar = tk.Frame(tab_frame, bg=COLOR_CARD_BG, padx=15, pady=10, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    top_bar.pack(fill="x", side="top", pady=(6, 8))

    lbl_title = tk.Label(
        top_bar,
        text="📜 CRYPTOGRAPHIC SHA-256 INCIDENT AUDIT LEDGER",
        font=("Segoe UI", 10, "bold"),
        fg=COLOR_CYAN,
        bg=COLOR_CARD_BG
    )
    lbl_title.pack(anchor="w")

    lbl_sub = tk.Label(
        top_bar,
        text="Tamper-Evident Hash-Chained Audit Ledger. Each log incorporates the SHA-256 digest of the preceding record.",
        font=("Segoe UI", 9),
        fg=COLOR_TEXT_MUTED,
        bg=COLOR_CARD_BG
    )
    lbl_sub.pack(anchor="w", pady=(2, 0))

    # Control Button Toolbar & Stat Cards
    control_frame = tk.Frame(tab_frame, bg=COLOR_BG_DARK)
    control_frame.pack(fill="x", side="top", pady=(0, 6))

    toolbar = tk.Frame(control_frame, bg=COLOR_BG_DARK)
    toolbar.pack(side="left", fill="x", expand=True)

    btn_verify = ttk.Button(
        toolbar,
        text="🔒 Verify SHA-256 Ledger Integrity",
        style="Primary.TButton",
        command=app._on_verify_ledger
    )
    btn_verify.pack(side="left", padx=(0, 8))

    btn_refresh = ttk.Button(
        toolbar,
        text="🔄 Refresh Records",
        style="Secondary.TButton",
        command=app._refresh_ledger_table
    )
    btn_refresh.pack(side="left", padx=(0, 8))

    btn_clear = ttk.Button(
        toolbar,
        text="🗑️ Clear Local Ledger",
        style="Danger.TButton",
        command=app._on_clear_ledger
    )
    btn_clear.pack(side="right")

    # Treeview Records Table Frame
    table_frame = tk.Frame(tab_frame, bg=COLOR_CARD_BG, padx=10, pady=10, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    table_frame.pack(fill="both", expand=True)

    columns = ("event_id", "timestamp", "session_id", "risk_score", "alert_level", "prev_hash", "record_hash")
    
    app.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
    
    app.tree.heading("event_id", text="Event ID")
    app.tree.heading("timestamp", text="UTC Timestamp")
    app.tree.heading("session_id", text="Session ID")
    app.tree.heading("risk_score", text="Risk Score")
    app.tree.heading("alert_level", text="Verdict Status")
    app.tree.heading("prev_hash", text="Previous Hash (SHA-256)")
    app.tree.heading("record_hash", text="Record Hash (SHA-256)")

    app.tree.column("event_id", width=110, anchor="center")
    app.tree.column("timestamp", width=140, anchor="center")
    app.tree.column("session_id", width=120, anchor="center")
    app.tree.column("risk_score", width=85, anchor="center")
    app.tree.column("alert_level", width=95, anchor="center")
    app.tree.column("prev_hash", width=160, anchor="w")
    app.tree.column("record_hash", width=160, anchor="w")

    # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=app.tree.yview)
    app.tree.configure(yscrollcommand=scrollbar.set)

    app.tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    app._refresh_ledger_table()

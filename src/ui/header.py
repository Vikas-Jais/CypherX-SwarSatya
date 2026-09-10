"""
Modular Header Component for SwarSatya Voice Security Application.
"""

import tkinter as tk
from tkinter import ttk
from config import (
    APP_NAME,
    TAGLINE,
    PROTOTYPE_VERSION,
    COLOR_BG_DARK,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_CYAN,
    COLOR_ORANGE,
    COLOR_GREEN,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED
)


def build_header(parent: tk.Widget) -> None:
    """
    Renders top application header navigation bar & security status strip.
    """
    header_frame = tk.Frame(parent, bg="#0B132B", padx=20, pady=12, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    header_frame.pack(fill="x", side="top")

    # Main Row Container
    row1 = tk.Frame(header_frame, bg="#0B132B")
    row1.pack(fill="x")

    # Left: Brand Title & Version Badge
    title_box = tk.Frame(row1, bg="#0B132B")
    title_box.pack(side="left", anchor="w")

    lbl_title = tk.Label(
        title_box,
        text=f"🎙️ {APP_NAME}",
        font=("Segoe UI", 18, "bold"),
        fg=COLOR_TEXT_PRIMARY,
        bg="#0B132B"
    )
    lbl_title.pack(side="left")

    lbl_ver = tk.Label(
        title_box,
        text=f" v{PROTOTYPE_VERSION} ",
        font=("Segoe UI", 8, "bold"),
        fg="#090D16",
        bg=COLOR_CYAN,
        padx=6,
        pady=2
    )
    lbl_ver.pack(side="left", padx=(10, 0))

    # Right: Live Engine Status Badge
    status_box = tk.Frame(row1, bg="#131C2E", padx=10, pady=4, highlightthickness=1, highlightbackground="#1E293B")
    status_box.pack(side="right", anchor="e")

    lbl_status_dot = tk.Label(
        status_box,
        text="🟢 LOCAL ENGINE ACTIVE",
        font=("Segoe UI", 8, "bold"),
        fg=COLOR_GREEN,
        bg="#131C2E"
    )
    lbl_status_dot.pack(side="left")

    # Subtitle / Tagline Strip
    lbl_tag = tk.Label(
        header_frame,
        text=f"“{TAGLINE}”",
        font=("Segoe UI", 9, "italic"),
        fg=COLOR_TEXT_MUTED,
        bg="#0B132B"
    )
    lbl_tag.pack(anchor="w", pady=(3, 0))

    # Security Policy Strip
    disc_frame = tk.Frame(parent, bg=COLOR_CARD_BG, padx=18, pady=5, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    disc_frame.pack(fill="x", side="top")

    lbl_disc = tk.Label(
        disc_frame,
        text="🛡️ LOCAL MEMORY PROTECTION: Zero Cloud Latency | SHA-256 Hash-Chained Incident Ledger Enabled",
        font=("Segoe UI", 8, "bold"),
        fg=COLOR_CYAN,
        bg=COLOR_CARD_BG
    )
    lbl_disc.pack(side="left")

    lbl_session = tk.Label(
        disc_frame,
        text=f"Session ID: {getattr(parent, 'session_id', 'SES-ACTIVE')[:12]}...",
        font=("Consolas", 8),
        fg=COLOR_TEXT_MUTED,
        bg=COLOR_CARD_BG
    )
    lbl_session.pack(side="right")

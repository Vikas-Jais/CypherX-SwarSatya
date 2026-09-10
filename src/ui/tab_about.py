"""
Modular About & System Architecture View Component (Tab 4) for SwarSatya Application.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from config import (
    APP_NAME,
    TAGLINE,
    PROTOTYPE_VERSION,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_CYAN,
    COLOR_ORANGE,
    COLOR_BG_DARK,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED
)


def build_tab_about(tab_frame: tk.Widget, app: tk.Tk) -> None:
    """
    Builds Tab 4 (About & System Architecture) UI layout.
    """
    top_bar = tk.Frame(tab_frame, bg=COLOR_CARD_BG, padx=15, pady=10, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    top_bar.pack(fill="x", side="top", pady=(6, 8))

    lbl_title = tk.Label(
        top_bar,
        text=f"ℹ️ ABOUT {APP_NAME.upper()} — SYSTEM ARCHITECTURE & METHODOLOGY",
        font=("Segoe UI", 10, "bold"),
        fg=COLOR_CYAN,
        bg=COLOR_CARD_BG
    )
    lbl_title.pack(anchor="w")

    lbl_sub = tk.Label(
        top_bar,
        text=f"{TAGLINE}  |  Version {PROTOTYPE_VERSION}",
        font=("Segoe UI", 9),
        fg=COLOR_TEXT_MUTED,
        bg=COLOR_CARD_BG
    )
    lbl_sub.pack(anchor="w", pady=(2, 0))

    txt_about = scrolledtext.ScrolledText(
        tab_frame,
        font=("Segoe UI", 9),
        bg=COLOR_CARD_BG,
        fg=COLOR_TEXT_PRIMARY,
        insertbackground="#FFFFFF",
        relief="flat",
        padx=15,
        pady=15,
        highlightthickness=1,
        highlightbackground=COLOR_CARD_BORDER
    )
    txt_about.pack(fill="both", expand=True)

    about_content = f"""
================================================================================
🎙️  {APP_NAME} — VOICE SECURITY & TRUTH ENGINE
================================================================================

1. SYSTEM PURPOSE & OVERVIEW
   SwarSatya is a native, offline-capable desktop security application designed for real-time
   detection of AI-generated synthetic voice clones and voice fraud. It executes 100% locally
   in transient system memory without relying on third-party cloud APIs.

2. CORE SECURITY & ML ARCHITECTURE
   • 100% Local Memory Processing:
     Audio signals are loaded directly into RAM, standardized to 16 kHz mono float32 format,
     and processed using sliding 1.0-second time windows with a 0.25-second hop size.
     No raw audio files are ever uploaded off-device.

   • 32-Dimensional Acoustic Feature Extraction:
     Each 1.0-second window is decomposed into 32 acoustic feature dimensions:
     - Pitch Inflection (YIN fundamental frequency F0 mean, std, variance & voiced ratio)
     - Spectral Geometry (Centroid, Bandwidth, Flatness & Rolloff)
     - Timbral Formants (13 MFCC means, 13 MFCC stds, and average MFCC std)
     - Energy Dynamics (RMS energy, Zero Crossing Rate mean & std, speech activity ratio)

   • Scikit-Learn Random Forest Classifier & Model Studio:
     Features are passed to a local Random Forest Classifier (`data/models/voice_classifier.pkl`).
     The Model Studio allows administrators to enroll custom voice samples (where 1 enrolled file
     yields 5 augmented dataset samples) and perform one-click model re-training.

   • Cryptographic SHA-256 Hash-Chained Incident Ledger:
     When call scans finish or incidents are reported, immutable audit logs are generated:
     - Each entry records event ID, session ID, UTC timestamp, and risk score.
     - Incorporates the SHA-256 hash digest of the preceding record (`previous_hash`),
       forming a tamper-evident audit ledger (`data/incident_ledger.jsonl`).
     - Includes built-in one-click integrity verification to detect unauthorized modifications.

3. AUDIT & SAFETY POLICIES
   • Risk Classification:
     - SAFE: Risk Score < 50.0%
     - WARNING: Risk Score 50.0% - 69.9%
     - CRITICAL: Risk Score >= 70.0%

   • Data Privacy Assurance:
     All operations run strictly on host hardware. Audit ledgers contain zero raw audio data,
     storing only cryptographic hashes and timestamp metrics for compliance records.
"""
    txt_about.insert(tk.END, about_content.strip())
    txt_about.config(state="disabled")

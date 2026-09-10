"""
UI styling helpers, custom Canvas components (Circular Risk Gauge & Audio Waveform Visualizer),
and Matplotlib chart embedding for SwarSatya Tkinter Desktop Application.
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

from config import (
    COLOR_DEEP_BLUE,
    COLOR_ACCENT_BLUE,
    COLOR_CYAN,
    COLOR_ORANGE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_BG_DARK,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    THRESHOLD_SAFE,
    THRESHOLD_WARNING,
    APP_NAME,
    TAGLINE
)


def apply_tkinter_theme(root: tk.Tk) -> ttk.Style:
    """
    Configure modern high-tech dark theme colors and fonts for Tkinter and TTK widgets.
    """
    root.configure(bg=COLOR_BG_DARK)
    style = ttk.Style(root)
    
    try:
        style.theme_use("clam")
    except Exception:
        pass

    font_main = ("Segoe UI", 9)
    font_bold = ("Segoe UI", 9, "bold")

    style.configure(".", background=COLOR_BG_DARK, foreground=COLOR_TEXT_PRIMARY, font=font_main)
    style.configure("TFrame", background=COLOR_BG_DARK)
    style.configure("Card.TFrame", background=COLOR_CARD_BG, relief="flat")
    
    # Modern Custom Styled Notebook Navigation Tabs
    style.configure("TNotebook", background=COLOR_BG_DARK, borderwidth=0, tabmargins=[10, 5, 10, 0])
    style.configure(
        "TNotebook.Tab",
        background="#162032",
        foreground=COLOR_TEXT_MUTED,
        padding=[18, 9],
        font=("Segoe UI", 10, "bold"),
        borderwidth=0
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLOR_CARD_BG), ("active", "#1E293B")],
        foreground=[("selected", COLOR_CYAN), ("active", "#FFFFFF")]
    )

    style.configure("TLabel", background=COLOR_BG_DARK, foreground=COLOR_TEXT_PRIMARY)
    style.configure("Card.TLabel", background=COLOR_CARD_BG, foreground=COLOR_TEXT_PRIMARY)
    
    # Modern Pill Buttons
    style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=COLOR_ORANGE, foreground="#FFFFFF", borderwidth=0, padding=[12, 8])
    style.map("Primary.TButton", background=[("active", "#EA580C"), ("disabled", "#334155")])

    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background=COLOR_ACCENT_BLUE, foreground="#FFFFFF", borderwidth=0, padding=[12, 8])
    style.map("Accent.TButton", background=[("active", "#1D4ED8"), ("disabled", "#334155")])

    style.configure("Secondary.TButton", font=("Segoe UI", 9, "bold"), background="#1E293B", foreground=COLOR_TEXT_PRIMARY, borderwidth=1, relief="flat", padding=[10, 6])
    style.map("Secondary.TButton", background=[("active", "#334155")])

    style.configure("Danger.TButton", font=("Segoe UI", 9, "bold"), background=COLOR_RED, foreground="#FFFFFF", borderwidth=0, padding=[10, 6])
    style.map("Danger.TButton", background=[("active", "#B91C1C")])

    # Progress bar
    style.configure("Horizontal.TProgressbar", background=COLOR_CYAN, troughcolor="#162032", bordercolor=COLOR_BG_DARK, thickness=8)

    # Entry & Radiobutton
    style.configure("TEntry", fieldbackground="#090D16", foreground=COLOR_TEXT_PRIMARY, insertcolor="#FFFFFF", borderwidth=1, relief="solid")

    # Treeview Dark Styling
    style.configure(
        "Treeview",
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_PRIMARY,
        fieldbackground=COLOR_CARD_BG,
        rowheight=28,
        font=("Segoe UI", 9),
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background="#162032",
        foreground=COLOR_CYAN,
        font=("Segoe UI", 9, "bold"),
        borderwidth=1,
        relief="flat"
    )
    style.map("Treeview", background=[("selected", COLOR_DEEP_BLUE)])

    return style


class RiskGaugeCanvas(tk.Canvas):
    """
    Custom Circular Speedometer / Arc Risk Gauge Canvas Widget.
    Renders an animated arc gauge (Safe Green -> Warning Amber -> Critical Red)
    with score readout and status indicator.
    """

    def __init__(self, parent, width=200, height=160, bg=COLOR_CARD_BG, **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.score = 0.0
        self.status = "SAFE"
        self.draw_gauge(0.0, "SAFE")

    def set_score(self, score: float, status: str = None):
        """Update gauge value and redraw arc."""
        self.score = max(0.0, min(1.0, score))
        if status:
            self.status = status
        elif self.score < THRESHOLD_SAFE:
            self.status = "SAFE"
        elif self.score < THRESHOLD_WARNING:
            self.status = "WARNING"
        else:
            self.status = "CRITICAL"
        self.draw_gauge(self.score, self.status)

    def draw_gauge(self, score: float, status: str):
        self.delete("all")
        cx = self.width / 2
        cy = self.height / 2 + 15
        r = min(self.width, self.height) / 2 - 16

        # Background track arc (start=210°, extent=-240°)
        start_angle = 210
        max_extent = -240

        self.create_arc(
            cx - r, cy - r, cx + r, cy + r,
            start=start_angle, extent=max_extent,
            style="arc", outline="#1E293B", width=14
        )

        # Active Score Fill Arc
        fill_color = COLOR_GREEN
        if status == "WARNING":
            fill_color = COLOR_ORANGE
        elif status == "CRITICAL":
            fill_color = COLOR_RED

        active_extent = max_extent * score
        if abs(active_extent) > 1:
            self.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start_angle, extent=active_extent,
                style="arc", outline=fill_color, width=14
            )

        # Inner Percentage Score Readout
        pct_text = f"{score * 100:.1f}%"
        self.create_text(
            cx, cy - 10,
            text=pct_text,
            fill="#FFFFFF",
            font=("Segoe UI", 22, "bold")
        )

        # Status Tag Readout
        status_icon = "🟢" if status == "SAFE" else ("🟠" if status == "WARNING" else "🔴")
        self.create_text(
            cx, cy + 18,
            text=f"{status_icon} {status}",
            fill=fill_color,
            font=("Segoe UI", 10, "bold")
        )


class AudioWaveformCanvas(tk.Canvas):
    """
    Custom Audio Waveform / Spectrum Visualization Canvas Widget.
    Pre-computes amplitude values once upon audio load for fast rendering.
    """

    def __init__(self, parent, width=500, height=70, bg="#090D16", **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=1, highlightbackground="#1F2937", **kwargs)
        self.width = width
        self.height = height
        self.cached_amps = None
        self.num_bars = 75
        self.draw_placeholder()

    def set_audio_data(self, audio_data: np.ndarray, num_bars: int = 75):
        """Pre-compute normalized amplitudes once when audio is loaded."""
        self.num_bars = num_bars
        if audio_data is None or len(audio_data) == 0:
            self.cached_amps = None
            self.draw_placeholder()
            return

        chunks = np.array_split(audio_data, num_bars)
        amps = [float(np.max(np.abs(c))) if len(c) > 0 else 0.0 for c in chunks]
        max_amp = max(amps) if max(amps) > 0 else 1.0
        self.cached_amps = [a / max_amp for a in amps]
        self.draw_waveform(active_progress=0.0)

    def draw_placeholder(self):
        self.delete("all")
        self.create_text(
            self.width / 2, self.height / 2,
            text="🎵 Audio Signal Waveform Window — Load Voice Recording or Demo Signal Above",
            fill="#475569",
            font=("Segoe UI", 9, "italic")
        )

    def draw_waveform(self, active_progress: float = 1.0, audio_data: np.ndarray = None):
        if audio_data is not None and self.cached_amps is None:
            self.set_audio_data(audio_data)

        self.delete("all")
        if self.cached_amps is None or len(self.cached_amps) == 0:
            self.draw_placeholder()
            return

        w = self.winfo_width() or self.width
        h = self.winfo_height() or self.height

        num_bars = len(self.cached_amps)
        bar_width = w / num_bars
        mid_y = h / 2

        active_bars_count = int(num_bars * active_progress)

        for i, amp in enumerate(self.cached_amps):
            x = i * bar_width + bar_width / 2
            bar_h = max(3, amp * (h * 0.8))
            
            y1 = mid_y - bar_h / 2
            y2 = mid_y + bar_h / 2

            bar_color = "#334155"
            if i <= active_bars_count:
                bar_color = COLOR_CYAN if amp < 0.5 else COLOR_ORANGE

            self.create_line(x, y1, x, y2, fill=bar_color, width=max(2, int(bar_width * 0.65)))


def update_risk_axes(ax, df: pd.DataFrame = None) -> None:
    """
    Safely update an existing Matplotlib Axes object with high-tech dashboard styling.
    Optimized for high-performance real-time updates.
    """
    ax.clear()
    ax.set_facecolor(COLOR_CARD_BG)

    ax.tick_params(colors=COLOR_TEXT_MUTED, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(COLOR_CARD_BORDER)

    ax.set_xlabel("Call Duration (Seconds)", color=COLOR_TEXT_MUTED, fontsize=9, fontweight="bold")
    ax.set_ylabel("Synthetic Risk Index [0.0 - 1.0]", color=COLOR_TEXT_MUTED, fontsize=9, fontweight="bold")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, color="#1E293B", linestyle=":", alpha=0.6)

    ax.axhline(y=THRESHOLD_SAFE, color=COLOR_ORANGE, linestyle="--", linewidth=1.2, label="Warning (0.50)")
    ax.axhline(y=THRESHOLD_WARNING, color=COLOR_RED, linestyle="--", linewidth=1.2, label="Critical (0.70)")

    if df is not None and not df.empty and "time" in df.columns:
        times = df["time"].astype(float).values
        raw_risks = df["raw_risk"].astype(float).values
        smoothed_risks = df["smoothed_risk"].astype(float).values

        ax.plot(times, raw_risks, color="#475569", linestyle=":", marker="o", markersize=3, alpha=0.7, label="Raw Window Risk")
        ax.plot(times, smoothed_risks, color=COLOR_CYAN, linewidth=2.5, label="Smoothed Risk (EMA α=0.35)")
        if len(times) > 1:
            ax.fill_between(times, 0, smoothed_risks, color=COLOR_CYAN, alpha=0.15)
        ax.set_xlim(0, max(float(times.max()) + 0.5, 5.0))
    else:
        ax.set_xlim(0, 5.0)

    ax.legend(loc="upper right", facecolor="#162032", edgecolor=COLOR_CARD_BORDER, labelcolor=COLOR_TEXT_PRIMARY, fontsize=8)

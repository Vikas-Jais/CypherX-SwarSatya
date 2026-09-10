"""
Modular Live Call Scan View Component (Tab 1) for SwarSatya Application.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import (
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_DEEP_BLUE,
    COLOR_CYAN,
    COLOR_ORANGE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_BG_DARK,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED
)
from src.ui_components import update_risk_axes, RiskGaugeCanvas, AudioWaveformCanvas


def build_tab_scan(tab_frame: tk.Widget, app: tk.Tk) -> None:
    """
    Builds Tab 1 (Live Call Scan) UI layout with interactive Canvas Gauge & Waveform.
    """
    # Top Control Bar (Audio Source Inputs)
    top_frame = tk.Frame(tab_frame, bg=COLOR_CARD_BG, padx=15, pady=10, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    top_frame.pack(fill="x", side="top", pady=(6, 8))

    lbl_section = tk.Label(
        top_frame,
        text="📁 AUDIO SOURCE SELECTION",
        font=("Segoe UI", 9, "bold"),
        fg=COLOR_CYAN,
        bg=COLOR_CARD_BG
    )
    lbl_section.pack(anchor="w", pady=(0, 6))

    btn_box = tk.Frame(top_frame, bg=COLOR_CARD_BG)
    btn_box.pack(fill="x")

    btn_upload = ttk.Button(
        btn_box,
        text="📂 Upload Audio File (WAV / MP3)",
        style="Primary.TButton",
        command=app._on_upload_file
    )
    btn_upload.pack(side="left", padx=(0, 10))

    btn_demo_ai = ttk.Button(
        btn_box,
        text="🤖 Load AI Voice Sample",
        style="Secondary.TButton",
        command=lambda: app._on_generate_demo(mode="robotic_synthetic")
    )
    btn_demo_ai.pack(side="left", padx=(0, 10))

    btn_demo_human = ttk.Button(
        btn_box,
        text="🎙️ Load Human Voice Sample",
        style="Secondary.TButton",
        command=lambda: app._on_generate_demo(mode="natural_human")
    )
    btn_demo_human.pack(side="left", padx=(0, 10))

    btn_open_top = ttk.Button(
        btn_box,
        text="📂 Open Reports Folder (CSV & Graphs)",
        style="Secondary.TButton",
        command=app._on_open_reports_folder
    )
    btn_open_top.pack(side="right")

    # Audio Waveform & Metadata Container
    wave_container = tk.Frame(tab_frame, bg="#090D16", padx=12, pady=8, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    wave_container.pack(fill="x", side="top", pady=(0, 8))

    app.lbl_meta_text = tk.Label(
        wave_container,
        text="No audio file loaded. Please upload a voice recording or select a sample above.",
        font=("Segoe UI", 9),
        fg=COLOR_TEXT_MUTED,
        bg="#090D16"
    )
    app.lbl_meta_text.pack(anchor="w", pady=(0, 4))

    # Interactive Waveform Canvas
    app.waveform_canvas = AudioWaveformCanvas(wave_container, width=800, height=60, bg="#090D16")
    app.waveform_canvas.pack(fill="x", expand=True)

    # Main Grid Layout (Left: Metrics & Explanations, Right: Trajectory Graph)
    main_grid = tk.Frame(tab_frame, bg=COLOR_BG_DARK)
    main_grid.pack(fill="both", expand=True)

    left_panel = tk.Frame(main_grid, bg=COLOR_CARD_BG, padx=14, pady=12, width=380, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    left_panel.pack(side="left", fill="both", expand=False, padx=(0, 8))
    left_panel.pack_propagate(False)

    right_panel = tk.Frame(main_grid, bg=COLOR_CARD_BG, padx=14, pady=12, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    right_panel.pack(side="right", fill="both", expand=True)

    # Left Panel: Scan Trigger Button
    app.btn_start_scan = ttk.Button(
        left_panel,
        text="⚡ START LIVE CALL SCAN",
        style="Accent.TButton",
        command=app._on_start_scan
    )
    app.btn_start_scan.pack(fill="x", pady=(0, 8))

    app.progress_bar = ttk.Progressbar(
        left_panel,
        orient="horizontal",
        mode="determinate",
        style="Horizontal.TProgressbar"
    )
    app.progress_bar.pack(fill="x", pady=(0, 10))

    # Live Circular Gauge Arc Canvas Widget
    app.gauge_canvas = RiskGaugeCanvas(left_panel, width=350, height=140, bg=COLOR_CARD_BG)
    app.gauge_canvas.pack(fill="x", pady=(0, 6))

    # Keep compatibility labels hidden/updated for state
    app.lbl_status_title = tk.Label(left_panel, text="", font=("Segoe UI", 1))
    app.lbl_score_val = tk.Label(left_panel, text="", font=("Segoe UI", 1))

    # Live Metrics Badges Box
    metrics_frame = tk.Frame(left_panel, bg="#090D16", padx=10, pady=8, highlightthickness=1, highlightbackground="#1F2937")
    metrics_frame.pack(fill="x", pady=(0, 8))

    app.lbl_metric_time = tk.Label(metrics_frame, text="⏱️ Timestamp: 0.0s / 0.0s", font=("Segoe UI", 8, "bold"), fg=COLOR_CYAN, bg="#090D16")
    app.lbl_metric_time.pack(anchor="w")

    app.lbl_metric_activity = tk.Label(metrics_frame, text="📊 Speech Activity: 0%", font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg="#090D16")
    app.lbl_metric_activity.pack(anchor="w", pady=(2, 0))

    app.lbl_metric_raw = tk.Label(metrics_frame, text="⚡ Raw Window Score: 0.0%", font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg="#090D16")
    app.lbl_metric_raw.pack(anchor="w", pady=(2, 0))

    # Acoustic Feature Attributions Box
    lbl_contrib_head = tk.Label(left_panel, text="🧠 Neural Acoustic Attributions:", font=("Segoe UI", 9, "bold"), fg=COLOR_CYAN, bg=COLOR_CARD_BG)
    lbl_contrib_head.pack(anchor="w", pady=(4, 2))

    app.txt_contrib = scrolledtext.ScrolledText(
        left_panel,
        height=5,
        font=("Consolas", 8),
        bg="#090D16",
        fg=COLOR_TEXT_PRIMARY,
        insertbackground="#FFFFFF",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#1F2937"
    )
    app.txt_contrib.pack(fill="both", expand=True, pady=(0, 8))
    app.txt_contrib.insert(tk.END, "• Upload audio or select a sample, then click 'Start Live Call Scan'.")

    # Action Toolbar
    act_box = tk.Frame(left_panel, bg=COLOR_CARD_BG)
    act_box.pack(fill="x", side="bottom")

    btn_report = ttk.Button(
        act_box,
        text="🚨 Log Incident",
        style="Secondary.TButton",
        command=app._on_report_fraud
    )
    btn_report.pack(side="left", fill="x", expand=True, padx=(0, 2))

    btn_open_reports = ttk.Button(
        act_box,
        text="📂 Open CSV & Graphs",
        style="Secondary.TButton",
        command=app._on_open_reports_folder
    )
    btn_open_reports.pack(side="left", fill="x", expand=True, padx=2)

    btn_guidance = ttk.Button(
        act_box,
        text="🛡️ Safety Defense",
        style="Secondary.TButton",
        command=app._show_safety_guidance
    )
    btn_guidance.pack(side="right", fill="x", expand=True, padx=(2, 0))

    # Right Panel: Matplotlib Risk Score Plot
    lbl_graph_title = tk.Label(
        right_panel,
        text="📈 REAL-TIME RISK SCORE TRAJECTORY (EMA Smoothing α=0.35)",
        font=("Segoe UI", 9, "bold"),
        fg=COLOR_CYAN,
        bg=COLOR_CARD_BG
    )
    lbl_graph_title.pack(anchor="w", pady=(0, 6))

    app.fig = Figure(figsize=(6, 4.2), dpi=100)
    app.fig.patch.set_facecolor(COLOR_CARD_BG)
    app.fig.subplots_adjust(left=0.10, right=0.96, top=0.94, bottom=0.14)
    app.ax = app.fig.add_subplot(111)

    update_risk_axes(app.ax)

    app.canvas = FigureCanvasTkAgg(app.fig, master=right_panel)
    app.canvas.draw()
    app.canvas.get_tk_widget().pack(fill="both", expand=True)

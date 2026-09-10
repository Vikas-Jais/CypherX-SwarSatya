"""
Modular Neural Model Studio View Component (Tab 3) for SwarSatya Application.
"""

import tkinter as tk
from tkinter import ttk
from config import (
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_ORANGE,
    COLOR_CYAN,
    COLOR_DEEP_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_BG_DARK,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED
)


def build_tab_studio(tab_frame: tk.Widget, app: tk.Tk) -> None:
    """
    Builds Tab 3 (Neural Model Studio) UI layout.
    """
    top_bar = tk.Frame(tab_frame, bg=COLOR_CARD_BG, padx=15, pady=10, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    top_bar.pack(fill="x", side="top", pady=(6, 8))

    lbl_title = tk.Label(
        top_bar,
        text="🧠 NEURAL MODEL STUDIO & CUSTOM VOICE SAMPLE ENROLLMENT",
        font=("Segoe UI", 10, "bold"),
        fg=COLOR_CYAN,
        bg=COLOR_CARD_BG
    )
    lbl_title.pack(anchor="w")

    lbl_sub = tk.Label(
        top_bar,
        text="Enroll custom voice samples into the dataset. 1 enrolled audio file automatically yields 5 augmented dataset samples.",
        font=("Segoe UI", 9),
        fg=COLOR_TEXT_MUTED,
        bg=COLOR_CARD_BG
    )
    lbl_sub.pack(anchor="w", pady=(2, 0))

    # Main Studio Layout Grid
    grid_frame = tk.Frame(tab_frame, bg=COLOR_BG_DARK)
    grid_frame.pack(fill="both", expand=True)

    # Left Column: Voice Enrollment Card
    enroll_card = tk.Frame(grid_frame, bg=COLOR_CARD_BG, padx=14, pady=12, width=310, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    enroll_card.pack(side="left", fill="y", padx=(0, 8))
    enroll_card.pack_propagate(False)

    lbl_enc_head = tk.Label(enroll_card, text="🎙️ Enroll Voice Sample", font=("Segoe UI", 10, "bold"), fg=COLOR_CYAN, bg=COLOR_CARD_BG)
    lbl_enc_head.pack(anchor="w", pady=(0, 8))

    # Tag Name Input
    lbl_sname = tk.Label(enroll_card, text="Tag / Speaker Name:", font=("Segoe UI", 9), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD_BG)
    lbl_sname.pack(anchor="w")

    app.ent_sample_name = ttk.Entry(enroll_card)
    app.ent_sample_name.pack(fill="x", pady=(2, 10))

    # Label Radio Selection
    lbl_rad = tk.Label(enroll_card, text="Voice Label Category:", font=("Segoe UI", 9), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD_BG)
    lbl_rad.pack(anchor="w")

    app.var_label = tk.IntVar(value=0)

    rad_human = tk.Radiobutton(
        enroll_card,
        text="Human Voice (Label = 0)",
        variable=app.var_label,
        value=0,
        font=("Segoe UI", 9, "bold"),
        fg=COLOR_GREEN,
        bg=COLOR_CARD_BG,
        selectcolor="#090D16",
        activebackground=COLOR_CARD_BG,
        activeforeground=COLOR_GREEN
    )
    rad_human.pack(anchor="w", pady=(4, 2))

    rad_ai = tk.Radiobutton(
        enroll_card,
        text="AI / Synthetic Voice (Label = 1)",
        variable=app.var_label,
        value=1,
        font=("Segoe UI", 9, "bold"),
        fg=COLOR_RED,
        bg=COLOR_CARD_BG,
        selectcolor="#090D16",
        activebackground=COLOR_CARD_BG,
        activeforeground=COLOR_RED
    )
    rad_ai.pack(anchor="w", pady=(0, 14))

    # Enrollment Action Buttons
    btn_enroll_file = ttk.Button(
        enroll_card,
        text="📂 Enroll Audio File",
        style="Primary.TButton",
        command=app._on_enroll_file
    )
    btn_enroll_file.pack(fill="x", pady=(0, 8))

    btn_enroll_demo = ttk.Button(
        enroll_card,
        text="🧪 Enroll Synthetic Demo Sample",
        style="Secondary.TButton",
        command=app._on_enroll_demo
    )
    btn_enroll_demo.pack(fill="x", pady=(0, 12))

    lbl_note = tk.Label(
        enroll_card,
        text="ℹ️ Augmentation Ratio:\n1 enrolled audio file yields 5 dataset entries using gain & time-shift augmentation.",
        font=("Segoe UI", 8, "italic"),
        fg=COLOR_TEXT_MUTED,
        bg=COLOR_CARD_BG,
        justify="left"
    )
    lbl_note.pack(anchor="w")

    # Center Column: Enrolled Dataset Table
    ds_card = tk.Frame(grid_frame, bg=COLOR_CARD_BG, padx=12, pady=12, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    ds_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

    ds_head = tk.Frame(ds_card, bg=COLOR_CARD_BG)
    ds_head.pack(fill="x", pady=(0, 8))

    lbl_ds_title = tk.Label(ds_head, text="📋 Enrolled Dataset Samples", font=("Segoe UI", 10, "bold"), fg=COLOR_CYAN, bg=COLOR_CARD_BG)
    lbl_ds_title.pack(side="left")

    btn_clear_ds = ttk.Button(
        ds_head,
        text="🗑️ Clear Dataset",
        style="Danger.TButton",
        command=app._on_clear_dataset
    )
    btn_clear_ds.pack(side="right")

    columns = ("sample_id", "sample_name", "label_text", "window_count", "timestamp")
    app.ds_tree = ttk.Treeview(ds_card, columns=columns, show="headings", height=12)

    app.ds_tree.heading("sample_id", text="Sample ID")
    app.ds_tree.heading("sample_name", text="Sample Tag Name")
    app.ds_tree.heading("label_text", text="Label Category")
    app.ds_tree.heading("window_count", text="Windows")
    app.ds_tree.heading("timestamp", text="UTC Enrolled")

    app.ds_tree.column("sample_id", width=95, anchor="center")
    app.ds_tree.column("sample_name", width=150, anchor="w")
    app.ds_tree.column("label_text", width=130, anchor="center")
    app.ds_tree.column("window_count", width=65, anchor="center")
    app.ds_tree.column("timestamp", width=125, anchor="center")

    ds_scrollbar = ttk.Scrollbar(ds_card, orient="vertical", command=app.ds_tree.yview)
    app.ds_tree.configure(yscrollcommand=ds_scrollbar.set)

    app.ds_tree.pack(side="left", fill="both", expand=True)
    ds_scrollbar.pack(side="right", fill="y")

    # Right Column: Model Training Control Card
    train_card = tk.Frame(grid_frame, bg=COLOR_CARD_BG, padx=14, pady=12, width=270, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
    train_card.pack(side="right", fill="y")
    train_card.pack_propagate(False)

    lbl_tr_head = tk.Label(train_card, text="⚡ Train Local Model", font=("Segoe UI", 10, "bold"), fg=COLOR_CYAN, bg=COLOR_CARD_BG)
    lbl_tr_head.pack(anchor="w", pady=(0, 8))

    app.lbl_train_status = tk.Label(
        train_card,
        text="Active Model: Baseline Default",
        font=("Segoe UI", 9, "bold"),
        fg=COLOR_GREEN,
        bg=COLOR_CARD_BG,
        wraplength=240,
        justify="left"
    )
    app.lbl_train_status.pack(anchor="w", pady=(0, 14))

    btn_train = ttk.Button(
        train_card,
        text="🚀 TRAIN CUSTOM MODEL",
        style="Primary.TButton",
        command=app._on_train_custom_model
    )
    btn_train.pack(fill="x", pady=(0, 14))

    lbl_tr_desc = tk.Label(
        train_card,
        text="Trains a Scikit-Learn Random Forest Classifier on custom enrolled voice samples + acoustic baseline features.\n\nSaves model weights locally to data/models/voice_classifier.pkl.",
        font=("Segoe UI", 8),
        fg=COLOR_TEXT_MUTED,
        bg=COLOR_CARD_BG,
        justify="left",
        wraplength=240
    )
    lbl_tr_desc.pack(anchor="w")

    app._refresh_dataset_table()

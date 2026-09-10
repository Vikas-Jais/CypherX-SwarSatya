"""
SwarSatya (स्वरसत्य) — Voice Security & Truth Engine Native Desktop Application.
Runs directly via `python app.py` as a native Tkinter desktop popup GUI window.
100% local, offline audio processing and Scikit-Learn ML risk classification.
"""

import sys
import os
import time
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np

from config import (
    APP_NAME,
    TAGLINE,
    PROTOTYPE_VERSION,
    LEDGER_PATH,
    REPORTS_DIR,
    COLOR_DEEP_BLUE,
    COLOR_CYAN,
    COLOR_ORANGE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_BG_DARK,
    COLOR_CARD_BG
)
from src.report_exporter import export_scan_report
from src.audio_io import (
    load_audio,
    get_audio_metadata,
    iter_audio_windows,
    generate_synthetic_demo_signal
)
from src.audio_features import extract_window_features
from src.risk_engine import PrototypeRiskEngine
from src.ml_classifier import (
    enroll_audio_sample,
    load_enrolled_dataset,
    clear_enrolled_dataset,
    train_custom_model_from_dataset,
    MODEL_PATH,
    DATASET_PATH
)
from src.ledger import (
    record_incident,
    verify_ledger,
    load_ledger_records,
    clear_ledger,
    generate_pseudonymous_session_id
)
from src.ui_components import (
    apply_tkinter_theme,
    update_risk_axes
)
from src.ui import (
    build_header,
    build_tab_scan,
    build_tab_ledger,
    build_tab_studio,
    build_tab_about
)


class SwarSatyaApp(tk.Tk):
    """
    Main SwarSatya Desktop GUI Popup Application Window.
    """

    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} v{PROTOTYPE_VERSION} — Desktop Security Engine")
        self.geometry("1160x780")
        self.minsize(1000, 700)

        # Apply Modern Custom Dark Theme
        self.style = apply_tkinter_theme(self)

        # Application State
        self.session_id = generate_pseudonymous_session_id()
        self.audio_data = None
        self.sr = 16000
        self.metadata = None
        self.audio_filename = None

        self.scan_results = []
        self.final_score = 0.0
        self.final_status = "SAFE"
        self.final_contributions = []
        self.reported_event = None
        self.is_scanning = False

        self.engine = PrototypeRiskEngine()

        self._build_ui()

    def _build_ui(self):
        """Build main UI layout by assembling modular Tkinter components."""
        # 1. Render Header Component
        build_header(self)

        # 2. Main Tabbed Notebook Navigation
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self.tab_scan = ttk.Frame(self.notebook)
        self.tab_ledger = ttk.Frame(self.notebook)
        self.tab_studio = ttk.Frame(self.notebook)
        self.tab_about = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_scan, text="  🎙️ Live Scan  ")
        self.notebook.add(self.tab_ledger, text="  📜 Incident Ledger  ")
        self.notebook.add(self.tab_studio, text="  🧠 Model Studio  ")
        self.notebook.add(self.tab_about, text="  ℹ️ System Architecture  ")

        # 3. Build Modular Tab Views
        build_tab_scan(self.tab_scan, self)
        build_tab_ledger(self.tab_ledger, self)
        build_tab_studio(self.tab_studio, self)
        build_tab_about(self.tab_about, self)

    # ==========================================
    # LIVE CALL SCAN EVENT HANDLERS
    # ==========================================
    def _on_upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Voice Recording File",
            filetypes=[("Audio Files", "*.wav *.flac *.mp3 *.ogg"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            audio, sr = load_audio(file_path, target_sr=16000)
            self.audio_data = audio
            self.sr = sr
            self.metadata = get_audio_metadata(audio, sr)
            self.audio_filename = Path(file_path).name
            self.engine.reset()

            self.lbl_meta_text.config(
                text=(
                    f"📁 Loaded File: {self.audio_filename}  |  "
                    f"⏱️ Duration: {self.metadata['duration_seconds']}s  |  "
                    f"🔊 Rate: {self.sr} Hz  |  "
                    f"⚡ Max Amplitude: {self.metadata['max_amplitude']}"
                ),
                fg=COLOR_CYAN
            )
            if hasattr(self, "waveform_canvas"):
                self.waveform_canvas.set_audio_data(self.audio_data)
            if hasattr(self, "gauge_canvas"):
                self.gauge_canvas.set_score(0.0, "SAFE")

            self.progress_bar["value"] = 0
            self.txt_contrib.delete("1.0", tk.END)
            self.txt_contrib.insert(tk.END, f"• Audio loaded cleanly from path: {self.audio_filename}\n• Click 'Start Live Call Scan' to begin analysis.")

            self.last_chart_draw_time = 0.0
            update_risk_axes(self.ax)
            self.canvas.draw()
            messagebox.showinfo("Audio Loaded", f"Voice recording loaded successfully!\n\nFile: {self.audio_filename}\nDuration: {self.metadata['duration_seconds']} sec")
        except Exception as e:
            messagebox.showerror("Audio Load Error", str(e))

    def _on_generate_demo(self, mode="robotic_synthetic"):
        try:
            audio, sr = generate_synthetic_demo_signal(duration_seconds=5.0, sr=16000, mode=mode)
            self.audio_data = audio
            self.sr = sr
            self.metadata = get_audio_metadata(audio, sr)
            label_text = "AI Synthetic Voice Demo" if mode == "robotic_synthetic" else "Natural Human Voice Demo"
            self.audio_filename = label_text
            self.engine.reset()

            self.lbl_meta_text.config(
                text=(
                    f"🧪 Active Demo Signal: {label_text}  |  "
                    f"⏱️ Duration: {self.metadata['duration_seconds']}s  |  "
                    f"🔊 Rate: {self.sr} Hz"
                ),
                fg=COLOR_ORANGE if mode == "robotic_synthetic" else COLOR_GREEN
            )
            if hasattr(self, "waveform_canvas"):
                self.waveform_canvas.set_audio_data(self.audio_data)
            if hasattr(self, "gauge_canvas"):
                self.gauge_canvas.set_score(0.0, "SAFE")

            self.progress_bar["value"] = 0
            self.txt_contrib.delete("1.0", tk.END)
            self.txt_contrib.insert(tk.END, f"• Loaded local demo audio: {label_text}\n• Click 'Start Live Call Scan' to evaluate acoustic profile.")

            self.last_chart_draw_time = 0.0
            update_risk_axes(self.ax)
            self.canvas.draw()
            messagebox.showinfo("Demo Signal Loaded", f"Loaded local demo audio signal: '{label_text}'\nReady for live risk analysis.")
        except Exception as e:
            messagebox.showerror("Signal Generation Error", str(e))

    def _on_start_scan(self):
        if self.audio_data is None:
            messagebox.showwarning("No Audio", "Please upload an audio file or select demo audio first.")
            return

        if self.is_scanning:
            return

        self.is_scanning = True
        self.btn_start_scan.config(state="disabled")
        self.scan_results = []
        self.reported_event = None
        self.last_chart_draw_time = 0.0

        threading.Thread(target=self._run_scan_thread, daemon=True).start()

    def _run_scan_thread(self):
        audio = self.audio_data
        sr = self.sr

        windows = list(iter_audio_windows(audio, sr, window_seconds=1.0, hop_seconds=0.25))
        total_windows = len(windows)
        prev_features = None

        for idx, (start_t, end_t, chunk) in enumerate(windows):
            features = extract_window_features(chunk, sr=sr)
            score_res = self.engine.score_window(features, prev_features)

            raw_score = score_res["raw_score"]
            skipped = score_res["skipped"]
            contributions = score_res["contributions"]

            smoothed_score = self.engine.update_ema(raw_score, skipped=skipped)
            current_status = self.engine.classify(smoothed_score)

            prev_features = features

            item = {
                "time": round(end_t, 2),
                "speech_activity": features["speech_activity"],
                "raw_risk": raw_score,
                "smoothed_risk": smoothed_score,
                "status": current_status,
                "contributions": contributions
            }
            self.scan_results.append(item)

            progress_pct = int(((idx + 1) / total_windows) * 100)
            is_last = (idx == total_windows - 1)
            
            self.after(0, lambda p=progress_pct, it=item, c=contributions, last=is_last: self._update_scan_gui(p, it, c, is_final=last))
            time.sleep(0.04)

        self.final_score = self.engine.ema_score
        self.final_status = self.engine.classify(self.engine.ema_score)
        self.final_contributions = self.engine.explain(contributions)

        self.after(0, self._on_scan_complete)

    def _update_scan_gui(self, progress_pct, current_item, contributions, is_final: bool = False):
        self.progress_bar["value"] = progress_pct
        
        status = current_item["status"]
        score = current_item["smoothed_risk"]

        if hasattr(self, "gauge_canvas"):
            self.gauge_canvas.set_score(score, status)
        if hasattr(self, "waveform_canvas"):
            self.waveform_canvas.draw_waveform(active_progress=progress_pct / 100.0)

        self.lbl_metric_time.config(text=f"⏱️ Timestamp: {current_item['time']}s / {self.metadata['duration_seconds']}s")
        self.lbl_metric_activity.config(text=f"📊 Speech Activity: {current_item['speech_activity']*100:.0f}%")
        self.lbl_metric_raw.config(text=f"⚡ Raw Window Score: {current_item['raw_risk']*100:.1f}%")

        self.txt_contrib.delete("1.0", tk.END)
        for c in contributions:
            self.txt_contrib.insert(tk.END, f"• {c}\n")

        now = time.time()
        if is_final or (now - getattr(self, "last_chart_draw_time", 0.0) > 0.15):
            self.last_chart_draw_time = now
            df = pd.DataFrame(list(self.scan_results))
            update_risk_axes(self.ax, df)
            self.canvas.draw_idle()

    def _on_scan_complete(self):
        self.is_scanning = False
        self.btn_start_scan.config(state="normal")
        
        event = record_incident(
            final_risk_score=self.final_score,
            alert_level=self.final_status,
            session_id=self.session_id,
            ledger_file=LEDGER_PATH
        )
        self.reported_event = event
        self._refresh_ledger_table()

        # Automatic Export of CSV Markings & Trajectory Graph PNG
        report_info = export_scan_report(
            audio_filename=self.audio_filename or "test_audio",
            scan_results=self.scan_results,
            final_score=self.final_score,
            final_status=self.final_status,
            fig=self.fig,
            session_id=self.session_id
        )

        msg = (
            f"Call Scan Completed!\n\n"
            f"Verdict Status: {self.final_status} ({self.final_score*100:.1f}%)\n\n"
            f"📊 CSV Markings & Graph Saved:\n"
            f"• Test Folder: data/reports/{report_info['folder_path'].name}\n"
            f"• CSV Results: {report_info['csv_path'].name}\n"
            f"• Graph Image: {report_info['graph_path'].name}\n\n"
            f"📝 Audit Record Logged:\n"
            f"• Event ID: {event['event_id']}\n"
            f"• SHA-256 Hash: {event['record_hash'][:20]}..."
        )
        messagebox.showinfo("Scan Complete — CSV & Graph Saved", msg)

    def _on_open_reports_folder(self):
        import subprocess
        try:
            folder_str = str(REPORTS_DIR.resolve())
            if os.name == 'nt':
                os.startfile(folder_str)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', folder_str])
            else:
                subprocess.Popen(['xdg-open', folder_str])
        except Exception as e:
            messagebox.showerror("Open Folder Error", str(e))

    def _show_safety_guidance(self):
        guidance = (
            "🛡️ RECOMMENDED IMMEDIATE DEFENSE STEPS:\n\n"
            "1. 📞 Hang Up & Call Back:\n"
            "   Never rely on incoming call numbers. Call back using an official number from a bank card, bill, or official site.\n\n"
            "2. 🔑 Protect Credentials:\n"
            "   Never share OTPs, PINs, passwords, or personal security answers over voice calls.\n\n"
            "3. 💬 Use Secondary Channel:\n"
            "   Contact the individual via a trusted secondary channel (family group, SMS, alternative messaging)."
        )
        messagebox.showwarning("Safety Defense Guidance", guidance)

    def _on_report_fraud(self):
        if not self.scan_results:
            messagebox.showwarning("No Scan", "Please run a call scan first.")
            return

        event = record_incident(
            final_risk_score=self.final_score,
            alert_level=self.final_status,
            session_id=self.session_id,
            ledger_file=LEDGER_PATH
        )
        self.reported_event = event
        self._refresh_ledger_table()

        cert_msg = (
            f"✅ Incident Metadata Logged to Cryptographic SHA-256 Ledger!\n\n"
            f"Event ID: {event['event_id']}\n"
            f"Session ID: {event['session_id']}\n"
            f"Timestamp (UTC): {event['timestamp_utc']}\n"
            f"SHA-256 Hash: {event['record_hash'][:24]}...\n"
            f"Previous Hash: {event['previous_hash'][:24]}..."
        )
        messagebox.showinfo("Incident Logged", cert_msg)

    # ==========================================
    # AUDIT LEDGER EVENT HANDLERS
    # ==========================================
    def _refresh_ledger_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = load_ledger_records(LEDGER_PATH)
        for rec in records:
            self.tree.insert("", "end", values=(
                rec.get("event_id", ""),
                rec.get("timestamp_utc", "")[:19].replace("T", " "),
                rec.get("session_id", ""),
                f"{rec.get('final_risk_score', 0.0)*100:.1f}%",
                rec.get("alert_level", ""),
                f"{rec.get('previous_hash', '')[:12]}...",
                f"{rec.get('record_hash', '')[:12]}..."
            ))

    def _on_verify_ledger(self):
        is_valid, errors = verify_ledger(LEDGER_PATH)
        if is_valid:
            messagebox.showinfo("Ledger Integrity Verified", "✅ LEDGER INTEGRITY VERIFIED!\n\nAll SHA-256 record hashes and previous-hash links match perfectly. No tampering detected.")
        else:
            err_msg = "🚨 LEDGER INTEGRITY BREACH DETECTED!\n\n" + "\n".join(errors)
            messagebox.showerror("Integrity Failure", err_msg)

    def _on_clear_ledger(self):
        confirm = messagebox.askyesno("Clear Ledger", "Are you sure you want to delete the local JSONL incident ledger?")
        if confirm:
            if clear_ledger(LEDGER_PATH):
                self._refresh_ledger_table()
                messagebox.showinfo("Ledger Cleared", "Local incident ledger cleared.")

    # ==========================================
    # NEURAL MODEL STUDIO HANDLERS
    # ==========================================
    def _on_enroll_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Voice Audio File to Enroll",
            filetypes=[("Audio Files", "*.wav *.flac *.mp3 *.ogg"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            audio, sr = load_audio(file_path, target_sr=16000)
            lbl = self.var_label.get()
            sname = self.ent_sample_name.get().strip() or Path(file_path).name

            entries = enroll_audio_sample(audio, sr, label=lbl, sample_name=sname)
            self._refresh_dataset_table()
            messagebox.showinfo(
                "Sample Enrolled (5 Augmented Entries Created)",
                f"Successfully enrolled voice file into dataset!\n\n"
                f"• Tag Name: {sname}\n"
                f"• Label Category: {'AI / Synthetic Voice' if lbl==1 else 'Human Voice'}\n"
                f"• Dataset Entries Added: 5 augmented dataset samples\n"
                f"• Saved To: {DATASET_PATH.resolve()}"
            )
        except Exception as e:
            messagebox.showerror("Enrollment Error", str(e))

    def _on_enroll_demo(self):
        try:
            lbl = self.var_label.get()
            mode = "robotic_synthetic" if lbl == 1 else "natural_human"
            sname_default = "AI Synthetic Demo Audio" if lbl == 1 else "Human Demo Audio"

            audio, sr = generate_synthetic_demo_signal(duration_seconds=6.0, sr=16000, mode=mode)
            sname = self.ent_sample_name.get().strip() or sname_default

            entries = enroll_audio_sample(audio, sr, label=lbl, sample_name=sname)
            self._refresh_dataset_table()
            messagebox.showinfo(
                "Demo Sample Enrolled (5 Augmented Entries Created)",
                f"Successfully enrolled demo voice sample!\n\n"
                f"• Tag Name: {sname}\n"
                f"• Label Category: {'AI / Synthetic Voice' if lbl==1 else 'Human Voice'}\n"
                f"• Dataset Entries Added: 5 augmented dataset samples\n"
                f"• Saved To: {DATASET_PATH.resolve()}"
            )
        except Exception as e:
            messagebox.showerror("Enrollment Error", str(e))

    def _refresh_dataset_table(self):
        for item in self.ds_tree.get_children():
            self.ds_tree.delete(item)

        dataset = load_enrolled_dataset()
        for sample in dataset:
            self.ds_tree.insert("", "end", values=(
                sample.get("sample_id", ""),
                sample.get("sample_name", ""),
                sample.get("label_text", ""),
                sample.get("window_count", 0),
                sample.get("timestamp_utc", "")
            ))

    def _on_clear_dataset(self):
        confirm = messagebox.askyesno("Clear Dataset", "Are you sure you want to delete all custom enrolled voice samples?")
        if confirm:
            if clear_enrolled_dataset():
                self._refresh_dataset_table()
                messagebox.showinfo("Dataset Cleared", "Enrolled voice dataset cleared.")

    def _on_train_custom_model(self):
        try:
            clf, summary = train_custom_model_from_dataset(MODEL_PATH)
            self.engine.classifier.reload_model()

            msg = (
                f"⚡ CUSTOM LOCAL MODEL TRAINED SUCCESSFULLY!\n\n"
                f"• Total Enrolled Dataset Entries: {summary['total_enrolled_samples']}\n"
                f"  - Human Samples: {summary['human_samples']}\n"
                f"  - AI Samples: {summary['ai_samples']}\n"
                f"• Model Training Accuracy: {summary['model_accuracy']}%\n\n"
                f"📁 Saved Model Weights:\n"
                f"• Model File: {summary['model_file_path']}\n"
                f"• Dataset File: {summary['dataset_file_path']}\n\n"
                f"Active model updated! Navigate to Tab 1 (Live Scan) to test your detector!"
            )
            self.lbl_train_status.config(
                text=f"Active Model: Custom Trained (Acc: {summary['model_accuracy']}%, Entries: {summary['total_enrolled_samples']})",
                fg=COLOR_GREEN
            )
            messagebox.showinfo("Model Training Complete", msg)
        except Exception as e:
            messagebox.showerror("Training Error", str(e))


if __name__ == "__main__":
    app = SwarSatyaApp()
    app.mainloop()

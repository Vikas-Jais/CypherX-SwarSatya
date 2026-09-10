# SwarSatya (स्वरसत्य) — Voice Security & Truth Engine 🎙️

> **Tagline:** Real-Time AI Voice Authentication & Tamper-Evident Incident Audit  
> **Version:** 1.0.0 (Native Desktop GUI Prototype)  
> **Execution Mode:** 100% Local Offline Memory Processing (Zero Cloud Dependencies)

---

## 📌 Executive Summary

**SwarSatya (स्वरसत्य)** is a native, offline-capable desktop security application engineered for real-time detection of AI-generated synthetic voice clones and telephony voice fraud. It executes 100% locally in transient host system memory without relying on external cloud APIs or uploading private voice recordings.

The application features:
- **32-Dimensional Acoustic Feature Extraction** (`librosa` & `scipy`)
- **Local Scikit-Learn Random Forest Classifier** (`data/models/voice_classifier.pkl`)
- **Interactive Neural Model Studio** with 1-to-5 audio data augmentation and 1-click re-training
- **Cryptographic SHA-256 Hash-Chained Audit Ledger** (`data/incident_ledger.jsonl`)
- **Futuristic High-Tech Native Dark GUI** (`tkinter`) featuring an interactive Circular Speedometer Arc Gauge, Real-Time Audio Waveform Visualizer, and Matplotlib Risk Score Trajectory Chart.

---

## 🏗️ System Architecture & Data Flow

```
+-----------------------------------------------------------------------------------+
|               SwarSatya Desktop GUI Application (python app.py)                   |
+-----------------------------------------------------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                                                       |
     v                                                                       v
+--------------------------+                               +--------------------------+
|   Local Audio File Input |                               |  Synthetic Demo Signal   |
|   (WAV / MP3 / FLAC)     |                               | Generator (AI / Human)   |
+--------------------------+                               +--------------------------+
             |                                                               |
             +-------------------------------+-------------------------------+
                                             |
                                             v
                                +--------------------------+
                                |  Audio Standardization   |
                                | (16 kHz Mono, float32)   |
                                +--------------------------+
                                             |
                                             v
                                +--------------------------+
                                | 1.0s Sliding Windowing   |
                                |   (0.25s Hop Step)       |
                                +--------------------------+
                                             |
                                             v
                                +--------------------------+
                                | 32-D Feature Extractor   |
                                | Pitch, Spectral, MFCCs   |
                                +--------------------------+
                                             |
                                             v
                                +--------------------------+     +------------------------+
                                |  Scikit-Learn Random     | <---| Tab 3: Model Studio   |
                                |  Forest ML Classifier    |     | (1 File = 5 Samples)   |
                                +--------------------------+     +------------------------+
                                             |
                                             v
                                +--------------------------+
                                |  EMA Trend Smoothing     |
                                |     (alpha = 0.35)       |
                                +--------------------------+
                                             |
                                             v
                                +--------------------------+
                                | Dynamic GUI Render:      |
                                | • Speedometer Arc Gauge  |
                                | • Audio Waveform Visual  |
                                | • Matplotlib Risk Chart  |
                                +--------------------------+
                                             |
                                             +-------------------------------+
                                             | (User Click: "Log Incident")  |
                                             v                               v
                                +--------------------------+     +------------------------+
                                | Actionable Safety Guide  |     | Cryptographic SHA-256  |
                                |   ("Defense Steps")      |     | Local Audit Ledger     |
                                +--------------------------+     +------------------------+
```

---

## 🖥️ Core Dashboard Tabs & Features

### Tab 1: Live Call Scan (🎙️ Live Scan)
- **Audio Source Selection**: Upload custom audio files or generate local demo signals (Human vs. AI synthetic voice).
- **Audio Waveform Canvas (`AudioWaveformCanvas`)**: Displays dynamic audio amplitude spikes across 75+ channels with active scan progress highlights.
- **Speedometer Arc Gauge (`RiskGaugeCanvas`)**: Renders a circular gauge arc with real-time score readouts and status badges (`🟢 SAFE`, `🟠 WARNING`, `🔴 CRITICAL`).
- **Real-Time Trajectory Chart**: Matplotlib dark chart tracking raw window risk vs. smoothed EMA risk ($\alpha=0.35$).
- **Neural Acoustic Attributions**: Explains key decision factors (pitch stability, spectral flatness, formant variances).
- **Automatic CSV & Graph Report Export**: Automatically saves window markings to `data/reports/{timestamp}_{test_name}/scan_results.csv`, graph trajectory PNG to `risk_trajectory_graph.png`, and logs summary entries to `master_scan_history.csv`. Includes 1-click `📂 Open CSV & Graphs` button.
- **Incident Toolbar**: 1-click incident logging to SHA-256 ledger and safety defense guidance popup.

### Tab 2: Cryptographic Incident Ledger (📜 Audit Ledger)
- **Hash-Chained Records**: Every logged scan incorporates the SHA-256 digest of the preceding log entry (`previous_hash -> record_hash`).
- **Integrity Verifier**: 1-click SHA-256 audit chain verification to detect unauthorized tampering or log modification.
- **Session Tracking**: Records event ID, UTC timestamp, pseudonymous session ID, and risk level.

### Tab 3: Neural Model Studio (🧠 Model Studio)
- **Voice Sample Enrollment**: Enroll custom voice samples with custom speaker tags and target categories (`Human Voice` vs `AI Voice`).
- **1-to-5 Data Augmentation**: Each enrolled audio file automatically creates 5 augmented dataset entries using gain scaling and time-shifting.
- **1-Click Model Training**: Re-trains the local Random Forest Classifier instantly and updates the active scanning model weights in memory without restarting the application.

### Tab 4: System Architecture & Privacy (ℹ️ System Info)
- Comprehensive technical documentation detailing the 32-D feature vector, ML model parameters, privacy guarantees, and safety classification policies.

---

## 🔬 How It Works (Under the Hood)

### 1. 32-Dimensional Acoustic Feature Extraction
For every 1.0-second time window, the system computes:
- **Pitch Dynamics (4 features)**: Fundamental frequency ($F_0$) mean, std, variance, and voiced frame ratio via YIN algorithm.
- **Spectral Geometry (4 features)**: Spectral Centroid, Spectral Bandwidth, Spectral Flatness, and Spectral Rolloff.
- **Timbral Formants (27 features)**: 13 MFCC means, 13 MFCC standard deviations, and overall average MFCC variance.
- **Energy & Voicing (3 features)**: RMS energy, Zero Crossing Rate (ZCR) mean & std, and speech activity ratio.

### 2. Differential Risk Engine & EMA Smoothing
- **Random Forest Prediction**: Predicts probability $P(\text{synthetic})$ for each active speech window.
- **Exponential Moving Average (EMA)**:
  $$\text{EMA}_t = \alpha \cdot \text{Score}_t + (1 - \alpha) \cdot \text{EMA}_{t-1} \quad (\alpha = 0.35)$$
- **Calibrated Thresholds**:
  - `SAFE`: Risk Score $< 0.50$ (🟢 Emerald)
  - `WARNING`: Risk Score $0.50 - 0.699$ (🟠 Saffron)
  - `CRITICAL`: Risk Score $\ge 0.70$ (🔴 Crimson)

---

## 📁 Codebase Directory Structure

```text
SHI-SIH/
├── app.py                  # Main Desktop Application GUI Entry Point (python app.py)
├── config.py               # Application settings, dark theme palette, risk thresholds
├── requirements.txt        # Pure desktop Python dependencies
├── run_app.bat             # One-click Windows launcher script
├── run_tests.bat           # One-click Windows test runner script
├── README.md               # Application documentation
├── data/
│   ├── dataset/            # Custom enrolled voice dataset (.pkl)
│   ├── models/             # Local Scikit-Learn Random Forest model weights (.pkl)
│   └── reports/            # CSV markings & graph PNG image export directory
├── src/
│   ├── __init__.py
│   ├── audio_io.py         # Audio loading, 16kHz resampling, sliding window generator
│   ├── audio_features.py   # 32-D acoustic feature vector extractor
│   ├── risk_engine.py      # Differential risk engine & EMA smoothing
│   ├── ml_classifier.py    # Random Forest training, reload & 1-to-5 augmentation
│   ├── report_exporter.py  # Automatic CSV markings exporter & PNG graph image saver
│   ├── ledger.py           # SHA-256 hash-chained incident ledger & verifier
│   ├── ui_components.py    # RiskGaugeCanvas, AudioWaveformCanvas, TTK styles & plot rendering
│   └── ui/                 # Modular GUI View Components
│       ├── __init__.py
│       ├── header.py       # Futuristic masthead & security status bar
│       ├── tab_scan.py     # Live Call Scan view (Tab 1)
│       ├── tab_ledger.py   # Audit Ledger view (Tab 2)
│       ├── tab_studio.py   # Model Studio view (Tab 3)
│       └── tab_about.py    # Architecture & methodology view (Tab 4)
└── tests/
    ├── __init__.py
    ├── test_audio_features.py
    ├── test_audio_io.py
    ├── test_ledger.py
    ├── test_ml_classifier.py
    ├── test_report_exporter.py
    └── test_risk_engine.py
```

---

## 🚀 Quickstart Guide

### 1. Requirements
- **Python 3.10+** (Tested on Python 3.10 – 3.14)
- Windows, macOS, or Linux

### 2. Setup Virtual Environment
```powershell
cd c:\Users\Admin\Downloads\Coder\SHI\SHI-SIH
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Run Automated Unit Tests (14 Tests)
```powershell
.\venv\Scripts\python.exe -m pytest -v
```
*(Or double-click `run_tests.bat`)*

### 4. Launch Native Desktop App
```powershell
.\venv\Scripts\python.exe app.py
```
*(Or double-click `run_app.bat`)*

---

## 🔒 Privacy & Compliance Assurance

- **100% On-Device Processing**: No raw audio recordings or voice features ever leave the host machine.
- **Tamper-Evident Compliance**: Audit logs store pseudonymous session IDs and cryptographic hash digests for compliance records without exposing biometric voice data.

# SwarSatya (स्वरसत्य) — Comprehensive System Explanation & Technical Guide

> **Project Name:** SwarSatya (Voice Security & Truth Engine)  
> **Target Application:** AI Voice Clone Detection & Telephony Fraud Prevention  
> **Architecture:** 100% Local Offline Desktop Engine (`python app.py`)  
> **Document Purpose:** Complete technical reference and presentation guide for judges, evaluators, and system architects.

---

## 📋 Table of Contents
1. [Problem Statement & Core Value Proposition](#1-problem-statement--core-value-proposition)
2. [End-to-End System Architecture](#2-end-to-end-system-architecture)
3. [The 32-Dimensional Acoustic Feature Pipeline](#3-the-32-dimensional-acoustic-feature-pipeline)
4. [Machine Learning Engine & Model Studio](#4-machine-learning-engine--model-studio)
5. [Risk Scoring & Exponential Moving Average (EMA)](#5-risk-scoring--exponential-moving-average-ema)
6. [Cryptographic SHA-256 Audit Ledger](#6-cryptographic-sha-256-audit-ledger)
7. [High-Tech Desktop User Interface Design](#7-high-tech-desktop-user-interface-design)
8. [Frequently Asked Questions & Evaluation Defense](#8-frequently-asked-questions--evaluation-defense)

---

## 1. Problem Statement & Core Value Proposition

### The Threat
With recent breakthroughs in deep learning and Neural Text-to-Speech (TTS) voice cloning (such as ElevenLabs, Vall-E, Bark, and Tacotron), cybercriminals can now clone a human voice using as little as 3 seconds of audio. This has fueled a surge in:
- **Impression Scams / Emergency Scams**: Impersonating family members in distress to request urgent wire transfers.
- **CEO / Banking Fraud**: Impersonating corporate executives or bank managers to authorize fraudulent transactions.
- **Vishing (Voice Phishing)**: Bypassing voice-biometric authentication systems used by financial institutions.

### Why Existing Solutions Fail
1. **Cloud Latency & Privacy Risks**: Uploading live call audio to third-party cloud APIs introduces unacceptable latency and violates strict privacy regulations (GDPR, DPDP Act).
2. **Caller ID Vulnerability**: Telephone networks rely on easily spoofed SIP headers. Caller ID cannot be trusted.
3. **Black-Box Outputs**: Many existing detectors provide binary outputs without explaining *why* a call was classified as fake.

### The SwarSatya Solution
SwarSatya provides an **offline, local-first voice verification engine**:
- **100% Local Memory Processing**: Audio is processed entirely in RAM on host hardware. Zero audio is sent over the internet.
- **Real-Time 32-D Feature Attribution**: Deconstructs audio into fundamental acoustic properties (pitch stability, MFCCs, spectral geometry) to explain verdicts.
- **Model Studio**: Allows users to enroll local voice samples (1 enrolled file yields 5 augmented dataset entries) and re-train the local classifier with 1 click.
- **Cryptographic SHA-256 Audit Ledger**: Generates immutable, tamper-evident logs for legal and security audit compliance.

---

## 2. End-to-End System Architecture

```
                                +-----------------------------------+
                                |     Voice Input / Call Audio      |
                                |  (WAV / MP3 / FLAC / Demo Signal) |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |    Audio Signal Preprocessing     |
                                | (16 kHz Mono, Float32 Normalize)  |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |   Sliding Window Segmenter        |
                                |  (Window = 1.0s, Hop Step = 0.25s)|
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |   Silence / Activity Filter       |
                                |       (RMS Threshold > 0.015)     |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |  32-D Feature Extraction Engine   |
                                |   • Pitch Inflection (YIN F0)     |
                                |   • Spectral Geometry             |
                                |   • Timbral Formants (26 MFCCs)   |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |  Random Forest ML Classifier      |
                                |  Predicts P(Synthetic) per window |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |  EMA Smoothing Filter (alpha=0.35)|
                                |   EMA_t = a*Score + (1-a)*EMA_t-1 |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |   Real-Time UI & Visualizers      |
                                |   • Circular Arc Gauge            |
                                |   • Audio Waveform Canvas         |
                                |   • Matplotlib Risk Curve         |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |   SHA-256 Hash-Chained Ledger     |
                                | H_n = SHA256(Record_n || H_n-1)   |
                                +-----------------------------------+
```

---

## 3. The 32-Dimensional Acoustic Feature Pipeline

Every 1.0-second audio window is converted into a 32-element floating-point feature vector ($\mathbf{x} \in \mathbb{R}^{32}$):

| Feature Subsystem | Count | Mathematical / Algorithmic Basis | Why It Identifies AI Voice Clones |
| :--- | :---: | :--- | :--- |
| **Pitch & Intonation ($F_0$)** | 4 | YIN Autocorrelation Algorithm (F0 Mean, Std, Variance, Voiced Ratio) | AI voices exhibit unnaturally flat pitch contours, artificial pitch micro-jitter, or sudden robotic frequency jumps. |
| **Spectral Geometry** | 4 | Spectral Centroid, Spectral Bandwidth, Spectral Flatness, Spectral Rolloff | Synthetic vocoders (like HiFi-GAN or WaveGlow) introduce high-frequency phase artifacts and unnatural spectral flatness ratios. |
| **Timbral Formants (MFCCs)** | 27 | 13 MFCC Means + 13 MFCC Std Devs + Average MFCC Variance | Mel-Frequency Cepstral Coefficients capture vocal tract shape. Human vocal tracts create smooth formant transitions, whereas AI models create over-smoothed or noisy cepstral coefficients. |
| **Energy & Voicing** | 3 | RMS Energy, Zero Crossing Rate (ZCR) Mean & Std, Speech Ratio | AI audio often lacks natural breath pauses and background room acoustics, leading to abnormal ZCR distribution. |

---

## 4. Machine Learning Engine & Model Studio

### Model Architecture
- **Algorithm**: Scikit-Learn `RandomForestClassifier` (100 Decision Trees, `max_depth=12`, `random_state=42`).
- **Input Dimensions**: 32 normalized acoustic features.
- **Output**: Calibrated probability score $P(\text{synthetic}) \in [0.0, 1.0]$.
- **Storage**: Saved locally to `data/models/voice_classifier.pkl`.

### Neural Model Studio & 1-to-5 Augmentation Logic
The Model Studio tab (`src/ui/tab_studio.py`) enables Administrators to enroll voice samples and adapt the detector to specific target speakers:

1. **Augmentation Ratio (1 File = 5 Samples)**:
   When 1 audio file is enrolled, the system generates 5 augmented dataset entries:
   - Sample 1: Original audio window features.
   - Sample 2: Gain boosted (+2.0 dB).
   - Sample 3: Gain attenuated (-2.0 dB).
   - Sample 4: Time-shifted left (0.05s offset).
   - Sample 5: Time-shifted right (0.05s offset).
2. **Weighted Training**:
   Custom enrolled samples are assigned a **10x sample weight** during training so that new voice enrollments instantly dominate model decision boundaries over baseline defaults.

---

## 5. Risk Scoring & Exponential Moving Average (EMA)

To prevent sporadic spike noise or minor coughs/clicks from triggering false alarms, SwarSatya uses an **Exponential Moving Average (EMA)** filter ($\alpha = 0.35$):

$$\text{EMA}_t = \alpha \cdot \text{RawScore}_t + (1 - \alpha) \cdot \text{EMA}_{t-1}$$

### Differential Risk Thresholds
- **`SAFE` (0.0% – 49.9%)**: Natural human voice acoustic patterns confirmed.
- **`WARNING` (50.0% – 69.9%)**: Minor acoustic anomalies detected (potential synthetic artifacts or low-quality channel).
- **`CRITICAL` (70.0% – 100.0%)**: Strong neural voice clone signatures identified (high pitch constancy, unnatural MFCC variances).

---

## 6. Cryptographic SHA-256 Audit Ledger

When a scan completes or an incident is logged, SwarSatya records an immutable audit record in `data/incident_ledger.jsonl`.

### Hash-Chaining Mechanism
Each record incorporates the SHA-256 digest of the previous record:

$$\text{RecordHash}_n = \text{SHA256}\left(\text{EventID}_n \mathbin{\Vert} \text{SessionID}_n \mathbin{\Vert} \text{RiskScore}_n \mathbin{\Vert} \text{Timestamp}_n \mathbin{\Vert} \text{PrevHash}_{n-1}\right)$$

```
+------------------+         +------------------+         +------------------+
|   Record #1      |         |   Record #2      |         |   Record #3      |
| Event ID: EVT-01 |         | Event ID: EVT-02 |         | Event ID: EVT-03 |
| PrevHash: 000... | ------->| PrevHash: HASH-1 | ------->| PrevHash: HASH-2 |
| RecordHash:HASH-1|         | RecordHash:HASH-2|         | RecordHash:HASH-3|
+------------------+         +------------------+         +------------------+
```

### Verification Engine
Clicking **"🔒 Verify Ledger Integrity"** recalculates every hash from index 0 to $N$. If a single character in `incident_ledger.jsonl` is modified externally, the hash chain breaks instantly and highlights the exact tampered row.

---

## 6.5. Automatic CSV Markings & Graph PNG Export Engine

In addition to audit log hashing, SwarSatya automatically generates detailed report exports upon scan completion:
1. **Timestamped Test Directories (`data/reports/{timestamp}_{test_name}/`)**:
   - `scan_results.csv`: Contains window-by-window metrics (`window_time_sec`, `speech_activity_ratio`, `raw_risk_score`, `smoothed_risk_score`, `alert_status`, `acoustic_attributions`, `timestamp_utc`).
   - `risk_trajectory_graph.png`: Saves a 150 DPI high-resolution image of the Matplotlib risk trajectory curve.
2. **Master Scan History (`data/reports/master_scan_history.csv`)**:
   - Appends a summary record of all historical test runs with direct file links for offline audit compliance.
3. **1-Click UI Folder Access**:
   - Clicking **"📂 Open CSV & Graphs"** opens `data/reports/` directly in File Explorer.

---

## 7. High-Tech Desktop User Interface Design

The GUI is built using Python's native `tkinter` framework, heavily styled with custom dark-mode canvas widgets and embedded Matplotlib graphics:

1. **`RiskGaugeCanvas`**: A custom circular arc gauge widget featuring smooth color transitions (Emerald $\rightarrow$ Saffron $\rightarrow$ Crimson) and centered percentage text.
2. **`AudioWaveformCanvas`**: Renders real-time audio amplitude spectrum bars across 75+ channels, highlighting active audio playback.
3. **Real-Time Risk Trajectory Graph**: An embedded Matplotlib canvas showing the smoothed risk curve, warning/critical threshold lines, and alpha gradient fill (`ax.fill_between`).
4. **Actionable Safety Guidance**: 1-click popup providing immediate defense steps (Hang up & call back, verify secondary channels, never disclose OTPs).

---

## 8. Frequently Asked Questions & Evaluation Defense

### Q1: Why did you build a native Tkinter app instead of a web app?
> **Answer:** Privacy and latency. Telephony risk detection requires real-time processing without network round-trips. Running natively via Tkinter ensures 100% local memory execution without web server overhead, browser memory leaks, or cloud privacy vulnerabilities.

### Q2: How does the system handle silence or background noise?
> **Answer:** Every 1.0s window is evaluated for Root Mean Square (RMS) energy. If $\text{RMS} < 0.015$, the window is flagged as silence and skipped by the ML classifier, preventing background room noise from distorting the score.

### Q3: What happens if a bad actor tries to delete audit records?
> **Answer:** The incident ledger uses SHA-256 hash-chaining. Deleting or modifying a record breaks the `previous_hash` link for all subsequent records, allowing the built-in ledger verifier to catch tampering immediately.

### Q4: How fast is the processing pipeline?
> **Answer:** On standard host hardware, 32-D feature extraction and Random Forest inference take less than **10 milliseconds** per 1-second window, enabling real-time live call scanning without lag.

---

## 🛠️ Launch & Verification Commands

```powershell
# Navigate to directory
cd c:\Users\Admin\Downloads\Coder\SHI\SHI-SIH

# Run Automated Test Suite (14 Tests)
.\venv\Scripts\python.exe -m pytest -v

# Launch Desktop Application
.\venv\Scripts\python.exe app.py
```

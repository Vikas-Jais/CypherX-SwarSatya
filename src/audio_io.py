"""
Audio input/output module for loading, standardizing, and streaming audio windows.
"""

import io
from typing import Generator, Tuple, Dict, Any, Union
import numpy as np
import soundfile as sf
import librosa


def load_audio(
    uploaded_file: Union[str, bytes, io.BytesIO],
    target_sr: int = 16000
) -> Tuple[np.ndarray, int]:
    """
    Load an audio file, convert stereo to mono, resample to target_sr Hz,
    and normalize amplitude safely into float32 range [-1.0, 1.0].

    Supports WAV, FLAC, MP3, and OGG files where soundfile/librosa dependencies permit.
    """
    audio_data = None
    orig_sr = None

    # Handle Streamlit UploadedFile or BytesIO
    if hasattr(uploaded_file, "read"):
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        file_bytes = uploaded_file.read()
        buffer = io.BytesIO(file_bytes)
        try:
            audio_data, orig_sr = sf.read(buffer, dtype="float32")
        except Exception as sf_err:
            # Fallback to librosa.load for formats soundfile may fail to parse
            try:
                buffer.seek(0)
                audio_data, orig_sr = librosa.load(buffer, sr=None, mono=False, dtype=np.float32)
                # librosa.load output format for multichannel is (channels, samples)
                if audio_data.ndim > 1:
                    audio_data = audio_data.T
            except Exception as lib_err:
                raise ValueError(
                    f"Could not load audio file. Please convert your file to standard WAV or FLAC format.\n"
                    f"Details: {str(sf_err)} | {str(lib_err)}"
                )
    elif isinstance(uploaded_file, str):
        try:
            audio_data, orig_sr = sf.read(uploaded_file, dtype="float32")
        except Exception as sf_err:
            try:
                audio_data, orig_sr = librosa.load(uploaded_file, sr=None, mono=False, dtype=np.float32)
                if audio_data.ndim > 1:
                    audio_data = audio_data.T
            except Exception as lib_err:
                raise ValueError(
                    f"Could not load audio file from path '{uploaded_file}'. "
                    f"Please verify format (WAV/FLAC recommended)."
                )
    else:
        raise ValueError("Unsupported audio file input format.")

    if audio_data is None or len(audio_data) == 0:
        raise ValueError("Audio file is empty or contains no readable audio data.")

    # Convert Stereo / Multichannel to Mono
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)

    # Ensure 1D float32 array
    audio_data = np.asarray(audio_data, dtype=np.float32)

    # Resample if sample rate does not match target_sr
    if orig_sr != target_sr:
        audio_data = librosa.resample(audio_data, orig_sr=orig_sr, target_sr=target_sr)

    # Peak normalization safely (avoid div by 0)
    max_val = np.max(np.abs(audio_data))
    if max_val > 1e-6:
        audio_data = audio_data / max_val

    return audio_data, target_sr


def get_audio_metadata(audio: np.ndarray, sr: int) -> Dict[str, Any]:
    """
    Compute basic metadata for loaded audio array.
    """
    total_samples = len(audio)
    duration_seconds = float(total_samples) / float(sr)
    max_amplitude = float(np.max(np.abs(audio))) if total_samples > 0 else 0.0
    rms_energy = float(np.sqrt(np.mean(audio**2))) if total_samples > 0 else 0.0

    return {
        "duration_seconds": round(duration_seconds, 2),
        "sample_rate": sr,
        "total_samples": total_samples,
        "max_amplitude": round(max_amplitude, 4),
        "rms_energy": round(rms_energy, 4),
        "channels": 1
    }


def iter_audio_windows(
    audio: np.ndarray,
    sr: int = 16000,
    window_seconds: float = 1.0,
    hop_seconds: float = 0.25
) -> Generator[Tuple[float, float, np.ndarray], None, None]:
    """
    Yield 1.0s sliding windows with a 0.25s hop.
    Yields (start_time_sec, end_time_sec, window_array).
    Pads trailing partial window with zeros if window contains at least 0.25s of audio.
    """
    window_samples = int(sr * window_seconds)
    hop_samples = int(sr * hop_seconds)
    total_samples = len(audio)

    if total_samples == 0:
        return

    start_idx = 0
    while start_idx < total_samples:
        end_idx = start_idx + window_samples
        chunk = audio[start_idx:end_idx]

        start_time = float(start_idx) / float(sr)
        end_time = float(end_idx) / float(sr)

        if len(chunk) < window_samples:
            # Pad with zeros if chunk has sufficient content (>= 0.25 seconds)
            if len(chunk) >= int(sr * 0.25):
                padded_chunk = np.zeros(window_samples, dtype=np.float32)
                padded_chunk[:len(chunk)] = chunk
                yield start_time, end_time, padded_chunk
            break
        else:
            yield start_time, end_time, chunk.astype(np.float32)

        start_idx += hop_samples


def generate_synthetic_demo_signal(
    duration_seconds: float = 5.0,
    sr: int = 16000,
    mode: str = "robotic_synthetic"
) -> Tuple[np.ndarray, int]:
    """
    Generate a local synthetic test audio signal for demonstration purposes.
    This creates an artificial signal with deterministic acoustic characteristics
    (e.g., flat pitch, unnatural spectral uniformity) to trigger the heuristic engine.
    Clearly labeled as an artificial demo signal.
    """
    t = np.linspace(0, duration_seconds, int(sr * duration_seconds), endpoint=False)
    
    if mode == "robotic_synthetic":
        # Constant pitch fundamental (160 Hz) + robotic harmonics with flat pitch envelope
        f0 = 160.0
        signal = 0.4 * np.sin(2 * np.pi * f0 * t)
        signal += 0.2 * np.sin(2 * np.pi * 2 * f0 * t)
        signal += 0.15 * np.sin(2 * np.pi * 3 * f0 * t)
        signal += 0.1 * np.sin(2 * np.pi * 4 * f0 * t)
        
        # Add slight periodic amplitude modulation (speech cadence) but zero pitch variation
        cadence = 0.5 + 0.5 * np.sin(2 * np.pi * 3.0 * t)
        signal = signal * cadence
    else:
        # Natural speech approximation with pitch modulation (vibrato/inflection)
        f0_mod = 150.0 + 30.0 * np.sin(2 * np.pi * 2.5 * t) + 15.0 * np.cos(2 * np.pi * 5.0 * t)
        phase = 2 * np.pi * np.cumsum(f0_mod) / sr
        signal = 0.4 * np.sin(phase) + 0.2 * np.sin(2 * phase)
        cadence = 0.5 + 0.5 * np.sin(2 * np.pi * 2.0 * t)
        signal = signal * cadence

    # Add very faint background noise
    noise = np.random.normal(0, 0.005, len(signal))
    signal = signal + noise
    
    # Normalize peak to 0.9
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        signal = (signal / max_val) * 0.9

    return signal.astype(np.float32), sr

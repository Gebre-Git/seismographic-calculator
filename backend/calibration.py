"""
calibration.py
--------------
Calibration module for the seismographic calculator.

Provides CalibrationParams model and apply_calibration() to keep
calibration logic fully separated from the core simulation physics.
"""

from __future__ import annotations

import numpy as np
from pydantic import BaseModel, Field
from typing import Tuple


# ---------------------------------------------------------------------------
# Calibration parameter model
# ---------------------------------------------------------------------------

class CalibrationParams(BaseModel):
    """
    Adjustable parameters that post-process and tune the simulated waveform.
    
    This model allows decoupling physics simulation from sensor-specific tuning
    or environmental noise factors. It uses Pydantic for validation.
    """

    amplitude_scale: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description="Multiplier applied to the full waveform amplitude to simulate gain.",
    )
    noise_level: float = Field(
        default=0.03,
        ge=0.0,
        le=1.0,
        description="Fraction of peak amplitude used as noise standard deviation (white noise).",
    )
    sensor_sensitivity: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description="Additional gain factor representing electronic sensor sensitivity.",
    )
    baseline_offset: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Constant offset (DC bias) added to the waveform to simulate shift/drift.",
    )
    time_scale: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description=(
            "Factor by which the time axis is stretched. "
            "Values > 1 slow the wave down (stretch); < 1 speed it up (compress)."
        ),
    )


# ---------------------------------------------------------------------------
# Calibration application pipeline
# ---------------------------------------------------------------------------

def apply_calibration(
    waveform: np.ndarray,
    time: np.ndarray,
    params: CalibrationParams,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply a 5-step post-processing pipeline to a simulated waveform.

    This function transforms raw physical displacement data into the 
    'calibrated' signal that would be seen on a real instrument.

    Steps:
    1. Apply primary amplitude scaling.
    2. Apply secondary sensor sensitivity gain.
    3. Generate and inject random noise based on signal peaks.
    4. Shift the baseline (DC offset).
    5. Recalculate time array (time scaling).

    Parameters:
        waveform: 1D numpy array of raw simulated displacement values.
        time: 1D numpy array of time steps from the simulation.
        params: Validated CalibrationParams object.

    Returns:
        A tuple of (calibrated_waveform, calibrated_time).
    """

    # 1. Primary Amplitude scaling (Simulation-level gain)
    calibrated = waveform * params.amplitude_scale

    # 2. Sensor sensitivity (Instrument-level hardware gain layer)
    calibrated = calibrated * params.sensor_sensitivity

    # 3. Calibration noise overlay
    # We use a fraction of peak amplitude so noise feels proportional to signal strength
    peak = float(np.max(np.abs(calibrated))) if len(calibrated) > 0 else 1.0
    calib_noise = np.random.normal(
        0, params.noise_level * peak, size=len(calibrated)
    )
    calibrated = calibrated + calib_noise

    # 4. Baseline offset (Simulating DC bias or sensor drift)
    calibrated = calibrated + params.baseline_offset

    # 5. Time scaling (Stretch/compress the time axis relative to real-time)
    calibrated_time = time * params.time_scale

    return calibrated, calibrated_time


# ---------------------------------------------------------------------------
# Preset calibration profiles
# ---------------------------------------------------------------------------

# Pre-defined configurations for common testing scenarios.
# These are shared with the frontend to populate profile buttons.
PRESETS: dict[str, dict] = {
    "default": {
        "label": "Default",
        "description": "Clean signal with minimal noise and unity gain.",
        "amplitude_scale": 1.0,
        "noise_level": 0.03,
        "sensor_sensitivity": 1.0,
        "baseline_offset": 0.0,
        "time_scale": 1.0,
    },
    "noisy_environment": {
        "label": "Noisy Environment",
        "description": "Simulates heavy environmental interference and slight drift.",
        "amplitude_scale": 1.0,
        "noise_level": 0.35,
        "sensor_sensitivity": 0.8,
        "baseline_offset": 0.1,
        "time_scale": 1.0,
    },
    "high_sensitivity": {
        "label": "High Sensitivity",
        "description": "Boosted gain for detecting weak signals in clean environments.",
        "amplitude_scale": 2.5,
        "noise_level": 0.01,
        "sensor_sensitivity": 3.0,
        "baseline_offset": 0.0,
        "time_scale": 1.0,
    },
    "low_sensitivity": {
        "label": "Low Sensitivity",
        "description": "Dampened response for high-magnitude event monitoring.",
        "amplitude_scale": 0.4,
        "noise_level": 0.05,
        "sensor_sensitivity": 0.3,
        "baseline_offset": 0.0,
        "time_scale": 1.2,
    },
}

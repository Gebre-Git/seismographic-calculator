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
    """Adjustable parameters that post-process / tune the simulated waveform."""

    amplitude_scale: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description="Multiplier applied to the full waveform amplitude.",
    )
    noise_level: float = Field(
        default=0.03,
        ge=0.0,
        le=1.0,
        description="Fraction of peak amplitude used as noise standard deviation.",
    )
    sensor_sensitivity: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description="Gain factor representing sensor sensitivity.",
    )
    baseline_offset: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Constant offset (DC bias) added to the waveform.",
    )
    time_scale: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description=(
            "Factor by which the time axis is stretched. "
            "Values > 1 slow the wave down; < 1 speed it up."
        ),
    )


# ---------------------------------------------------------------------------
# Calibration application
# ---------------------------------------------------------------------------

def apply_calibration(
    waveform: np.ndarray,
    time: np.ndarray,
    params: CalibrationParams,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Post-process a simulated waveform with the given calibration parameters.

    Parameters
    ----------
    waveform : np.ndarray
        Raw simulated displacement values.
    time : np.ndarray
        Corresponding time array produced by the simulation.
    params : CalibrationParams
        Calibration parameters to apply.

    Returns
    -------
    (calibrated_waveform, calibrated_time) as a tuple of np.ndarray.
    """

    # 1. Amplitude scaling
    calibrated = waveform * params.amplitude_scale

    # 2. Sensor sensitivity (additional gain layer)
    calibrated = calibrated * params.sensor_sensitivity

    # 3. Calibration noise overlay
    peak = float(np.max(np.abs(calibrated))) if len(calibrated) > 0 else 1.0
    calib_noise = np.random.normal(
        0, params.noise_level * peak, size=len(calibrated)
    )
    calibrated = calibrated + calib_noise

    # 4. Baseline offset (DC shift)
    calibrated = calibrated + params.baseline_offset

    # 5. Time scaling (stretch / compress the time axis)
    calibrated_time = time * params.time_scale

    return calibrated, calibrated_time


# ---------------------------------------------------------------------------
# Preset calibration profiles
# ---------------------------------------------------------------------------

PRESETS: dict[str, dict] = {
    "default": {
        "label": "Default",
        "amplitude_scale": 1.0,
        "noise_level": 0.03,
        "sensor_sensitivity": 1.0,
        "baseline_offset": 0.0,
        "time_scale": 1.0,
    },
    "noisy_environment": {
        "label": "Noisy Environment",
        "amplitude_scale": 1.0,
        "noise_level": 0.35,
        "sensor_sensitivity": 0.8,
        "baseline_offset": 0.1,
        "time_scale": 1.0,
    },
    "high_sensitivity": {
        "label": "High Sensitivity",
        "amplitude_scale": 2.5,
        "noise_level": 0.01,
        "sensor_sensitivity": 3.0,
        "baseline_offset": 0.0,
        "time_scale": 1.0,
    },
    "low_sensitivity": {
        "label": "Low Sensitivity",
        "amplitude_scale": 0.4,
        "noise_level": 0.05,
        "sensor_sensitivity": 0.3,
        "baseline_offset": 0.0,
        "time_scale": 1.2,
    },
}

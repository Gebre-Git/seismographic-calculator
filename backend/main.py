from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EarthquakeInput(BaseModel):
    magnitude: float
    duration: float
    frequency: float

@app.post("/simulate")
def simulate_quake(data: EarthquakeInput):
    # -------------------------
    # TIME SETTINGS
    # -------------------------
    dt = 0.01  # 100 Hz sampling
    t = np.arange(0, data.duration, dt)

    # -------------------------
    # EARTHQUAKE GROUND MOTION
    # -------------------------
    p_wave = (
        0.3 * data.magnitude *
        np.exp(-0.15 * t) *
        np.sin(2 * np.pi * (data.frequency * 2) * t)
    )

    s_wave = (
        0.6 * data.magnitude *
        np.exp(-0.1 * (t - 1)) *
        np.sin(2 * np.pi * data.frequency * (t - 1))
    )
    s_wave[t < 1] = 0

    surface_wave = (
        data.magnitude *
        np.exp(-0.05 * (t - 2)) *
        np.sin(2 * np.pi * (data.frequency * 0.5) * (t - 2))
    )
    surface_wave[t < 2] = 0

    ground_motion = p_wave + s_wave + surface_wave

    # -------------------------
    # NOISE
    # -------------------------
    noise = np.random.normal(0, 0.05 * data.magnitude, size=len(t))
    ground_motion += noise

    # -------------------------
    # MASS–SPRING–DAMPER
    # -------------------------
    m, k, c = 1.0, 20.0, 5.0
    x, v = 0.0, 0.0
    recorded = []

    ground_acc = np.gradient(np.gradient(ground_motion, dt), dt)

    for a_g in ground_acc:
        a = (-c * v - k * x - m * a_g) / m
        v += a * dt
        x += v * dt
        recorded.append(x)

    recorded = np.array(recorded)

    # -------------------------
    # FFT SIGNAL PROCESSING
    # -------------------------
    fft_vals = np.fft.fft(recorded)
    freqs = np.fft.fftfreq(len(fft_vals), dt)

    # Keep only positive frequencies
    positive = freqs > 0
    freqs = freqs[positive]
    spectrum = np.abs(fft_vals[positive])

    return {
        "time": t.tolist(),
        "waveform": recorded.tolist(),
        "frequency": freqs.tolist(),
        "spectrum": spectrum.tolist(),
    }


# app.mount("/", StaticFiles(directory="dist", html=True), name="static")

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

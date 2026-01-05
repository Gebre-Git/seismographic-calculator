from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from collections import deque

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#----------------------
# Simulation Part
#----------------------

def magnitude_to_amplitude(magnitude):
    energy = 10 ** (1.5 * magnitude)
    return np.sqrt(energy) / 1e5 


class EarthquakeInput(BaseModel):
    magnitude: float
    duration: float
    frequency: float

@app.post("/simulate")
def simulate_quake(data: EarthquakeInput):

    A = magnitude_to_amplitude(data.magnitude)
    
    dt = 0.01 
    t = np.arange(0, data.duration, dt)

  
    p_wave = (
        0.3 * A *
        np.exp(-0.15 * t) *
        np.sin(2 * np.pi * (data.frequency * 2) * t)
    )

    s_wave = (
        0.6 * A *
        np.exp(-0.1 * (t - 1)) *
        np.sin(2 * np.pi * data.frequency * (t - 1))
    )
    s_wave[t < 1] = 0

    surface_wave = (
        A *
        np.exp(-0.05 * (t - 2)) *
        np.sin(2 * np.pi * (data.frequency * 0.5) * (t - 2))
    )
    surface_wave[t < 2] = 0

    ground_motion = p_wave + s_wave + surface_wave

   
    noise_strength = 0.03 * A
    noise = np.random.normal(0, noise_strength, size=len(t))
    ground_motion += noise

   
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

    fft_vals = np.fft.fft(recorded)
    freqs = np.fft.fftfreq(len(fft_vals), dt)

    positive = freqs > 0
    freqs = freqs[positive]
    spectrum = np.abs(fft_vals[positive])

    return {
        "time": t.tolist(),
        "waveform": recorded.tolist(),
        "frequency": freqs.tolist(),
        "spectrum": spectrum.tolist(),
    }



# ---------------------------------------------------
# real time seismograph processing
# -----------------------------------------------------

sensor_buffer = deque(maxlen=500)
display_clients = set()

SAMPLE_RATE = 20  # Hz
DT = 1 / SAMPLE_RATE

VP = 6.0   # speed of p-waves in km/s
VS = 3.5   # speed of s-waves in km/s


# P waves and S waves filtering

def low_pass(signal, alpha=0.1):
    """S-waves (lower frequency)"""
    filtered = []
    y = signal[0]
    for x in signal:
        y = y + alpha * (x - y)
        filtered.append(y)
    return filtered


def high_pass(signal, alpha=0.1):
    """P-waves (higher frequency)"""
    filtered = []
    y = signal[0]
    prev_x = signal[0]
    for x in signal:
        y = alpha * (y + x - prev_x)
        filtered.append(y)
        prev_x = x
    return filtered


# Numerical Integration

def integrate(signal, dt):
    integrated = np.zeros(len(signal))
    for i in range(1, len(signal)):
        integrated[i] = integrated[i-1] + 0.5 * (signal[i] + signal[i-1]) * dt
    return integrated

# Arrival Detection

def detect_arrival(signal, threshold=0.02):
    """
    Detects first significant wave arrival
    using amplitude threshold.
    """
    for i, v in enumerate(signal):
        if abs(v) > threshold:
            return i
    return None



# signal processing function

def process_signal(buffer):

    if len(buffer) < 50:
        return None

    acc = np.array(buffer, dtype=float)

    acc = acc - np.mean(acc)

    acc = acc / (np.max(np.abs(acc)) + 1e-6)

    velocity = integrate(acc, DT)
    velocity -= np.mean(velocity)

    displacement = integrate(velocity, DT)
    displacement /= np.max(np.abs(displacement)) + 1e-6

    p_wave = high_pass(displacement, alpha=0.25)
    s_wave = low_pass(displacement, alpha=0.03)

    p_idx = detect_arrival(p_wave)
    s_idx = detect_arrival(s_wave)

    distance_km = None

    if p_idx is not None and s_idx is not None and s_idx > p_idx:
        delta_t = (s_idx - p_idx) / SAMPLE_RATE
        distance_km = delta_t / ((1 / VS) - (1 / VP))

    return {
        "raw": acc.tolist(),
        "velocity": velocity.tolist(),
        "displacement": displacement.tolist(),
        "p_wave": p_wave,
        "s_wave": s_wave,
        "distance_km": distance_km
    }


# sensor websocket

@app.websocket("/sensor")
async def sensor_stream(ws: WebSocket):
    await ws.accept()
    print("📱 Sensor connected")

    try:
        while True:
            data = await ws.receive_json()

            ax = float(data["ax"])
            ay = float(data["ay"])
            az = float(data["az"])

            sensor_buffer.append(az)

            if len(sensor_buffer) >= 50:
                processed = process_signal(sensor_buffer)

                if processed:
                    for client in list(display_clients):
                        await client.send_json(processed)

                sensor_buffer.clear()

    except WebSocketDisconnect:
        print("📱 Sensor disconnected")


# display websocket

@app.websocket("/display")
async def display_stream(ws: WebSocket):
    await ws.accept()
    display_clients.add(ws)
    print("🖥️ Display connected")

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        display_clients.discard(ws)
        print("🖥️ Display disconnected")

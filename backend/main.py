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


#----------------------
# WebSocket Part
#----------------------

sensor_buffer = deque(maxlen=500)  
display_clients = set()             

SAMPLE_RATE = 100


# signal processing function

def process_signal(buffer):

    if len(buffer) < 20:
        return None

    signal = np.array(buffer, dtype=float)

    
    signal = signal - np.mean(signal)

    signal = signal / (np.max(np.abs(signal)) + 1e-6)

    return signal.tolist()

# sensor socket (phone)

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

            a = np.sqrt(ax**2 + ay**2 + az**2)
            sensor_buffer.append(a)

            print(f"📥 Buffer size: {len(sensor_buffer)}")

            if len(sensor_buffer) >= 20:
                processed = process_signal(sensor_buffer)

                if processed:
                    print("📤 Broadcasting waveform")

                    for client in list(display_clients):
                        await client.send_json({
                            "waveform": processed
                        })

                sensor_buffer.clear()

    except WebSocketDisconnect:
        print("📱 Sensor disconnected")

# display socket (web client)

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

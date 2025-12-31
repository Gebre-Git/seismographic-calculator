<script setup>
import { ref, onBeforeUnmount } from "vue";

const status = ref("Idle");
const connected = ref(false);

let socket = null;
let motionHandler = null;

function startSensor() {
  if (typeof DeviceMotionEvent !== "undefined" &&
      typeof DeviceMotionEvent.requestPermission === "function") {

    DeviceMotionEvent.requestPermission()
      .then(permission => {
        if (permission === "granted") {
          connectSocket();
        } else {
          status.value = "Motion permission denied";
        }
      })
      .catch(err => {
        status.value = "Permission error";
        console.error(err);
      });

  } else {
    connectSocket();
  }
}

function connectSocket() {
  status.value = "Connecting to backend...";

  // change the IP address and port as needed
  socket = new WebSocket("ws://192.168.8.145:8000/sensor");

  socket.onopen = () => {
    connected.value = true;
    status.value = "Connected — sensor active";

    motionHandler = (event) => {
      if (!event.accelerationIncludingGravity) return;

      const acc = event.accelerationIncludingGravity;

      socket.send(JSON.stringify({
        ax: acc.x || 0,
        ay: acc.y || 0,
        az: acc.z || 0,
        t: Date.now()
      }));
    };

    window.addEventListener("devicemotion", motionHandler);
  };

  socket.onerror = () => {
    status.value = "WebSocket error";
  };

  socket.onclose = () => {
    status.value = "Disconnected";
    connected.value = false;
  };
}

function stopSensor() {
  if (motionHandler) {
    window.removeEventListener("devicemotion", motionHandler);
    motionHandler = null;
  }
  if (socket) {
    socket.close();
    socket = null;
  }
  connected.value = false;
  status.value = "Stopped";
}

onBeforeUnmount(() => {
  stopSensor();
});
</script>

<template>
  <div class="sensor-container">
    <h2>📱 Mobile Seismograph Sensor</h2>

    <p class="status">
      Status:
      <span :class="{ ok: connected, bad: !connected }">
        {{ status }}
      </span>
    </p>

    <button v-if="!connected" @click="startSensor">
      ▶ Start Sensor
    </button>

    <button v-else @click="stopSensor" class="stop">
      ⏹ Stop Sensor
    </button>

    <p class="hint">
      Place the phone on a table and tap nearby to generate vibrations.
    </p>
  </div>
</template>

<style scoped>
.sensor-container {
  min-height: 100vh;
  background: #111;
  color: #eee;
  padding: 20px;
  text-align: center;
}

button {
  padding: 14px 22px;
  font-size: 16px;
  border-radius: 6px;
  border: none;
  margin-top: 15px;
}

button.stop {
  background: #e74c3c;
  color: white;
}

button:not(.stop) {
  background: #2ecc71;
  color: black;
}

.status {
  margin: 10px 0;
}

.ok {
  color: #2ecc71;
}

.bad {
  color: #e67e22;
}

.hint {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #aaa;
}
</style>

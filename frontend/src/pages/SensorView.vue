<script setup>
import { ref, onBeforeUnmount, computed } from "vue";

const status = ref("Idle");
const connected = ref(false);
const loading = ref(false);

let socket = null;
let motionHandler = null;

const statusColor = computed(() => {
  if (connected.value) return "success";
  if (status.value.includes("error") || status.value.includes("denied")) return "error";
  return "warning";
});

function startSensor() {
  loading.value = true;
  if (typeof DeviceMotionEvent !== "undefined" &&
    typeof DeviceMotionEvent.requestPermission === "function") {

    DeviceMotionEvent.requestPermission()
      .then(permission => {
        if (permission === "granted") {
          connectSocket();
        } else {
          status.value = "Motion permission denied";
          loading.value = false;
        }
      })
      .catch(err => {
        status.value = "Permission error";
        loading.value = false;
        console.error(err);
      });

  } else {
    connectSocket();
  }
}

function connectSocket() {
  status.value = "Connecting to backend...";

  socket = new WebSocket("ws://192.168.30.187:8000/sensor");

  socket.onopen = () => {
    connected.value = true;
    loading.value = false;
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
    loading.value = false;
  };

  socket.onclose = () => {
    status.value = "Disconnected";
    connected.value = false;
    loading.value = false;
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
  <v-app theme="dark">
    <v-main class="d-flex justify-center my-2">
      <v-container maxWidth="400">
        <v-card class="pa-6 text-center" elevation="10" rounded="xl">

          <v-icon :icon="connected ? 'mdi-pulse' : 'mdi-cellphone-off'" size="64" :color="statusColor"
            class="mb-4"></v-icon>

          <h2 class="text-h5 font-weight-bold mb-2">Mobile Seismograph</h2>

          <v-chip :color="statusColor" variant="tonal" class="mb-6" label>
            {{ status }}
          </v-chip>

          <div class="mb-6">
            <v-btn v-if="!connected" color="success" size="large" block rounded="lg" :loading="loading"
              prepend-icon="mdi-play" @click="startSensor">
              Start Sensor
            </v-btn>

            <v-btn v-else color="error" size="large" block rounded="lg" prepend-icon="mdi-stop" @click="stopSensor">
              Stop Sensor
            </v-btn>
          </div>

          <v-alert type="info" variant="text" density="compact" icon="mdi-information-outline">
            Place the phone on a table and tap nearby to generate vibrations.
          </v-alert>

        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
.v-main {
  background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
}
</style>
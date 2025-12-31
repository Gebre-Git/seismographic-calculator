<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import Chart from "chart.js/auto";

const canvasRef = ref(null);
let chart = null;
let socket = null;

const MAX_POINTS = 200;

onMounted(() => {
  chart = new Chart(canvasRef.value.getContext("2d"), {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Live Seismograph Signal",
          data: [],
          borderColor: "#2ecc71",
          borderWidth: 2,
          pointRadius: 0,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: { display: false },
        y: {
          suggestedMin: -1,
          suggestedMax: 1,
          title: { display: true, text: "Normalized Amplitude" }
        }
      }
    }
  });

  connectSocket();
});

function connectSocket() {

  // change the IP address and port as needed
  socket = new WebSocket("ws://192.168.8.145:8000/display");

  socket.onopen = () => {
    console.log("🖥️ Display connected to backend");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (!data.waveform) return;

    data.waveform.forEach((value) => {
      chart.data.labels.push("");
      chart.data.datasets[0].data.push(value);

      if (chart.data.datasets[0].data.length > MAX_POINTS) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
      }
    });

    chart.update("none");
  };

  socket.onclose = () => {
    console.warn("🖥️ Display disconnected");
  };
}

onBeforeUnmount(() => {
  if (socket) socket.close();
  if (chart) chart.destroy();
});
</script>

<template>
  <div class="display-container">
    <h2>🖥️ Real-Time Digital Seismograph</h2>
    <p class="subtitle">
      Live ground vibration data streamed from mobile sensor
    </p>

    <div class="chart-wrapper">
      <canvas ref="canvasRef"></canvas>
    </div>
  </div>
</template>

<style scoped>
.display-container {
  background: #0f0f0f;
  color: #eaeaea;
  padding: 20px;
  min-height: 100vh;
}

.subtitle {
  font-size: 0.9rem;
  color: #aaa;
  margin-bottom: 10px;
}

.chart-wrapper {
  height: 400px;
  background: #151515;
  border-radius: 8px;
  padding: 10px;
  border-left: 4px solid #2ecc71;
}
</style>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import Chart from "chart.js/auto";

const rawRef = ref(null);
const pwaveRef = ref(null);
const swaveRef = ref(null);
const dispRef = ref(null);
const velocityRef = ref(null);

let rawChart = null;
let pChart = null;
let sChart = null;
let dChart = null;
let vChart = null;

let socket = null;

const MAX_POINTS = 200;

function createChart(ctx, label, color, yLabel = "Normalized") {
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label,
        data: [],
        borderColor: color,
        borderWidth: 2,
        pointRadius: 0
      }]
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
          title: { display: true, text: yLabel }
        }
      }
    }
  });
}

function updateChart(chart, values) {
  if (!chart || !Array.isArray(values)) return;

  values.forEach(v => {
    chart.data.labels.push("");
    chart.data.datasets[0].data.push(v);

    if (chart.data.datasets[0].data.length > MAX_POINTS) {
      chart.data.labels.shift();
      chart.data.datasets[0].data.shift();
    }
  });

  chart.update("none");
}

onMounted(() => {
  rawChart = createChart(
    rawRef.value.getContext("2d"),
    "Raw Acceleration",
    "#95a5a6"
  );

  pChart = createChart(
    pwaveRef.value.getContext("2d"),
    "P-Wave (High Frequency)",
    "#3498db"
  );

  sChart = createChart(
    swaveRef.value.getContext("2d"),
    "S-Wave (Low Frequency)",
    "#e74c3c"
  );

  dChart = createChart(
    dispRef.value.getContext("2d"),
    "Ground Displacement",
    "#f1c40f",
    "Relative Displacement"
  );

  vChart = createChart(
    velocityRef.value.getContext("2d"),
    "Ground Velocity",
    "#9b59b6",
    "Relative Velocity"
  );

  connectSocket();
});

function connectSocket() {
  socket = new WebSocket("ws://192.168.30.186:8000/display");

  socket.onopen = () => {
    console.log("🖥️ Connected to backend");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (!data) return;

    updateChart(rawChart, data.raw);
    updateChart(pChart, data.p_wave);
    updateChart(sChart, data.s_wave);
    updateChart(dChart, data.displacement);
    updateChart(vChart, data.velocity);
  };

  socket.onclose = () => {
    console.warn("🖥️ WebSocket disconnected");
  };
}

onBeforeUnmount(() => {
  socket?.close();
  rawChart?.destroy();
  pChart?.destroy();
  sChart?.destroy();
  dChart?.destroy();
});
</script>

<template>
  <div class="display-container">
    <h2>🖥️ Real-Time Digital Seismograph</h2>
    <p class="subtitle">
      Live ground vibration data streamed from mobile accelerometer
    </p>

    <div class="chart-wrapper raw">
      <canvas ref="rawRef"></canvas>
    </div>

    <v-divider class="my-4" />

    <div class="chart-wrapper p">
      <canvas ref="pwaveRef"></canvas>
    </div>

    <v-divider class="my-4" />

    <div class="chart-wrapper s">
      <canvas ref="swaveRef"></canvas>
    </div>

    <v-divider class="my-4" />

    <div class="chart-wrapper displacement">
      <canvas ref="dispRef"></canvas>
    </div>

    <v-divider class="my-4" />

    <div class="chart-wrapper velocity">
      <canvas ref="velocityRef"></canvas>
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
  margin-bottom: 16px;
}

.chart-wrapper {
  height: 300px;
  background: #151515;
  border-radius: 8px;
  padding: 10px;
}

.chart-wrapper.raw {
  border-left: 4px solid #95a5a6;
}

.chart-wrapper.p {
  border-left: 4px solid #3498db;
}

.chart-wrapper.s {
  border-left: 4px solid #e74c3c;
}

.chart-wrapper.displacement {
  border-left: 4px solid #f1c40f;
}

.chart-wrapper.velocity {
  border-left: 4px solid #9b59b6;
}
</style>

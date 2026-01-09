<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import Chart from "chart.js/auto";

const rawRef = ref(null);
const pwaveRef = ref(null);
const swaveRef = ref(null);
const dispRef = ref(null);
const velocityRef = ref(null);
const distRef = ref(null);
const mapRef = ref(null);

const distance = ref(null);
const magnitude = ref(null);

const waveTab = ref(0);
const motionTab = ref(0);

let rawChart, pChart, sChart, dChart, vChart, distChart;
let mapCtx, socket;

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
        pointRadius: 0,
        tension: 0.25
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: { display: false },
        y: {
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

function drawEpicenter(radiusKm) {
  const ctx = mapCtx;
  const w = mapRef.value.width;
  const h = mapRef.value.height;

  ctx.fillStyle = "rgba(0,0,0,0.15)";
  ctx.fillRect(0, 0, w, h);

  const maxVisualRadius = Math.min(w, h) * 0.45;
  
  const rangeLimitKm = 200; 

  const r = (radiusKm / rangeLimitKm) * maxVisualRadius * 40;

  ctx.beginPath();
  ctx.arc(w / 2, h / 2, 6, 0, Math.PI * 2);
  ctx.fillStyle = "#2ecc71";
  ctx.fill();

  // Epicenter Circle
  ctx.beginPath();
  ctx.arc(w / 2, h / 2, r, 0, Math.PI * 2);
  ctx.strokeStyle = "#9b59b6";
  ctx.lineWidth = 5;
  ctx.stroke();
}


onMounted(() => {
  rawChart = createChart(rawRef.value.getContext("2d"), "Raw Acceleration", "#95a5a6");
  pChart   = createChart(pwaveRef.value.getContext("2d"), "P-Wave", "#3498db");
  sChart   = createChart(swaveRef.value.getContext("2d"), "S-Wave", "#e74c3c");
  dChart   = createChart(dispRef.value.getContext("2d"), "Displacement", "#f1c40f", "Displacement");
  vChart   = createChart(velocityRef.value.getContext("2d"), "Velocity", "#9b59b6", "Velocity");
  distChart= createChart(distRef.value.getContext("2d"), "Epicenter Distance", "#2ecc71", "km");

  mapCtx = mapRef.value.getContext("2d");
  mapCtx.fillStyle = "#000";
  mapCtx.fillRect(0, 0, 250, 250);

  connectSocket();
});

function connectSocket() {
  socket = new WebSocket("ws://192.168.30.187:8000/display");

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    updateChart(rawChart, data.raw);
    updateChart(pChart, data.p_wave);
    updateChart(sChart, data.s_wave);
    updateChart(dChart, data.displacement);
    updateChart(vChart, data.velocity);

    if (data.distance_km !== null) {
      distance.value = data.distance_km.toFixed(1);
      drawEpicenter(data.distance_km);
      updateChart(distChart, [data.distance_km]);
    }

    if (data.magnitude !== null) {
      magnitude.value = data.magnitude;
    }
  };
}

onBeforeUnmount(() => {
  socket?.close();
  rawChart?.destroy();
  pChart?.destroy();
  sChart?.destroy();
  dChart?.destroy();
  vChart?.destroy();
  distChart?.destroy();
});
</script>

<template>
<v-container fluid class="pa-6">

  <!-- HEADER -->
  <v-card class="mb-4" elevation="6">
    <v-card-title class="text-h5">
      Real-Time Digital Seismograph
    </v-card-title>
    <v-card-subtitle>
      Live seismic monitoring & epicenter estimation
    </v-card-subtitle>

    <v-card-text class="d-flex gap-4">
      <v-chip color="deep-purple" variant="elevated" class="mx-2">
        Distance: {{ distance ?? "--" }} km
      </v-chip>

      <v-chip color="blue" variant="elevated" class="mx-2">
        Magnitude: {{ magnitude ? magnitude.toFixed(2) : "--" }}
      </v-chip>
    </v-card-text>
  </v-card>

  <!-- EPICENTER -->
  <v-card class="mb-4" elevation="6">
    <v-card-title>Epicenter (Radial Model)</v-card-title>
    <v-card-text class="d-flex justify-center">
      <div class="map-container">
        <canvas ref="mapRef" width="250" height="250"></canvas>
      </div>
    </v-card-text>
  </v-card>

  <!-- WAVES -->
  <v-card class="mb-4" elevation="6">
    <v-card-title>Waveform Analysis</v-card-title>

    <v-tabs v-model="waveTab" grow>
      <v-tab>Raw</v-tab>
      <v-tab>P-Wave</v-tab>
      <v-tab>S-Wave</v-tab>
    </v-tabs>

    <v-card-text>
      <div v-show="waveTab === 0" class="chart-box"><canvas ref="rawRef"/></div>
      <div v-show="waveTab === 1" class="chart-box"><canvas ref="pwaveRef"/></div>
      <div v-show="waveTab === 2" class="chart-box"><canvas ref="swaveRef"/></div>
    </v-card-text>
  </v-card>

  <!-- MOTION -->
  <v-card class="mb-4" elevation="6">
    <v-card-title>Ground Motion</v-card-title>

    <v-tabs v-model="motionTab" grow>
      <v-tab>Displacement</v-tab>
      <v-tab>Velocity</v-tab>
      <v-tab>Distance</v-tab>
    </v-tabs>

    <v-card-text>
      <div v-show="motionTab === 0" class="chart-box"><canvas ref="dispRef"/></div>
      <div v-show="motionTab === 1" class="chart-box"><canvas ref="velocityRef"/></div>
      <div v-show="motionTab === 2" class="chart-box"><canvas ref="distRef"/></div>
    </v-card-text>
  </v-card>

</v-container>
</template>

<style scoped>
.chart-box {
  height: 280px;
}

.chart-box canvas {
  width: 100% !important;
  height: 100% !important;
}

.map-container {
  width: 250px;
  height: 250px;
}
</style>

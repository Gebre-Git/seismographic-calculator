<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeUnmount } from "vue";
import Chart from "chart.js/auto";

const magnitude = ref(5);
const duration = ref(10);
const frequent = ref(2);

const historicalCanvas = ref(null);
const liveCanvas = ref(null);
let historicalChart = null;
let liveChart = null;
let intervalId = null;

const fftCanvas = ref(null);
let fftChart = null;


onMounted(() => {
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    elements: { point: { radius: 0 } },
    scales: { x: { display: false }, y: { suggestedMin: -10, suggestedMax: 10 } }
  };

  historicalChart = new Chart(historicalCanvas.value.getContext('2d'), {
    type: "line",
    data: { labels: [], datasets: [{ label: "Static Analysis", data: [], borderColor: "#3498db", borderWidth: 1 }] },
    options: commonOptions
  });

  liveChart = new Chart(liveCanvas.value.getContext('2d'), {
    type: "line",
    data: { labels: [], datasets: [{ label: "Live Feed", data: [], borderColor: "#2ecc71", borderWidth: 2 }] },
    options: { ...commonOptions, animation: false }
  });

  fftChart = new Chart(fftCanvas.value.getContext("2d"), {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "Frequency Spectrum (FFT)",
        data: [],
        borderColor: "#e74c3c",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      elements: { point: { radius: 0 } },
      scales: {
        x: { title: { display: true, text: "Frequency (Hz)" } },
        y: { title: { display: true, text: "Amplitude" } }
      }
    }
  });

});

async function simulate() {
  if (intervalId) clearInterval(intervalId);

  try {
    const response = await axios.post("http://127.0.0.1:8000/simulate", {
      magnitude: magnitude.value,
      duration: duration.value,
      frequency: frequent.value
    });

    const { time, waveform, frequency, spectrum } = response.data;

    historicalChart.data.labels = time;
    historicalChart.data.datasets[0].data = waveform;
    historicalChart.update();

    fftChart.data.labels = frequency;
    fftChart.data.datasets[0].data = spectrum;
    fftChart.update();


    liveChart.data.labels = [];
    liveChart.data.datasets[0].data = [];
    let currentIndex = 0;

    intervalId = setInterval(() => {
      if (currentIndex < waveform.length) {
        liveChart.data.labels.push("");
        liveChart.data.datasets[0].data.push(waveform[currentIndex]);

        if (liveChart.data.datasets[0].data.length > 80) {
          liveChart.data.labels.shift();
          liveChart.data.datasets[0].data.shift();
        }

        liveChart.update('none');
        currentIndex++;
      } else {
        clearInterval(intervalId);
      }
    }, 25);

  } catch (error) {
    console.error("Simulation error", error);
  }
}

onBeforeUnmount(() => { if (intervalId) clearInterval(intervalId); });
</script>

<template>
  <div>
    <v-card class="my-5 mx-5 pa-4">
      <v-card-title class="text-h4"><strong>Digital Seismograph Suite</strong></v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <v-text-field type="number" v-model="duration" label="Duration (seconds)"></v-text-field>
            <!-- <v-range-slider v-model="duration" step="1"></v-range-slider> -->
          </v-col>
          <v-col>
            <v-text-field type="number" v-model="magnitude" label="Magnitude"></v-text-field>
          </v-col>
          <v-col>
            <v-text-field type="number" v-model="frequent" label="Frequency (Hz)"></v-text-field>
          </v-col>
          <v-col>
            <v-btn color="primary" @click="simulate" block size="large" class="mt-2">Run Simulation</v-btn>
          </v-col>
        </v-row>

        <v-divider class="my-2"></v-divider>

        <v-row>
          <v-col cols="6">
            <div class="chart-card">
              <h3>Historical Waveform (Rendered)</h3>
              <p>Full dataset visualization for geological analysis.</p>
              <div class="canvas-container">
                <canvas ref="historicalCanvas"></canvas>
              </div>
            </div>
          </v-col>

          <v-col cols="6">
            <div class="chart-card live">
              <h3>Real-Time Seismograph (Live)</h3>
              <p>Simulated sensor telemetry from the epicenter.</p>
              <div class="canvas-container">
                <canvas ref="liveCanvas"></canvas>
              </div>
            </div>
          </v-col>
        </v-row>
        <v-row class="mt-4">
          <v-col cols="12">
            <div class="chart-card">
              <h3>Frequency Spectrum (FFT Analysis)</h3>
              <p>Frequency-domain representation of seismic energy.</p>
              <div class="canvas-container">
                <canvas ref="fftCanvas"></canvas>
              </div>
            </div>
          </v-col>
        </v-row>

      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
.chart-card {
  background: #1e1e1e;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #333;
}

.live {
  border-left: 4px solid #2ecc71;
}

.canvas-container {
  height: 350px;
  margin-top: 10px;
}

h3 {
  margin: 0;
  color: #bbb;
}

p {
  font-size: 0.8rem;
  color: #666;
}
</style>
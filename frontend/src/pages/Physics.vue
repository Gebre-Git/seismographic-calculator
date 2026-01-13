<script setup>
import { ref } from "vue";

const sections = [
  {
    title: "Raw Acceleration",
    color: "grey",
    formula: "a(t) = √(aₓ² + aᵧ² + a_z²)",
    explanation: `
The smartphone accelerometer measures acceleration along three axes.
We compute the magnitude to obtain orientation-independent ground motion.
This signal represents raw ground acceleration.
    `,
    output: "Raw Acceleration Graph"
  },
  {
    title: "Signal Normalization",
    color: "blue-grey",
    formula: "aₙ(t) = (a(t) − μ) / max(|a(t)|)",
    explanation: `
The raw signal contains bias and gravity effects.
We remove the mean and normalize to stabilize visualization
and enable filtering without scale distortion.
    `,
    output: "Normalized Acceleration"
  },
  {
    title: "P-Wave Extraction (High-Pass Filter)",
    color: "blue",
    formula: "P(t) = HPF(aₙ(t))",
    explanation: `
P-waves arrive first and contain higher frequency components.
A high-pass filter isolates these rapid oscillations.
    `,
    output: "P-Wave Graph"
  },
  {
    title: "S-Wave Extraction (Low-Pass Filter)",
    color: "red",
    formula: "S(t) = LPF(aₙ(t))",
    explanation: `
S-waves arrive later and dominate lower frequencies.
A low-pass filter enhances shear-wave motion.
    `,
    output: "S-Wave Graph"
  },
  {
    title: "Velocity (Numerical Integration)",
    color: "purple",
    formula: "v(t) = ∫ a(t) dt",
    explanation: `
Ground velocity is obtained by numerically integrating acceleration
using the trapezoidal method.
    `,
    output: "Velocity Graph"
  },
  {
    title: "Displacement (Double Integration)",
    color: "amber",
    formula: "x(t) = ∫ v(t) dt",
    explanation: `
Displacement represents actual ground movement.
It is computed by integrating velocity over time.
This is used for magnitude estimation.
    `,
    output: "Displacement Graph"
  },
  {
    title: "Epicenter Distance Estimation",
    color: "green",
    formula: "D = Δt / (1/Vs − 1/Vp)",
    explanation: `
The time difference between P-wave and S-wave arrivals
is used to estimate the distance to the epicenter.
Typical velocities:
Vp ≈ 6 km/s, Vs ≈ 3.5 km/s.
    `,
    output: "Distance Graph & Radial Map"
  },
  {
    title: "Magnitude Estimation",
    color: "indigo",
    formula: "M ≈ log₁₀(A) + C",
    explanation: `
Magnitude is estimated from peak ground displacement.
This follows a simplified Richter-like logarithmic model.
    `,
    output: "Magnitude Indicator"
  }
];
</script>

<template>
<v-container fluid class="pa-6">

  <v-card elevation="8" class="mb-6">
    <v-card-title class="text-h5">
      📐 Seismic Computation & Physics Model
    </v-card-title>
    <v-card-subtitle>
      Mathematical formulation and processing pipeline
    </v-card-subtitle>
  </v-card>

  <v-row dense>
    <v-col
      v-for="(sec, i) in sections"
      :key="i"
      cols="12"
      md="6"
    >
      <v-card elevation="6" class="h-100">
        <v-card-title>
          <v-chip :color="sec.color" variant="elevated" class="mr-2">
            {{ i + 1 }}
          </v-chip>
          {{ sec.title }}
        </v-card-title>

        <v-card-text>
          <v-alert type="info" variant="tonal" class="mb-3">
            <strong>Formula:</strong><br/>
            <code>{{ sec.formula }}</code>
          </v-alert>

          <p class="mb-3" style="white-space: pre-line;">
            {{ sec.explanation }}
          </p>

          <v-chip color="deep-purple" variant="outlined">
            Output: {{ sec.output }}
          </v-chip>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

</v-container>
</template>

<style scoped>
code {
  font-size: 1rem;
  background: #111;
  padding: 6px 10px;
  border-radius: 6px;
  display: inline-block;
}
</style>

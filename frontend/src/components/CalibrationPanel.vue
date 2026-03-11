<script setup>
import { ref, reactive, watch, defineEmits } from 'vue';

// Define events to communicate with the parent (Simulation.vue)
const emit = defineEmits(['calibration-change']);

// ---------------------------------------------------------------------------
// Preset definitions (Must mirror backend/calibration.py PRESETS)
// ---------------------------------------------------------------------------
const PRESETS = {
  default: {
    label: 'Default',
    amplitude_scale: 1.0,
    noise_level: 0.03,
    sensor_sensitivity: 1.0,
    baseline_offset: 0.0,
    time_scale: 1.0,
  },
  noisy_environment: {
    label: 'Noisy Environment',
    amplitude_scale: 1.0,
    noise_level: 0.35,
    sensor_sensitivity: 0.8,
    baseline_offset: 0.1,
    time_scale: 1.0,
  },
  high_sensitivity: {
    label: 'High Sensitivity',
    amplitude_scale: 2.5,
    noise_level: 0.01,
    sensor_sensitivity: 3.0,
    baseline_offset: 0.0,
    time_scale: 1.0,
  },
  low_sensitivity: {
    label: 'Low Sensitivity',
    amplitude_scale: 0.4,
    noise_level: 0.05,
    sensor_sensitivity: 0.3,
    baseline_offset: 0.0,
    time_scale: 1.2,
  },
};

// Convert PRESETS object to a flat array for v-for rendering
const presetOptions = Object.entries(PRESETS).map(([key, val]) => ({
  value: key,
  title: val.label,
}));

// ---------------------------------------------------------------------------
// Reactive calibration state
// ---------------------------------------------------------------------------
const DEFAULT_PARAMS = {
  amplitude_scale: 1.0,
  noise_level: 0.03,
  sensor_sensitivity: 1.0,
  baseline_offset: 0.0,
  time_scale: 1.0,
};

// 'params' holds the local working copy of calibration values
const params = reactive({ ...DEFAULT_PARAMS });
const selectedPreset = ref('default');

// 'pendingChanges' is true if the sliders were moved but 'Apply' wasn't clicked
const pendingChanges = ref(false);

// ---------------------------------------------------------------------------
// Slider configurations (Declarative UI pattern)
// ---------------------------------------------------------------------------
const sliders = [
  {
    key: 'amplitude_scale',
    label: 'Amplitude Scale',
    unit: '×',
    min: 0.1,
    max: 5.0,
    step: 0.1,
    description: 'Scales the overall waveform amplitude',
  },
  {
    key: 'noise_level',
    label: 'Noise Level',
    unit: '',
    min: 0.0,
    max: 1.0,
    step: 0.01,
    description: 'Fraction of peak amplitude used as noise',
  },
  {
    key: 'sensor_sensitivity',
    label: 'Sensor Sensitivity',
    unit: '×',
    min: 0.1,
    max: 5.0,
    step: 0.1,
    description: 'Sensor gain multiplier (Instrument specific)',
  },
  {
    key: 'baseline_offset',
    label: 'Baseline Offset',
    unit: '',
    min: -2.0,
    max: 2.0,
    step: 0.05,
    description: 'DC bias / constant baseline shift',
  },
  {
    key: 'time_scale',
    label: 'Time Scale',
    unit: '×',
    min: 0.1,
    max: 5.0,
    step: 0.1,
    description: 'Stretches or compresses the time axis',
  },
];

// ---------------------------------------------------------------------------
// Helper functions
// ---------------------------------------------------------------------------

// Formats numeric values based on the parameter type
const fmt = (val, key) => {
  if (key === 'noise_level' || key === 'baseline_offset') return val.toFixed(2);
  return val.toFixed(1);
};

// Push local params up to the parent component
const emitChange = () => {
  pendingChanges.value = false;
  emit('calibration-change', { ...params });
};

// Bulk-update params based on a preset profile
const applyPreset = (key) => {
  if (!PRESETS[key]) return;
  const p = PRESETS[key];
  Object.keys(DEFAULT_PARAMS).forEach((k) => {
    params[k] = p[k];
  });
  selectedPreset.value = key;
  emitChange(); // Auto-apply when switching presets
};

// Factory reset
const resetToDefaults = () => {
  applyPreset('default');
};

// Watch for any deep change in params to toggle the 'pending' UI indicator
watch(
  () => ({ ...params }),
  () => { pendingChanges.value = true; },
  { deep: true }
);
</script>

<template>
  <div class="calibration-panel">
    <!-- Header -->
    <div class="panel-header">
      <div class="header-icon">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
          <path d="M15.54 8.46a5 5 0 0 1 0 7.07M8.46 8.46a5 5 0 0 0 0 7.07"/>
        </svg>
      </div>
      <span class="panel-title">Calibration Settings</span>
      <div v-if="pendingChanges" class="pending-dot" title="Unsaved changes"></div>
    </div>

    <!-- Preset Selector -->
    <div class="preset-section">
      <label class="section-label">Preset Profile</label>
      <div class="preset-grid">
        <button
          v-for="opt in presetOptions"
          :key="opt.value"
          class="preset-btn"
          :class="{ active: selectedPreset === opt.value }"
          @click="applyPreset(opt.value)"
        >
          {{ opt.title }}
        </button>
      </div>
    </div>

    <div class="divider"></div>

    <!-- Sliders -->
    <div class="sliders-section">
      <label class="section-label">Parameters</label>
      <div v-for="s in sliders" :key="s.key" class="slider-row">
        <div class="slider-header">
          <span class="slider-label" :title="s.description">{{ s.label }}</span>
          <span class="slider-value">{{ fmt(params[s.key], s.key) }}{{ s.unit }}</span>
        </div>
        <v-slider
          v-model="params[s.key]"
          :min="s.min"
          :max="s.max"
          :step="s.step"
          color="green"
          hide-details
          thumb-color="green"
          track-color="rgba(16,185,129,0.25)"
          density="compact"
          class="calib-slider"
        />
      </div>
    </div>

    <div class="divider"></div>

    <!-- Current values display -->
    <div class="values-grid">
      <label class="section-label">Current Values</label>
      <div class="values-table">
        <div v-for="s in sliders" :key="s.key" class="value-row">
          <span class="value-key">{{ s.label }}</span>
          <span class="value-num">{{ fmt(params[s.key], s.key) }}{{ s.unit }}</span>
        </div>
      </div>
    </div>

    <div class="divider"></div>

    <!-- Action Buttons -->
    <div class="action-row">
      <button class="action-btn reset-btn" @click="resetToDefaults">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
          <path d="M3 3v5h5"/>
        </svg>
        Reset
      </button>
      <button class="action-btn apply-btn" @click="emitChange">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        Apply
      </button>
    </div>
  </div>
</template>

<style scoped>
.calibration-panel {
  background: rgba(9, 9, 11, 0.7);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 0.75rem;
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  backdrop-filter: blur(8px);
  box-shadow:
    0 0 8px rgba(16, 185, 129, 0.2),
    inset 0 0 6px rgba(16, 185, 129, 0.08);
}

/* Header */
.panel-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.header-icon {
  color: #10b981;
  display: flex;
  align-items: center;
}
.panel-title {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #34d399;
}
.pending-dot {
  width: 6px;
  height: 6px;
  background: #f59e0b;
  border-radius: 50%;
  margin-left: auto;
  animation: blink 1.2s ease-in-out infinite alternate;
  box-shadow: 0 0 6px #f59e0b;
}
@keyframes blink { from { opacity: 0.4; } to { opacity: 1; } }

/* Section label */
.section-label {
  display: block;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #64748b;
  margin-bottom: 0.5rem;
}

/* Presets */
.preset-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.4rem;
}
.preset-btn {
  padding: 0.35rem 0.5rem;
  font-size: 0.68rem;
  font-weight: 600;
  border-radius: 0.4rem;
  border: 1px solid rgba(16, 185, 129, 0.25);
  background: rgba(15, 23, 42, 0.5);
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}
.preset-btn:hover {
  border-color: rgba(16, 185, 129, 0.6);
  color: #10b981;
  background: rgba(16, 185, 129, 0.08);
  transform: translateY(-1px);
}
.preset-btn.active {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.3);
}

/* Divider */
.divider {
  height: 1px;
  background: rgba(16, 185, 129, 0.12);
}

/* Sliders */
.sliders-section {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.slider-row {
  margin-bottom: 0.1rem;
}
.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: -0.3rem;
}
.slider-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #94a3b8;
  cursor: help;
}
.slider-value {
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
  color: #10b981;
  font-weight: 700;
}
.calib-slider :deep(.v-slider__track) {
  height: 3px !important;
}
.calib-slider :deep(.v-slider__thumb) {
  width: 12px !important;
  height: 12px !important;
}

/* Values table */
.values-table {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.value-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.2rem 0.4rem;
  border-radius: 0.3rem;
  background: rgba(15, 23, 42, 0.4);
}
.value-key {
  font-size: 0.65rem;
  color: #64748b;
}
.value-num {
  font-family: 'Courier New', monospace;
  font-size: 0.68rem;
  color: #34d399;
  font-weight: 700;
}

/* Action buttons */
.action-row {
  display: flex;
  gap: 0.5rem;
}
.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.5rem;
  border-radius: 0.45rem;
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.22s ease;
  letter-spacing: 0.05em;
}
.reset-btn {
  background: rgba(100, 116, 139, 0.15);
  color: #94a3b8;
  border: 1px solid rgba(100, 116, 139, 0.3);
}
.reset-btn:hover {
  background: rgba(100, 116, 139, 0.28);
  color: #e2e8f0;
  transform: translateY(-1px);
}
.apply-btn {
  background: linear-gradient(135deg, #059669, #10b981);
  color: #ecfdf5;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
}
.apply-btn:hover {
  background: linear-gradient(135deg, #10b981, #34d399);
  box-shadow: 0 0 18px rgba(16, 185, 129, 0.55);
  transform: translateY(-1px);
}
.apply-btn:active {
  transform: scale(0.97);
}
</style>

<template>
  <div id="app" class="app-container">
    <!-- Header / Navigation -->
    <nav class="tabs bg-slate-950 shadow-lg">
      <router-link
        to="/"
        class="tab-button"
        active-class="active"
      >
        Simulation
      </router-link>
      <router-link
        to="/sensorview"
        class="tab-button"
        active-class="active"
      >
        Sensor
      </router-link>
      <router-link
        to="/graphdisplay"
        class="tab-button"
        active-class="active"
      >
        Graph Display
      </router-link>
      <router-link
        to="/physicsmodel"
        class="tab-button"
        active-class="active"
      >
        Physics Model
      </router-link>
      <div class="tab-underline"></div>
    </nav>

    <!-- Page Content -->
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>
/* Base App Container */
.app-container {
  font-family: 'Poppins', sans-serif;
  color: #f4f4f5;
  background-color: #09090b;
  min-height: 100vh;
}

/* Header / Tabs */
.tabs {
  display: flex;
  position: relative;
  justify-content: start;
  gap: 2rem;
  padding: 0.75rem 2rem;
  border-bottom: 1px solid rgba(16, 185, 129, 0.2);
  background: linear-gradient(90deg, rgba(9,9,11,0.95), rgba(15,23,42,0.95));
  box-shadow: 0 2px 12px rgba(16,185,129,0.2);
  z-index: 10;
}

/* Each Tab Button */
.tab-button {
  position: relative;
  text-decoration: none;
  color: #a1a1aa;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

/* Hover Animation */
.tab-button:hover {
  color: #10b981;
  transform: translateY(-2px) scale(1.05);
  text-shadow: 0 0 6px #10b981, 0 0 12px #34d399;
}

/* Active Tab */
.active {
  color: #10b981;
  font-weight: 700;
  text-shadow: 0 0 6px #10b981, 0 0 14px #34d399;
}

/* Glowing underline effect for active tab */
.tab-underline {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #10b981, #34d399);
  box-shadow: 0 0 15px #10b981, 0 0 30px #34d399;
  border-radius: 3px;
  pointer-events: none;
  animation: pulse-underline 2s infinite alternate;
}

/* Pulse animation */
@keyframes pulse-underline {
  0% { transform: scaleX(0.95); opacity: 0.7; }
  100% { transform: scaleX(1.05); opacity: 1; }
}

/* Page Content */
.content {
  padding: 1rem 2rem;
}

/* Responsive: Stack tabs on small screens */
@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>

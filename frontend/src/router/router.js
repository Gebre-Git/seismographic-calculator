import { createRouter, createWebHistory } from 'vue-router';

import Simulation from '../pages/Simulation.vue'
import SensorView from '../pages/SensorView.vue'
import graphDisplay from '../pages/GraphDisplay.vue';

const routes = [
  { path: '/', component: Simulation },
  { path: '/sensorview', component: SensorView },
  { path: '/graphdisplay', component: graphDisplay}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
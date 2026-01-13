import { createRouter, createWebHistory } from 'vue-router';

import Simulation from '../pages/Simulation.vue'
import SensorView from '../pages/SensorView.vue'
import graphDisplay from '../pages/GraphDisplay.vue'
import PhysicsModel from '../pages/PhysicsModel.vue';

const routes = [
  { path: '/', component: Simulation },
  { path: '/sensorview', component: SensorView },
  { path: '/graphdisplay', component: graphDisplay},
  { path: '/physicsmodel', component: PhysicsModel }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
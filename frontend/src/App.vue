<template>
  <div id="app">
    <nav class="tabs">
      <router-link to="/" class="tab-button" active-class="active">Simulation</router-link>
      <router-link to="/sensorview" class="tab-button" active-class="active">Sensor</router-link>
      <router-link to="/graphdisplay" class="tab-button" active-class="active">Graph Display</router-link>
      <router-link to="/physicsmodel" class="tab-button" active-class="active">Physics Model</router-link>
    </nav>

    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<style>
.tabs {
  display: flex;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 20px;
  text-decoration: none;
  color: #333;
  cursor: pointer;
}

/* This class is automatically applied when the route matches */
.active {
  border-bottom: 3px solid #42b983;
  color: #42b983;
  font-weight: bold;
}

.content {
  padding: 20px;
  border: 1px solid #eee;
}
</style>
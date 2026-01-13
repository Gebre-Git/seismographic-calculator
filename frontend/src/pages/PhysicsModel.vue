<template>
  <v-app>
    <!-- Main Content -->
    <v-main class="grey lighten-4">
      <v-container fluid class="pa-4">
        <!-- Welcome Card -->
        <v-card class="mb-6 rounded-lg" elevation="2">
          <v-card-title class="primary white--text">
            <v-icon left>mdi-earth</v-icon>
            Earthquake Simulation Backend System
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="8">
                <p class="text-body-1">
                  This backend system provides comprehensive earthquake simulation and real-time 
                  seismic monitoring capabilities. Built with FastAPI, it handles both synthetic 
                  earthquake generation and real-time accelerometer data processing.
                </p>
                
                <v-row class="mt-4">
                  <v-col cols="6" sm="3">
                    <v-card color="blue lighten-5" flat rounded class="text-center pa-3">
                      <v-icon large color="blue">mdi-post</v-icon>
                      <div class="subtitle-2 mt-2">POST /simulate</div>
                      <div class="caption">Simulation Endpoint</div>
                    </v-card>
                  </v-col>
                  <v-col cols="6" sm="3">
                    <v-card color="green lighten-5" flat rounded class="text-center pa-3">
                      <v-icon large color="green">mdi-web</v-icon>
                      <div class="subtitle-2 mt-2">WebSocket</div>
                      <div class="caption">Real-time Streaming</div>
                    </v-card>
                  </v-col>
                  <v-col cols="6" sm="3">
                    <v-card color="orange lighten-5" flat rounded class="text-center pa-3">
                      <v-icon large color="orange">mdi-chart-bell-curve</v-icon>
                      <div class="subtitle-2 mt-2">Signal Processing</div>
                      <div class="caption">FFT & Filters</div>
                    </v-card>
                  </v-col>
                  <v-col cols="6" sm="3">
                    <v-card color="red lighten-5" flat rounded class="text-center pa-3">
                      <v-icon large color="red">mdi-calculator</v-icon>
                      <div class="subtitle-2 mt-2">Physics Models</div>
                      <div class="caption">SDOF System</div>
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-card outlined rounded class="pa-2">
                  <v-card-title class="subtitle-2">System Endpoints</v-card-title>
                  <v-list dense>
                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon color="green" small>mdi-post</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title class="caption">POST /simulate</v-list-item-title>
                        <v-list-item-subtitle class="caption">Generate synthetic earthquake</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon color="orange" small>mdi-web</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title class="caption">WS /sensor</v-list-item-title>
                        <v-list-item-subtitle class="caption">Sensor data input stream</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon color="blue" small>mdi-web</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title class="caption">WS /display</v-list-item-title>
                        <v-list-item-subtitle class="caption">Display data stream</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Main Content Tabs -->
        <v-tabs v-model="selectedTab" grow class="mb-6 rounded-lg elevation-2" background-color="white" color="primary">
          <v-tab v-for="item in navigationItems" :key="item.title">
            <v-icon left>{{ item.icon }}</v-icon>
            {{ item.title }}
          </v-tab>
        </v-tabs>

        <!-- Tab Content -->
        <v-window v-model="selectedTab">
          <!-- Tab 1: Imports & Setup -->
          <v-window-item>
            <v-card elevation="2" rounded-lg>
              <v-card-title class="secondary white--text">
                <v-icon left>mdi-import</v-icon>
                Import Statements & Initial Setup
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-language-python</v-icon>
                        Import Statements
                      </v-card-title>
                      <v-card-text>
                        <pre class="code-block">{{ importsCode }}</pre>
                      </v-card-text>
                    </v-card>
                    
                    <v-expansion-panels class="mb-4" flat>
                      <v-expansion-panel>
                        <v-expansion-panel-header>
                          <v-icon left small>mdi-fast-forward</v-icon>
                          FastAPI Framework
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <p class="text-caption">
                            FastAPI is a modern, fast web framework for building APIs with Python 3.7+ 
                            based on standard Python type hints.
                          </p>
                          <v-list dense>
                            <v-list-item>
                              <v-list-item-icon>
                                <v-icon small color="green">mdi-check</v-icon>
                              </v-list-item-icon>
                              <v-list-item-content>
                                <v-list-item-title class="caption">Automatic API documentation</v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                            <v-list-item>
                              <v-list-item-icon>
                                <v-icon small color="green">mdi-check</v-icon>
                              </v-list-item-icon>
                              <v-list-item-content>
                                <v-list-item-title class="caption">Data validation with Pydantic</v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                            <v-list-item>
                              <v-list-item-icon>
                                <v-icon small color="green">mdi-check</v-icon>
                              </v-list-item-icon>
                              <v-list-item-content>
                                <v-list-item-title class="caption">WebSocket support</v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                          </v-list>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                    </v-expansion-panels>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-cog</v-icon>
                        Application Setup
                      </v-card-title>
                      <v-card-text>
                        <pre class="code-block">{{ setupCode }}</pre>
                      </v-card-text>
                    </v-card>
                    
                    <v-alert type="info" border="left" colored-border elevation="1" class="mb-4">
                      <strong class="caption">CORS Middleware:</strong>
                      <span class="caption">
                        Allows cross-origin requests from browsers. The asterisk (*) allows all origins - 
                        in production, you should restrict this to specific domains.
                      </span>
                    </v-alert>
                    
                    <v-alert type="warning" border="left" colored-border elevation="1">
                      <strong class="caption">deque (Double-ended queue):</strong>
                      <span class="caption">
                        Used for sensor buffers because it provides O(1) time complexity for appends 
                        and pops from both ends, and automatically maintains maximum length.
                      </span>
                    </v-alert>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-window-item>

          <!-- Tab 2: Simulation Logic -->
          <v-window-item>
            <v-card elevation="2" rounded-lg>
              <v-card-title class="secondary white--text">
                <v-icon left>mdi-chart-bell-curve</v-icon>
                Earthquake Simulation Logic
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="4">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-weight</v-icon>
                        Magnitude to Amplitude Conversion
                      </v-card-title>
                      <v-card-text>
                        <pre class="code-block">{{ magnitudeCode }}</pre>
                        
                        <div class="mt-4">
                          <h4 class="subtitle-2 mb-2">Formula</h4>
                          <div class="formula-box" v-html="renderMath('E = 10^{(1.5 \\times M)} \\\\ A = \\frac{\\sqrt{E}}{10^5}')"></div>
                          
                          <v-slider
                            v-model="magnitudeValue"
                            label="Magnitude (M)"
                            :min="1"
                            :max="10"
                            :step="0.1"
                            thumb-label
                            color="primary"
                            class="mt-4"
                          ></v-slider>
                          
                          <div class="text-center">
                            <v-chip class="ma-1" color="orange" small>
                              Energy: {{ calculateEnergy(magnitudeValue).toExponential(2) }}
                            </v-chip>
                            <v-chip class="ma-1" color="blue" small>
                              Amplitude: {{ calculateAmplitude(magnitudeValue).toFixed(6) }}
                            </v-chip>
                          </div>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  
                  <v-col cols="12" md="8">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-wave</v-icon>
                        Seismic Wave Generation
                      </v-card-title>
                      <v-card-text>
                        <v-tabs v-model="waveType" grow background-color="grey lighten-4" color="primary">
                          <v-tab value="p">
                            <v-icon left small>mdi-ray-start</v-icon>
                            P-Wave
                          </v-tab>
                          <v-tab value="s">
                            <v-icon left small>mdi-ray-vertex</v-icon>
                            S-Wave
                          </v-tab>
                          <v-tab value="surface">
                            <v-icon left small>mdi-earth</v-icon>
                            Surface Wave
                          </v-tab>
                        </v-tabs>
                        
                        <v-window v-model="waveType" class="mt-4">
                          <!-- P-Wave -->
                          <v-window-item value="p">
                            <div class="formula-box pa-3" v-html="renderMath('P(t) = 0.3A \\times e^{-0.15t} \\times \\sin(2\\pi \\times 2f \\times t)')"></div>
                            <v-list dense class="mt-2">
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon small color="blue">mdi-clock-fast</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title class="caption">Arrival: 0 seconds (first)</v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon small color="green">mdi-speedometer</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title class="caption">Velocity: ~6.0 km/s</v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                            </v-list>
                          </v-window-item>
                          
                          <!-- S-Wave -->
                          <v-window-item value="s">
                            <div class="formula-box pa-3" v-html="renderMath('\\begin{cases} 0 & t < 1 \\\\ 0.6A \\times e^{-0.1(t-1)} \\times \\sin(2\\pi \\times f \\times (t-1)) & t \\geq 1 \\end{cases}')"></div>
                            <v-list dense class="mt-2">
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon small color="orange">mdi-clock</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title class="caption">Arrival: 1 second delay</v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon small color="green">mdi-speedometer</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title class="caption">Velocity: ~3.5 km/s</v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                            </v-list>
                          </v-window-item>
                          
                          <!-- Surface Wave -->
                          <v-window-item value="surface">
                            <div class="formula-box pa-3" v-html="renderMath('\\begin{cases} 0 & t < 2 \\\\ A \\times e^{-0.05(t-2)} \\times \\sin(2\\pi \\times 0.5f \\times (t-2)) & t \\geq 2 \\end{cases}')"></div>
                            <v-list dense class="mt-2">
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon small color="red">mdi-clock-slow</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title class="caption">Arrival: 2 seconds delay</v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon small color="red">mdi-amplitude</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title class="caption">Largest amplitude</v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                            </v-list>
                          </v-window-item>
                        </v-window>
                        
                        <v-divider class="my-4"></v-divider>
                        
                        <pre class="code-block">{{ waveGenerationCode }}</pre>
                      </v-card-text>
                    </v-card>
                    
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-card outlined rounded class="mb-4">
                          <v-card-title class="subtitle-2">
                            <v-icon left small>mdi-plus-circle</v-icon>
                            Wave Composition
                          </v-card-title>
                          <v-card-text>
                            <pre class="code-block">{{ compositionCode }}</pre>
                            <div class="formula-box pa-2 mt-2" v-html="renderMath('G(t) = P(t) + S(t) + R(t)')"></div>
                          </v-card-text>
                        </v-card>
                      </v-col>
                      
                      <v-col cols="12" md="6">
                        <v-card outlined rounded>
                          <v-card-title class="subtitle-2">
                            <v-icon left small>mdi-white-balance-sunny</v-icon>
                            Noise Addition
                          </v-card-title>
                          <v-card-text>
                            <pre class="code-block">{{ noiseCode }}</pre>
                            <div class="formula-box pa-2 mt-2" v-html="renderMath('\\mathcal{N}(\\mu=0, \\sigma=0.03A)')"></div>
                          </v-card-text>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-window-item>

          <!-- Tab 3: SDOF System -->
          <v-window-item>
            <v-card elevation="2" rounded-lg>
              <v-card-title class="secondary white--text">
                <v-icon left>mdi-home</v-icon>
                Single Degree of Freedom (SDOF) System
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="5">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-cog</v-icon>
                        SDOF Implementation
                      </v-card-title>
                      <v-card-text>
                        <pre class="code-block">{{ sdofCode }}</pre>
                        
                        <div class="mt-4">
                          <h4 class="subtitle-2 mb-2">System Parameters</h4>
                          <v-simple-table dense>
                            <thead>
                              <tr>
                                <th>Parameter</th>
                                <th>Symbol</th>
                                <th>Value</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr>
                                <td>Mass</td>
                                <td>m</td>
                                <td>1.0 kg</td>
                              </tr>
                              <tr>
                                <td>Stiffness</td>
                                <td>k</td>
                                <td>20.0 N/m</td>
                              </tr>
                              <tr>
                                <td>Damping</td>
                                <td>c</td>
                                <td>5.0 Ns/m</td>
                              </tr>
                            </tbody>
                          </v-simple-table>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  
                  <v-col cols="12" md="7">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-calculator</v-icon>
                        Equation of Motion
                      </v-card-title>
                      <v-card-text>
                        <div class="formula-box pa-4 text-center" v-html="renderMath('m\\ddot{x} + c\\dot{x} + kx = -ma_g(t)')"></div>
                        
                        <v-divider class="my-4"></v-divider>
                        
                        <v-row>
                          <v-col cols="12" md="6">
                            <h4 class="subtitle-2 mb-2">Variables</h4>
                            <v-simple-table dense>
                              <tbody>
                                <tr>
                                  <td v-html="renderMath('\\ddot{x}')"></td>
                                  <td>Relative acceleration</td>
                                </tr>
                                <tr>
                                  <td v-html="renderMath('\\dot{x}')"></td>
                                  <td>Relative velocity</td>
                                </tr>
                                <tr>
                                  <td v-html="renderMath('x')"></td>
                                  <td>Displacement</td>
                                </tr>
                                <tr>
                                  <td v-html="renderMath('a_g')"></td>
                                  <td>Ground acceleration</td>
                                </tr>
                              </tbody>
                            </v-simple-table>
                          </v-col>
                          
                          <v-col cols="12" md="6">
                            <h4 class="subtitle-2 mb-2">System Properties</h4>
                            <v-alert type="info" dense colored-border elevation="1" class="mb-2">
                              <strong>Natural Frequency:</strong>
                              <div v-html="renderMath('\\omega_n = \\sqrt{\\frac{k}{m}} = \\sqrt{20} \\approx 4.47 \\text{ rad/s}')"></div>
                            </v-alert>
                            <v-alert type="info" dense colored-border elevation="1">
                              <strong>Damping Ratio:</strong>
                              <div v-html="renderMath('\\zeta = \\frac{c}{2\\sqrt{km}} = \\frac{5}{2\\sqrt{20}} \\approx 0.56')"></div>
                            </v-alert>
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-card>
                    
                    <v-card outlined rounded>
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-chart-line</v-icon>
                        Numerical Integration (Euler Method)
                      </v-card-title>
                      <v-card-text>
                        <div class="formula-box pa-3" v-html="renderMath('a = \\frac{-cv - kx - ma_g}{m} \\\\ v_{n+1} = v_n + a \\cdot \\Delta t \\\\ x_{n+1} = x_n + v_{n+1} \\cdot \\Delta t')"></div>
                        <p class="caption mt-2">Where \(\Delta t = 0.01\) seconds</p>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-window-item>

          <!-- Tab 4: FFT Analysis -->
          <v-window-item>
            <v-card elevation="2" rounded-lg>
              <v-card-title class="secondary white--text">
                <v-icon left>mdi-chart-bell-curve-cumulative</v-icon>
                Frequency Domain Analysis (FFT)
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="5">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-function</v-icon>
                        FFT Implementation
                      </v-card-title>
                      <v-card-text>
                        <pre class="code-block">{{ fftCode }}</pre>
                        
                        <div class="mt-4">
                          <h4 class="subtitle-2 mb-2">Sampling Parameters</h4>
                          <v-simple-table dense>
                            <thead>
                              <tr>
                                <th>Parameter</th>
                                <th>Value</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr>
                                <td>Sampling Rate</td>
                                <td>100 Hz</td>
                              </tr>
                              <tr>
                                <td>Nyquist Frequency</td>
                                <td>50 Hz</td>
                              </tr>
                              <tr>
                                <td>Time Step (\(\Delta t\))</td>
                                <td>0.01 s</td>
                              </tr>
                            </tbody>
                          </v-simple-table>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  
                  <v-col cols="12" md="7">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-math-integral</v-icon>
                        Discrete Fourier Transform
                      </v-card-title>
                      <v-card-text>
                        <div class="formula-box pa-4" v-html="renderMath('X[k] = \\sum_{n=0}^{N-1} x[n] \\cdot e^{-i2\\pi kn/N}')"></div>
                        
                        <v-divider class="my-4"></v-divider>
                        
                        <v-row>
                          <v-col cols="12" md="6">
                            <h4 class="subtitle-2 mb-2">Variables</h4>
                            <ul class="caption">
                              <li v-html="renderMath('X[k]')"></li>
                              <li v-html="renderMath('x[n]')"></li>
                              <li v-html="renderMath('N')"></li>
                              <li v-html="renderMath('k')"></li>
                              <li v-html="renderMath('n')"></li>
                            </ul>
                          </v-col>
                          
                          <v-col cols="12" md="6">
                            <h4 class="subtitle-2 mb-2">Frequency Bins</h4>
                            <div class="formula-box pa-2" v-html="renderMath('f_k = \\frac{k}{N\\Delta t}')"></div>
                            <p class="caption mt-2">For \(k = 0,1,...,N-1\)</p>
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-card>
                    
                    <v-card outlined rounded>
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-chart-bar</v-icon>
                        Amplitude Spectrum
                      </v-card-title>
                      <v-card-text>
                        <p class="caption mb-2">The amplitude spectrum shows frequency content:</p>
                        <div class="formula-box pa-3" v-html="renderMath('\\text{Spectrum}[k] = |X[k]| = \\sqrt{\\text{Re}(X[k])^2 + \\text{Im}(X[k])^2}')"></div>
                        
                        <v-alert type="info" dense colored-border elevation="1" class="mt-4">
                          <strong>Why only positive frequencies?</strong>
                          <span class="caption">
                            For real-valued signals, FFT output is symmetric. Negative frequencies 
                            are mirror images of positive frequencies.
                          </span>
                        </v-alert>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-window-item>

          <!-- Tab 5: Real-time Processing -->
          <v-window-item>
            <v-card elevation="2" rounded-lg>
              <v-card-title class="secondary white--text">
                <v-icon left>mdi-web</v-icon>
                Real-time WebSocket Processing
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-cog-outline</v-icon>
                        WebSocket Configuration
                      </v-card-title>
                      <v-card-text>
                        <pre class="code-block">{{ websocketConfig }}</pre>
                        
                        <div class="mt-4">
                          <h4 class="subtitle-2 mb-2">Buffer Configuration</h4>
                          <v-simple-table dense>
                            <thead>
                              <tr>
                                <th>Buffer</th>
                                <th>Size</th>
                                <th>Duration</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr>
                                <td>sensor_buffer</td>
                                <td>500 samples</td>
                                <td>25 seconds</td>
                              </tr>
                              <tr>
                                <td>distance_buffer</td>
                                <td>200 samples</td>
                                <td>History</td>
                              </tr>
                            </tbody>
                          </v-simple-table>
                        </div>
                      </v-card-text>
                    </v-card>
                    
                    <v-card outlined rounded>
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-speedometer</v-icon>
                        Wave Velocities
                      </v-card-title>
                      <v-card-text>
                        <div class="formula-box pa-3" v-html="renderMath('V_P = 6.0 \\text{ km/s} \\quad \\text{(P-wave)} \\\\ V_S = 3.5 \\text{ km/s} \\quad \\text{(S-wave)}')"></div>
                        <p class="caption mt-2">Typical values for Earth's crust</p>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-card outlined rounded class="mb-4">
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-chart-timeline</v-icon>
                        Processing Pipeline
                      </v-card-title>
                      <v-card-text>
                        <v-stepper v-model="processingStep" vertical flat>
                          <v-stepper-step step="1" :complete="processingStep > 1">
                            Raw Acceleration
                            <small>From accelerometer</small>
                          </v-stepper-step>
                          
                          <v-stepper-content step="1">
                            <pre class="code-block">{{ accelerationCode }}</pre>
                          </v-stepper-content>
                          
                          <v-stepper-step step="2" :complete="processingStep > 2">
                            Signal Filtering
                            <small>Separate P and S waves</small>
                          </v-stepper-step>
                          
                          <v-stepper-content step="2">
                            <v-row>
                              <v-col cols="6">
                                <strong class="caption">High-pass (P-wave):</strong>
                                <pre class="code-block small">{{ highPassCode }}</pre>
                              </v-col>
                              <v-col cols="6">
                                <strong class="caption">Low-pass (S-wave):</strong>
                                <pre class="code-block small">{{ lowPassCode }}</pre>
                              </v-col>
                            </v-row>
                          </v-stepper-content>
                          
                          <v-stepper-step step="3" :complete="processingStep > 3">
                            Numerical Integration
                            <small>Acceleration → Velocity → Displacement</small>
                          </v-stepper-step>
                          
                          <v-stepper-content step="3">
                            <pre class="code-block">{{ integrationCode }}</pre>
                            <div class="formula-box pa-2 mt-2" v-html="renderMath('\\int f(t)dt \\approx \\sum \\frac{1}{2}(f_i + f_{i-1})\\Delta t')"></div>
                          </v-stepper-content>
                          
                          <v-stepper-step step="4">
                            Arrival Detection
                            <small>Detect wave onsets</small>
                          </v-stepper-step>
                          
                          <v-stepper-content step="4">
                            <pre class="code-block">{{ arrivalCode }}</pre>
                          </v-stepper-content>
                        </v-stepper>
                        
                        <div class="text-center mt-4">
                          <v-btn small color="primary" @click="processingStep = 1">Reset Pipeline</v-btn>
                          <v-btn small color="primary" @click="processingStep++" :disabled="processingStep >= 4" class="ml-2">
                            Next Step
                          </v-btn>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
                
                <v-row>
                  <v-col cols="12">
                    <v-card outlined rounded>
                      <v-card-title class="subtitle-2">
                        <v-icon left small>mdi-connection</v-icon>
                        WebSocket Endpoints
                      </v-card-title>
                      <v-card-text>
                        <v-row>
                          <v-col cols="12" md="6">
                            <v-card flat color="blue-grey lighten-5" rounded class="mb-4 pa-3">
                              <v-card-title class="subtitle-2">/sensor Endpoint</v-card-title>
                              <v-card-text>
                                <p class="caption">Receives accelerometer data from mobile devices:</p>
                                <pre class="code-block small">{"ax": 0.1, "ay": -0.2, "az": 9.8}</pre>
                                <ul class="caption mt-2">
                                  <li>Calculates magnitude: \(a = \sqrt{a_x^2 + a_y^2 + a_z^2}\)</li>
                                  <li>Processes when buffer has 50+ samples</li>
                                  <li>Broadcasts to display clients</li>
                                </ul>
                              </v-card-text>
                            </v-card>
                          </v-col>
                          
                          <v-col cols="12" md="6">
                            <v-card flat color="blue-grey lighten-5" rounded class="pa-3">
                              <v-card-title class="subtitle-2">/display Endpoint</v-card-title>
                              <v-card-text>
                                <p class="caption">Sends processed data to visualization clients:</p>
                                <ul class="caption">
                                  <li>Maintains set of connected clients</li>
                                  <li>Publisher-subscriber pattern</li>
                                  <li>Real-time data streaming</li>
                                  <li>Handles disconnections</li>
                                </ul>
                              </v-card-text>
                            </v-card>
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-window-item>

          <!-- Tab 6: Mathematical Formulas -->
          <v-window-item>
            <v-card elevation="2" rounded-lg>
              <v-card-title class="secondary white--text">
                <v-icon left>mdi-math-compass</v-icon>
                Complete Mathematical Reference
              </v-card-title>
              <v-card-text>
                <v-tabs v-model="formulaTab" grow class="mb-4" background-color="grey lighten-4" color="primary">
                  <v-tab value="simulation">Simulation</v-tab>
                  <v-tab value="realtime">Real-time</v-tab>
                  <v-tab value="physics">Physics</v-tab>
                </v-tabs>
                
                <v-window v-model="formulaTab">
                  <!-- Simulation Formulas -->
                  <v-window-item value="simulation">
                    <v-simple-table>
                      <thead>
                        <tr>
                          <th>Formula</th>
                          <th>Description</th>
                          <th>Code</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('E = 10^{1.5M}')"></td>
                          <td>Energy-magnitude relation</td>
                          <td><code>10 ** (1.5 * magnitude)</code></td>
                        </tr>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('A = \\frac{\\sqrt{E}}{10^5}')"></td>
                          <td>Energy to amplitude</td>
                          <td><code>np.sqrt(energy) / 1e5</code></td>
                        </tr>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('y = Ae^{-\\beta t}\\sin(2\\pi ft)')"></td>
                          <td>Damped sine wave</td>
                          <td><code>A * np.exp(-β*t) * np.sin(2π*f*t)</code></td>
                        </tr>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('G = P + S + R + N')"></td>
                          <td>Ground motion composition</td>
                          <td><code>p_wave + s_wave + surface_wave + noise</code></td>
                        </tr>
                      </tbody>
                    </v-simple-table>
                  </v-window-item>
                  
                  <!-- Real-time Formulas -->
                  <v-window-item value="realtime">
                    <v-simple-table>
                      <thead>
                        <tr>
                          <th>Formula</th>
                          <th>Description</th>
                          <th>Use</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('a = \\sqrt{a_x^2 + a_y^2 + a_z^2}')"></td>
                          <td>Acceleration magnitude</td>
                          <td>Sensor data processing</td>
                        </tr>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('y[n] = y[n-1] + \\alpha(x[n] - y[n-1])')"></td>
                          <td>Low-pass filter</td>
                          <td>S-wave extraction</td>
                        </tr>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('y[n] = \\alpha(y[n-1] + x[n] - x[n-1])')"></td>
                          <td>High-pass filter</td>
                          <td>P-wave extraction</td>
                        </tr>
                        <tr>
                          <td class="formula-cell" v-html="renderMath('D = \\frac{\\Delta T}{V_S^{-1} - V_P^{-1}}')"></td>
                          <td>Distance calculation</td>
                          <td>Epicenter location</td>
                        </tr>
                      </tbody>
                    </v-simple-table>
                  </v-window-item>
                  
                  <!-- Physics Formulas -->
                  <v-window-item value="physics">
                    <v-expansion-panels flat>
                      <v-expansion-panel>
                        <v-expansion-panel-header>
                          Wave Propagation Equations
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <div class="formula-box pa-3" v-html="renderMath('V_P = \\sqrt{\\frac{\\lambda + 2\\mu}{\\rho}} \\quad V_S = \\sqrt{\\frac{\\mu}{\\rho}}')"></div>
                          <p class="caption mt-2">Where λ, μ are Lamé parameters, ρ is density</p>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                      
                      <v-expansion-panel>
                        <v-expansion-panel-header>
                          SDOF System Analysis
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <div class="formula-box pa-3" v-html="renderMath('m\\ddot{x} + c\\dot{x} + kx = -ma_g \\\\ \\omega_n = \\sqrt{\\frac{k}{m}}, \\quad \\zeta = \\frac{c}{2\\sqrt{km}}')"></div>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                      
                      <v-expansion-panel>
                        <v-expansion-panel-header>
                          Sampling Theory
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <div class="formula-box pa-3" v-html="renderMath('f_{max} = \\frac{f_s}{2} \\quad \\text{(Nyquist frequency)} \\\\ \\Delta f = \\frac{f_s}{N} \\quad \\text{(Frequency resolution)}')"></div>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                    </v-expansion-panels>
                  </v-window-item>
                </v-window>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app color="grey darken-3" class="white--text">
      <v-container>
        <v-row align="center">
          <v-col cols="12" class="text-center">
            <v-icon small class="mr-1">mdi-code-tags</v-icon>
            Backend Analysis Dashboard
            <v-divider vertical class="mx-3"></v-divider>
            <v-icon small class="mr-1">mdi-api</v-icon>
            FastAPI + WebSockets
            <v-divider vertical class="mx-3"></v-divider>
            <v-icon small class="mr-1">mdi-chart-bell-curve</v-icon>
            Signal Processing Engine
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
import katex from 'katex';
import 'katex/dist/katex.min.css';

export default {
  name: 'BackendAnalysisDashboard',
  
  data() {
    return {
      drawer: false,
      selectedTab: 0,
      waveType: 'p',
      formulaTab: 'simulation',
      processingStep: 1,
      magnitudeValue: 5.0,
      backendStatus: 'Running',
      
      navigationItems: [
        { title: 'Imports & Setup', icon: 'mdi-import' },
        { title: 'Simulation Logic', icon: 'mdi-chart-bell-curve' },
        { title: 'SDOF System', icon: 'mdi-home' },
        { title: 'FFT Analysis', icon: 'mdi-chart-bell-curve-cumulative' },
        { title: 'Real-time Processing', icon: 'mdi-web' },
        { title: 'Formulas Reference', icon: 'mdi-math-compass' },
      ],
      
      // Code snippets
      importsCode: `from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from collections import deque`,
      
      setupCode: `app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)`,
      
      magnitudeCode: `def magnitude_to_amplitude(magnitude):
    energy = 10 ** (1.5 * magnitude)
    return np.sqrt(energy) / 1e5`,
      
      waveGenerationCode: `p_wave = 0.3 * A * np.exp(-0.15 * t) * np.sin(2 * np.pi * (frequency * 2) * t)
s_wave = 0.6 * A * np.exp(-0.1 * (t - 1)) * np.sin(2 * np.pi * frequency * (t - 1))
surface_wave = A * np.exp(-0.05 * (t - 2)) * np.sin(2 * np.pi * (frequency * 0.5) * (t - 2))`,
      
      compositionCode: `ground_motion = p_wave + s_wave + surface_wave`,
      
      noiseCode: `noise_strength = 0.03 * A
noise = np.random.normal(0, noise_strength, size=len(t))
ground_motion += noise`,
      
      sdofCode: `m, k, c = 1.0, 20.0, 5.0
x, v = 0.0, 0.0
recorded = []

ground_acc = np.gradient(np.gradient(ground_motion, dt), dt)

for a_g in ground_acc:
    a = (-c * v - k * x - m * a_g) / m
    v += a * dt
    x += v * dt
    recorded.append(x)`,
      
      fftCode: `fft_vals = np.fft.fft(recorded)
freqs = np.fft.fftfreq(len(fft_vals), dt)

positive = freqs > 0
freqs = freqs[positive]
spectrum = np.abs(fft_vals[positive])`,
      
      websocketConfig: `sensor_buffer = deque(maxlen=500)
distance_buffer = deque(maxlen=200)
display_clients = set()

SAMPLE_RATE = 20  # Hz
DT = 1 / SAMPLE_RATE

VP = 6.0   # P-wave speed (km/s)
VS = 3.5   # S-wave speed (km/s)`,
      
      accelerationCode: `ax = float(data["ax"])
ay = float(data["ay"])
az = float(data["az"])

a = np.sqrt(ax**2 + ay**2 + az**2)
sensor_buffer.append(a)`,
      
      highPassCode: `def high_pass(signal, alpha=0.1):
    filtered = []
    y = signal[0]
    prev_x = signal[0]
    for x in signal:
        y = alpha * (y + x - prev_x)
        filtered.append(y)
        prev_x = x
    return filtered`,
      
      lowPassCode: `def low_pass(signal, alpha=0.1):
    filtered = []
    y = signal[0]
    for x in signal:
        y = y + alpha * (x - y)
        filtered.append(y)
    return filtered`,
      
      integrationCode: `def integrate(signal, dt):
    integrated = np.zeros(len(signal))
    for i in range(1, len(signal)):
        integrated[i] = integrated[i-1] + 0.5 * (signal[i] + signal[i-1]) * dt
    return integrated`,
      
      arrivalCode: `def detect_arrival(signal, threshold=0.02):
    for i, v in enumerate(signal):
        if abs(v) > threshold:
            return i
    return None`,
    };
  },
  
  methods: {
    calculateEnergy(magnitude) {
      return Math.pow(10, 1.5 * magnitude);
    },
    
    calculateAmplitude(magnitude) {
      const energy = this.calculateEnergy(magnitude);
      return Math.sqrt(energy) / 1e5;
    },

    renderMath(tex) {
      return katex.renderToString(tex, {
        throwOnError: false,
        displayMode: true,
      });
    },
  },
  
  watch: {
    selectedTab() {
      this.processingStep = 1;
    },
  },
};
</script>

<style scoped>
.code-block {
  background-color: #f5f5f5;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  padding: 12px;
  overflow-x: auto;
  margin: 0;
  line-height: 1.4;
  white-space: pre-wrap;
  border: 1px solid #e0e0e0;
}

.code-block.small {
  font-size: 0.8em;
  padding: 8px;
}

.formula-box {
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 4px solid #2196F3;
  padding: 8px;
  text-align: center;
}

.formula-cell {
  padding: 8px;
  text-align: center;
}

.v-stepper__step {
  padding: 8px;
}

.v-stepper__content {
  padding: 8px 0;
}

.v-list-item__title.caption {
  font-size: 0.75rem;
}

.v-list-item__subtitle.caption {
  font-size: 0.7rem;
}

.text-caption {
  font-size: 0.75rem;
  line-height: 1.4;
}

.v-alert {
  padding: 8px 12px;
}

.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
}
</style>
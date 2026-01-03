import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
  ],
  server: {
    host: '10.53.25.190', // Replace with your specific IP address
    port: 3000,           // Optional: Specify a port (default is 5173)
  }
})

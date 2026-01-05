import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
  ],
  server: {
    host: '192.168.30.186', // Replace with your specific IP address
    port: 3000,           // Optional: Specify a port (default is 5173)
  }
})

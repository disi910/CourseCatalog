import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'


// https://vite.dev/config/
export default defineConfig({
  // base sets the public path for all assets when the app is served from a sub-path
  // Without this, the browser would look for /assets/main.js instead of /coursecatalog/assets/main.js
  base: '/coursecatalog/',
  plugins: [
    tailwindcss(),
    react(),
  ],
})

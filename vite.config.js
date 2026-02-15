/**
 * ============================================
 * VITE CONFIG - DEFAULT
 * ============================================
 * Konfigurasi default saat menjalankan `npm run dev`.
 * Menggunakan konfigurasi OPTIMIZED (1B) sebagai default.
 *
 * Untuk menjalankan versi spesifik:
 *   npm run dev:baseline   → vite.config.baseline.js
 *   npm run dev:optimized  → vite.config.optimized.js
 * ============================================
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  server: {
    port: 3000,
  },
})

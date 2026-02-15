/**
 * ============================================
 * VITE CONFIG - VERSI 1A (BASELINE)
 * ============================================
 * Pendekatan: NAIF / MONOLITHIC
 * - Tidak ada code splitting manual
 * - Tidak ada compression
 * - Tidak ada bundle analysis
 * - Config standar / default
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

    // Build config standar — TANPA OPTIMASI
    build: {
        // Output ke folder terpisah agar bisa dibandingkan
        outDir: 'dist-baseline',

        // Entry point: index.baseline.html
        rollupOptions: {
            input: 'index.baseline.html',
        },

        // TIDAK ada konfigurasi manualChunks
        // Semua kode akan di-bundle menjadi satu atau dua chunk besar
    },

    // Dev server
    server: {
        port: 3001, // Port berbeda dari versi optimized
    },
})

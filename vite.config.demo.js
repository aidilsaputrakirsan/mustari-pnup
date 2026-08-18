/**
 * ============================================
 * VITE CONFIG - VARIAN DEMO
 * ============================================
 * Varian yang dipublikasikan ke Netlify.
 * Terpisah dari konfigurasi Baseline (1A) & Optimized (1B)
 * agar berkas pengukuran tesis tidak ikut terpengaruh.
 * ============================================
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
    plugins: [vue()],
    server: {
        port: 3100,
    },
    build: {
        outDir: 'dist-demo',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: path.resolve(__dirname, 'index.demo.html'),
            },
            output: {
                // Hanya inti Vue dan Chart.js yang dikelompokkan manual.
                // PrimeVue sengaja TIDAK disatukan: bila digabung menjadi
                // satu chunk, halaman masuk ikut mengunduh seluruh pustaka
                // tabel dan grafik yang belum dipakai. Dibiarkan terpecah
                // otomatis, tiap rute hanya menarik komponen miliknya.
                manualChunks(id) {
                    if (!id.includes('node_modules')) return
                    if (id.includes('chart.js')) return 'vendor-chart'
                    if (id.includes('vue-router') || id.includes('pinia') || id.includes('/vue/')) return 'vendor-vue'
                },
                chunkFileNames: 'assets/js/[name]-[hash].js',
                entryFileNames: 'assets/js/[name]-[hash].js',
                assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
            },
        },
    },
})

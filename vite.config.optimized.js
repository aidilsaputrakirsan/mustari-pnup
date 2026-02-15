/**
 * ============================================
 * VITE CONFIG - VERSI 1B (OPTIMIZED)
 * ============================================
 * Pendekatan: MODERN / BEST PRACTICE
 * - Manual chunks (memisahkan vendor: vue, pinia, chart.js)
 * - Gzip & Brotli compression
 * - Bundle visualizer (rollup-plugin-visualizer)
 * - Optimasi aset dan chunking
 * ============================================
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { visualizer } from 'rollup-plugin-visualizer'
import viteCompression from 'vite-plugin-compression'

export default defineConfig({
    plugins: [
        vue(),
        tailwindcss(),

        // Plugin: Bundle Visualizer
        // Menghasilkan stats.html untuk analisis ukuran bundle
        visualizer({
            filename: 'stats.html',
            open: false, // Jangan buka otomatis saat build
            gzipSize: true,
            brotliSize: true,
            template: 'treemap', // Tampilan treemap lebih informatif
        }),

        // Plugin: Gzip Compression
        viteCompression({
            algorithm: 'gzip',
            ext: '.gz',
            threshold: 1024, // Hanya compress file > 1KB
        }),

        // Plugin: Brotli Compression
        viteCompression({
            algorithm: 'brotliCompress',
            ext: '.br',
            threshold: 1024,
        }),
    ],

    build: {
        // Output ke folder terpisah
        outDir: 'dist-optimized',

        // Konfigurasi Rollup untuk Code Splitting
        rollupOptions: {
            // Entry point: index.optimized.html
            input: 'index.optimized.html',
            output: {
                /**
                 * manualChunks (Function format untuk kompatibilitas Vite 8):
                 * Memisahkan vendor libraries ke chunk terpisah
                 *
                 * Keuntungan:
                 * 1. Browser bisa cache vendor chunks terpisah dari app code
                 * 2. Update kode aplikasi tidak memaksa re-download library vendor
                 * 3. Parallel loading multiple chunks kecil lebih cepat dari 1 chunk besar
                 */
                manualChunks(id) {
                    // Chunk 1: Core Vue ecosystem
                    if (id.includes('node_modules/vue') || id.includes('node_modules/vue-router') || id.includes('node_modules/pinia') || id.includes('node_modules/@vue')) {
                        return 'vendor-vue'
                    }
                    // Chunk 2: Chart.js (library berat ~200KB)
                    if (id.includes('node_modules/chart.js') || id.includes('node_modules/vue-chartjs')) {
                        return 'vendor-chart'
                    }
                },

                // Penamaan chunk yang rapi untuk analisis
                chunkFileNames: 'assets/js/[name]-[hash].js',
                entryFileNames: 'assets/js/[name]-[hash].js',
                assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
            },
        },

        // Target browser modern untuk output yang lebih kecil
        target: 'es2020',

        // Aktifkan source map untuk debugging (opsional untuk production)
        sourcemap: false,

        // Batas peringatan ukuran chunk (500KB)
        chunkSizeWarningLimit: 500,
    },

    // Dev server
    server: {
        port: 3002, // Port berbeda dari versi baseline
    },
})

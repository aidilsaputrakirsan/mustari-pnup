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

/**
 * Dev server Vite selalu jatuh ke index.html (varian 1B) untuk rute
 * seperti /masuk. Arahkan setiap navigasi halaman ke index.demo.html
 * agar refresh dan deep link tetap memuat aplikasi demo.
 */
const fallbackDemo = {
    name: 'fallback-demo',
    configureServer(server) {
        server.middlewares.use((req, _res, next) => {
            const jalur = req.url.split('?')[0]
            if (req.headers.accept?.includes('text/html') && !jalur.includes('.')) {
                req.url = '/index.demo.html'
            }
            next()
        })
    },
}

export default defineConfig({
    plugins: [vue(), fallbackDemo],
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

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
import path from 'node:path'
import fs from 'node:fs/promises'
import zlib from 'node:zlib'

/**
 * Plugin kompresi Gzip + Brotli buatan sendiri.
 *
 * CATATAN: sebelumnya dipakai `vite-plugin-compression` dipanggil dua kali
 * (sekali untuk gzip, sekali untuk brotli). Paket itu punya `mtimeCache`
 * bertingkat modul (bukan per-instance), jadi saat instance kedua (brotli)
 * berjalan, ia mengira file sudah "ditangani" oleh instance pertama (gzip)
 * dan langsung melewatkannya — hasilnya file .br tidak pernah terbentuk.
 * Plugin di bawah ini melakukan gzip & brotli dalam satu jalur per file,
 * jadi tidak ada cache yang bentrok.
 */
function compressAssets({ filter = /\.(js|mjs|json|css|html)$/i, threshold = 1024 } = {}) {
    let outDir

    async function collectFiles(dir) {
        const entries = await fs.readdir(dir, { withFileTypes: true })
        const files = await Promise.all(entries.map((entry) => {
            const full = path.join(dir, entry.name)
            return entry.isDirectory() ? collectFiles(full) : [full]
        }))
        return files.flat()
    }

    return {
        name: 'compress-gzip-brotli',
        apply: 'build',
        enforce: 'post',
        configResolved(resolvedConfig) {
            outDir = path.isAbsolute(resolvedConfig.build.outDir)
                ? resolvedConfig.build.outDir
                : path.join(resolvedConfig.root, resolvedConfig.build.outDir)
        },
        async closeBundle() {
            const files = (await collectFiles(outDir)).filter((f) => filter.test(f))
            for (const file of files) {
                const { size } = await fs.stat(file)
                if (size < threshold) continue
                const content = await fs.readFile(file)

                const gz = zlib.gzipSync(content, { level: zlib.constants.Z_BEST_COMPRESSION })
                await fs.writeFile(`${file}.gz`, gz)

                const br = zlib.brotliCompressSync(content, {
                    params: {
                        [zlib.constants.BROTLI_PARAM_QUALITY]: zlib.constants.BROTLI_MAX_QUALITY,
                        [zlib.constants.BROTLI_PARAM_MODE]: zlib.constants.BROTLI_MODE_TEXT,
                    },
                })
                await fs.writeFile(`${file}.br`, br)
            }
            console.log(`✨ [compress-gzip-brotli]: ${files.length} file dikompres (gzip + brotli)`)
        },
    }
}

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

        // Plugin: Kompresi Gzip + Brotli (lihat catatan di atas)
        compressAssets({ threshold: 1024 }),
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

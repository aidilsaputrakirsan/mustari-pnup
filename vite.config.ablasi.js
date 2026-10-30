/**
 * ============================================
 * VITE CONFIG - STUDI ABLASI (REVISI PENGUJI)
 * ============================================
 * Membangun beberapa varian SIMTA yang masing-masing hanya mengaktifkan
 * SATU teknik optimasi, agar kontribusi tiap teknik dapat diukur terpisah:
 *
 *   A0-kontrol   : eager, 1 bundle, tanpa kompresi
 *   A1-splitting : + manualChunks (vendor-vue, vendor-chart)
 *   A2-lazy      : + lazy loading rute (dynamic import), tanpa prefetch
 *   A3-prefetch  : + lazy loading rute + prefetching requestIdleCallback
 *   A4-gzip      : + kompresi gzip saja (bundle tetap monolitik)
 *   A5-gabungan  : splitting + lazy + prefetch + gzip
 *
 * Pemakaian: VARIAN=A1-splitting npx vite build --config vite.config.ablasi.js
 * (atau `node build_ablasi.cjs` untuk membangun semuanya)
 * ============================================
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import path from 'node:path'
import fs from 'node:fs/promises'
import zlib from 'node:zlib'

export const VARIAN = {
    'A0-kontrol': { router: 'eager', splitting: false, gzip: false },
    'A1-splitting': { router: 'eager', splitting: true, gzip: false },
    'A2-lazy': { router: 'lazy', splitting: false, gzip: false },
    'A3-prefetch': { router: 'prefetch', splitting: false, gzip: false },
    'A4-gzip': { router: 'eager', splitting: false, gzip: true },
    'A5-gabungan': { router: 'prefetch', splitting: true, gzip: true },
}

// Kompresi gzip saja (tanpa brotli) agar efek gzip dapat diisolasi
function gzipAssets({ filter = /\.(js|mjs|json|css|html)$/i, threshold = 1024 } = {}) {
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
        name: 'compress-gzip',
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
                const gz = zlib.gzipSync(await fs.readFile(file), { level: zlib.constants.Z_BEST_COMPRESSION })
                await fs.writeFile(`${file}.gz`, gz)
            }
        },
    }
}

function manualChunks(id) {
    if (id.includes('node_modules/vue') || id.includes('node_modules/vue-router') || id.includes('node_modules/pinia') || id.includes('node_modules/@vue')) {
        return 'vendor-vue'
    }
    if (id.includes('node_modules/chart.js') || id.includes('node_modules/vue-chartjs')) {
        return 'vendor-chart'
    }
}

export default defineConfig(() => {
    const nama = process.env.VARIAN
    const v = VARIAN[nama]
    if (!v) throw new Error(`VARIAN tidak dikenal: ${nama}. Pilihan: ${Object.keys(VARIAN).join(', ')}`)

    return {
        plugins: [vue(), tailwindcss(), ...(v.gzip ? [gzipAssets()] : [])],
        define: { __VARIAN_ABLASI__: JSON.stringify(nama) },
        resolve: {
            alias: { '@ablasi-router': path.resolve(__dirname, `src/ablasi/router.${v.router}.js`) },
        },
        build: {
            outDir: `dist-ablasi/${nama}`,
            emptyOutDir: true,
            target: 'es2020',
            rollupOptions: {
                input: 'index.ablasi.html',
                output: {
                    ...(v.splitting ? { manualChunks } : {}),
                    chunkFileNames: 'assets/js/[name]-[hash].js',
                    entryFileNames: 'assets/js/[name]-[hash].js',
                    assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
                },
            },
        },
    }
})

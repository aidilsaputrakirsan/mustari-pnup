/**
 * ============================================
 * BUILD UNTUK NETLIFY
 * ============================================
 * Membungkus hasil `vite build` menjadi folder publish
 * yang siap dilayani Netlify sebagai static site:
 *   1. Menyalin dist hasil build ke folder publish
 *   2. Mengganti nama entry HTML menjadi index.html
 *   3. Menulis _redirects agar deep link SPA tidak 404
 *
 * Pemakaian: node scripts/build-netlify.mjs <simta|cp>
 * ============================================
 */
import { cp, rename, rm, writeFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'

const TARGET = {
    simta: {
        sumber: 'dist-optimized',
        entri: 'index.optimized.html',
        publish: 'dist-netlify-simta',
    },
    cp: {
        sumber: 'dist-cp-optimized',
        entri: 'index.cp.optimized.html',
        publish: 'dist-netlify-cp',
    },
}

const nama = process.argv[2]
const cfg = TARGET[nama]

if (!cfg) {
    console.error(`Target tidak dikenal: "${nama}". Pilih salah satu: ${Object.keys(TARGET).join(', ')}`)
    process.exit(1)
}

if (!existsSync(cfg.sumber)) {
    console.error(`Folder "${cfg.sumber}" tidak ada. Jalankan build vite-nya lebih dulu.`)
    process.exit(1)
}

await rm(cfg.publish, { recursive: true, force: true })
await cp(cfg.sumber, cfg.publish, { recursive: true })
await rename(`${cfg.publish}/${cfg.entri}`, `${cfg.publish}/index.html`)

// Fallback SPA: semua rute vue-router dilayani index.html
await writeFile(`${cfg.publish}/_redirects`, '/*    /index.html   200\n')

console.log(`[netlify] ${cfg.sumber} → ${cfg.publish}/ (entri: index.html, + _redirects)`)

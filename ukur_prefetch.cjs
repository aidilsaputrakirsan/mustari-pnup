/**
 * ============================================
 * BUKTI MEKANISME PREFETCHING
 * ============================================
 * Merekam berkas JavaScript apa saja yang diminta peramban beserta waktunya,
 * pada versi optimized, TANPA satu pun interaksi klik dari pengguna.
 *
 * Tujuannya membuktikan secara faktual bahwa chunk halaman yang belum diakses
 * (DaftarJudulView dan DetailBimbinganView) tetap terunduh di latar belakang
 * berkat router.afterEach + requestIdleCallback.
 *
 * CATATAN: skrip ini TIDAK mengukur kecepatan navigasi. Yang direkam hanyalah
 * urutan dan waktu permintaan berkas, sebagai bukti bahwa mekanisme prefetching
 * benar-benar berjalan.
 *
 * Keluaran: laporan_tesis/data_pengukuran/prefetch_network_log.json
 */
const puppeteer = require('puppeteer');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'data_pengukuran');
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const PORT = 4011;
const URL = `http://localhost:${PORT}/index.optimized.html`;
const RUNS = 5;
const TUNGGU_MS = 6000; // beri waktu requestIdleCallback menyala

function rekamSatuRun(browser) {
    return new Promise(async (resolve) => {
        const page = await browser.newPage();
        const jejak = [];
        let t0 = null;

        page.on('request', (req) => {
            const url = req.url();
            if (!url.endsWith('.js') && !url.includes('.js?')) return;
            if (t0 === null) t0 = Date.now();
            jejak.push({
                file: path.basename(url.split('?')[0]),
                waktu_ms: Date.now() - t0,
            });
        });

        await page.goto(URL, { waitUntil: 'load' });
        // TIDAK ada klik, TIDAK ada navigasi — murni diam menunggu
        await new Promise((r) => setTimeout(r, TUNGGU_MS));
        await page.close();
        resolve(jejak);
    });
}

async function start() {
    const HTTP_SERVER = path.join(__dirname, 'node_modules', 'http-server', 'bin', 'http-server');
    console.log(`Menjalankan server dist-optimized di port ${PORT} ...`);
    const server = exec(`node "${HTTP_SERVER}" dist-optimized -p ${PORT} -c-1 -g -b`, { cwd: __dirname });
    await new Promise((r) => setTimeout(r, 3000));

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const semua = [];
    for (let i = 0; i < RUNS; i++) {
        console.log(`  Run ${i + 1}/${RUNS} ...`);
        const jejak = await rekamSatuRun(browser);
        semua.push(jejak);
        jejak.forEach((j) => console.log(`      ${String(j.waktu_ms).padStart(5)} ms  ${j.file}`));
        console.log('');
    }

    await browser.close();
    server.kill();

    const keluaran = path.join(OUTPUT_DIR, 'prefetch_network_log.json');
    fs.writeFileSync(keluaran, JSON.stringify(semua, null, 2));
    console.log(`Tersimpan: ${path.basename(keluaran)} (${RUNS} run, tanpa interaksi klik)`);
    process.exit(0);
}

start();

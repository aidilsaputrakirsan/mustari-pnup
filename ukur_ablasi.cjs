/**
 * ============================================
 * PENGUKURAN STUDI ABLASI (REVISI PENGUJI)
 * ============================================
 * Mengukur kontribusi masing-masing teknik (splitting, lazy loading,
 * prefetching, gzip) secara terpisah. Varian dibangun oleh build_ablasi.cjs.
 *
 * Per varian dan per skenario (5 repetisi):
 *   - FCP, LCP, TBT, Load Time, JS Heap (PerformanceObserver, sama seperti ukur_multirun.cjs)
 *   - jumlah & ukuran transfer berkas JS pada muatan awal (Resource Timing)
 *   - latensi navigasi Dashboard -> Daftar Judul setelah halaman idle
 * Ditambah audit Lighthouse 5 repetisi per varian.
 *
 * Keluaran: laporan_tesis/data_pengukuran/ablasi/*.json
 * ============================================
 */
const puppeteer = require('puppeteer');
const { exec } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');

process.env.CHROME_PATH = puppeteer.executablePath();

const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'data_pengukuran', 'ablasi');
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const RUNS = Number(process.env.RUNS) || 5;
const LIGHTHOUSE_CLI = path.join(__dirname, 'node_modules', 'lighthouse', 'cli', 'index.js');

const TARGETS = [
    { name: 'R-baseline', dir: 'dist-baseline', html: 'index.baseline.html', port: 4101, flags: '-g -b' },
    { name: 'A0-kontrol', dir: 'dist-ablasi/A0-kontrol', html: 'index.ablasi.html', port: 4102, flags: '-g' },
    { name: 'A1-splitting', dir: 'dist-ablasi/A1-splitting', html: 'index.ablasi.html', port: 4103, flags: '-g' },
    { name: 'A2-lazy', dir: 'dist-ablasi/A2-lazy', html: 'index.ablasi.html', port: 4104, flags: '-g' },
    { name: 'A3-prefetch', dir: 'dist-ablasi/A3-prefetch', html: 'index.ablasi.html', port: 4105, flags: '-g' },
    { name: 'A4-gzip', dir: 'dist-ablasi/A4-gzip', html: 'index.ablasi.html', port: 4106, flags: '-g' },
    { name: 'A5-gabungan', dir: 'dist-ablasi/A5-gabungan', html: 'index.ablasi.html', port: 4107, flags: '-g' },
    { name: 'R-optimized', dir: 'dist-optimized', html: 'index.optimized.html', port: 4108, flags: '-g -b' },
]

// Profil jaringan setara "Slow 4G" Lighthouse (RTT 150 ms, 1,6 Mbps turun, 750 Kbps naik)
const JARINGAN_LAMBAT = {
    offline: false,
    latency: 150,
    downloadThroughput: (1.6 * 1024 * 1024) / 8,
    uploadThroughput: (750 * 1024) / 8,
};

const SCENARIOS = [
    { name: 'ideal', cpu: 1, network: null },
    { name: 'cpu_lambat', cpu: 4, network: null },
    { name: 'jaringan_lambat', cpu: 4, network: JARINGAN_LAMBAT },
];

const tunggu = (ms) => new Promise((r) => setTimeout(r, ms));

const MIME = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.json': 'application/json' };

/**
 * Server statis di dalam proses (setara `http-server -c-1 -g [-b]`): menyajikan
 * varian .br/.gz yang sudah dikompres saat build bila peramban menerimanya.
 * Dipakai alih-alih child process http-server agar server tidak mati diam-diam
 * saat skrip dijalankan di latar belakang.
 */
function jalankanServer(t) {
    const root = path.join(__dirname, t.dir);
    const brotli = t.flags.includes('-b');
    const server = http.createServer((req, res) => {
        const rel = decodeURIComponent(req.url.split('?')[0]);
        const file = path.join(root, rel === '/' ? t.html : rel);
        if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
            res.writeHead(404); return res.end();
        }
        const ae = req.headers['accept-encoding'] || '';
        const headers = { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache, no-store' };
        let kirim = file;
        if (brotli && /\bbr\b/.test(ae) && fs.existsSync(file + '.br')) { kirim = file + '.br'; headers['Content-Encoding'] = 'br'; }
        else if (/\bgzip\b/.test(ae) && fs.existsSync(file + '.gz')) { kirim = file + '.gz'; headers['Content-Encoding'] = 'gzip'; }
        if (headers['Content-Encoding']) headers['Vary'] = 'Accept-Encoding';
        res.writeHead(200, headers);
        fs.createReadStream(kirim).pipe(res);
    });
    return new Promise((resolve, reject) => {
        server.once('error', reject);
        server.listen(t.port, '127.0.0.1', () => resolve(server));
    });
}

async function ukurSatuRun(url, scenario) {
    const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--disable-setuid-sandbox'] });
    try {
        const page = await browser.newPage();
        const client = await page.target().createCDPSession();
        await client.send('Emulation.setCPUThrottlingRate', { rate: scenario.cpu });
        if (scenario.network) {
            await client.send('Network.enable');
            await client.send('Network.emulateNetworkConditions', scenario.network);
        }

        let metrik = null;
        page.on('console', (msg) => {
            const text = msg.text();
            if (!text.includes('"Variant"')) return;
            try { metrik = JSON.parse(text.substring(text.indexOf('{'))); } catch (e) { }
        });

        await page.goto(url, { waitUntil: 'load', timeout: 60000 });
        for (let i = 0; i < 100 && !metrik; i++) await tunggu(100);
        if (!metrik) return null;

        // Beri waktu idle agar prefetching (requestIdleCallback) sempat berjalan
        await tunggu(2000);

        const muatanAwal = await page.evaluate(() => {
            const js = performance.getEntriesByType('resource').filter((e) => /\.js(\?|$)/.test(e.name));
            return {
                jumlah_js: js.length,
                transfer_js_KB: +(js.reduce((a, e) => a + e.transferSize, 0) / 1024).toFixed(2),
                dekode_js_KB: +(js.reduce((a, e) => a + e.decodedBodySize, 0) / 1024).toFixed(2),
                berkas_js: js.map((e) => e.name.split('/').pop()),
            };
        });

        const navigasi_ms = await page.evaluate(() => new Promise((resolve) => {
            const t0 = performance.now();
            location.hash = '#/daftar-judul';
            const cek = () => {
                if (document.querySelector('.daftar-judul')) resolve(+(performance.now() - t0).toFixed(1));
                else if (performance.now() - t0 > 20000) resolve(null);
                else requestAnimationFrame(cek);
            };
            requestAnimationFrame(cek);
        }));

        return {
            FCP_ms: metrik.FCP_ms,
            LCP_ms: metrik.LCP_ms,
            TBT_ms: metrik.TBT_ms,
            LoadTime_ms: metrik.LoadTime_ms,
            MemoryUsed_MB: metrik.MemoryUsed_MB,
            ...muatanAwal,
            Navigasi_ms: navigasi_ms,
        };
    } finally {
        await browser.close();
    }
}

function runLighthouse(url) {
    return new Promise((resolve) => {
        const cmd = `node "${LIGHTHOUSE_CLI}" "${url}" --output=json --chrome-flags="--headless --no-sandbox" --only-categories=performance --quiet`;
        exec(cmd, { maxBuffer: 20 * 1024 * 1024, cwd: __dirname }, (err, stdout) => {
            if (err) { console.error(`Lighthouse error: ${err.message}`); return resolve(null); }
            try {
                const report = JSON.parse(stdout);
                const a = report.audits;
                resolve({
                    PerformanceScore: Math.round(report.categories.performance.score * 100),
                    FCP_ms: Math.round(a['first-contentful-paint'].numericValue),
                    LCP_ms: Math.round(a['largest-contentful-paint'].numericValue),
                    TTI_ms: a['interactive'] ? Math.round(a['interactive'].numericValue) : null,
                    TBT_ms: Math.round(a['total-blocking-time'].numericValue),
                    SpeedIndex: Math.round(a['speed-index'].numericValue),
                });
            } catch (e) { console.error(`JSON parse error: ${e.message}`); resolve(null); }
        });
    });
}

async function start() {
    const hanyaLighthouse = process.argv.includes('--lighthouse');
    const tanpaLighthouse = process.argv.includes('--tanpa-lighthouse');

    const servers = await Promise.all(TARGETS.map(jalankanServer));

    for (const t of TARGETS) {
        const url = `http://127.0.0.1:${t.port}/${t.html}`;

        if (!hanyaLighthouse) {
            for (const s of SCENARIOS) {
                const hasil = [];
                for (let i = 0; i < RUNS; i++) {
                    const d = await ukurSatuRun(url, s).catch((e) => { console.error(e.message); return null; });
                    if (d) hasil.push(d);
                    console.log(`${t.name} | ${s.name} | run ${i + 1}: ` +
                        (d ? `FCP=${d.FCP_ms} TBT=${d.TBT_ms} Load=${d.LoadTime_ms} JS=${d.jumlah_js}/${d.transfer_js_KB}KB Nav=${d.Navigasi_ms}` : 'GAGAL'));
                }
                fs.writeFileSync(path.join(OUTPUT_DIR, `po_${t.name}_${s.name}.json`), JSON.stringify(hasil, null, 2));
            }
        }

        if (!tanpaLighthouse) {
            const hasil = [];
            for (let i = 0; i < RUNS; i++) {
                const d = await runLighthouse(url);
                if (d) hasil.push(d);
                console.log(`${t.name} | lighthouse | run ${i + 1}: ` + (d ? `Score=${d.PerformanceScore} FCP=${d.FCP_ms} LCP=${d.LCP_ms} TBT=${d.TBT_ms}` : 'GAGAL'));
            }
            fs.writeFileSync(path.join(OUTPUT_DIR, `lh_${t.name}.json`), JSON.stringify(hasil, null, 2));
        }
    }

    servers.forEach((s) => s.close());
    console.log('✅ Pengukuran ablasi selesai');
    process.exit(0);
}

start();

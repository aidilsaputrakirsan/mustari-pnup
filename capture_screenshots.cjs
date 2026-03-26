const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'chapters', 'images');
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const PAGES = [
    { name: 'dashboard',      hash: '#/',               label: 'Dashboard' },
    { name: 'daftar_judul',   hash: '#/daftar-judul',   label: 'Daftar Judul' },
    { name: 'jadwal_seminar', hash: '#/jadwal-seminar',  label: 'Jadwal Seminar' },
];

async function captureScreenshots() {
    console.log("Mulai mengambil screenshot bukti...");
    const browser = await puppeteer.launch({
        headless: "new",
        defaultViewport: { width: 1280, height: 800 }
    });

    const page = await browser.newPage();

    try {
        for (const p of PAGES) {
            // Baseline
            await page.goto(`http://localhost:4001/index.baseline.html${p.hash}`, { waitUntil: 'networkidle2' });
            await page.screenshot({ path: path.join(OUTPUT_DIR, `bukti_baseline_${p.name}.png`) });
            console.log(`✅ Baseline - ${p.label} tersimpan.`);

            // Optimized
            await page.goto(`http://localhost:4002/index.optimized.html${p.hash}`, { waitUntil: 'networkidle2' });
            await page.screenshot({ path: path.join(OUTPUT_DIR, `bukti_optimized_${p.name}.png`) });
            console.log(`✅ Optimized - ${p.label} tersimpan.`);
        }

        // Tetap simpan file lama (backward compat untuk gambar 3.2 & 3.3 yang sudah ada)
        await page.goto('http://localhost:4001/index.baseline.html#/', { waitUntil: 'networkidle2' });
        await page.screenshot({ path: path.join(OUTPUT_DIR, 'bukti_baseline.png') });

        await page.goto('http://localhost:4002/index.optimized.html#/', { waitUntil: 'networkidle2' });
        await page.screenshot({ path: path.join(OUTPUT_DIR, 'bukti_optimized.png') });

    } catch (e) {
        console.log("Error mengambil screenshot:", e);
    }

    await browser.close();
    console.log("Selesai.");
}

captureScreenshots();

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'chapters', 'images');
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function captureScreenshots() {
    console.log("Mulai mengambil screenshot bukti...");
    const browser = await puppeteer.launch({
        headless: "new",
        defaultViewport: { width: 1280, height: 800 }
    });

    const page = await browser.newPage();

    try {
        await page.goto('http://localhost:4001/index.baseline.html', { waitUntil: 'networkidle2' });
        await page.screenshot({ path: path.join(OUTPUT_DIR, 'bukti_baseline.png') });
        console.log("✅ Screenshot Baseline tersimpan.");

        await page.goto('http://localhost:4002/index.optimized.html', { waitUntil: 'networkidle2' });
        await page.screenshot({ path: path.join(OUTPUT_DIR, 'bukti_optimized.png') });
        console.log("✅ Screenshot Optimized tersimpan.");

    } catch (e) {
        console.log("Error mengambil screenshot:", e);
    }

    await browser.close();
    console.log("Selesai.");
}

captureScreenshots();

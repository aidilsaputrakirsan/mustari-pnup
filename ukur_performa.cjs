const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'data_pengukuran');
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Konfigurasi Skenario: [Nama Skenario, CPU Throttling Rate]
const SCENARIOS = [
    { name: 'ideal', cpuThrottling: 1 },         // Fast CPU, No delay
    { name: 'cpu_lambat', cpuThrottling: 4 },    // 4x CPU Slowdown
];

const TARGETS = [
    { name: 'baseline', url: 'http://localhost:4001/index.baseline.html' },
    { name: 'optimized', url: 'http://localhost:4002/index.optimized.html' }
];

async function runMeasurement(target, scenario) {
    console.log(`Mengukur: ${target.name} | Skenario: ${scenario.name}`);

    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Set CPU Throttling via Chrome DevTools Protocol (CDP)
    const client = await page.target().createCDPSession();
    await client.send('Emulation.setCPUThrottlingRate', { rate: scenario.cpuThrottling });

    // Menitipkan penangkap console.log JSON dari PerformanceTracker
    let metricsData = null;
    page.on('console', msg => {
        try {
            const text = msg.text();
            if (text.includes('"Variant"')) {
                // Remove prefix if any
                const jsonStr = text.substring(text.indexOf('{'));
                metricsData = JSON.parse(jsonStr);
                console.log("  -> (Data Tertangkap)");
            }
        } catch (e) { }
    });

    await page.goto(target.url, { waitUntil: 'load' });

    // Tunggu 5 detik untuk mengakomodasi setTimeout PerformanceTracker
    await new Promise(r => setTimeout(r, 5000));

    await browser.close();

    if (metricsData) {
        // Tulis ke File
        const filename = `${target.name}_${scenario.name}.json`;
        fs.writeFileSync(
            path.join(OUTPUT_DIR, filename),
            JSON.stringify(metricsData, null, 2)
        );
        console.log(`✅ Tersimpan: ${filename}`);
    } else {
        console.log(`❌ Gagal mendapat data untuk: ${target.name}_${scenario.name}`);
    }
}

async function start() {
    for (const target of TARGETS) {
        for (const scenario of SCENARIOS) {
            await runMeasurement(target, scenario);
        }
    }
    console.log("Semua pengukuran selesai dilakukan!");
}

start();

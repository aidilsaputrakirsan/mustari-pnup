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

// Target Port web server lokak untuk Company profile
const TARGETS = [
    { name: 'cp_baseline', url: 'http://127.0.0.1:4005/index.cp.baseline.html' },
    { name: 'cp_optimized', url: 'http://127.0.0.1:4006/index.cp.optimized.html' }
];

async function runMeasurement(target, scenario) {
    console.log(`Mengukur: ${target.name} | Skenario: ${scenario.name}`);

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Set CPU Throttling via Chrome DevTools Protocol (CDP)
    const client = await page.target().createCDPSession();
    await client.send('Emulation.setCPUThrottlingRate', { rate: scenario.cpuThrottling });

    // Menitipkan penangkap console.log JSON dari PerformanceTracker
    let metricsData = null;
    page.on('console', msg => {
        const text = msg.text();
        console.log(`[BROWSER]: ${text}`); // See what browser says
        try {
            if (text.includes('"Variant"')) {
                // Remove prefix if any
                const jsonStr = text.substring(text.indexOf('{'));
                metricsData = JSON.parse(jsonStr);
                console.log("  -> (Data Tertangkap)");
            }
        } catch (e) { }
    });

    page.on('response', response => {
        if (!response.ok()) {
            console.log(`[HTTP ERROR] ${response.status()} on ${response.url()}`);
        }
    });

    try {
        await page.goto(target.url, { waitUntil: 'load' });
    } catch (err) {
        console.error("Gagal membuka halaman: ", err);
    }

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
    const { exec } = require('child_process');
    console.log("Menghidupkan server statis di port 4005 dan 4006...");
    const server1 = exec('npx.cmd http-server dist-cp-baseline -p 4005 -c-1', { cwd: __dirname });
    const server2 = exec('npx.cmd http-server dist-cp-optimized -p 4006 -c-1', { cwd: __dirname });

    // Beri waktu 3 detik agar server siap
    await new Promise(r => setTimeout(r, 3000));

    for (const target of TARGETS) {
        for (const scenario of SCENARIOS) {
            await runMeasurement(target, scenario);
        }
    }

    // Matikan server setelah selesai
    server1.kill();
    server2.kill();
    console.log("Semua pengukuran Company Profile selesai dilakukan!");
}

start();

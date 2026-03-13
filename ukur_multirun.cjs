/**
 * Multi-Run PerformanceObserver Measurement for SIMTA
 * Runs 5 repetitions per scenario for statistical analysis
 */
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'data_pengukuran');
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const SCENARIOS = [
    { name: 'ideal', cpuThrottling: 1 },
    { name: 'cpu_lambat', cpuThrottling: 4 },
];

const TARGETS = [
    { name: 'baseline', url: 'http://localhost:4001/index.baseline.html' },
    { name: 'optimized', url: 'http://localhost:4002/index.optimized.html' }
];

const RUNS = 5;

async function runMeasurement(target, scenario) {
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    const client = await page.target().createCDPSession();
    await client.send('Emulation.setCPUThrottlingRate', { rate: scenario.cpuThrottling });

    let metricsData = null;
    page.on('console', msg => {
        try {
            const text = msg.text();
            if (text.includes('"Variant"')) {
                const jsonStr = text.substring(text.indexOf('{'));
                metricsData = JSON.parse(jsonStr);
            }
        } catch (e) { }
    });

    await page.goto(target.url, { waitUntil: 'load' });
    await new Promise(r => setTimeout(r, 5000));
    await browser.close();

    return metricsData;
}

async function start() {
    const { exec } = require('child_process');
    console.log("Starting servers on ports 4001 and 4002...");
    const server1 = exec('npx.cmd http-server dist-baseline -p 4001 -c-1', { cwd: __dirname });
    const server2 = exec('npx.cmd http-server dist-optimized -p 4002 -c-1', { cwd: __dirname });
    await new Promise(r => setTimeout(r, 3000));

    for (const target of TARGETS) {
        for (const scenario of SCENARIOS) {
            const results = [];
            for (let i = 0; i < RUNS; i++) {
                console.log(`  Run ${i + 1}/${RUNS}: ${target.name} | ${scenario.name}`);
                const data = await runMeasurement(target, scenario);
                if (data) {
                    results.push(data);
                    console.log(`    -> FCP=${data.FCP_ms} LCP=${data.LCP_ms} TBT=${data.TBT_ms}`);
                } else {
                    console.log(`    -> FAILED`);
                }
            }
            const filename = `multirun_${target.name}_${scenario.name}.json`;
            fs.writeFileSync(
                path.join(OUTPUT_DIR, filename),
                JSON.stringify(results, null, 2)
            );
            console.log(`✅ Saved: ${filename} (${results.length} runs)`);
        }
    }

    server1.kill();
    server2.kill();
    console.log("All SIMTA multi-run measurements complete!");
}

start();

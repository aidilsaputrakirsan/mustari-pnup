/**
 * Lighthouse Automated Measurement Script
 * Measures both SIMTA and Company Profile with Lighthouse
 * Output: JSON files with Performance Score, FCP, LCP, TTI, TBT, Speed Index
 */
const { exec, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'data_pengukuran');
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const RUNS = 5;

// All targets to measure
const TARGETS = [
    { name: 'lighthouse_baseline', url: 'http://localhost:4001/index.baseline.html', server: { dir: 'dist-baseline', port: 4001 } },
    { name: 'lighthouse_optimized', url: 'http://localhost:4002/index.optimized.html', server: { dir: 'dist-optimized', port: 4002 } },
    { name: 'lighthouse_cp_baseline', url: 'http://127.0.0.1:4005/index.cp.baseline.html', server: { dir: 'dist-cp-baseline', port: 4005 } },
    { name: 'lighthouse_cp_optimized', url: 'http://127.0.0.1:4006/index.cp.optimized.html', server: { dir: 'dist-cp-optimized', port: 4006 } },
];

function runLighthouse(url) {
    return new Promise((resolve, reject) => {
        const cmd = `npx.cmd lighthouse "${url}" --output=json --chrome-flags="--headless=new --no-sandbox" --only-categories=performance --quiet`;
        exec(cmd, { maxBuffer: 10 * 1024 * 1024, cwd: __dirname }, (err, stdout, stderr) => {
            if (err) {
                console.error(`Lighthouse error: ${err.message}`);
                resolve(null);
                return;
            }
            try {
                const report = JSON.parse(stdout);
                const audits = report.audits;
                const result = {
                    PerformanceScore: Math.round(report.categories.performance.score * 100),
                    FCP_ms: Math.round(audits['first-contentful-paint'].numericValue),
                    LCP_ms: Math.round(audits['largest-contentful-paint'].numericValue),
                    TTI_ms: audits['interactive'] ? Math.round(audits['interactive'].numericValue) : null,
                    TBT_ms: Math.round(audits['total-blocking-time'].numericValue),
                    SpeedIndex: Math.round(audits['speed-index'].numericValue),
                    CLS: audits['cumulative-layout-shift'] ? parseFloat(audits['cumulative-layout-shift'].numericValue.toFixed(4)) : null,
                };
                resolve(result);
            } catch (e) {
                console.error(`JSON parse error: ${e.message}`);
                resolve(null);
            }
        });
    });
}

async function start() {
    // Start all servers
    console.log("Starting all servers...");
    const servers = [];
    for (const t of TARGETS) {
        const s = exec(`npx.cmd http-server ${t.server.dir} -p ${t.server.port} -c-1`, { cwd: __dirname });
        servers.push(s);
    }
    await new Promise(r => setTimeout(r, 3000));
    console.log("Servers ready.");

    for (const target of TARGETS) {
        const results = [];
        for (let i = 0; i < RUNS; i++) {
            console.log(`  Run ${i + 1}/${RUNS}: ${target.name}`);
            const data = await runLighthouse(target.url);
            if (data) {
                results.push(data);
                console.log(`    -> Score=${data.PerformanceScore} FCP=${data.FCP_ms} LCP=${data.LCP_ms} TTI=${data.TTI_ms} TBT=${data.TBT_ms}`);
            } else {
                console.log(`    -> FAILED`);
            }
        }
        const filename = `${target.name}.json`;
        fs.writeFileSync(
            path.join(OUTPUT_DIR, filename),
            JSON.stringify(results, null, 2)
        );
        console.log(`✅ Saved: ${filename} (${results.length} runs)\n`);
    }

    // Kill all servers
    servers.forEach(s => s.kill());
    console.log("All Lighthouse measurements complete!");
}

start();

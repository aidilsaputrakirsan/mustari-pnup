/**
 * ============================================
 * PERFORMANCE TRACKER (Algoritma Pengukuran)
 * ============================================
 * Script murni untuk mengukur metrik performa aplikasi SPA.
 * Menggunakan standar Web Performance API (Bawaan Browser).
 * 
 * Pengukuran meliputi:
 * 1. FCP (First Contentful Paint)
 * 2. LCP (Largest Contentful Paint) 
 * 3. TBT (Total Blocking Time)
 * 4. JS Memory Used
 * 5. Window Load Time
 * 
 * Data akan dicetak te Console dalam format JSON / Tabel
 * untuk memudahkan *copy-paste* ke laporan tesis.
 * ============================================
 */

export function initPerformanceTracker(variantName = 'Unknown') {
    console.group(`📊 [ALG-TRACKER] Inisialisasi Pengukuran untuk: ${variantName}`);

    const metrics = {
        Variant: variantName,
        FCP_ms: null,
        LCP_ms: null,
        TBT_ms: 0,
        LoadTime_ms: null,
        MemoryUsed_MB: null,
        UserAgent: navigator.userAgent
    };

    // 1 & 2. Observer untuk FCP dan LCP
    try {
        const paintObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.name === 'first-contentful-paint') {
                    metrics.FCP_ms = Math.round(entry.startTime);
                    console.log(`[Metric] FCP: ${metrics.FCP_ms} ms`);
                }
            }
        });
        paintObserver.observe({ type: 'paint', buffered: true });

        const lcpObserver = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            metrics.LCP_ms = Math.round(lastEntry.startTime);
            console.log(`[Metric] LCP: ${metrics.LCP_ms} ms`);
        });
        lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });

    } catch (e) {
        console.warn("PerformanceObserver for Paint/LCP not supported in this browser.");
    }

    // 3. Observer untuk TBT (Long Tasks)
    try {
        const longTaskObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                // TBT adalah akumulasi durasi tugas yg lebih dari 50ms
                if (entry.duration > 50) {
                    metrics.TBT_ms += Math.round(entry.duration - 50);
                }
            }
        });
        longTaskObserver.observe({ type: 'longtask', buffered: true });
    } catch (e) {
        console.warn("PerformanceObserver for LongTask not supported in this browser.");
    }

    // 4. Pengukuran saat Window Load Selesai
    window.addEventListener('load', () => {
        setTimeout(() => {
            // Calculate Load Time
            const navEntry = performance.getEntriesByType('navigation')[0];
            if (navEntry) {
                metrics.LoadTime_ms = Math.round(navEntry.loadEventEnd - navEntry.startTime);
            }

            // Calculate JS Memory (Bila di-support oleh V8 JS Engine spt Chrome)
            if (performance.memory) {
                metrics.MemoryUsed_MB = (performance.memory.usedJSHeapSize / (1024 * 1024)).toFixed(2);
            }

            console.group(`✨ [ALG-TRACKER] HASIL AKHIR: ${variantName}`);
            console.table(metrics);
            console.log("JSON Untuk Disalin ke Laporan:");
            console.log(JSON.stringify(metrics, null, 2));
            console.groupEnd();

        }, 3000); // Beri jeda 3 detik setelah load untuk memastikan LCP / Long Tasks selesai tercatat
    });

    console.groupEnd();
}

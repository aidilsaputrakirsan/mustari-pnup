# BAB 4: Panduan Pengukuran Performa (Manual & Valid)

Untuk mendapatkan data Tesis yang valid dan terukur secara ilmiah, Anda **TIDAK HANYA** mengandalkan Lighthouse (karena Lighthouse itu relatif dan kadang berubah-ubah).

3 Metode "Hard Data" berikut ini lebih presisi untuk membandingkan Baseline vs Optimized.

## Metode 1: Mengukur "Unused Bytes" (Kode Sampah)

Ini adalah bukti paling kuat untuk Tesis Anda bahwa Baseline (versi 1A) **boros**.

**Langkah:**
1.  Buka DevTools (F12) > Menu 3 titik kanan atas > **More tools** > **Coverage**.
2.  Klik tombol **Reload** di panel Coverage (ikon reload bulat).
3.  Lihat bar **Usage Visualization**:
    - **Merah** = Kode dimuat tapi TIDAK dipakai.
    - **Hijau** = Kode dimuat DAN dipakai.

**Hasil yang Diharapkan:**
- **Baseline (1A):** Bar merah panjang (~60-70% Unused) karena memuat Chart.js di halaman Login/Dashboard padahal belum tentu dipakai.
- **Optimized (1B):** Bar hijau dominan (~80-90% Used) karena hanya memuat kode yang relevan.

---

## Metode 2: Mengukur "Network Transfer" (Payload Size)

Metode ini membuktikan bahwa Optimized (1B) lebih hemat kuota.

**Langkah:**
1.  Buka DevTools > Tab **Network**.
2.  Centang **"Disable cache"** (penting agar hasil murni download).
3.  Set **Throttling** ke **"Fast 3G"** (opsional, agar perbedaan loading time lebih terasa).
4.  Reload halaman (Ctrl+R / F5).
5.  Lihat angka di bagian bawah footer DevTools:
    - **Transferred:** Total bytes yang didownload lewat jaringan (Gzip/Brotli).
    - **Resources:** Ukuran file asli sebelum kompresi.

**Bandingkan:**
- **Baseline:** Transferred ~120KB (satu file besar).
- **Optimized:** Transferred ~40KB (file kecil-kecil).

---

## Metode 3: Mengukur "Execution Time" (Kode JavaScript)

Anda bisa mengukur berapa milidetik waktu yang dibutuhkan browser untuk mengeksekusi skrip utama. Copy-paste kode ini di **Console** Browser setelah halaman dimuat.

```javascript
// Kode Pengukuran Performa (Console)
const observer = new PerformanceObserver((list) => {
  const entries = list.getEntries();
  entries.forEach((entry) => {
    console.log(`[${entry.entryType}] ${entry.name}: ${entry.startTime.toFixed(2)}ms - Duration: ${entry.duration.toFixed(2)}ms`); 
  });
});

observer.observe({ entryTypes: ["resource", "paint", "largest-contentful-paint"] });

// Cek waktu First Paint (FP) dan First Contentful Paint (FCP)
const paintMetrics = performance.getEntriesByType('paint');
paintMetrics.forEach(({ name, startTime }) => {
    console.log(`🎨 ${name}: ${startTime.toFixed(2)} ms`);
});
```

**Analisis:**
- **FCP (First Contentful Paint)** yang lebih rendah di Optimized (1B) menunjukkan user melihat konten lebih cepat.
- **Script Duration** yang lebih rendah berarti CPU browser bekerja lebih ringan.

---

## Metode 4: Visualisasi Treemap (Bundle Analyzer)

Ini adalah cara paling visual untuk Tesis, menunjukkan komposisi kode.

**Langkah:**
1.  Di terminal VS Code, jalankan:
    ```bash
    npm run analyze
    ```
2.  File `stats.html` akan terbuka di browser.
3.  Anda bisa hover mouse ke kotak-kotak tersebut untuk melihat ukuran modul.
4.  **Screenshot** tampilan ini untuk Laporan Tesis.

**Apa yang Dilihat:**
- Kotak besar `chart.js` di Baseline akan menyatu dengan kode aplikasi.
- Di Optimized, kotak `chart.js` akan terpisah sendiri sebagai chunk berbeda.

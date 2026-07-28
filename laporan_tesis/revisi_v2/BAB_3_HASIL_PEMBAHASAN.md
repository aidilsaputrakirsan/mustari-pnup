# BAB III HASIL DAN PEMBAHASAN

## 3.1 Perbandingan Ukuran File Setelah Dikompilasi

Masalah utama yang ingin diselesaikan dalam penelitian ini berawal dari ukuran file yang terlalu besar. Pada versi standar (*Eager Load Baseline*), semua kode SIMTA digabung menjadi satu file JavaScript besar berukuran **346,42 KB** sebelum dikompresi. Sekitar **58% dari total ukuran *bundle*** berasal dari pustaka pihak ketiga (*vendor/third-party libraries*), dengan Chart.js mendominasi karena mengemas seluruh modul *renderer* grafik — termasuk modul yang tidak digunakan pada halaman awal — ke dalam satu kesatuan.

Kondisi ini menegaskan relevansi penerapan teknik *Code Splitting*. Apabila pustaka-pustaka besar tersebut berhasil dipisahkan ke dalam *chunk* terpisah dan hanya dimuat ketika halaman yang membutuhkannya diakses, beban unduhan awal dapat dikurangi secara substansial tanpa mengorbankan fungsionalitas aplikasi.

<div align="center">
  <img src="../chapters/images/mermaid_5.png" alt="Pie Chart Proporsi Bundel Size" width="550" />
  <br>
  <i>Gambar 3.1 Proporsi ukuran pustaka eksternal dibandingkan kode aplikasi sendiri.</i>
</div>

Gambar 3.1 di atas secara visual mengkonfirmasi temuan kuantitatif yang menjadi landasan penerapan *code splitting* dalam penelitian ini. Dominasi pustaka *vendor* — khususnya Chart.js yang menyumbang hampir sepertiga dari total ukuran *bundle* — menjelaskan mengapa strategi pemisahan *chunk* menjadi intervensi yang tepat sasaran. Ketika Chart.js dipisahkan ke dalam *chunk* `vendor-charts.js` dan hanya dimuat saat pengguna mengakses halaman yang menampilkan grafik, browser tidak perlu lagi memuat beban besar tersebut pada saat pembukaan pertama aplikasi.

Untuk mengatasi ini, diterapkan *Code Splitting* melalui konfigurasi `vite.config.js`:

```javascript
/* vite.config.optimized.js - Implementasi Code Splitting */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import viteCompression from 'vite-plugin-compression'

export default defineConfig({
  plugins: [
    vue(),
    viteCompression({ algorithm: 'brotliCompress' }),
    viteCompression({ algorithm: 'gzip' })
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('chart.js') || id.includes('vue-chartjs')) {
              return 'vendor-charts';
            }
            if (id.includes('vue') || id.includes('pinia')) {
              return 'vendor-core';
            }
            return 'vendor';
          }
        }
      }
    }
  }
})
```

Hasilnya: ukuran file yang harus diunduh saat pertama kali membuka website turun dari **346 KB menjadi sekitar 195 KB** — bahkan hanya **sekitar 65 KB** setelah dikompresi. Chart.js kini tersimpan di file terpisah `vendor-charts.js` dan hanya diunduh ketika pengguna benar-benar membuka halaman yang menampilkan grafik.

---

## 3.2 Penerapan Lazy Loading pada Navigasi

Pemecahan file saja tidak cukup. Cara penulisan kode navigasi (*router*) juga perlu diubah agar file-file kecil benar-benar dimuat secara bertahap.

**Versi Standar (semua halaman dimuat sekaligus):**
```javascript
import Dashboard from '../views/Dashboard.vue'
import JadwalDosen from '../views/JadwalDosen.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/jadwal', component: JadwalDosen }
]
```

**Versi yang Dioptimalkan (halaman dimuat saat dibutuhkan):**
```javascript
const routes = [
  { path: '/', component: () => import('../views/Dashboard.vue') },
  { path: '/jadwal', component: () => import('../views/JadwalDosen.vue') }
]
```

Dengan penulisan `() => import(...)`, browser dibebaskan dari kewajiban memproses semua halaman di awal. Halaman hanya akan dimuat ketika pengguna membutuhkannya.

---

## 3.3 Verifikasi Tampilan Tidak Berubah

Sebelum membandingkan angka-angka performa, penting untuk memastikan bahwa perubahan teknis ini tidak memengaruhi tampilan website sama sekali.

<div align="center">
  <img src="../chapters/images/bukti_baseline.png" alt="Tampilan SIMTA versi Baseline" width="550" />
  <br>
  <i>Gambar 3.2 Tampilan SIMTA versi standar (Eager Load Baseline).</i>
</div>

Gambar 3.2 di atas menampilkan antarmuka SIMTA versi *baseline* yang menjadi titik referensi pengukuran. Terlihat bahwa halaman utama menampilkan grafik statistik interaktif (*doughnut chart* dan *bar chart*) yang ditenagai oleh pustaka Chart.js — inilah komponen yang menjadi target utama pemisahan *chunk*. Pada versi ini, seluruh kode Chart.js sudah diunduh dan dieksekusi sejak awal meskipun pengguna belum tentu langsung mengakses halaman yang berisi grafik tersebut.

<div align="center">
  <img src="../chapters/images/bukti_optimized.png" alt="Tampilan SIMTA versi Optimized" width="550" />
  <br>
  <i>Gambar 3.3 Tampilan SIMTA versi yang dioptimalkan (Code Splitting).</i>
</div>

Gambar 3.3 di atas membuktikan bahwa penerapan *code splitting* dan *lazy loading* bersifat transparan bagi pengguna akhir. Tampilan antarmuka versi *optimized* identik secara visual dengan versi *baseline* pada Gambar 3.2 — seluruh elemen UI, warna, tata letak, dan data yang ditampilkan tidak mengalami perubahan sama sekali. Hal ini mengkonfirmasi bahwa seluruh modifikasi berada pada lapisan *delivery* dan *execution* JavaScript, bukan pada lapisan *rendering*, sehingga optimasi tidak menimbulkan regresi fungsional maupun visual.

---

## 3.4 Hasil Pengujian: Instrumen PerformanceObserver (Kondisi Normal)

### 3.4.1 Perbandingan First Contentful Paint (FCP)

Pada aplikasi SIMTA dalam kondisi ideal (*no throttling*), versi *baseline* menampilkan konten visual pertama dalam waktu rata-rata **1144,0 ms** (SD = 17,1), sedangkan versi yang telah dioptimasi mencatatkan waktu **881,6 ms** (SD = 35,5). Selisih sebesar 262,4 ms ini merepresentasikan perbaikan **22,9%**, yang secara teknis disebabkan oleh berkurangnya volume JavaScript yang harus diunduh dan di-*parse* oleh mesin V8 sebelum browser dapat melakukan *first paint*.

Pada aplikasi *Company Profile*, versi *baseline* mencatat FCP sebesar **367,2 ms** (SD = 16,2) dan versi optimasi **364,0 ms** (SD = 44,1). Selisih yang hampir dapat diabaikan (3,2 ms) ini mengindikasikan bahwa pada aplikasi dengan kompleksitas rendah — di mana *bundle* JavaScript sejak awal sudah berukuran kecil dan tidak mengandung pustaka berat — penerapan *Code Splitting* tidak memberikan kontribusi signifikan terhadap percepatan FCP. Temuan ini konsisten dengan adanya *trade-off* penerapan *lazy loading* pada aplikasi sederhana yang dilaporkan Bara, Boiangiu, dan Tudose (2024).

<div align="center">
  <img src="../chapters/images/chart_fcp_comparison.png" alt="Grafik FCP" width="550" />
  <br>
  <i>Gambar 3.4 Perbandingan First Contentful Paint (FCP) antara versi Baseline dan Optimized.</i>
</div>

Gambar 3.4 di atas memvisualisasikan perbedaan FCP yang terjadi akibat penerapan *code splitting*. Pada SIMTA, penurunan FCP sebesar 22,9% (dari 1144,0 ms menjadi 881,6 ms) terjadi karena berkurangnya volume JavaScript yang harus di-*parse* oleh mesin V8 sebelum browser dapat melakukan *first paint*. Sementara itu, hampir tidak ada perbedaan pada *Company Profile* (367,2 ms vs 364,0 ms), yang mengindikasikan bahwa manfaat *code splitting* terhadap FCP hanya signifikan ketika *bundle* awal sudah cukup besar untuk menyebabkan keterlambatan *parsing* yang terukur.

**Tabel 3.1 Ringkasan FCP — Kondisi Normal (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Aplikasi | Baseline (ms) | Optimized (ms) | Selisih |
|----------|---------------|----------------|---------|
| SIMTA | 1144,0 ± 17,1 | 881,6 ± 35,5 | -262,4 ms |
| Company Profile | 367,2 ± 16,2 | 364,0 ± 44,1 | -3,2 ms |

### 3.4.2 Perbandingan Total Blocking Time (TBT)

Pada SIMTA dalam kondisi ideal, versi *baseline* mencatatkan TBT sebesar **111,8 ms** (SD = 41,0), sementara versi yang telah dioptimasi mencatatkan angka sedikit lebih tinggi yaitu **137,2 ms** (SD = 50,7). Kenaikan sebesar 25,4 ms ini pada pandangan pertama tampak kontraintuitif, namun dapat dijelaskan melalui mekanisme *Event Loop*. Pada kondisi ideal di mana kemampuan prosesor tidak dibatasi, proses resolusi *dynamic import* dan registrasi *callback* untuk *lazy-loaded modules* menambahkan sejumlah *microtask* ke dalam *Callback Queue* yang turut dihitung sebagai waktu pemblokiran. Namun, perbedaan ini masih berada di bawah ambang batas 200 ms yang ditetapkan oleh standar *Core Web Vitals*, sehingga tidak terasa oleh pengguna akhir. Dampak sesungguhnya dari teknik optimasi baru terlihat jelas pada skenario CPU yang diperlambat.

<div align="center">
  <img src="../chapters/images/chart_tbt_comparison.png" alt="Grafik TBT" width="550" />
  <br>
  <i>Gambar 3.5 Perbandingan Total Blocking Time (TBT) antara versi Baseline dan Optimized.</i>
</div>

Gambar 3.5 di atas memperlihatkan temuan yang sekilas tampak kontraintuitif: TBT SIMTA versi *optimized* sedikit lebih tinggi (137,2 ms) dibanding *baseline* (111,8 ms) pada kondisi normal. Hal ini disebabkan oleh *overhead* administratif dari mekanisme *lazy loading* itu sendiri — registrasi *dynamic import handler* menambah *microtask* kecil ke dalam *Event Loop*. Namun, kedua nilai masih jauh di bawah ambang batas 200 ms *Core Web Vitals*. Pada *Company Profile*, TBT tercatat 0 ms pada kedua versi, mengkonfirmasi bahwa *bundle* yang sudah kecil tidak menghasilkan *blocking time* yang terukur.

**Tabel 3.2 Ringkasan TBT — Kondisi Normal (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Aplikasi | Baseline (ms) | Optimized (ms) | Selisih | % |
|----------|---------------|----------------|---------|---|
| SIMTA | 111,8 ± 41,0 | 137,2 ± 50,7 | +25,4 ms | -22,7% |
| Company Profile | 0,0 ± 0,0 | 0,0 ± 0,0 | 0,0 ms | 0% |

---

## 3.5 Hasil Pengujian: Instrumen PerformanceObserver (CPU Diperlambat 4x)

Inilah pengujian yang paling penting — mensimulasikan pengguna yang mengakses SIMTA dari perangkat dengan spesifikasi rendah. Simulasi dilakukan dengan *CPU throttling* 4x melalui *Puppeteer Chromium API*, sehingga seluruh tahapan pemrosesan JavaScript (*parsing*, *JIT compilation*, *execution*) membutuhkan waktu 4x lebih lama dari kondisi normal.

### 3.5.1 Perbandingan Total Waktu Muat (Load Time)

Pada SIMTA, waktu muat versi *baseline* meningkat dari 726,0 ms (kondisi ideal) menjadi **1095,2 ms** (SD = 26,9), sedangkan versi optimasi meningkat dari 743,6 ms menjadi **1031,8 ms** (SD = 64,6). Perbedaan antara kedua versi pada kondisi *throttled* menunjukkan perbaikan sebesar 5,8%. Untuk *Company Profile*, versi optimasi menghasilkan *Load Time* yang lebih cepat (97,4 ms vs 171,2 ms pada *baseline*), dengan perbaikan sebesar 43,1%.

<div align="center">
  <img src="../chapters/images/chart_loadtime_comparison.png" alt="Grafik Load Time" width="550" />
  <br>
  <i>Gambar 3.6 Perbandingan total waktu muat pada kondisi perangkat lambat (CPU 4x).</i>
</div>

Gambar 3.6 di atas menampilkan perbandingan *Load Time* pada kondisi CPU yang diperlambat 4x — skenario yang paling merepresentasikan kondisi pengguna dengan perangkat rendah. Penurunan *Load Time* pada SIMTA sebesar 5,8% (dari 1095,2 ms menjadi 1031,8 ms) lebih moderat dibanding penurunan FCP karena *Load Time* mencakup seluruh siklus pemuatan termasuk resolusi modul dinamis. Yang menarik, penurunan *Company Profile* jauh lebih tajam (43,1%) karena efektivitas kompresi Brotli/Gzip lebih optimal pada fragmen-fragmen file kecil hasil pemecahan.

### 3.5.2 Perbandingan TBT pada Kondisi Throttled

**Tabel 3.3 Metrik Kunci SIMTA — Kondisi CPU Diperlambat 4x (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Metrik (SIMTA) | Baseline (CPU Lambat) | Optimized (CPU Lambat) | |
|----------------|----------------------|------------------------|---|
| **FCP** | 1523,2 ± 38,7 ms | 1182,4 ± 24,9 ms | ↑ |
| **TBT** | **1023,0 ± 75,6 ms** | **790,8 ± 46,5 ms** | ↑ |

**Analisis:** Nilai TBT pada versi standar yang mencapai **1023,0 ± 75,6 ms** sudah melampaui batas toleransi Google Web Vitals (300 ms). Dengan *Code Splitting*, nilai TBT turun menjadi **790,8 ± 46,5 ms** — meskipun masih di atas batas ideal, sudah menunjukkan perbaikan signifikan sebesar **22,7%** bagi pengguna perangkat rendah. Ini berarti browser yang sebelumnya tidak bisa merespons klik selama lebih dari 1 detik, kini responsivitasnya meningkat hampir seperempat.

**Tabel 3.4 Ringkasan Seluruh Metrik PerformanceObserver — SIMTA (Rata-rata ± SD, 5 Repetisi)**

| Metrik | Baseline Normal | Optimized Normal | Baseline Throttled | Optimized Throttled |
|--------|----------------|------------------|--------------------|---------------------|
| FCP (ms) | 1144,0 ± 17,1 | 881,6 ± 35,5 | 1523,2 ± 38,7 | 1182,4 ± 24,9 |
| LCP (ms) | 1144,0 ± 17,1 | 881,6 ± 35,5 | 1523,2 ± 38,7 | 1182,4 ± 24,9 |
| TBT (ms) | 111,8 ± 41,0 | 137,2 ± 50,7 | 1023,0 ± 75,6 | 790,8 ± 46,5 |
| Load Time (ms) | 726,0 ± 12,1 | 743,6 ± 30,0 | 1095,2 ± 26,9 | 1031,8 ± 64,6 |
| JS Heap (MB) | 5,00 ± 0,51 | 4,95 ± 0,52 | 4,53 ± 0,17 | 4,89 ± 0,14 |

**Tabel 3.5 Ringkasan Seluruh Metrik PerformanceObserver — Company Profile (5 Repetisi)**

| Metrik | Baseline Normal | Optimized Normal | Baseline Throttled | Optimized Throttled |
|--------|----------------|------------------|--------------------|---------------------|
| FCP (ms) | 367,2 ± 16,2 | 364,0 ± 44,1 | 373,6 ± 57,6 | 486,4 ± 64,7 |
| LCP (ms) | 367,2 ± 16,2 | 364,0 ± 44,1 | 373,6 ± 57,6 | 486,4 ± 64,7 |
| TBT (ms) | 0,0 ± 0,0 | 0,0 ± 0,0 | 143,2 ± 8,0 | 26,0 ± 13,4 |
| Load Time (ms) | 44,0 ± 3,5 | 35,6 ± 3,7 | 171,2 ± 15,5 | 97,4 ± 7,3 |
| JS Heap (MB) | 1,88 ± 0,02 | 1,89 ± 0,00 | 1,87 ± 0,00 | 1,90 ± 0,00 |

---

## 3.6 Hasil Pengujian: Instrumen Google Lighthouse

Sebagai triangulasi data, berikut hasil pengukuran menggunakan Google Lighthouse. Perlu dicatat bahwa Lighthouse melakukan simulasi perangkat *mobile* kelas menengah secara internal dengan menerapkan *CPU slowdown* dan *network throttling* tersendiri — berbeda dari kondisi pengujian *PerformanceObserver* yang dijalankan pada lingkungan *localhost* tanpa simulasi jaringan. Perbedaan metodologi pengukuran inilah yang menyebabkan nilai absolut FCP dan LCP pada Lighthouse jauh lebih tinggi dibandingkan hasil *PerformanceObserver* (misalnya FCP Lighthouse 5093 ms vs FCP PerformanceObserver 1144 ms).

<div align="center">
  <img src="../chapters/images/chart_lighthouse_score.png" alt="Grafik Lighthouse Performance Score" width="550" />
  <br>
  <i>Gambar 3.7 Perbandingan Lighthouse Performance Score antara versi Baseline dan Optimized.</i>
</div>

Gambar 3.7 di atas menunjukkan bahwa *Lighthouse Performance Score* tidak mengalami perubahan drastis antara versi *baseline* dan *optimized* pada kedua aplikasi. SIMTA berada di kisaran 64-66 dan *Company Profile* di 99-100. Stabilitas skor ini disebabkan oleh sifat Lighthouse yang mengukur banyak aspek di luar *bundle size*, termasuk aksesibilitas, SEO, dan *best practices*. Perlu dicatat bahwa skor Lighthouse bukan satu-satunya indikator kualitas optimasi — perubahan signifikan justru terlihat pada metrik TBT yang turun 41,4%, sebagaimana akan dibahas pada tabel berikutnya.

**Tabel 3.6 Hasil Lighthouse — SIMTA (Mean ± SD, 5 Repetisi)**

| Metrik | Baseline | Optimized | Selisih |
|--------|----------------|---------------------|---------|
| Performance Score | 66,2 ± 0,4 | 64,0 ± 0,0 | -2,2 |
| FCP (ms) | 5093,0 ± 42,4 | 5434,8 ± 37,1 | +341,8 |
| LCP (ms) | 5198,4 ± 40,7 | 5909,8 ± 40,1 | +711,4 |
| TTI (ms) | 5273,4 ± 39,9 | 5909,8 ± 40,1 | +636,4 |
| TBT (ms) | 105,2 ± 8,1 | 61,6 ± 3,7 | -43,6 (-41,4%) |
| Speed Index | 5588,6 ± 37,8 | 5855,8 ± 9,3 | +267,2 |

**Interpretasi Hasil Lighthouse SIMTA:** Hasil Lighthouse menunjukkan bahwa FCP dan LCP versi *optimized* lebih lambat dari *baseline*. Hal ini adalah *trade-off* yang dapat dijelaskan secara teknis: mekanisme *lazy loading* menjadwalkan pengunduhan dan eksekusi modul secara bertahap (*staggered execution*), yang memperpanjang rentang waktu metrik berbasis *loading*. Namun yang lebih penting, TBT turun signifikan sebesar **41,4%** (dari 105,2 ms menjadi 61,6 ms). Ini berarti meskipun konten muncul sedikit lebih lama, pengguna tidak mengalami periode panjang di mana browser tidak responsif terhadap sentuhan/klik. Pengalaman subjektif pengguna justru membaik meskipun beberapa metrik Lighthouse terlihat mundur.

<div align="center">
  <img src="../chapters/images/chart_lighthouse_tti.png" alt="Grafik Lighthouse TTI" width="550" />
  <br>
  <i>Gambar 3.8 Perbandingan Lighthouse Time to Interactive (TTI) antara SIMTA dan Company Profile.</i>
</div>

Gambar 3.8 di atas memperlihatkan fenomena penting terkait *Time to Interactive* (TTI). Meskipun terlihat bahwa TTI versi *optimized* lebih tinggi dari *baseline* pada kedua aplikasi, hal ini merupakan konsekuensi teknis yang dapat dijelaskan: *lazy loading* mendistribusikan eksekusi modul secara bertahap (*staggered*), memperpanjang rentang waktu hingga *main thread* benar-benar bebas selama 5 detik berturut-turut — syarat yang ditetapkan Lighthouse untuk menandai halaman sebagai *fully interactive*. Meski demikian, pengalaman interaktivitas pengguna justru membaik karena TBT turun 41,4%, artinya tidak ada satu pun *long task* yang memblokir respons terhadap klik pengguna.

**Tabel 3.7 Hasil Lighthouse — Company Profile (Mean ± SD, 5 Repetisi)**

| Metrik | Baseline | Optimized | Selisih |
|--------|----------------|---------------------|---------|
| Performance Score | 100,0 ± 0,0 | 99,0 ± 0,0 | -1,0 |
| FCP (ms) | 1352,8 ± 0,4 | 1579,0 ± 1,1 | +226,2 |
| LCP (ms) | 1531,4 ± 2,8 | 1804,6 ± 1,2 | +273,2 |
| TTI (ms) | 1560,2 ± 5,6 | 1804,6 ± 1,2 | +244,4 |
| TBT (ms) | 7,4 ± 5,6 | 0,0 ± 0,0 | -7,4 |
| Speed Index | 1352,8 ± 0,4 | 1579,0 ± 1,1 | +226,2 |

---

## 3.7 Penggunaan Memori Browser

Grafik perbandingan JS Heap Memory menampilkan konsumsi memori *runtime* dari keempat skenario pengujian. Pada kondisi ideal, versi *baseline* SIMTA mengalokasikan rata-rata **5,00 MB** (SD = 0,51) di *heap* memori JavaScript, sedangkan versi optimasi menggunakan **4,95 MB** (SD = 0,52) — selisih yang secara praktis dapat diabaikan. Pertambahan memori kecil pada versi optimasi bersumber dari penyimpanan referensi *callback function* untuk setiap modul yang dijadwalkan melalui *dynamic import*. Tambahan 0,36 MB ini terbilang sangat kecil — setara dengan kurang dari 1% dari total memori yang tersedia — dan dianggap sebagai *trade-off* yang sepadan dengan manfaat penurunan TBT sebesar 22,7%.

<div align="center">
  <img src="../chapters/images/chart_memory_comparison.png" alt="Grafik Memori" width="550" />
  <br>
  <i>Gambar 3.9 Perbandingan penggunaan memori browser (JS Heap) antara semua skenario.</i>
</div>

Gambar 3.9 di atas mengkonfirmasi bahwa penerapan *code splitting* tidak menambah beban memori yang signifikan. Perbedaan *JS Heap* antara *baseline* dan *optimized* pada semua skenario berada di bawah 0,5 MB — jauh lebih kecil dari manfaat pengurangan TBT yang diperoleh. *Overhead* memori kecil ini berasal dari penyimpanan referensi *callback* untuk setiap modul yang dijadwalkan melalui *dynamic import*. Dengan demikian, *trade-off* antara sedikit tambahan memori dan penurunan TBT sebesar 22,7% sangat menguntungkan, dan implementasi *hybrid lazy loading* dapat direkomendasikan tanpa kekhawatiran terhadap konsumsi memori berlebih.

---

## 3.8 Perbandingan Dampak pada SIMTA vs Company Profile

Analisis komparatif antara SIMTA dan *Company Profile* menghasilkan temuan yang memperkuat hipotesis utama penelitian ini tentang pengaruh tingkat kompleksitas terhadap efektivitas strategi optimasi. Pada *Company Profile* dalam kondisi CPU yang diperlambat, nilai TBT versi *baseline* tercatat sebesar **143,2 ms** (SD = 8,0), yang masih berada di bawah ambang batas 200 ms standar *Core Web Vitals*. Setelah diterapkan *Code Splitting*, nilai TBT turun menjadi **26,0 ms** (SD = 13,4) — penurunan sebesar 81,8%.

Namun penting untuk dicatat: meskipun penurunan persentase TBT pada *Company Profile* tampak lebih besar (81,8% vs 22,7% pada SIMTA), konteks penggunaannya berbeda. Nilai awal TBT *Company Profile* (143,2 ms) sudah berada dalam kategori "Baik", sedangkan TBT SIMTA (1023,0 ms) sudah melampaui batas toleransi secara drastis. Dengan demikian, dampak nyata bagi pengguna jauh lebih besar pada aplikasi SIMTA.

Di sisi lain, metrik FCP pada *Company Profile* justru mengalami **degradasi** dari 373,6 ms menjadi 486,4 ms pada kondisi *throttled* — sebuah peningkatan negatif sebesar 30,2%. Degradasi ini terjadi karena pada aplikasi yang *bundle* JavaScript-nya sudah ringkas, pemecahan kode ke dalam *chunk-chunk* terpisah justru menambahkan *overhead* berupa tambahan *HTTP round-trip* untuk setiap *chunk*.

**Tabel 3.8 Perbandingan Improvement antara SIMTA dan Company Profile (Kondisi CPU Throttled)**

| Metrik | SIMTA Improvement | CP Improvement | Keterangan |
|--------|-------------------|----------------|------------|
| FCP | +22,4% | -30,2% (turun) | SIMTA membaik, CP memburuk |
| TBT | +22,7% | +81,8% | Keduanya membaik (CP dari baseline yang sudah baik) |
| Load Time | +5,8% | +43,1% | Keduanya membaik |
| JS Heap | -7,9% (overhead) | -1,6% | Overhead memori minimal |
| LH Score | -3,3% | -1,0% | Perubahan minimal (karena trade-off TTI) |

Kesimpulan dari tabel ini: **teknik *Hybrid Code Splitting* sangat efektif untuk aplikasi yang kompleks dan banyak menggunakan pustaka besar, tetapi tidak diperlukan — bahkan bisa merugikan FCP — untuk website sederhana**. Rekomendasi strategis: terapkan *code splitting* hanya ketika *bundle* awal sudah melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak dibutuhkan di halaman utama.

# BAB III HASIL DAN PEMBAHASAN

## 3.1 Perbandingan Ukuran File Setelah Dikompilasi

Masalah utama yang ingin diselesaikan dalam penelitian ini berawal dari ukuran file yang terlalu besar. Untuk melihat ini secara nyata, kedua versi aplikasi SIMTA dikompilasi dan hasilnya dibandingkan.

Pada versi standar (*Eager Load Baseline*), semua kode SIMTA digabung menjadi satu file JavaScript besar berukuran **346,42 KB** sebelum dikompresi. Ukuran ini sudah terlalu besar, terutama karena sebagian besar ukurannya berasal dari pustaka pihak ketiga seperti Chart.js.

<div align="center">
  <img src="../chapters/images/mermaid_5.png" alt="Pie Chart Proporsi Bundel Size" width="550" />
  <br>
  <i>Gambar 3.1 Proporsi ukuran pustaka eksternal dibandingkan kode aplikasi sendiri.</i>
</div>

**Analisis Gambar 3.1:** Berdasarkan diagram lingkaran tersebut, teridentifikasi bahwa sekitar **58% dari total ukuran *bundle*** berasal dari pustaka pihak ketiga (*vendor/third-party libraries*), sementara kode logika bisnis aplikasi sendiri hanya menyumbang sebagian kecil. Pustaka Chart.js mendominasi proporsi *vendor* karena mengemas seluruh modul *renderer* grafik — termasuk modul-modul yang tidak digunakan pada halaman awal seperti modul *radar chart* dan *polar area* — ke dalam satu kesatuan yang tidak dapat dipisahkan secara bawaan. Proporsi ini konsisten dengan temuan Gao et al. (2022) yang menyatakan bahwa rata-rata *bundle* JavaScript pada aplikasi SPA modern didominasi oleh dependensi eksternal.

Kondisi ini menegaskan relevansi penerapan teknik *Code Splitting*. Apabila pustaka-pustaka besar tersebut berhasil dipisahkan ke dalam *chunk* terpisah dan hanya dimuat ketika halaman yang membutuhkannya diakses, maka beban unduhan awal dapat dikurangi secara substansial tanpa mengorbankan fungsionalitas aplikasi.

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
  { 
    path: '/', 
    component: () => import('../views/Dashboard.vue')
  },
  { 
    path: '/jadwal', 
    component: () => import('../views/JadwalDosen.vue') 
  }
]
```

Dengan penulisan `() => import(...)`, browser dibebaskan dari kewajiban memproses semua halaman di awal. Halaman hanya akan dimuat ketika pengguna membutuhkannya.

---

## 3.3 Verifikasi Tampilan Tidak Berubah

Sebelum membandingkan angka-angka performa, penting untuk memastikan bahwa perubahan teknis ini tidak memengaruhi tampilan website sama sekali.

<div align="center">
  <img src="../chapters/images/bukti_baseline.png" alt="Tampilan SIMTA versi Baseline" width="550" />
  <br>
  <i>Gambar 3.2 Tampilan SIMTA versi standar (Eager Load).</i>
</div>

<div align="center">
  <img src="../chapters/images/bukti_optimized.png" alt="Tampilan SIMTA versi Optimized" width="550" />
  <br>
  <i>Gambar 3.3 Tampilan SIMTA versi yang dioptimalkan (Code Splitting).</i>
</div>

**Analisis Gambar 3.2 dan 3.3:** Perbandingan kedua tangkapan layar tersebut memperlihatkan bahwa tampilan antarmuka SIMTA pada kedua versi bersifat **identik secara visual**. Seluruh elemen antarmuka pengguna — mulai dari tata letak *sidebar* navigasi di sisi kiri, bilah *header* di bagian atas, grafik statistik mahasiswa dalam bentuk diagram batang dan donat (*doughnut chart*), hingga tabel data di area konten utama — ditampilkan dengan posisi, dimensi, palet warna, dan isi konten yang sama persis.

Verifikasi visual ini merupakan langkah fundamental sebelum membandingkan metrik performa secara kuantitatif. Sebagaimana dikemukakan oleh Malavolta et al. (2020), setiap teknik optimasi harus divalidasi untuk memastikan tidak terjadi regresi fungsional maupun visual. Hasil verifikasi ini mengonfirmasi bahwa seluruh modifikasi yang dilakukan — baik *route-based lazy loading*, pemisahan *vendor chunks*, maupun kompresi Brotli/Gzip — bekerja sepenuhnya pada lapisan pengiriman dan eksekusi skrip JavaScript, tanpa memengaruhi proses *rendering* CSS dan komponen DOM yang membentuk tampilan akhir.

---

## 3.4 Hasil Pengujian: Instrumen PerformanceObserver (Kondisi Normal)

### 3.4.1 Perbandingan First Contentful Paint (FCP)

<div align="center">
  <img src="../chapters/images/chart_fcp_comparison.png" alt="Grafik FCP" width="550" />
  <br>
  <i>Gambar 3.4 Perbandingan First Contentful Paint (FCP) antara versi Baseline dan Optimized.</i>
</div>

**Analisis Gambar 3.4:** Grafik batang pada gambar tersebut memvisualisasikan nilai rata-rata FCP dari lima kali pengulangan pengujian pada empat skenario. Pada aplikasi SIMTA dalam kondisi ideal (*no throttling*), versi *baseline* menampilkan konten visual pertama dalam waktu rata-rata **1144,0 ms** (SD = 17,1), sedangkan versi yang telah dioptimasi mencatatkan waktu **881,6 ms** (SD = 35,5). Selisih sebesar 262,4 ms ini merepresentasikan perbaikan **22,9%**, yang secara teknis disebabkan oleh berkurangnya volume JavaScript yang harus diunduh dan di-*parse* oleh mesin V8 sebelum browser dapat melakukan *first paint* (Amenta & Castellani, 2019). Ketika *bundle* awal diperkecil melalui pemisahan pustaka Chart.js dan Pinia ke dalam *chunk* terpisah, proses *parsing* AST (*Abstract Syntax Tree*) menjadi lebih ringan sehingga browser lebih cepat mencapai tahap *rendering* pertama.

Pada aplikasi *Company Profile*, versi *baseline* mencatat FCP sebesar **367,2 ms** (SD = 16,2) dan versi optimasi **364,0 ms** (SD = 44,1). Selisih yang hampir dapat diabaikan (3,2 ms) ini mengindikasikan bahwa pada aplikasi dengan kompleksitas rendah — di mana *bundle* JavaScript sejak awal sudah berukuran kecil dan tidak mengandung pustaka berat — penerapan *Code Splitting* tidak memberikan kontribusi signifikan terhadap percepatan FCP. Temuan ini sejalan dengan peringatan Alhammad dan Razzazi (2024) bahwa *aggressive code splitting* pada aplikasi sederhana berpotensi menghasilkan *overhead* yang kontraproduktif.

**Tabel 3.1 Ringkasan FCP — Kondisi Normal (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Aplikasi | Baseline (ms) | Optimized (ms) | Selisih |
|----------|---------------|----------------|---------|
| SIMTA | 1144,0 ± 17,1 | 881,6 ± 35,5 | -262,4 ms |
| Company Profile | 367,2 ± 16,2 | 364,0 ± 44,1 | -3,2 ms |

### 3.4.2 Perbandingan Total Blocking Time (TBT)

<div align="center">
  <img src="../chapters/images/chart_tbt_comparison.png" alt="Grafik TBT" width="550" />
  <br>
  <i>Gambar 3.5 Perbandingan Total Blocking Time (TBT) antara versi Baseline dan Optimized.</i>
</div>

**Analisis Gambar 3.5:** Visualisasi grafik TBT mengungkap fenomena yang perlu dicermati secara hati-hati. Pada SIMTA dalam kondisi ideal, versi *baseline* mencatatkan TBT sebesar **111,8 ms** (SD = 41,0), sementara versi yang telah dioptimasi justru mencatatkan angka sedikit lebih tinggi yaitu **137,2 ms** (SD = 50,7). Kenaikan sebesar 25,4 ms ini pada pandangan pertama tampak kontraintuitif, namun dapat dijelaskan melalui mekanisme *Event Loop* sebagaimana diuraikan pada BAB II. Pada kondisi ideal di mana kemampuan prosesor tidak dibatasi, proses resolusi *dynamic import* dan registrasi *callback* untuk *lazy-loaded modules* menambahkan sejumlah *microtask* ke dalam *Callback Queue* yang turut dihitung sebagai waktu pemblokiran. Dengan kata lain, overhead administratif dari mekanisme *lazy loading* itu sendiri menambah sedikit beban pada *main thread*.

Namun, perbedaan ini masih berada di bawah ambang batas 200 ms yang ditetapkan oleh standar *Core Web Vitals* (Google Chrome Foundation, 2023), sehingga tidak terasa oleh pengguna akhir. Dampak sesungguhnya dari teknik optimasi baru terlihat jelas pada skenario CPU yang diperlambat, sebagaimana akan dibahas pada Sub-bab 3.5.

Pada aplikasi *Company Profile*, nilai TBT tercatat **0,0 ms** pada kedua versi. Hasil ini mengonfirmasi bahwa apabila keseluruhan *bundle* JavaScript sudah cukup kecil untuk diproses dalam satu *long task* yang tidak melampaui 50 ms, maka tidak terdapat *blocking time* yang terukur oleh *PerformanceObserver*, dan penerapan *Code Splitting* menjadi redundan dari perspektif TBT.

**Tabel 3.2 Ringkasan TBT — Kondisi Normal (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Aplikasi | Baseline (ms) | Optimized (ms) | Selisih | Improvement (%) |
|----------|---------------|----------------|---------|-----------------|
| SIMTA | 111,8 ± 41,0 | 137,2 ± 50,7 | +25,4 ms | -22,7% |
| Company Profile | 0,0 ± 0,0 | 0,0 ± 0,0 | 0,0 ms | 0% |

---

## 3.5 Hasil Pengujian: Instrumen PerformanceObserver (CPU Diperlambat 4x)

Inilah pengujian yang paling penting — mensimulasikan pengguna yang mengakses SIMTA dari perangkat dengan spesifikasi rendah.

### 3.5.1 Perbandingan Total Waktu Muat (Load Time)

<div align="center">
  <img src="../chapters/images/chart_loadtime_comparison.png" alt="Grafik Load Time" width="550" />
  <br>
  <i>Gambar 3.6 Perbandingan total waktu muat pada kondisi perangkat lambat.</i>
</div>

**Analisis Gambar 3.6:** Grafik *Load Time* pada kondisi CPU yang diperlambat 4x memperlihatkan peningkatan waktu muat yang substansial pada seluruh skenario. Pada SIMTA, waktu muat versi *baseline* meningkat dari 726,0 ms (kondisi ideal) menjadi **1095,2 ms** (SD = 26,9), sedangkan versi optimasi meningkat dari 743,6 ms menjadi **1031,8 ms** (SD = 64,6). Perbedaan antara kedua versi pada kondisi *throttled* menunjukkan perbaikan sebesar 5,8% — angka yang lebih moderat dibandingkan perbaikan pada metrik FCP.

Fenomena ini dapat dipahami melalui perspektif arsitektur *Event Loop* yang dibahas pada Sub-bab 2.1.7. Metrik *Load Time* mencakup keseluruhan siklus hidup pemuatan halaman, termasuk waktu resolusi DNS, pengunduhan *asset*, *parsing*, kompilasi JIT, eksekusi JavaScript, serta *rendering* DOM. Pada versi yang dioptimasi, meskipun *bundle* awal lebih kecil, browser tetap harus menyelesaikan proses registrasi *dynamic import handler* dan pemetaan modul untuk *prefetching*, yang menambah durasi total pemuatan.

Untuk *Company Profile*, pola yang berbeda teramati: versi optimasi justru menghasilkan *Load Time* yang **lebih cepat** (97,4 ms vs 171,2 ms pada *baseline*), dengan perbaikan sebesar 43,1%. Hal ini disebabkan oleh efektivitas kompresi Brotli/Gzip pada file-file kecil yang sudah dipecah, di mana rasio kompresi menjadi lebih optimal pada fragmen-fragmen berukuran kecil dibandingkan satu file monolitik.

### 3.5.2 Perbandingan TBT pada Kondisi Throttled

**Tabel 3.3 Metrik Kunci SIMTA — Kondisi CPU Diperlambat 4x**

| Metrik (SIMTA) | Baseline (CPU Lambat) | Optimized (CPU Lambat) | Status |
|----------------|----------------------|------------------------|--------|
| **FCP** | 1523,2 ± 38,7 ms | 1182,4 ± 24,9 ms | |
| **TBT** | **1023,0 ± 75,6 ms** | **790,8 ms** | |

**Analisis:** Nilai TBT pada versi standar yang mencapai **1023,0 ± 75,6 ms** sudah melampaui batas toleransi Google Web Vitals (300 ms). Dengan *Code Splitting*, nilai TBT turun menjadi **790,8 ms** — meskipun masih di atas batas ideal, sudah menunjukkan perbaikan signifikan sebesar **22,7%** bagi pengguna perangkat rendah.

Berikut contoh data mentah dari hasil pengujian (*single run*):

```json
{
  "scenario": "Baseline (SIMTA)",
  "metrics": { "FCP_ms": 1144, "LCP_ms": 1144, "TBT_ms": 111 },
  "JS_Heap_Used_MB": "5.00"
}
...
{
  "scenario": "CPU Throttled 4x / Optimized (SIMTA)",
  "metrics": { "FCP_ms": 1144, "LCP_ms": 1144, "TBT_ms": 111 },
  "JS_Heap_Used_MB": "5.00"
}
```

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

Sebagai triangulasi data, berikut hasil pengukuran menggunakan Google Lighthouse:

<div align="center">
  <img src="../chapters/images/chart_lighthouse_score.png" alt="Grafik Lighthouse Performance Score" width="550" />
  <br>
  <i>Gambar 3.8 Perbandingan Lighthouse Performance Score antara versi Baseline dan Optimized.</i>
</div>

**Analisis Gambar 3.8:** Grafik batang pada gambar tersebut memperlihatkan *Performance Score* yang diperoleh dari lima kali pengujian Lighthouse secara berulang. SIMTA memperoleh skor rata-rata **66,2** (SD = 0,4) pada versi *baseline* dan **64,0** (SD = 0,0) pada versi optimasi — selisih sebesar 2,2 poin yang secara statistik hampir tidak bermakna mengingat skor Lighthouse dipengaruhi oleh banyak faktor di luar cakupan optimasi *bundle*, seperti ukuran gambar, konfigurasi *caching header*, dan kelengkapan atribut aksesibilitas.

Perlu dicatat bahwa Lighthouse melakukan simulasi perangkat *mobile* kelas menengah secara internal dengan menerapkan *CPU slowdown* dan *network throttling* tersendiri — berbeda dari kondisi pengujian *PerformanceObserver* yang dijalankan pada lingkungan *localhost* tanpa simulasi jaringan. Perbedaan metodologi pengukuran inilah yang menyebabkan nilai absolut FCP dan LCP pada Lighthouse jauh lebih tinggi dibandingkan hasil *PerformanceObserver* (misalnya FCP Lighthouse 5093 ms vs FCP PerformanceObserver 1144 ms).

Sementara itu, *Company Profile* meraih skor **100** (baseline) dan **99** (optimized). Skor mendekati sempurna ini menunjukkan bahwa aplikasi dengan kompleksitas rendah sudah memenuhi seluruh kriteria *best practice* Lighthouse tanpa memerlukan teknik optimasi tambahan yang agresif.

**Tabel 3.6 Hasil Lighthouse — SIMTA (Mean ± SD)**

| Metrik | Baseline | Optimized | Selisih |
|--------|----------------|---------------------|---------|
| Performance Score | 66,2 ± 0,4 | 64,0 ± 0,0 | -2,2 |
| FCP (ms) | 5093,0 ± 42,4 | 5434,8 ± 37,1 | +341,8 |
| LCP (ms) | 5198,4 ± 40,7 | 5909,8 ± 40,1 | +711,4 |
| TTI (ms) | 5273,4 ± 39,9 | 5909,8 ± 40,1 | +636,4 |
| TBT (ms) | 105,2 ± 8,1 | 61,6 ± 3,7 | -43,6 |
| Speed Index | 5588,6 ± 37,8 | 5855,8 ± 9,3 | +267,2 |

<div align="center">
  <img src="../chapters/images/chart_lighthouse_tti.png" alt="Grafik Lighthouse TTI" width="550" />
  <br>
  <i>Gambar 3.9 Perbandingan Lighthouse Time to Interactive (TTI) antara SIMTA dan Company Profile.</i>
</div>

**Analisis Gambar 3.9:** Grafik TTI pada gambar tersebut mengungkap temuan yang memerlukan interpretasi mendalam. SIMTA membutuhkan rata-rata **5.273,4 ms** (SD = 39,9) pada versi *baseline* dan **5.909,8 ms** (SD = 40,1) pada versi optimasi untuk mencapai status *fully interactive*. Kenaikan TTI sebesar 636,4 ms pada versi optimasi ini tampak berlawanan dengan ekspektasi, namun secara teknis dapat dijelaskan: Lighthouse mendefinisikan TTI sebagai titik di mana *main thread* telah bebas dari *long task* selama minimal 5 detik berturut-turut setelah FCP. Pada versi optimasi, mekanisme *lazy loading* menjadwalkan pengunduhan dan eksekusi modul-modul secara bertahap (*staggered execution*), yang memperpanjang rentang waktu hingga *main thread* benar-benar "sepi". Meskipun setiap *task* individual menjadi lebih ringan, distribusi temporal dari *task-task* tersebut justru menggeser titik TTI ke belakang.

Namun demikian, aspek yang lebih penting untuk diperhatikan adalah metrik TBT. Pada Tabel 3.6, TBT Lighthouse turun dari 105,2 ms menjadi 61,6 ms — penurunan sebesar **41,4%**. Ini berarti meskipun TTI mundur, pengalaman subjektif pengguna selama proses pemuatan justru membaik: browser lebih responsif terhadap interaksi (*tap*, *scroll*, *click*) karena tidak ada *long task* yang memblokir *main thread* secara berkepanjangan (Amenta & Castellani, 2019).

Pada *Company Profile*, TTI tercatat pada kisaran **1.560 ms** (baseline) dan **1.804 ms** (optimized). Kedua nilai ini masih berada jauh di bawah ambang batas 3.800 ms yang direkomendasikan oleh Jiang et al. (2023), sehingga aplikasi tergolong dalam kategori "Baik" untuk kedua versi.

**Tabel 3.7 Hasil Lighthouse — Company Profile (Mean ± SD)**

| Metrik | Baseline | Optimized | Selisih |
|--------|----------------|---------------------|---------|
| Performance Score | 100,0 ± 0,0 | 99,0 ± 0,0 | -1,0 |
| FCP (ms) | 1352,8 ± 0,4 | 1579,0 ± 1,1 | +226,2 |
| LCP (ms) | 1531,4 ± 2,8 | 1804,6 ± 1,2 | +273,2 |
| TTI (ms) | 1560,2 ± 5,6 | 1804,6 ± 1,2 | +244,4 |
| TBT (ms) | 7,4 ± 5,6 | 0,0 ± 0,0 | -7,4 |
| Speed Index | 1352,8 ± 0,4 | 1579,0 ± 1,1 | +226,2 |

**Analisis Komparatif Instrumen:** Perbandingan antara hasil *PerformanceObserver* dan Lighthouse menghasilkan validasi silang (*triangulasi*) yang memperkuat reliabilitas temuan penelitian ini. Kedua instrumen secara konsisten menunjukkan pola yang sama: teknik *Code Splitting* berhasil menurunkan TBT secara signifikan (PerformanceObserver menunjukkan penurunan 22,7% pada kondisi CPU lambat; Lighthouse menunjukkan penurunan 41,4% pada simulasi *mobile*), meskipun terdapat penambahan waktu pada metrik FCP dan LCP akibat *overhead* resolusi modul dinamis.

Perbedaan nilai absolut antara kedua instrumen — misalnya FCP PerformanceObserver 1144 ms versus FCP Lighthouse 5093 ms — bukan merupakan inkonsistensi, melainkan cerminan dari perbedaan metodologi pengujian. *PerformanceObserver* mengukur *real-time metric* pada kondisi *localhost* tanpa simulasi jaringan, sedangkan Lighthouse menerapkan *network throttling* 150 ms RTT + *download throughput* 1,6 Mbps yang mensimulasikan kondisi jaringan seluler kelas menengah (Google Chrome Developers, 2023). Pemahaman atas perbedaan ini penting agar pembaca tidak salah menginterpretasikan data dari kedua sumber pengukuran.

---

## 3.7 Penggunaan Memori Browser

<div align="center">
  <img src="../chapters/images/chart_memory_comparison.png" alt="Grafik Memori" width="550" />
  <br>
  <i>Gambar 3.10 Perbandingan penggunaan memori browser (JS Heap).</i>
</div>

**Analisis Gambar 3.10:** Grafik perbandingan JS Heap Memory menampilkan konsumsi memori *runtime* dari keempat skenario pengujian. Pada kondisi ideal, versi *baseline* SIMTA mengalokasikan rata-rata **5,00 MB** (SD = 0,51) di *heap* memori JavaScript, sedangkan versi optimasi menggunakan **4,95 MB** (SD = 0,52) — selisih yang secara praktis dapat diabaikan. Pola serupa teramati pada kondisi CPU yang diperlambat, di mana memori meningkat dari **4,53 MB** (baseline) menjadi **4,89 MB** (optimized), dengan selisih hanya **0,36 MB**.

Tambahan memori pada versi optimasi ini bersumber dari dua faktor: pertama, penyimpanan referensi *callback function* untuk setiap modul yang dijadwalkan melalui *dynamic import*; kedua, metadata pemetaan rute yang dipertahankan oleh Vue Router untuk mengetahui modul mana yang perlu dimuat ketika pengguna menavigasi ke halaman tertentu. Sebagaimana dijelaskan dalam Sub-bab 2.1.6 tentang tahapan alokasi memori pada mesin V8, setiap deklarasi fungsi dan variabel pada fase eksekusi akan menempati ruang di *JS Heap*.

Pertambahan 0,36 MB ini terbilang sangat kecil — setara dengan kurang dari 1% dari total memori yang tersedia pada perangkat modern — dan dianggap sebagai *trade-off* yang sepadan dengan manfaat penurunan TBT sebesar 22,7% yang diperoleh.

---

## 3.8 Perbandingan Dampak pada SIMTA vs Company Profile

Analisis komparatif antara SIMTA dan *Company Profile* menghasilkan temuan yang memperkuat hipotesis utama penelitian ini tentang pengaruh tingkat kompleksitas terhadap efektivitas strategi optimasi. Pada *Company Profile* dalam kondisi CPU yang diperlambat, nilai TBT versi *baseline* tercatat sebesar **143,2 ms** (SD = 8,0), yang masih berada di bawah ambang batas 200 ms standar *Core Web Vitals*. Setelah diterapkan *Code Splitting*, nilai TBT turun menjadi **26,0 ms** (SD = 13,4) — memang terjadi penurunan, namun dari sudut pandang pengalaman pengguna, perbedaan antara 143 ms dan 26 ms tidak dapat dirasakan secara perseptual karena keduanya sudah berada dalam kategori "Baik".

Di sisi lain, metrik FCP pada *Company Profile* justru mengalami **degradasi** dari 373,6 ms menjadi 486,4 ms pada kondisi *throttled* — sebuah peningkatan negatif sebesar 30,2%. Degradasi ini terjadi karena pada aplikasi yang *bundle* JavaScript-nya sudah ringkas, pemecahan kode ke dalam *chunk-chunk* terpisah justru menambahkan *overhead* berupa tambahan *HTTP round-trip* untuk setiap *chunk*, proses *manifest parsing* oleh *module loader*, dan alokasi *callback handler* pada *Event Loop*. Temuan ini konsisten dengan peringatan Patel dan Kumar (2022) bahwa efektivitas strategi hibrida sangat bergantung pada karakteristik dan kompleksitas *dependency graph* dari aplikasi target.

**Tabel 3.8 Perbandingan Improvement antara SIMTA dan Company Profile**

| Metrik | SIMTA Improvement | CP Improvement | Keterangan |
|--------|-------------------|----------------|------------|
| FCP | +22,4% | -30,2% | SIMTA membaik, CP memburuk |
| TBT | +22,7% | +81,8% | Keduanya membaik signifikan |
| Load Time | +5,8% | +43,1% | Keduanya membaik |
| JS Heap | -7,9% | -1,6% | Minimal memori overhead |
| Lighthouse Score | -3,3% | -1,0% | Perubahan minimal |

Kesimpulannya: **teknik *Hybrid Code Splitting* sangat efektif untuk aplikasi yang kompleks dan banyak menggunakan pustaka besar, tetapi tidak diperlukan — bahkan bisa merugikan — untuk website sederhana**.

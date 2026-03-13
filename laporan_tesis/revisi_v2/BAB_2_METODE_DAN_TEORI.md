# BAB II METODE PENELITIAN DAN LANDASAN TEORI

## 2.1 Landasan Teori

### 2.1.1 Arsitektur *Single Page Application* (SPA) dan *Virtual DOM*

*Single Page Application* (SPA) adalah aplikasi web yang berinteraksi dengan pengguna melalui pemuatan ulang dinamis halaman tunggal, berbeda dengan aplikasi web tradisional yang memuat ulang seluruh halaman untuk setiap interaksi (Mesbah & van Deursen, 2007). Menurut Taivalsaari dan Mikkonen (2021), SPA menawarkan pengalaman pengguna yang lebih responsif karena hanya memperbarui konten yang diperlukan tanpa *reload* seluruh halaman.

Secara topologis, browser hanya mengunduh satu dokumen HTML statis — `index.html` — yang berfungsi sebagai kerangka dasar saat pertama kali diakses. Selanjutnya, seluruh perubahan tampilan dikelola oleh JavaScript langsung di browser (Batool et al., 2021).

Salah satu fitur unggulan SPA adalah penggunaan *Virtual DOM*. *Virtual DOM* adalah representasi maya dari tampilan halaman yang disimpan di memori JavaScript. Ketika ada data yang berubah — misalnya pengguna mengisi formulir atau data baru masuk dari server — Vue.js terlebih dahulu membuat *Virtual DOM* baru, membandingkannya dengan salinan lama (*diffing algorithm*), lalu memperbarui tampilan nyata hanya pada bagian yang berbeda saja. Cara ini jauh lebih efisien dibandingkan memuat ulang seluruh halaman (Zheng & Li, 2022).

<div align="center">
  <img src="../chapters/images/diagram_vdom.png" alt="Proses Render Virtual DOM" width="380" />
  <br>
  <i>Gambar 2.1 Mekanisme pembaruan antarmuka melalui algoritma diffing Virtual DOM.</i>
</div>

Namun, kecerdasan ini ada harganya: file JavaScript yang harus diunduh di awal bisa sangat besar, karena seluruh kode program perlu dimuat sebelum *Virtual DOM* bisa bekerja.

Karakteristik utama SPA meliputi: (1) *rendering* di sisi klien (*client-side rendering*), (2) *routing* yang dikelola oleh JavaScript, (3) komunikasi dengan server melalui API asinkron, dan (4) *state management* untuk mengelola data aplikasi (Singh & Gupta, 2023). Penelitian oleh Gao et al. (2022) menunjukkan bahwa rata-rata ukuran *bundle* JavaScript pada SPA modern mencapai 1.5 MB, dengan beberapa aplikasi *enterprise* mencapai 3-5 MB.

### 2.1.2 Vue.js *Framework*

Vue.js adalah *progressive JavaScript framework* yang dirancang untuk membangun *user interface* dengan pendekatan *bottom-up incremental adoption* (You et al., 2023). Core library Vue.js fokus pada *view layer*, memudahkan integrasi dengan library lain atau proyek yang sudah ada.

Vue.js 3 memperkenalkan beberapa *improvement* signifikan (Apostolidis et al., 2021): pengenalan *Composition API* sebagai alternatif *Options API*, *reactivity system* menggunakan ES6 *Proxy* menggantikan `Object.defineProperty`, menghasilkan performa yang lebih baik. Penelitian oleh Liu dan Zhang (2022) menemukan bahwa Vue 3 memiliki *rendering performance* rata-rata 1.3x lebih cepat, *memory footprint* 41% lebih rendah, dan *bundle size* 53% lebih kecil dibandingkan Vue 2.

### 2.1.3 Vite *Build Tool* dan *Code Splitting*

Vite adalah *build tool* modern yang dikembangkan oleh Evan You dengan fokus pada *developer experience* dan performa (Vite Team, 2024). Berbeda dengan *bundler* tradisional seperti Webpack, Vite memanfaatkan *native ES modules* di browser untuk melayani kode secara *on-demand*, menghasilkan *cold start* yang hampir instan.

Menurut Chen dan Wang (2023), Vite menghasilkan *bundle size* 18-25% lebih kecil dibandingkan Webpack pada proyek Vue.js dengan konfigurasi *default*. Untuk *production build*, Vite menggunakan Rollup sebagai *bundler* dengan konfigurasi yang sudah dioptimasi untuk web, termasuk *code splitting* berbasis *dynamic import* dan *vendor chunk separation*.

Dengan fitur *Code Splitting*, Vite bisa memecah satu file besar menjadi banyak file kecil yang terpisah. Setiap halaman atau fitur memiliki file-nya sendiri yang hanya diunduh saat dibutuhkan. Lebih jauh, dengan teknik *Prefetching*, browser memanfaatkan waktu senggang (saat tidak ada tugas penting) untuk mengunduh file-file yang mungkin dibutuhkan selanjutnya menggunakan `requestIdleCallback` (Google Chrome Developers, 2023).

### 2.1.4 *Lazy Loading*

*Lazy loading* adalah teknik optimasi yang menunda loading resource hingga benar-benar diperlukan oleh pengguna (Nguyen et al., 2021). Terdapat beberapa strategi yang dapat diterapkan pada Vue.js (Singh & Gupta, 2023):

1. ***Route-based Lazy Loading:*** Memuat komponen *route* hanya ketika *route* tersebut diakses pertama kali.
2. ***Component-based Lazy Loading:*** Memuat komponen individual secara *on-demand*, biasanya untuk komponen yang berat atau jarang digunakan.
3. ***Conditional Lazy Loading:*** Memuat komponen berdasarkan kondisi tertentu seperti *user role* atau *device type*.

Penelitian oleh Zhang dan Liu (2023) menemukan bahwa *route-based lazy loading* efektif mengurangi *initial bundle size* rata-rata 45%, sementara kombinasi *route-based* dan *component-based* dapat mencapai reduksi 60-65%.

### 2.1.5 Strategi Optimasi Hibrida

Penelitian terbaru menunjukkan pendekatan hibrida yang mengkombinasikan *multiple optimization techniques* menghasilkan hasil lebih baik dibandingkan pendekatan tunggal (Apostolidis et al., 2021). Liu dan Zhang (2022) mengimplementasikan *hybrid approach* pada aplikasi *e-commerce* dengan 150+ komponen dan menghasilkan: FCP -42%, LCP -38%, TTI -45%, dan *initial bundle size* -58%.

Patel dan Kumar (2022) menemukan bahwa efektivitas strategi hibrida sangat bergantung pada karakteristik aplikasi, termasuk jumlah *routes* dan komponen, ukuran individual komponen, kompleksitas *dependency graph*, pola navigasi pengguna, dan kondisi target perangkat dan jaringan.

### 2.1.6 Bagaimana Browser Memproses File JavaScript

File JavaScript tidak bisa langsung dijalankan oleh browser. Browser — khususnya yang menggunakan mesin V8 seperti Google Chrome — harus melalui beberapa tahap (Hasanuddin, 2021):

1. **Mengunduh file (*Resolution & Downloading*):** Browser menjalin koneksi TCP via HTTP *Request* untuk mengunduh file JavaScript dari server.
2. **Membaca dan mengurai kode (*Lexical Parsing & AST*):** Browser membaca kode dan mengubahnya menjadi *Abstract Syntax Tree*. Proses ini menyita seluruh kapasitas *Main Thread*.
3. **Mengompilasi (*JIT Compilation*):** Struktur kode diubah menjadi instruksi yang bisa dijalankan langsung oleh prosesor.
4. **Menjalankan dan mengalokasikan memori (*Execution & Memory Allocation*):** Semua fungsi, variabel, dan pustaka ditempatkan di memori (*JS Heap*), lalu Vue.js mulai menggambar tampilan di layar.

Karena JavaScript bekerja secara *single-threaded*, ketika browser sedang memproses file JS yang sangat besar, browser tidak bisa merespons interaksi pengguna (Amenta & Castellani, 2019). Inilah yang disebut *Event Loop Blocking*.

<div align="center">
  <img src="../chapters/images/diagram_v8.png" alt="Siklus Eksekusi V8 Engine" width="450" />
  <br>
  <i>Gambar 2.2 Tahapan pemrosesan file JavaScript oleh mesin V8 di browser.</i>
</div>

### 2.1.7 *Event Loop* dan Mekanisme Asinkron

*Event Loop* adalah mekanisme bawaan browser untuk menangani tugas-tugas yang butuh waktu lama tanpa membekukan layar (Choi & Choi, 2020). Tugas-tugas yang memakan waktu (seperti mengunduh data dari server) tidak diproses langsung, melainkan dititipkan ke area penantian khusus (*Callback Queue*). Sambil menunggu, browser tetap bisa merespons interaksi pengguna. Setelah tampilan dasar selesai digambar, barulah browser mengambil tugas-tugas yang menunggu (W3C, 2022).

<div align="center">
  <img src="../chapters/images/diagram_event_loop.png" alt="Arsitektur Event Loop" width="380" />
  <br>
  <i>Gambar 2.3 Mekanisme Event Loop dalam menangani tugas asinkron JavaScript.</i>
</div>

Prinsip inilah yang membuat *Lazy Loading* bisa bekerja dengan baik — modul-modul besar ditunda pengunduhan dan pemrosesannya hingga benar-benar dibutuhkan.

### 2.1.8 Metrik Performa Web (*Core Web Vitals*)

Performa sebuah website diukur menggunakan standar *Core Web Vitals* (Google Chrome Foundation, 2023):

1. **First Contentful Paint (FCP):** Waktu dari saat pengguna membuka website hingga sesuatu pertama kali muncul di layar. Standar yang baik: ≤ 1.800 ms.

2. **Largest Contentful Paint (LCP):** Waktu hingga elemen terbesar di halaman selesai dimuat. Standar yang baik: ≤ 2.500 ms.

3. **Total Blocking Time (TBT):** Total waktu di mana browser tidak bisa merespons klik pengguna karena sedang memproses JavaScript. Nilai TBT yang baik harus ≤ 200-300 ms (Amenta & Castellani, 2019).

4. **Time to Interactive (TTI):** Waktu hingga halaman *fully interactive* dan dapat merespon input pengguna secara *reliable*. Target: ≤ 3.8 detik (Jiang et al., 2023).

Penelitian oleh Gao et al. (2022) menemukan bahwa website dengan nilai *Web Vitals* kategori "Good" memiliki 20-30% *higher engagement* dibanding yang tidak memenuhi standar.

### 2.1.9 Kompleksitas Aplikasi Web

Kompleksitas aplikasi web dapat dikategorikan berdasarkan beberapa faktor (Patel & Kumar, 2022):

**Kompleksitas Rendah:**
- 5-10 *routes/pages*, < 50 komponen
- Minimal *state management* (local state)
- Konten dominan statis, interaksi pengguna sederhana

**Kompleksitas Tinggi:**
- 10-30+ *routes/pages*, 50-200+ komponen
- *Centralized state management* (Vuex/Pinia)
- Operasi CRUD dengan integrasi API, visualisasi data (*Chart.js*)
- *Complex user workflows*

Alhammad dan Razzazi (2024) menemukan bahwa strategi optimasi yang efektif untuk aplikasi kompleksitas rendah tidak selalu efektif untuk kompleksitas tinggi. *Aggressive code splitting* pada aplikasi sederhana dapat menghasilkan *overhead HTTP requests* yang kontraproduktif.

---

## 2.2 Jenis dan Pendekatan Penelitian

Penelitian ini menggunakan pendekatan eksperimental kuantitatif dengan desain *comparative experimental*. Dua versi aplikasi dikompilasi dan diuji dengan cara yang sama:

1. **Versi Standar (Monolithic / Eager Load):** Semua kode dikemas dalam satu file besar dan dimuat sekaligus ketika website dibuka.
2. **Versi Dioptimalkan (Hybrid Splitting):** Kode dipecah menggunakan *Code Splitting*, *Lazy Loading*, kompresi (Brotli/Gzip), dan *Prefetching*.

Eksperimen dilakukan pada dua tingkat kompleksitas aplikasi (SIMTA dan *Company Profile*).

## 2.3 Variabel Penelitian

### 2.3.1 Variabel Independen
1. **Strategi Optimasi:** Tanpa optimasi (*baseline*) vs Dengan *hybrid lazy loading* dan *code splitting*
2. **Tingkat Kompleksitas Aplikasi:** Tinggi (SIMTA) vs Rendah (*Company Profile*)

### 2.3.2 Variabel Dependen
1. *First Contentful Paint* (FCP) — dalam milidetik
2. *Largest Contentful Paint* (LCP) — dalam milidetik
3. *Total Blocking Time* (TBT) — dalam milidetik
4. *Load Time* — dalam milidetik
5. *JS Heap Memory Used* — dalam MB
6. Lighthouse *Performance Score* — skala 0-100
7. *Time to Interactive* (TTI) — dalam milidetik (via Lighthouse)
8. *Bundle Size* — dalam kilobyte

### 2.3.3 Variabel Kontrol
1. Versi Vue.js (3.x), Versi Vite
2. *Hardware* pengujian (spesifikasi sama)
3. Browser (*Chrome/Chromium* versi terbaru)
4. Jaringan (*localhost*, eliminasi variabel jaringan)

## 2.4 Spesifikasi Perangkat yang Digunakan

**Perangkat Keras:**
- Sistem Operasi: Windows 10/11, 64-bit
- Prosesor: Setara generasi *quad core* atau *octa core*
- RAM: Minimal 8 GB
- Jaringan: Server lokal (*localhost*)

**Perangkat Lunak:**
1. Node.js (versi LTS v18/v20) — untuk menjalankan server lokal
2. Vue.js versi 3 — kerangka kerja untuk membangun tampilan
3. Vue-Router 4, Pinia Store v2, Chart.js — pustaka pendukung
4. Vite.js — alat untuk mengompilasi dan mengemas kode
5. Puppeteer — alat otomasi browser untuk menjalankan pengujian secara otomatis
6. Google Lighthouse — alat audit performa standar industri

## 2.5 Langkah-Langkah Penelitian

Penelitian dilakukan melalui enam tahap:

1. **Membangun dua aplikasi uji:** Membuat aplikasi SIMTA (kompleks) dan *Company Profile* (sederhana) sebagai objek perbandingan.
2. **Memastikan kode berjalan dengan benar:** Memverifikasi bahwa kedua aplikasi bisa dikompilasi tanpa *error*.
3. **Membuat dua versi kompilasi:** Mengompilasi masing-masing aplikasi dua kali — versi standar (*Baseline*) dan versi yang dioptimalkan (*Optimized*).
4. **Memasang alat ukur performa:** Menambahkan kode pelacak *PerformanceObserver* (standar W3C) ke dalam aplikasi, serta mengkonfigurasi Lighthouse untuk pengukuran tambahan.
5. **Menjalankan pengujian otomatis:** Menggunakan Puppeteer untuk membuka website secara otomatis dan merekam metrik. Pengujian dilakukan dalam dua kondisi (normal dan CPU diperlambat 4x), dengan **5 repetisi per skenario** untuk memastikan validitas data.
6. **Menganalisis hasil:** Menghitung rata-rata dan standar deviasi, membandingkan data dari semua skenario, dan membuat grafik perbandingan.

## 2.6 Gambaran Kompleksitas Sistem SIMTA

### 2.6.1 Struktur Data (*Entity Relationship Diagram*)

SIMTA mengelola banyak jenis data yang saling terhubung — mulai dari data mahasiswa, jadwal bimbingan, catatan pertemuan, hingga laporan akhir.

<div align="center">
  <img src="../chapters/images/mermaid_1.png" alt="Diagram Relasi Basis Data SIMTA/ERD" width="380" />
  <br>
  <i>Gambar 2.4 Entity Relationship Diagram (ERD) dari modul bimbingan SIMTA.</i>
</div>

### 2.6.2 Aliran Data (*Data Flow Diagram*)

Setiap perubahan data (misalnya ketika grafik baru dimuat atau daftar mahasiswa diperbarui) memicu pembaruan tampilan secara otomatis melalui Pinia dan Vue.js.

<div align="center">
  <img src="../chapters/images/mermaid_2.png" alt="Diagram Alir Komunikasi State Management Berbasis Pinia" width="380" />
  <br>
  <i>Gambar 2.5 Aliran data asinkron pada aplikasi SIMTA.</i>
</div>

Kerumitan ini menjadi alasan utama mengapa pendekatan *Lazy Loading* diperlukan — untuk meringankan beban browser saat pertama kali halaman dibuka.

## 2.7 Instrumen Pengumpulan Data

Penelitian ini menggunakan dua instrumen pengumpulan data utama:

### 2.7.1 Instrumen Primer: W3C *PerformanceObserver*

*PerformanceObserver* adalah antarmuka bawaan browser yang menjadi standar resmi W3C untuk merekam metrik secara langsung tanpa menambah beban pada sistem. Instrumen ini digunakan untuk merekam FCP, LCP, TBT, *Load Time*, dan *JS Heap Memory*.

<div align="center">
  <img src="../chapters/images/mermaid_3.png" alt="Alur Eksekusi Instrumen Pelacakan API Peramban" width="380" />
  <br>
  <i>Gambar 2.6 Struktur kerja alat ukur performa bawaan browser (PerformanceObserver).</i>
</div>

Berikut contoh potongan kode untuk merekam nilai FCP:

```javascript
const paintObserver = new PerformanceObserver((list) => {
    for (const entry of list.getEntriesByName('first-contentful-paint')) {
        let fcpDelay = Math.round(entry.startTime);
        MetricsTracker.record({ "FCP_ms": fcpDelay });
    }
});
paintObserver.observe({ type: 'paint', buffered: true });
```

### 2.7.2 Instrumen Sekunder: Google Lighthouse

Sebagai pelengkap pengukuran *PerformanceObserver*, penelitian ini juga menggunakan Google Lighthouse v11.x untuk mengaudit performa secara standar industri. Lighthouse memberikan metrik tambahan yang penting:
- **Performance Score** (0-100): Skor keseluruhan performa halaman
- **Time to Interactive (TTI):** Waktu hingga halaman *fully interactive*
- **Speed Index:** Seberapa cepat konten halaman terlihat secara visual

Penggunaan dua instrumen ini bertujuan untuk **triangulasi data** — memvalidasi hasil pengukuran dari satu instrumen dengan instrumen lainnya, sehingga meningkatkan keandalan temuan penelitian.

## 2.8 Skenario Pengujian

Pengujian dilakukan dalam dua kondisi menggunakan Puppeteer:

1. **Kondisi Normal:** Browser berjalan dengan kemampuan penuh tanpa hambatan. Berfungsi sebagai patokan awal.
2. **Kondisi Perangkat Lambat (CPU diperlambat 4x):** Kemampuan prosesor dibatasi hingga 4 kali lebih lambat, untuk mensimulasikan kondisi pengguna yang mengakses dari perangkat dengan spesifikasi rendah.

<div align="center">
  <img src="../chapters/images/mermaid_4.png" alt="Alur Logika Pengujian Otomasi" width="380" />
  <br>
  <i>Gambar 2.7 Alur pengujian otomatis dalam kondisi normal dan perangkat lambat.</i>
</div>

Setiap skenario dijalankan **5 kali** untuk memastikan konsistensi data. Dengan menggunakan alat otomasi, hasil pengujian menjadi lebih akurat dan konsisten karena tidak ada variasi dari perbedaan reaksi manusia.

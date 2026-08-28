<h1 align="center">Optimasi Performa Single Page Application Menggunakan Hybrid Lazy Loading dan Code Splitting Berdasarkan Tingkat Kompleksitas Sistem</h1>

---

# BAB I PENDAHULUAN

## 1.1 Latar Belakang Masalah

Single Page Application (SPA) telah menjadi arsitektur dominan dalam pengembangan aplikasi web modern karena kemampuannya memberikan pengalaman pengguna yang responsif dan interaktif (Kowalczyk & Szandała, 2024). Berbeda dengan aplikasi web tradisional *Multi-Page Application* (MPA) yang memuat ulang seluruh halaman untuk setiap interaksi pengguna, SPA memuat seluruh konten dalam satu halaman HTML dan secara dinamis memperbarui tampilan tanpa *reload* halaman penuh, menghasilkan pengalaman yang lebih mirip aplikasi *desktop* (Taivalsaari & Mikkonen, 2021).

Dalam arsitektur MPA konvensional, setiap interaksi pengguna mengharuskan server memproses ulang halaman HTML secara utuh dan mengirimkannya kembali ke browser. Mekanisme pemuatan penuh (*full page reload*) ini tidak hanya membebani lalu lintas server, tetapi juga mendegradasi pengalaman pengguna karena timbulnya layar putih berkedip (*white screen blanking*) selama masa tunggu transmisi jaringan (Kowalczyk & Szandała, 2024).

<div align="center">
  <img src="../chapters/images/diagram_mpa_spa.png" alt="Perbandingan Alur MPA dan SPA" width="380" />
  <br>
  <i>Gambar 1.1 Perbandingan arsitektur MPA (Multi-Page Application) dan SPA (Single Page Application).</i>
</div>

Gambar 1.1 di atas memperlihatkan perbedaan mendasar antara arsitektur MPA dan SPA. Pada MPA, setiap klik pengguna memaksa server untuk memproses dan mengirimkan ulang seluruh halaman HTML, menghasilkan layar putih berkedip yang mengganggu pengalaman pengguna. Sebaliknya, pada SPA, server hanya mengirimkan data JSON berukuran kecil, sementara browser memperbarui tampilan secara parsial melalui JavaScript. Perbedaan inilah yang menjadi dasar mengapa ukuran *bundle* JavaScript pada SPA perlu dikelola dengan cermat melalui teknik seperti *lazy loading* dan *code splitting*.

Sebagai solusi dari masalah tersebut, paradigma SPA hadir sebagai standar industri mutakhir yang dipelopori oleh kerangka kerja JavaScript reaktif berbasis komponen seperti Vue.js, React, dan Angular. SPA memungkinkan aplikasi web untuk mengunduh satu kerangka HTML (`index.html`) pada muatan perdana, kemudian semua perubahan tampilan dikelola oleh JavaScript di browser. Ketika pengguna berpindah halaman, aplikasi hanya mengambil data kecil dalam format JSON dari server melalui API asinkron, lalu memperbarui bagian-bagian tertentu di layar saja (Taivalsaari & Mikkonen, 2021).

Namun, pertumbuhan kompleksitas aplikasi web menyebabkan peningkatan ukuran *bundle* JavaScript yang berdampak negatif pada performa. Ukuran *bundle* JavaScript yang besar berdampak langsung pada waktu muat halaman; keterlambatan pemuatan beberapa detik saja terbukti meningkatkan *bounce rate* secara signifikan (Google, 2020).

Ketika sebuah aplikasi SPA tidak dioptimalkan dengan benar, browser terpaksa mengunduh seluruh kode program — termasuk semua halaman, komponen, gambar, dan pustaka pihak ketiga — sekaligus dalam satu file JavaScript yang sangat besar (*monolithic build*). Untuk website sederhana seperti halaman profil perusahaan, hal ini mungkin tidak masalah. Tetapi untuk aplikasi yang kompleks seperti Sistem Informasi Manajemen Tugas Akhir (SIMTA) — yang menggunakan banyak fitur seperti grafik interaktif (*Chart.js*), manajemen data global (*Pinia*), lapisan layanan data asinkron, dan otentikasi pengguna — ukuran file-nya dapat melebihi batas wajar yang direkomendasikan untuk browser (lebih dari 300 KB terkompresi).

Pada tahap awal, aplikasi berkompleksitas tinggi ditetapkan melalui kajian awal (*preliminary study*). Kandidat awal berupa *dashboard* admin toko dinilai kurang representatif karena tidak memiliki ketergantungan pustaka eksternal yang cukup berat untuk menghasilkan perbedaan yang terukur secara signifikan pada strategi *code splitting*. Oleh karena itu, objek penelitian ditetapkan pada Sistem Informasi Manajemen Tugas Akhir (SIMTA) yang secara bersamaan menggunakan Chart.js (grafik interaktif), Pinia (*state management*), lapisan layanan data asinkron bergaya Supabase, dan Vue Router dengan 15+ rute. Kombinasi ini menghasilkan *bundle* monolitik yang jauh lebih besar sehingga mewakili aplikasi kompleksitas tinggi secara lebih representatif, tanpa mengubah pertanyaan penelitian, variabel, maupun tujuan yang telah ditetapkan.

Akibat dari *bundle* yang terlalu besar ini sangat merugikan. Nilai-nilai penting dalam pengukuran performa web yang disebut *Core Web Vitals* — yang digunakan oleh mesin pencari seperti Google — akan turun drastis (Google Chrome Developers, 2023). Perbaikan pada metrik pemuatan seperti LCP dan FCP berkorelasi dengan peningkatan keterlibatan pengguna dan penurunan *bounce rate*. Saat browser harus memproses file JavaScript yang sangat besar, seluruh kemampuan prosesor digunakan untuk membaca, menguraikan, dan menjalankan kode tersebut. Selama proses ini berlangsung, browser tidak bisa merespons klik atau interaksi pengguna sama sekali — kondisi yang diukur melalui metrik *Total Blocking Time* (TBT) (Google Chrome Developers, 2023).

Untuk mengatasi masalah ini, pendekatan *Code Splitting* dan *Lazy Loading* telah dikembangkan (Kumar, Singh & Sharma, 2024). Alih-alih mengirimkan semua kode sekaligus, hanya bagian yang diperlukan saat pengguna membuka halaman tertentu yang dikirimkan. Kumar, Singh, dan Sharma (2024) menunjukkan bahwa kombinasi *lazy loading* dan *code splitting* dapat menurunkan waktu muat halaman hingga sekitar 40% dibandingkan implementasi standar. Lebih lanjut, teknik *Hybrid Lazy Loading* atau *Prefetching* memanfaatkan waktu senggang browser untuk diam-diam mengunduh terlebih dahulu bagian kode yang kemungkinan akan dibutuhkan selanjutnya (Google Chrome Developers, 2023).

Tingkat kompleksitas aplikasi web mempengaruhi efektivitas strategi optimasi. Aplikasi dengan kompleksitas rendah seperti *company profile* memiliki karakteristik berbeda dengan aplikasi kompleksitas tinggi yang melibatkan operasi CRUD dan visualisasi data *real-time*. Namun, belum ada penelitian yang secara spesifik mengkaji bagaimana tingkat kompleksitas ini mempengaruhi efektivitas strategi *hybrid lazy loading* dan *code splitting*.

Berdasarkan permasalahan di atas, penelitian ini membahas topik: **"Optimasi Performa Single Page Application Menggunakan Hybrid Lazy Loading dan Code Splitting Berdasarkan Tingkat Kompleksitas Sistem"**.

---

## 1.2 Rumusan Masalah

Berdasarkan permasalahan yang telah diuraikan, penelitian ini difokuskan pada pertanyaan-pertanyaan berikut:

1. Bagaimana pengaruh implementasi *hybrid lazy loading* dan *code splitting* terhadap metrik performa SPA (FCP, LCP, TBT, dan *bundle size*) pada aplikasi dengan tingkat kompleksitas tinggi (SIMTA)?

2. Bagaimana pengaruh implementasi *hybrid lazy loading* dan *code splitting* terhadap metrik performa SPA pada aplikasi dengan tingkat kompleksitas rendah (*Company Profile*)?

3. Bagaimana perbedaan efektivitas strategi *hybrid lazy loading* dan *code splitting* antara aplikasi kompleksitas tinggi dan rendah?

4. Bagaimana rekomendasi strategi optimasi *hybrid lazy loading* dan *code splitting* yang sesuai berdasarkan tingkat kompleksitas aplikasi web?

---

## 1.3 Batasan Masalah

Agar penelitian ini fokus dan hasilnya dapat diukur dengan jelas, batasan penelitian ditetapkan sebagai berikut:

1. **Framework dan Build Tool:** Vue.js versi 3.x dengan Composition API, menggunakan Vite sebagai *build tool*.

2. Penelitian menggunakan dua jenis aplikasi sebagai objek percobaan:
   - **Aplikasi Kompleks/Tinggi (SIMTA):** Sistem Informasi Manajemen Tugas Akhir yang menggunakan Vue.js 3, Chart.js, Pinia, dan Vue Router secara bersamaan, dengan lapisan layanan data asinkron bergaya Supabase.
   - **Aplikasi Sederhana/Rendah (Company Profile):** Website profil perusahaan yang hanya menampilkan konten statis tanpa grafik interaktif atau manajemen data yang kompleks.

3. **Teknik Optimasi:** *Route-based lazy loading*, *component-based lazy loading*, *dynamic import*, *code splitting* berbasis *chunk*, dan *intelligent prefetching*.

4. **Metrik Performa:** *First Contentful Paint* (FCP), *Largest Contentful Paint* (LCP), *Total Blocking Time* (TBT), *Load Time*, penggunaan memori JavaScript (*JS Heap*), serta data tambahan dari Lighthouse (*Performance Score*, *Time to Interactive*).

5. **Alat pengukuran:** Kombinasi *W3C PerformanceObserver* (pengukuran langsung dari browser) dan Google Lighthouse (sebagai alat audit standar industri), dijalankan secara otomatis melalui Puppeteer.

6. **Pengujian:** Dilakukan di server lokal (*localhost*) menggunakan Puppeteer untuk automasi browser, dengan simulasi pelambatan CPU 4x melalui *Puppeteer Chromium API*, sehingga variabel jaringan dapat dieleminasi untuk mendapatkan pengukuran *CPU-bound* yang murni.

7. **Tidak mencakup:** *Server-Side Rendering* (SSR), *Progressive Web App* (PWA), dan optimasi *backend/database*.

---

## 1.4 Tujuan Penelitian

Penelitian ini bertujuan untuk:

1. Menganalisis pengaruh implementasi *hybrid lazy loading* dan *code splitting* terhadap metrik performa SPA pada aplikasi kompleksitas tinggi (SIMTA), khususnya dalam memisahkan pustaka-pustaka besar seperti Chart.js dan Pinia ke dalam file-file terpisah.

2. Menganalisis pengaruh implementasi *hybrid lazy loading* dan *code splitting* terhadap metrik performa SPA pada aplikasi kompleksitas rendah (*Company Profile*).

3. Membandingkan efektivitas strategi *hybrid lazy loading* dan *code splitting* antara aplikasi kompleksitas tinggi dan rendah.

4. Merumuskan rekomendasi strategi optimasi *hybrid lazy loading* dan *code splitting* berdasarkan tingkat kompleksitas aplikasi web.

---

## 1.5 Manfaat Penelitian

### 1.5.1 Manfaat Teoritis

1. Memberikan kontribusi pada *body of knowledge* terkait optimasi performa *Single Page Application* khususnya dalam konteks Vue.js dan Vite *build tool*.
2. Memperkaya literatur tentang strategi *adaptive optimization* yang mempertimbangkan karakteristik dan kompleksitas aplikasi web.
3. Memberikan referensi baru tentang cara mengoptimalkan performa SPA menggunakan pengukuran yang akurat dan langsung dari browser (W3C *PerformanceObserver*), sehingga hasilnya lebih representatif terhadap kondisi nyata.

### 1.5.2 Manfaat Praktis

1. **Bagi Developer:** Memberikan panduan praktis dalam menerapkan strategi *hybrid lazy loading* dan *code splitting* pada proyek Vue.js berdasarkan tingkat kompleksitas aplikasi.
2. **Bagi Industri:** Membantu organisasi dalam mengoptimalkan performa aplikasi web yang berdampak pada peningkatan *user experience* dan *conversion rate*.
3. **Bagi Peneliti Selanjutnya:** Menyediakan *baseline* dan metodologi yang dapat dikembangkan untuk penelitian lebih lanjut terkait optimasi performa web.

---

## 1.6 Tinjauan Pustaka / Penelitian Terdahulu

Optimasi performa *Single Page Application* melalui *code splitting* dan *lazy loading* telah menjadi fokus berbagai penelitian dalam beberapa tahun terakhir. Untuk memposisikan kontribusi penelitian ini secara jelas, Tabel 1.1 merangkum enam penelitian terdahulu yang paling relevan — mencakup fokus dan metode, temuan utama, serta kesenjangan (*gap*) masing-masing terhadap penelitian yang dilakukan. Sintesis dari keseluruhan tinjauan pustaka disajikan setelah tabel.

**Tabel 1.1** Rangkuman Perbandingan Penelitian Terdahulu

| No | Peneliti (Tahun) | Fokus & Metode | Hasil / Temuan | Gap & Perbedaan dengan Penelitian Ini |
|----|------------------|----------------|----------------|----------------------------------------|
| 1 | Kowalczyk & Szandała (2024) | Evaluasi SEO & visibilitas SPA vs MPA (*IEEE Access*); studi review + eksperimen. | SPA menghadapi tantangan indexing/SEO dibanding MPA; diusulkan strategi peningkatan visibilitas. | Fokus pada SEO, bukan optimasi performa. Penelitian ini fokus *lazy loading* + *code splitting* dan tingkat kompleksitas. |
| 2 | Emmanni (2023) | Analisis komparatif Angular, React, dan Vue.js untuk pengembangan SPA (benchmark + survei). | Setiap framework unggul pada konteks berbeda; pemilihan bergantung kebutuhan proyek. | Perbandingan bersifat umum; tidak menerapkan/mengukur teknik optimasi maupun faktor kompleksitas. Penelitian ini fokus Vue.js + Vite. |
| 3 | Bara, Boiangiu & Tudose (2024) | Analisis empiris dampak *lazy loading* (situs statis vs dinamis, variasi kondisi jaringan). | *Lazy loading* memperbaiki FCP/LCP, terutama pada jaringan lambat; terdapat *trade-off* eager vs lazy. | Hanya *lazy loading* tanpa *code splitting*; tidak spesifik Vue+Vite dan tidak mengklasifikasi tingkat kompleksitas. |
| 4 | Kumar, Singh & Sharma (2024) | Implementasi *lazy loading* + *code splitting* lintas framework (React, Angular, Vue). | Kombinasi keduanya menurunkan *page load time* hingga ±40%. | Bersifat umum; tidak *deep-dive* Vue.js + Vite dan tidak mempertimbangkan tingkat kompleksitas sistem sebagai penentu strategi. |
| 5 | Setiawan & Fauzi (2025) | Komparatif *lazy loading* + *code splitting* pada React/Vue/Angular berdasarkan skor Lighthouse (FCP, LCP, TBT, CLS). | React waktu muat tercepat & stabilitas layout terbaik; Vue fleksibel; Angular lebih rendah. | Pengukuran hanya via Lighthouse (bukan *PerformanceObserver* real-user), tanpa uji tingkat kompleksitas & *CPU throttling*; keduanya ditambahkan di penelitian ini. |
| 6 | Taivalsaari & Mikkonen (2021) | *Roadmap* arsitektur SPA di era *programmable world* (konseptual). | SPA memberi pengalaman responsif; menyoroti tantangan arsitektur & beban di sisi klien. | Bersifat visioner/konseptual, bukan evaluasi teknik optimasi konkret. |

Di luar keenam studi utama pada Tabel 1.1, sejumlah penelitian lain memperkuat konteks penelitian ini. Perbandingan performa antar-*framework* JavaScript modern telah banyak dikaji (Piastou, 2023; Jihadi & Syarabil, 2023; Sofi'ie & Qoiriah, 2023; Anggraeni dkk., 2024; Khoirurrizal dkk., 2024; Wijaya & Farisi, 2025), termasuk pengembangan SPA berbasis React (Jonathan & Suprihadi, 2023) dan efisiensi *build tool* modern seperti Vite (Fauzi, 2024). Teknik *lazy loading* dan *code splitting* untuk meningkatkan responsivitas juga menjadi perhatian (Turcotte, Gokhale & Tip, 2023; Larissa & Suartana, 2026), demikian pula aspek pendukung seperti manajemen *state* (Donvir dkk., 2024), kualitas kode JavaScript dan TypeScript (Saboury dkk., 2017; Johannes dkk., 2019; Bogner & Merkel, 2022), mekanisme *rendering* dan *Server-Side Rendering* (Noer & Suartana, 2024; Hermanto & Engel, 2025), pengujian *end-to-end* (Rezeki dkk., 2026), serta tinjauan umum teknik optimasi performa web (Vepsäläinen, Hellas & Vuorimaa, 2023).

**Gap Penelitian:** Berdasarkan tinjauan di atas, belum terdapat penelitian komprehensif yang mengkaji implementasi *hybrid lazy loading* dan *code splitting* pada Vue.js dengan Vite yang mempertimbangkan tingkat kompleksitas aplikasi sebagai faktor penentu strategi optimasi. Penelitian ini mengisi gap tersebut dengan membandingkan dua aplikasi dengan kompleksitas yang sangat berbeda, menggunakan kombinasi alat pengukuran (*PerformanceObserver* + Lighthouse), dan menguji pada kondisi perangkat yang terbatas (*CPU throttling*).

---

## 1.7 Sistematika Penulisan

Penulisan tesis ini dibagi menjadi empat bab utama:

- **BAB I PENDAHULUAN:** Menjelaskan latar belakang mengapa performa SPA perlu dioptimalkan, masalah yang ingin diselesaikan, batasan penelitian, tujuan, manfaat, dan ringkasan penelitian-penelitian terdahulu yang relevan.

- **BAB II METODE PENELITIAN DAN LANDASAN TEORI:** Menjelaskan teori-teori dasar yang digunakan serta metodologi penelitian secara detail termasuk variabel penelitian, spesifikasi alat yang digunakan, dan langkah-langkah pengujian.

- **BAB III HASIL DAN PEMBAHASAN:** Menyajikan hasil pengukuran dari kedua versi aplikasi (standar dan yang dioptimalkan), termasuk kode program, grafik perbandingan, data Lighthouse, analisis statistik, dan interpretasi mendalam tentang setiap temuan.

- **BAB IV PENUTUP:** Merangkum kesimpulan dari penelitian dan memberikan saran untuk penelitian lanjutan.

---

# BAB II METODE PENELITIAN DAN LANDASAN TEORI

## 2.1 Landasan Teori

### 2.1.1 Arsitektur *Single Page Application* (SPA) dan *Virtual DOM*

*Single Page Application* (SPA) adalah aplikasi web yang berinteraksi dengan pengguna melalui pemuatan ulang dinamis halaman tunggal, berbeda dengan aplikasi web tradisional yang memuat ulang seluruh halaman untuk setiap interaksi (Kowalczyk & Szandała, 2024). Menurut Taivalsaari dan Mikkonen (2021), SPA menawarkan pengalaman pengguna yang lebih responsif karena hanya memperbarui konten yang diperlukan tanpa *reload* seluruh halaman.

Salah satu fitur unggulan SPA adalah penggunaan *Virtual DOM*. *Virtual DOM* adalah representasi maya dari tampilan halaman yang disimpan di memori JavaScript. Ketika ada data yang berubah, Vue.js terlebih dahulu membuat *Virtual DOM* baru, membandingkannya dengan salinan lama (*diffing algorithm*), lalu memperbarui tampilan nyata hanya pada bagian yang berbeda saja. Cara ini jauh lebih efisien dibandingkan memuat ulang seluruh halaman (You et al., 2023).

<div align="center">
  <img src="../chapters/images/diagram_vdom.png" alt="Proses Render Virtual DOM" width="380" />
  <br>
  <i>Gambar 2.1 Mekanisme pembaruan antarmuka melalui algoritma diffing Virtual DOM.</i>
</div>

Gambar 2.1 di atas mengilustrasikan cara *Virtual DOM* mengoptimalkan proses pembaruan antarmuka. Daripada menggambar ulang seluruh halaman setiap kali data berubah, Vue.js hanya memperbarui *node-node* DOM yang benar-benar berbeda antara *snapshot Virtual DOM* lama dan baru. Efisiensi ini sangat relevan dengan topik penelitian karena menjelaskan mengapa penundaan *parsing* JavaScript melalui *lazy loading* tidak mengurangi kecepatan pembaruan antarmuka setelah komponen berhasil dimuat.

### 2.1.2 Vue.js *Framework*

Vue.js adalah *progressive JavaScript framework* yang dirancang untuk membangun *user interface* dengan pendekatan *bottom-up incremental adoption* (You et al., 2023). Vue.js 3 memperkenalkan *Composition API* sebagai alternatif *Options API*, serta *reactivity system* menggunakan ES6 *Proxy* yang menghasilkan performa lebih baik. Menurut dokumentasi resmi Vue.js (You et al., 2023), Vue 3 menghadirkan peningkatan *rendering performance*, *memory footprint* yang lebih rendah, serta *bundle size* yang lebih kecil dibandingkan Vue 2.

### 2.1.3 Vite *Build Tool* dan *Code Splitting*

Vite adalah *build tool* modern yang dikembangkan oleh Evan You dengan fokus pada *developer experience* dan performa (Vite Team, 2024). Berbeda dengan *bundler* tradisional seperti Webpack, Vite memanfaatkan *native ES modules* di browser untuk melayani kode secara *on-demand*. Vite juga menyediakan optimasi ukuran *bundle* secara *default* melalui konfigurasi Rollup yang telah dioptimasi untuk web (Vite Team, 2024). Untuk *production build*, Vite menggunakan Rollup sebagai *bundler* dengan konfigurasi yang sudah dioptimasi, termasuk *code splitting* berbasis *dynamic import* dan *vendor chunk separation*.

### 2.1.4 *Lazy Loading*

*Lazy loading* adalah teknik optimasi yang menunda *loading resource* hingga benar-benar diperlukan oleh pengguna (Bara, Boiangiu & Tudose, 2024). Terdapat beberapa strategi yang dapat diterapkan pada Vue.js:

1. ***Route-based Lazy Loading:*** Memuat komponen *route* hanya ketika *route* tersebut diakses pertama kali.
2. ***Component-based Lazy Loading:*** Memuat komponen individual secara *on-demand*, biasanya untuk komponen yang berat atau jarang digunakan.
3. ***Conditional Lazy Loading:*** Memuat komponen berdasarkan kondisi tertentu seperti *user role* atau *device type*.

Bara, Boiangiu, dan Tudose (2024) menemukan bahwa penerapan *lazy loading* efektif mengurangi *initial bundle size* dan memperbaiki metrik pemuatan awal, terutama pada kondisi jaringan lambat.

### 2.1.5 Strategi Optimasi Hibrida

Penelitian terbaru menunjukkan bahwa pendekatan hibrida yang mengkombinasikan beberapa teknik optimasi menghasilkan hasil lebih baik dibandingkan pendekatan tunggal (Setiawan & Fauzi, 2025). Efektivitas strategi hibrida ini bergantung pada karakteristik aplikasi, termasuk jumlah *routes* dan komponen, ukuran individual komponen, kompleksitas *dependency graph*, pola navigasi pengguna, serta kondisi target perangkat dan jaringan.

### 2.1.6 Bagaimana Browser Memproses File JavaScript

File JavaScript tidak bisa langsung dijalankan oleh browser. Browser — khususnya yang menggunakan mesin V8 seperti Google Chrome — harus melalui beberapa tahap (Hasanuddin, 2021):

1. **Mengunduh file (*Resolution & Downloading*):** Browser menjalin koneksi TCP via HTTP *Request* untuk mengunduh file JavaScript dari server.
2. **Membaca dan mengurai kode (*Lexical Parsing & AST*):** Browser membaca kode dan mengubahnya menjadi *Abstract Syntax Tree*. Proses ini menyita seluruh kapasitas *Main Thread*.
3. **Mengompilasi (*JIT Compilation*):** Struktur kode diubah menjadi instruksi yang bisa dijalankan langsung oleh prosesor.
4. **Menjalankan dan mengalokasikan memori (*Execution & Memory Allocation*):** Semua fungsi, variabel, dan pustaka ditempatkan di memori (*JS Heap*), lalu Vue.js mulai menggambar tampilan di layar.

Karena JavaScript bekerja secara *single-threaded*, ketika browser sedang memproses file JS yang sangat besar, browser tidak bisa merespons interaksi pengguna (Google Chrome Developers, 2023). Inilah yang disebut *Event Loop Blocking*, dan yang diukur oleh metrik *Total Blocking Time* (TBT).

<div align="center">
  <img src="../chapters/images/diagram_v8.png" alt="Siklus Eksekusi V8 Engine" width="450" />
  <br>
  <i>Gambar 2.2 Tahapan pemrosesan file JavaScript oleh mesin V8 di browser.</i>
</div>

Gambar 2.2 di atas menunjukkan bahwa pemrosesan JavaScript merupakan proses bertahap yang membebani *Main Thread* secara eksklusif. Tahap *Parsing* dan Kompilasi adalah yang paling kritis karena selama tahap ini browser sepenuhnya tidak dapat merespons interaksi pengguna — inilah yang diukur oleh metrik *Total Blocking Time* (TBT). Pemahaman atas tahapan ini menjadi landasan teknis mengapa *code splitting* efektif: dengan memperkecil ukuran file yang harus diproses pada muatan awal, durasi pemblokiran *Main Thread* dapat dikurangi secara signifikan.

### 2.1.7 *Event Loop* dan Mekanisme Asinkron

*Event Loop* adalah mekanisme bawaan browser untuk menangani tugas-tugas yang butuh waktu lama tanpa membekukan layar. Tugas-tugas yang memakan waktu tidak diproses langsung, melainkan dititipkan ke area penantian khusus (*Callback Queue*). Sambil menunggu, browser tetap bisa merespons interaksi pengguna. Setelah tampilan dasar selesai digambar, barulah browser mengambil tugas-tugas yang menunggu (W3C, 2022). Prinsip inilah yang membuat *Lazy Loading* bisa bekerja dengan baik — modul-modul besar ditunda pengunduhan dan pemrosesannya hingga benar-benar dibutuhkan.

<div align="center">
  <img src="../chapters/images/diagram_event_loop.png" alt="Arsitektur Event Loop" width="380" />
  <br>
  <i>Gambar 2.3 Mekanisme Event Loop dalam menangani tugas asinkron JavaScript.</i>
</div>

Gambar 2.3 di atas memperlihatkan bahwa *Event Loop* adalah mekanisme yang memungkinkan *lazy loading* bekerja tanpa membekukan antarmuka. Ketika pengguna berpindah ke halaman baru, permintaan pengunduhan modul ditempatkan ke *Web APIs* dan *Callback Queue*, sehingga browser tetap responsif sambil modul sedang diunduh di latar belakang. Mekanisme inilah yang menjadi fondasi teknis dari strategi *hybrid lazy loading* yang diimplementasikan dalam penelitian ini.

### 2.1.8 Metrik Performa Web (*Core Web Vitals*)

Performa sebuah website diukur menggunakan standar *Core Web Vitals* (Google Chrome Developers, 2023):

1. **First Contentful Paint (FCP):** Waktu dari saat pengguna membuka website hingga sesuatu pertama kali muncul di layar. Standar yang baik: ≤ 1.800 ms.

2. **Largest Contentful Paint (LCP):** Waktu hingga elemen terbesar di halaman selesai dimuat. Standar yang baik: ≤ 2.500 ms.

3. **Total Blocking Time (TBT):** Total waktu di mana browser tidak bisa merespons klik pengguna karena sedang memproses JavaScript. Nilai TBT yang baik harus ≤ 200-300 ms (Google Chrome Developers, 2023). TBT adalah metrik yang paling langsung mengukur dampak *bundle* JavaScript yang besar terhadap interaktivitas pengguna.

4. **Time to Interactive (TTI):** Waktu hingga halaman *fully interactive* dan dapat merespons input pengguna secara *reliable*. Target: ≤ 3,8 detik (Google Chrome Developers, 2023).

### 2.1.9 Kompleksitas Aplikasi Web

Kompleksitas aplikasi web dapat dikategorikan berdasarkan beberapa faktor:

1. **Kompleksitas Rendah:** 5-10 *routes/pages*, < 50 komponen, minimal *state management* (*local state*), konten dominan statis, interaksi pengguna sederhana.
2. **Kompleksitas Tinggi:** 10-30+ *routes/pages*, 50-200+ komponen, *centralized state management* (Vuex/Pinia), operasi CRUD dengan integrasi API, visualisasi data (*Chart.js*), *complex user workflows*, integrasi dengan layanan eksternal (Supabase, dll).

Strategi optimasi yang efektif untuk aplikasi kompleksitas rendah tidak selalu efektif untuk kompleksitas tinggi. *Aggressive code splitting* pada aplikasi sederhana justru dapat menghasilkan *overhead HTTP requests* yang kontraproduktif — konsisten dengan adanya *trade-off* eager vs lazy loading yang dilaporkan Bara, Boiangiu, dan Tudose (2024).

---

## 2.2 Jenis dan Pendekatan Penelitian

Penelitian ini menggunakan pendekatan eksperimental kuantitatif dengan desain *comparative experimental*. Dua versi aplikasi dikompilasi dan diuji dengan cara yang sama:

1. **Versi Standar (Monolithic / Eager Load):** Semua kode dikemas dalam satu file besar dan dimuat sekaligus ketika website dibuka.
2. **Versi Dioptimalkan (Hybrid Splitting):** Kode dipecah menggunakan *Code Splitting*, *Lazy Loading*, kompresi (Brotli/Gzip), dan *Prefetching*.

Eksperimen dilakukan pada dua tingkat kompleksitas aplikasi (SIMTA sebagai aplikasi kompleksitas tinggi dan *Company Profile* sebagai aplikasi kompleksitas rendah).

## 2.3 Variabel Penelitian

### 2.3.1 Variabel Independen

1. **Strategi Optimasi:** Tanpa optimasi (*baseline*) vs. Dengan *hybrid lazy loading* dan *code splitting*.
2. **Tingkat Kompleksitas Aplikasi:** Tinggi (SIMTA) vs. Rendah (*Company Profile*).

### 2.3.2 Variabel Dependen

Berdasarkan kajian literatur dan kebutuhan pengukuran yang lebih komprehensif, variabel dependen yang digunakan dalam penelitian ini adalah:

1. *First Contentful Paint* (FCP) — dalam milidetik
2. *Largest Contentful Paint* (LCP) — dalam milidetik
3. *Total Blocking Time* (TBT) — dalam milidetik. Metrik ini ditambahkan karena secara langsung mengukur dampak *blocking* JavaScript terhadap interaktivitas, yang merupakan inti permasalahan yang diteliti.
4. *Load Time* — dalam milidetik
5. *JS Heap Memory Used* — dalam MB
6. Lighthouse *Performance Score* — skala 0-100
7. *Time to Interactive* (TTI) — dalam milidetik (via Lighthouse)
8. *Bundle Size* — dalam kilobyte

Variabel dependen utama dalam penelitian ini mencakup *Initial Bundle Size*, *Total Bundle Size*, dan *Number of Chunks*. Selain itu, *Total Blocking Time* (TBT) turut ditetapkan sebagai variabel dependen utama karena terbukti menjadi indikator paling sensitif terhadap efek *code splitting* pada *Main Thread blocking*, sementara *Time to Interactive* (TTI) tetap diukur melalui Lighthouse sebagai data sekunder.

### 2.3.3 Variabel Kontrol

1. Versi Vue.js (3.x) dan Versi Vite
2. *Hardware* pengujian (spesifikasi sama untuk seluruh skenario)
3. Browser (*Chrome/Chromium* versi terbaru via Puppeteer)
4. Jaringan (*localhost*, eliminasi variabel jaringan untuk mendapatkan pengukuran *CPU-bound* yang murni)

## 2.4 Spesifikasi Perangkat yang Digunakan

### 2.4.1 Perangkat Keras

- Sistem Operasi: Windows 10/11, 64-bit
- Prosesor: Setara generasi *quad core* atau *octa core*
- RAM: Minimal 8 GB
- Jaringan: Server lokal (*localhost*)

### 2.4.2 Perangkat Lunak

1. Node.js (versi LTS v18/v20) — untuk menjalankan server lokal
2. Vue.js versi 3 — kerangka kerja untuk membangun tampilan
3. Vue-Router 4, Pinia Store v2, Chart.js, Tailwind CSS — pustaka pendukung SIMTA
4. Vite.js — alat untuk mengompilasi dan mengemas kode
5. Puppeteer — alat otomasi browser untuk menjalankan pengujian secara otomatis
6. Google Lighthouse v11.x — alat audit performa standar industri

## 2.5 Langkah-Langkah Penelitian

Penelitian dilakukan melalui enam tahap:

1. **Membangun dua aplikasi uji:** Membuat aplikasi SIMTA (kompleks/tinggi) dan *Company Profile* (sederhana/rendah) sebagai objek perbandingan.
2. **Memastikan kode berjalan dengan benar:** Memverifikasi bahwa kedua aplikasi bisa dikompilasi tanpa *error*.
3. **Membuat dua versi kompilasi:** Mengompilasi masing-masing aplikasi dua kali — versi standar (*Baseline*) dan versi yang dioptimalkan (*Optimized*).
4. **Memasang alat ukur performa:** Menambahkan kode pelacak *PerformanceObserver* (standar W3C) ke dalam aplikasi, serta mengkonfigurasi Lighthouse untuk pengukuran tambahan.
5. **Menjalankan pengujian otomatis:** Menggunakan Puppeteer untuk membuka website secara otomatis dan merekam metrik. Pengujian dilakukan dalam dua kondisi (normal dan CPU diperlambat 4x), dengan **5 repetisi per skenario** untuk memastikan validitas data.
6. **Menganalisis hasil:** Menghitung rata-rata dan standar deviasi, membandingkan data dari semua skenario, dan membuat grafik perbandingan.

## 2.6 Gambaran Kompleksitas Sistem SIMTA

SIMTA (Sistem Informasi Manajemen Tugas Akhir) mengelola banyak jenis data yang saling terhubung — mulai dari data mahasiswa, jadwal bimbingan, catatan pertemuan, hingga laporan akhir. Kompleksitas SIMTA dapat diukur dari beberapa karakteristik:

1. 15+ rute navigasi yang berbeda
2. 50+ komponen Vue.js
3. Ketergantungan pada 3 pustaka besar secara bersamaan: Chart.js, Pinia, dan Vue-Router
4. Operasi CRUD melalui lapisan layanan data asinkron
5. Visualisasi data *real-time* menggunakan Chart.js
6. Alur autentikasi pengguna

Kerumitan ini menjadi alasan utama mengapa pendekatan *Lazy Loading* diperlukan — untuk meringankan beban browser saat pertama kali halaman dibuka, terutama dengan memindahkan Chart.js (yang tidak dibutuhkan di halaman login) ke *chunk* terpisah.

Perlu dicatat bahwa lapisan akses data pada SIMTA diimplementasikan sebagai *service layer* asinkron yang meniru pola pemanggilan Supabase (*promise-based* dengan penundaan jaringan tersimulasi), bukan koneksi ke basis data daring. Pilihan ini diambil agar pengujian sepenuhnya *CPU-bound* dan hasilnya dapat direproduksi tanpa bergantung pada ketersediaan layanan pihak ketiga maupun latensi jaringan. Karena strategi *code splitting* yang diteliti bekerja pada lapisan pemuatan modul JavaScript, keputusan ini tidak memengaruhi validitas perbandingan antara versi *baseline* dan *optimized*.

### 2.6.1 Struktur Data (*Entity Relationship Diagram*)

SIMTA mengelola banyak jenis data yang saling terhubung — mulai dari data mahasiswa, jadwal bimbingan, catatan pertemuan, hingga laporan akhir.

<div align="center">
  <img src="../chapters/images/mermaid_1.png" alt="Diagram Relasi Basis Data SIMTA/ERD" width="380" />
  <br>
  <i>Gambar 2.4 Entity Relationship Diagram (ERD) dari modul bimbingan SIMTA.</i>
</div>

Gambar 2.4 di atas menggambarkan kompleksitas relasi data pada SIMTA yang menjadi justifikasi utama dipilihnya aplikasi ini sebagai objek penelitian kompleksitas tinggi. Terdapat lima entitas utama yang saling terhubung melalui relasi *one-to-many* dan *one-to-one*. Kompleksitas relasi ini berimplikasi pada kebutuhan *state management* terpusat (Pinia) dan visualisasi data (Chart.js) — dua pustaka yang masing-masing berkontribusi signifikan terhadap ukuran *bundle* JavaScript dan menjadi target utama pemisahan *chunk* dalam implementasi *code splitting*.

### 2.6.2 Aliran Data (*Data Flow Diagram*)

Setiap perubahan data (misalnya ketika grafik baru dimuat atau daftar mahasiswa diperbarui) memicu pembaruan tampilan secara otomatis melalui Pinia dan Vue.js.

<div align="center">
  <img src="../chapters/images/mermaid_2.png" alt="Diagram Alir Komunikasi State Management Berbasis Pinia" width="380" />
  <br>
  <i>Gambar 2.5 Aliran data asinkron pada aplikasi SIMTA.</i>
</div>

Gambar 2.5 di atas mengilustrasikan aliran data reaktif pada SIMTA yang melibatkan tiga lapisan: komponen Vue sebagai lapisan tampilan, Pinia *Store* sebagai lapisan *state management*, dan lapisan layanan data asinkron (*service layer*) yang meniru pola akses Supabase. Setiap perubahan data dari lapisan layanan tersebut secara otomatis memperbarui seluruh komponen yang berlangganan (*subscribe*) *state* terkait tanpa intervensi manual. Kompleksitas aliran data ini memperkuat argumentasi bahwa SIMTA memerlukan strategi *lazy loading* yang berbeda dari aplikasi *Company Profile* yang tidak memiliki lapisan reaktivitas serumit ini.

## 2.7 Instrumen Pengumpulan Data

### 2.7.1 Instrumen Primer: W3C *PerformanceObserver*

*PerformanceObserver* adalah antarmuka bawaan browser yang menjadi standar resmi W3C untuk merekam metrik secara langsung tanpa menambah beban pada sistem. Instrumen ini digunakan untuk merekam FCP, LCP, TBT, *Load Time*, dan *JS Heap Memory*.

<div align="center">
  <img src="../chapters/images/mermaid_3.png" alt="Alur Eksekusi Instrumen Pelacakan API Peramban" width="380" />
  <br>
  <i>Gambar 2.6 Struktur kerja alat ukur performa bawaan browser (PerformanceObserver).</i>
</div>

Gambar 2.6 di atas memperlihatkan cara kerja instrumen pengukuran primer yang digunakan dalam penelitian ini. *PerformanceObserver* beroperasi secara pasif di dalam browser — ia tidak menambah beban proses karena browser sendiri yang mendorong *data entry* ke *callback observer* saat *event* terjadi. Pendekatan pengukuran ini lebih akurat dibandingkan *polling* manual atau alat eksternal karena data diambil langsung dari mesin pengukur internal browser, sehingga hasil yang diperoleh mencerminkan kondisi performa yang sesungguhnya dialami oleh pengguna akhir.

Pengukuran performa dilakukan menggunakan kombinasi W3C *PerformanceObserver* dan Puppeteer. Pendekatan ini dipilih karena: (1) *PerformanceObserver* mengukur metrik secara langsung dari dalam browser tanpa *overhead* eksternal, sehingga menghasilkan data yang lebih akurat dan *reproducible*; (2) Puppeteer memungkinkan otomasi pengujian yang konsisten dengan 5 repetisi per skenario dan simulasi *CPU throttling* yang terkontrol; dan (3) pengukuran tidak bergantung pada koneksi internet eksternal yang dapat menambahkan variabel jaringan yang tidak diinginkan. Kombinasi ini juga memungkinkan triangulasi data antara *PerformanceObserver* dan Lighthouse.

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

Sebagai pelengkap pengukuran *PerformanceObserver*, penelitian ini juga menggunakan Google Lighthouse v11.x untuk mengaudit performa secara standar industri. Lighthouse memberikan metrik tambahan yang penting: *Performance Score* (0-100), *Time to Interactive* (TTI), dan *Speed Index*. Penggunaan dua instrumen ini bertujuan untuk **triangulasi data** — memvalidasi hasil pengukuran dari satu instrumen dengan instrumen lainnya.

## 2.8 Skenario Pengujian

Pengujian dilakukan dalam dua kondisi menggunakan Puppeteer:

1. **Kondisi Normal:** Browser berjalan dengan kemampuan penuh tanpa hambatan. Berfungsi sebagai patokan awal.
2. **Kondisi Perangkat Lambat (CPU diperlambat 4x):** Kemampuan prosesor dibatasi hingga 4 kali lebih lambat, untuk mensimulasikan kondisi pengguna yang mengakses dari perangkat dengan spesifikasi rendah.

<div align="center">
  <img src="../chapters/images/mermaid_4.png" alt="Alur Logika Pengujian Otomasi" width="380" />
  <br>
  <i>Gambar 2.7 Alur pengujian otomatis dalam kondisi normal dan perangkat lambat.</i>
</div>

Gambar 2.7 di atas menggambarkan alur otomasi pengujian yang memastikan konsistensi dan reprodusibilitas data. Setiap skenario dijalankan 5 kali pengulangan pada dua kondisi berbeda, menghasilkan total 20 titik data per metrik per aplikasi. Penggunaan Puppeteer sebagai pengontrol browser mengeliminasi variabilitas yang muncul akibat interaksi manual, sementara percabangan kondisi Normal dan *CPU Throttled* 4x memungkinkan penelitian untuk mengisolasi dampak beban komputasi terhadap efektivitas strategi optimasi.

Pengujian dilakukan pada kondisi *CPU throttling* 4x melalui *Puppeteer Chromium API*. Kondisi ini dipilih karena: (1) *CPU throttling* lebih representatif untuk mengukur dampak *bundle* JavaScript yang besar, karena masalah utama terletak pada beban *parsing* dan eksekusi kode pada *Main Thread*, bukan latensi jaringan; (2) pengujian di *localhost* mengeliminasi variabel jaringan sehingga seluruh perbedaan yang terukur dapat diatribusikan murni pada strategi *code splitting*; dan (3) hasilnya lebih *reproducible* karena tidak bergantung pada kondisi ISP atau CDN. Untuk penelitian lanjutan, kombinasi *network throttling* dan *CPU throttling* direkomendasikan.

Setiap skenario dijalankan **5 kali** untuk memastikan konsistensi data. Dengan menggunakan alat otomasi, hasil pengujian menjadi lebih akurat dan konsisten karena tidak ada variasi dari perbedaan reaksi manusia.

---

# BAB III HASIL DAN PEMBAHASAN

## 3.1 Perbandingan Ukuran File Setelah Dikompilasi

Masalah utama yang ingin diselesaikan dalam penelitian ini berawal dari ukuran file yang terlalu besar. Pada versi standar (*Eager Load Baseline*), semua kode SIMTA digabung menjadi satu file JavaScript besar berukuran **346,53 KB** sebelum dikompresi. Sekitar **58% dari total ukuran *bundle*** berasal dari pustaka pihak ketiga (*vendor/third-party libraries*), dengan Chart.js mendominasi karena mengemas seluruh modul *renderer* grafik — termasuk modul yang tidak digunakan pada halaman awal — ke dalam satu kesatuan.

Kondisi ini menegaskan relevansi penerapan teknik *Code Splitting*. Apabila pustaka-pustaka besar tersebut berhasil dipisahkan ke dalam *chunk* terpisah dan hanya dimuat ketika halaman yang membutuhkannya diakses, beban unduhan awal dapat dikurangi secara substansial tanpa mengorbankan fungsionalitas aplikasi.

<div align="center">
  <img src="../chapters/images/mermaid_5.png" alt="Pie Chart Proporsi Bundel Size" width="550" />
  <br>
  <i>Gambar 3.1 Proporsi ukuran pustaka eksternal dibandingkan kode aplikasi sendiri.</i>
</div>

Gambar 3.1 di atas secara visual mengkonfirmasi temuan kuantitatif yang menjadi landasan penerapan *code splitting* dalam penelitian ini. Dominasi pustaka *vendor* — khususnya Chart.js yang menyumbang hampir sepertiga dari total ukuran *bundle* — menjelaskan mengapa strategi pemisahan *chunk* menjadi intervensi yang tepat sasaran.

Perlu diluruskan bahwa manfaat pemisahan Chart.js ke dalam *chunk* `vendor-chart.js` pada SIMTA **bukan** berasal dari menunda pengunduhannya sampai pengguna membuka halaman tertentu — halaman Dashboard yang menjadi rute pertama (`/`) sudah menampilkan grafik statistik sejak awal (lihat `DashboardView.vue` yang meng-*import* `ChartStatistik.vue`), sehingga `vendor-chart.js` tetap ikut diunduh pada kunjungan pertama. Manfaat nyatanya berasal dari tiga hal lain: (1) browser dapat mengunduh beberapa *chunk* kecil secara **paralel** alih-alih menunggu satu berkas besar selesai diunduh secara berurutan; (2) `vendor-chart.js` dan `vendor-vue.js` menjadi berkas yang dapat di-*cache* terpisah oleh browser, sehingga pembaruan kode aplikasi tidak memaksa pengunduhan ulang pustaka pihak ketiga; dan (3) pada skenario navigasi yang tidak dimulai dari Dashboard (misalnya *deep link* langsung ke `/pengaturan` melalui *hash routing*), `vendor-chart.js` tidak pernah diunduh sama sekali. Ketiga faktor inilah — bukan penundaan Chart.js secara spesifik — yang mendasari perbaikan metrik pemuatan yang diukur pada sub-bab berikutnya.

Untuk mengatasi ini, diterapkan *Code Splitting* melalui konfigurasi `vite.config.js`:

```javascript
/* vite.config.optimized.js - Implementasi Code Splitting (disederhanakan) */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
    compressAssets(), // plugin kustom: gzip + brotli dalam satu langkah, lihat teks di bawah
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('chart.js') || id.includes('vue-chartjs')) {
              return 'vendor-chart';
            }
            if (id.includes('vue') || id.includes('pinia')) {
              return 'vendor-vue';
            }
          }
        }
      }
    }
  }
})
```

Hasilnya, total ukuran JavaScript SIMTA versi *optimized* terpecah menjadi delapan berkas terpisah (`vendor-vue.js`, `vendor-chart.js`, lima *chunk* per halaman, dan satu *chunk* layanan data), dibandingkan satu berkas tunggal 346,53 KB pada *baseline*. Pemisahan ini membuka jalan bagi dua teknik tambahan yang diuji pada penelitian ini: **kompresi Brotli/Gzip** dan **prefetching**, keduanya dibahas di bawah.

**Kompresi Brotli dan Gzip.** Setiap *chunk* hasil pemecahan dikompresi otomatis saat build melalui plugin kustom pada `vite.config.optimized.js` (`compressAssets`), menghasilkan varian `.gz` dan `.br` di samping berkas asli. Sebagai contoh, `vendor-vue.js` (103,40 KB mentah) mengecil menjadi 39,89 KB (Gzip) dan lebih kecil lagi dengan Brotli; `vendor-chart.js` (199,59 KB mentah) mengecil menjadi 68,18 KB (Gzip). Server pengujian (`http-server`) diaktifkan untuk menyajikan varian terkompresi ini sesuai *header* `Accept-Encoding` peramban (*flag* `-g -b`), sehingga manfaat kompresi benar-benar terukur pada metrik jaringan di sub-bab berikutnya — bukan sekadar tersedia sebagai berkas yang tidak pernah diminta peramban.

---

## 3.2 Penerapan Lazy Loading dan Prefetching pada Navigasi

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

**Kelemahan yang muncul dari lazy loading.** Meskipun berhasil menekan ukuran *bundle* awal, pendekatan ini memunculkan konsekuensi baru yang perlu diantisipasi. Pada *lazy loading* murni, berkas JavaScript sebuah halaman baru mulai diunduh tepat pada saat pengguna menekan menu navigasi. Akibatnya, beban yang semula ditanggung sekali di awal kini terpecah menjadi jeda-jeda kecil pada setiap perpindahan halaman: pengguna menekan menu, lalu menunggu *chunk* halaman tersebut selesai diunduh dan dieksekusi sebelum antarmuka benar-benar berganti. Pada jaringan lambat maupun perangkat berspesifikasi rendah, jeda ini dapat cukup terasa dan justru mengurangi kesan responsif yang ingin dicapai. Dengan kata lain, *code splitting* dan *lazy loading* berhasil memperkecil beban muat awal, tetapi memindahkan sebagian biaya tersebut ke waktu navigasi antar-halaman.

**Prefetching sebagai penutup celah jeda navigasi.** Untuk mengatasi kelemahan tersebut, router versi *optimized* tidak berhenti pada *lazy loading*, melainkan melengkapinya dengan strategi *prefetching*. Prinsipnya sederhana: alih-alih menunggu pengguna menekan menu, aplikasi memanfaatkan waktu senggang peramban untuk mengunduh lebih awal halaman yang kemungkinan besar dituju berikutnya. Pada SIMTA, setelah navigasi ke Dashboard selesai, `router.afterEach` menjadwalkan pengunduhan `DaftarJudulView.vue` dan `DetailBimbinganView.vue` di latar belakang melalui `requestIdleCallback` (dengan `setTimeout` sebagai *fallback*).

```javascript
router.afterEach((to) => {
  if (to.name === 'Dashboard') {
    const prefetch = () => {
      import('../views/DaftarJudulView.vue')
      import('../views/DetailBimbinganView.vue')
    }
    if ('requestIdleCallback' in window) requestIdleCallback(prefetch)
    else setTimeout(prefetch, 1000)
  }
})
```

Dengan cara ini, ketika pengguna benar-benar menekan menu Daftar Judul, berkasnya sudah tersedia di *cache* peramban sehingga perpindahan halaman terasa seketika — jeda yang menjadi kelemahan *lazy loading* murni dapat ditekan tanpa mengorbankan keunggulan *bundle* awal yang kecil. Karena dijadwalkan lewat `requestIdleCallback`, pengunduhan ini hanya berjalan saat *main thread* sedang senggang, sehingga tidak menunda konten yang sedang ditampilkan. Bukti bahwa mekanisme ini benar-benar berjalan pada aplikasi yang diuji disajikan pada Sub-bab 3.9.


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

Pada aplikasi SIMTA dalam kondisi ideal (*no throttling*), versi *baseline* menampilkan konten visual pertama dalam waktu rata-rata **1103,2 ms** (SD = 179,4), sedangkan versi yang telah dioptimasi mencatatkan waktu **842,4 ms** (SD = 20,0). Selisih sebesar 260,8 ms ini merepresentasikan perbaikan **23,6%**, yang secara teknis disebabkan oleh berkurangnya volume JavaScript yang harus diunduh dan di-*parse* oleh mesin V8 sebelum browser dapat melakukan *first paint*, ditambah manfaat kompresi Brotli/Gzip yang mengecilkan ukuran transfer setiap *chunk*.

Pada aplikasi *Company Profile*, versi *baseline* mencatat FCP sebesar **511,2 ms** (SD = 31,7) dan versi optimasi **483,2 ms** (SD = 18,8) — perbaikan kecil sebesar **5,5%**. Selisih ini jauh lebih tipis dibanding SIMTA, mengindikasikan bahwa pada aplikasi dengan kompleksitas rendah — di mana *bundle* JavaScript sejak awal sudah berukuran kecil dan tidak mengandung pustaka berat — penerapan *Code Splitting* tidak memberikan kontribusi sebesar pada aplikasi kompleks terhadap percepatan FCP.

<div align="center">
  <img src="../chapters/images/chart_fcp_comparison.png" alt="Grafik FCP" width="550" />
  <br>
  <i>Gambar 3.4 Perbandingan First Contentful Paint (FCP) antara versi Baseline dan Optimized.</i>
</div>

Gambar 3.4 di atas memvisualisasikan perbedaan FCP yang terjadi akibat penerapan *code splitting*, *lazy loading*, dan kompresi. Pada SIMTA, penurunan FCP sebesar 23,6% (dari 1103,2 ms menjadi 842,4 ms) terjadi karena berkurangnya volume JavaScript yang harus di-*parse* oleh mesin V8 sebelum browser dapat melakukan *first paint*, ditambah transfer *chunk* yang lebih kecil berkat kompresi. Sementara itu, perbedaan pada *Company Profile* jauh lebih tipis (511,2 ms vs 483,2 ms, perbaikan 5,5%), yang mengindikasikan bahwa manfaat *code splitting* terhadap FCP jauh lebih terasa ketika *bundle* awal sudah cukup besar untuk menyebabkan keterlambatan *parsing* dan transfer yang terukur.

**Tabel 3.1 Ringkasan FCP — Kondisi Normal (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Aplikasi | Baseline (ms) | Optimized (ms) | Selisih |
|----------|---------------|----------------|---------|
| SIMTA | 1103,2 ± 179,4 | 842,4 ± 20,0 | -260,8 ms (-23,6%) |
| Company Profile | 511,2 ± 31,7 | 483,2 ± 18,8 | -28,0 ms (-5,5%) |

### 3.4.2 Perbandingan Total Blocking Time (TBT)

Pada SIMTA dalam kondisi ideal, versi *baseline* mencatatkan TBT sebesar **139,2 ms** (SD = 77,0), sementara versi yang telah dioptimasi mencatatkan angka lebih rendah yaitu **104,6 ms** (SD = 34,6) — perbaikan 24,9%. Kedua nilai ini masih berada di bawah ambang batas 200 ms yang ditetapkan oleh standar *Core Web Vitals*, sehingga tidak terlalu terasa oleh pengguna akhir pada kondisi perangkat yang mumpuni. Dampak sesungguhnya dari teknik optimasi ini terlihat jauh lebih jelas pada skenario CPU yang diperlambat.

<div align="center">
  <img src="../chapters/images/chart_tbt_comparison.png" alt="Grafik TBT" width="550" />
  <br>
  <i>Gambar 3.5 Perbandingan Total Blocking Time (TBT) antara versi Baseline dan Optimized.</i>
</div>

Gambar 3.5 di atas memperlihatkan TBT SIMTA versi *optimized* konsisten lebih rendah dibanding *baseline*, baik pada kondisi normal (104,6 ms vs 139,2 ms) maupun — seperti akan ditunjukkan pada sub-bab berikutnya — pada kondisi CPU diperlambat. Kedua nilai pada kondisi normal masih berada di bawah ambang batas 200 ms *Core Web Vitals*. Pada *Company Profile*, TBT tercatat 0 ms pada kedua versi, mengkonfirmasi bahwa *bundle* yang sudah kecil tidak menghasilkan *blocking time* yang terukur pada kondisi ideal.

**Tabel 3.2 Ringkasan TBT — Kondisi Normal (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Aplikasi | Baseline (ms) | Optimized (ms) | Selisih | % |
|----------|---------------|----------------|---------|---|
| SIMTA | 139,2 ± 77,0 | 104,6 ± 34,6 | -34,6 ms | -24,9% |
| Company Profile | 0,0 ± 0,0 | 0,0 ± 0,0 | 0,0 ms | 0% |

---

## 3.5 Hasil Pengujian: Instrumen PerformanceObserver (CPU Diperlambat 4x)

Inilah pengujian yang paling penting — mensimulasikan pengguna yang mengakses SIMTA dari perangkat dengan spesifikasi rendah. Simulasi dilakukan dengan *CPU throttling* 4x melalui *Puppeteer Chromium API*, sehingga seluruh tahapan pemrosesan JavaScript (*parsing*, *JIT compilation*, *execution*) membutuhkan waktu 4x lebih lama dari kondisi normal.

### 3.5.1 Perbandingan Total Waktu Muat (Load Time)

Pada SIMTA, waktu muat versi *baseline* meningkat dari 694,2 ms (kondisi ideal) menjadi **1121,6 ms** (SD = 218,5), sedangkan versi optimasi meningkat dari 688,6 ms menjadi **975,8 ms** (SD = 45,5). Perbedaan antara kedua versi pada kondisi *throttled* menunjukkan perbaikan sebesar 13,0%. Untuk *Company Profile*, versi optimasi juga menghasilkan *Load Time* yang lebih cepat (106,0 ms vs 140,4 ms pada *baseline*), dengan perbaikan sebesar 24,5%.

<div align="center">
  <img src="../chapters/images/chart_loadtime_comparison.png" alt="Grafik Load Time" width="550" />
  <br>
  <i>Gambar 3.6 Perbandingan total waktu muat pada kondisi perangkat lambat (CPU 4x).</i>
</div>

Gambar 3.6 di atas menampilkan perbandingan *Load Time* pada kondisi CPU yang diperlambat 4x — skenario yang paling merepresentasikan kondisi pengguna dengan perangkat rendah. Penurunan *Load Time* pada SIMTA sebesar 13,0% (dari 1121,6 ms menjadi 975,8 ms) berasal dari kombinasi *code splitting*, *lazy loading*, dan kompresi Brotli/Gzip yang kini benar-benar aktif tersaji ke peramban. *Company Profile* turut membaik sebesar 24,5%, murni dari *code splitting* dan *lazy loading* — perlu dicatat bahwa konfigurasi *build Company Profile* tidak menyertakan kompresi Brotli/Gzip, sehingga perbaikannya tidak dapat dikaitkan dengan kompresi.

### 3.5.2 Perbandingan TBT pada Kondisi Throttled

**Tabel 3.3 Metrik Kunci SIMTA — Kondisi CPU Diperlambat 4x (Rata-rata ± Standar Deviasi, 5 Repetisi)**

| Metrik (SIMTA) | Baseline (CPU Lambat) | Optimized (CPU Lambat) | |
|----------------|----------------------|------------------------|---|
| **FCP** | 1371,2 ± 49,4 ms | 1134,4 ± 47,1 ms | ↑ |
| **TBT** | **710,4 ± 89,2 ms** | **579,0 ± 63,1 ms** | ↑ |

**Analisis:** Nilai TBT pada versi standar yang mencapai **710,4 ± 89,2 ms** sudah melampaui batas toleransi Google Web Vitals (300 ms). Dengan *Code Splitting*, *Lazy Loading*, dan kompresi, nilai TBT turun menjadi **579,0 ± 63,1 ms** — meskipun masih di atas batas ideal, sudah menunjukkan perbaikan signifikan sebesar **18,5%** bagi pengguna perangkat rendah.

**Tabel 3.4 Ringkasan Seluruh Metrik PerformanceObserver — SIMTA (Rata-rata ± SD, 5 Repetisi)**

| Metrik | Baseline Normal | Optimized Normal | Baseline Throttled | Optimized Throttled |
|--------|----------------|------------------|--------------------|---------------------|
| FCP (ms) | 1103,2 ± 179,4 | 842,4 ± 20,0 | 1371,2 ± 49,4 | 1134,4 ± 47,1 |
| LCP (ms) | 1103,2 ± 179,4 | 842,4 ± 20,0 | 1371,2 ± 49,4 | 1134,4 ± 47,1 |
| TBT (ms) | 139,2 ± 77,0 | 104,6 ± 34,6 | 710,4 ± 89,2 | 579,0 ± 63,1 |
| Load Time (ms) | 694,2 ± 22,2 | 688,6 ± 17,6 | 1121,6 ± 218,5 | 975,8 ± 45,5 |
| JS Heap (MB) | 5,09 ± 0,42 | 5,40 ± 0,08 | 4,81 ± 0,13 | 4,92 ± 0,12 |

**Tabel 3.5 Ringkasan Seluruh Metrik PerformanceObserver — Company Profile (5 Repetisi)**

| Metrik | Baseline Normal | Optimized Normal | Baseline Throttled | Optimized Throttled |
|--------|----------------|------------------|--------------------|---------------------|
| FCP (ms) | 511,2 ± 31,7 | 483,2 ± 18,8 | 508,0 ± 15,2 | 508,8 ± 22,4 |
| LCP (ms) | 511,2 ± 31,7 | 483,2 ± 18,8 | 508,0 ± 15,2 | 508,8 ± 22,4 |
| TBT (ms) | 0,0 ± 0,0 | 0,0 ± 0,0 | 66,6 ± 4,4 | 7,6 ± 4,6 |
| Load Time (ms) | 58,8 ± 7,6 | 45,2 ± 5,5 | 140,4 ± 7,4 | 106,0 ± 13,6 |
| JS Heap (MB) | 1,87 ± 0,00 | 1,90 ± 0,00 | 1,88 ± 0,02 | 1,90 ± 0,00 |

Perlu dicatat: berbeda dengan pengukuran sebelumnya yang menunjukkan FCP *Company Profile* memburuk cukup besar pada kondisi *throttled*, pengukuran ulang ini menunjukkan FCP baseline (508,0 ms) dan optimized (508,8 ms) **praktis tidak berbeda** — selisih 0,8 ms berada jauh di dalam rentang simpangan baku kedua kelompok. Ini mengindikasikan bahwa pada aplikasi sesederhana *Company Profile*, dengan skala waktu muat yang sangat kecil (ratusan milidetik), pengukuran berbasis *PerformanceObserver* dari satu sesi 5 repetisi rentan terhadap variasi kondisi mesin pengujian (proses latar belakang, *thermal throttling*, dsb.), sehingga sulit dijadikan dasar klaim persentase yang presisi. Sub-bab 3.8 membahas hal ini lebih lanjut menggunakan data Lighthouse yang terbukti lebih stabil pada aplikasi ini (simpangan baku mendekati nol, lihat Tabel 3.7).

---

## 3.6 Hasil Pengujian: Instrumen Google Lighthouse

Sebagai triangulasi data, berikut hasil pengukuran menggunakan Google Lighthouse. Perlu dicatat bahwa Lighthouse melakukan simulasi perangkat *mobile* kelas menengah secara internal dengan menerapkan *CPU slowdown* dan *network throttling* tersendiri — berbeda dari kondisi pengujian *PerformanceObserver* yang dijalankan pada lingkungan *localhost* tanpa simulasi jaringan. Perbedaan metodologi pengukuran inilah yang menyebabkan nilai absolut FCP dan LCP pada Lighthouse jauh lebih tinggi dibandingkan hasil *PerformanceObserver* (misalnya FCP Lighthouse 4960 ms vs FCP PerformanceObserver 1103 ms).

<div align="center">
  <img src="../chapters/images/chart_lighthouse_score.png" alt="Grafik Lighthouse Performance Score" width="550" />
  <br>
  <i>Gambar 3.7 Perbandingan Lighthouse Performance Score antara versi Baseline dan Optimized.</i>
</div>

Gambar 3.7 di atas menunjukkan bahwa *Lighthouse Performance Score* SIMTA naik cukup besar dari *baseline* ke *optimized* (56,8 menjadi 75,0, kenaikan 32,0%), sementara *Company Profile* nyaris tidak berubah (100 menjadi 99). Pola ini konsisten dengan hipotesis utama penelitian: manfaat *code splitting* dan *lazy loading* jauh lebih terasa pada aplikasi kompleks dengan pustaka berat, dan nyaris tidak berpengaruh pada aplikasi yang *bundle* awalnya sudah kecil.

**Tabel 3.6 Hasil Lighthouse — SIMTA (Mean ± SD, 5 Repetisi)**

| Metrik | Baseline | Optimized | Selisih |
|--------|----------------|---------------------|---------|
| Performance Score | 56,8 ± 4,2 | 75,0 ± 13,3 | +18,2 (+32,0%) |
| FCP (ms) | 4960,4 ± 56,4 | 3250,2 ± 404,6 | -1710,2 (-34,5%) |
| LCP (ms) | 5228,4 ± 60,6 | 3790,8 ± 774,3 | -1437,6 (-27,5%) |
| TTI (ms) | 5566,8 ± 181,9 | 3964,0 ± 918,3 | -1602,8 (-28,8%) |
| TBT (ms) | 454,8 ± 152,0 | 315,4 ± 241,5 | -139,4 (-30,6%) |
| Speed Index | 4960,4 ± 56,4 | 3265,2 ± 386,8 | -1695,2 (-34,2%) |

**Interpretasi Hasil Lighthouse SIMTA:** Berbeda dengan dugaan awal bahwa *lazy loading* akan memperlambat metrik berbasis *loading* (FCP, LCP, TTI) sebagai *trade-off* dari eksekusi modul yang bertahap, hasil pengukuran menunjukkan **seluruh metrik Lighthouse membaik** pada versi *optimized* — termasuk FCP, LCP, dan TTI yang pada pengukuran sebelumnya (sebelum kompresi Brotli/Gzip diperbaiki agar benar-benar tersaji ke peramban) sempat terlihat memburuk. Setelah kompresi berfungsi sebagaimana mestinya, ukuran transfer setiap *chunk* mengecil cukup jauh sehingga manfaat *code splitting* tidak lagi tertutupi oleh biaya tambahan *request* jaringan per *chunk*. Simpangan baku pada versi *optimized* (misalnya TBT 315,4 ± 241,5 ms) juga jauh lebih besar dibanding *baseline* — ini wajar karena Lighthouse mengukur seluruh rangkaian pemuatan modul dinamis yang waktunya lebih bervariasi dibanding satu berkas monolitik, namun rata-ratanya tetap menunjukkan perbaikan yang jelas.

<div align="center">
  <img src="../chapters/images/chart_lighthouse_tti.png" alt="Grafik Lighthouse TTI" width="550" />
  <br>
  <i>Gambar 3.8 Perbandingan Lighthouse Time to Interactive (TTI) antara SIMTA dan Company Profile.</i>
</div>

Gambar 3.8 di atas memperlihatkan TTI SIMTA membaik dari 5566,8 ms menjadi 3964,0 ms (28,8%) — sejalan dengan perbaikan pada FCP, LCP, TBT, dan Speed Index. Artinya, pada SIMTA, optimasi tidak hanya membuat halaman lebih responsif terhadap klik (TBT turun), tetapi juga membuat *main thread* lebih cepat mencapai kondisi benar-benar bebas dan interaktif secara keseluruhan.

**Tabel 3.7 Hasil Lighthouse — Company Profile (Mean ± SD, 5 Repetisi)**

| Metrik | Baseline | Optimized | Selisih |
|--------|----------------|---------------------|---------|
| Performance Score | 100,0 ± 0,0 | 99,0 ± 0,0 | -1,0 |
| FCP (ms) | 1361,4 ± 16,8 | 1578,2 ± 1,0 | +216,8 (+15,9%) |
| LCP (ms) | 1528,8 ± 8,2 | 1804,4 ± 1,4 | +275,6 (+18,0%) |
| TTI (ms) | 1530,6 ± 7,4 | 1804,4 ± 1,4 | +273,8 (+17,9%) |
| TBT (ms) | 0,0 ± 0,0 | 0,0 ± 0,0 | 0,0 |
| Speed Index | 1361,4 ± 16,8 | 1578,2 ± 1,0 | +216,8 (+15,9%) |

Berbeda dengan SIMTA, hasil Lighthouse *Company Profile* tetap menunjukkan sedikit degradasi FCP/LCP/TTI pada versi *optimized* — pola ini konsisten baik sebelum maupun sesudah perbaikan kompresi dan pengukuran ulang (dengan simpangan baku yang sangat kecil, menandakan hasil ini stabil dan bukan kebetulan). Penyebabnya adalah *overhead* tambahan berupa beberapa kali *request* HTTP untuk *chunk* yang terpisah, yang pada aplikasi sekecil *Company Profile* — tanpa pustaka berat yang perlu dipisahkan — tidak sebanding dengan manfaatnya.

---

## 3.7 Penggunaan Memori Browser

Grafik perbandingan JS Heap Memory menampilkan konsumsi memori *runtime* dari keempat skenario pengujian. Pada kondisi ideal, versi *baseline* SIMTA mengalokasikan rata-rata **5,09 MB** (SD = 0,42) di *heap* memori JavaScript, sedangkan versi optimasi menggunakan **5,40 MB** (SD = 0,08) — tambahan 0,31 MB. Pada kondisi CPU diperlambat, polanya konsisten: *baseline* 4,81 MB (SD = 0,13) vs *optimized* 4,92 MB (SD = 0,12), tambahan 0,11 MB. Pertambahan memori kecil dan konsisten pada versi optimasi ini bersumber dari penyimpanan referensi *callback function* untuk setiap modul yang dijadwalkan melalui *dynamic import*, termasuk dua modul yang dijadwalkan lewat mekanisme *prefetching* (Sub-bab 3.2).

<div align="center">
  <img src="../chapters/images/chart_memory_comparison.png" alt="Grafik Memori" width="550" />
  <br>
  <i>Gambar 3.9 Perbandingan penggunaan memori browser (JS Heap) antara semua skenario.</i>
</div>

Gambar 3.9 di atas mengkonfirmasi bahwa penerapan *code splitting* tidak menambah beban memori yang signifikan. Perbedaan *JS Heap* antara *baseline* dan *optimized* pada semua skenario SIMTA berada di bawah 0,35 MB — jauh lebih kecil dari manfaat pengurangan TBT yang diperoleh (18,5%–24,9%, Sub-bab 3.4–3.5). Dengan demikian, *trade-off* antara sedikit tambahan memori dan penurunan TBT yang jauh lebih besar tetap menguntungkan, dan implementasi *hybrid lazy loading* dapat direkomendasikan tanpa kekhawatiran terhadap konsumsi memori berlebih.

---

## 3.8 Perbandingan Dampak pada SIMTA vs Company Profile

Analisis komparatif antara SIMTA dan *Company Profile* menghasilkan temuan yang memperkuat hipotesis utama penelitian ini tentang pengaruh tingkat kompleksitas terhadap efektivitas strategi optimasi — dengan satu catatan metodologis penting yang perlu disampaikan secara jujur.

Pada *Company Profile* dalam kondisi CPU yang diperlambat, nilai TBT versi *baseline* tercatat sebesar **66,6 ms** (SD = 4,4), yang masih berada jauh di bawah ambang batas 200 ms standar *Core Web Vitals*. Setelah diterapkan *Code Splitting*, nilai TBT turun menjadi **7,6 ms** (SD = 4,6) — penurunan sebesar 88,6%. Sebagaimana SIMTA (18,5%–24,9%, Sub-bab 3.4–3.5), TBT *Company Profile* juga konsisten membaik, meski nilai awalnya sudah tergolong baik sehingga dampak praktis bagi pengguna jauh lebih kecil dibanding SIMTA yang TBT *baseline*-nya (710,4 ms) sudah melampaui batas toleransi secara drastis.

**Catatan metodologis mengenai FCP *Company Profile*.** Pengukuran awal penelitian ini pada kondisi *throttled* sempat mencatat FCP *baseline* 373,6 ms dan *optimized* 486,4 ms — memberi kesan *code splitting* men-degradasi FCP sebesar 30,2% pada aplikasi sederhana. Pengukuran ulang dengan metodologi yang telah diperbaiki (lihat Lampiran) mencatat FCP *baseline* 508,0 ms dan *optimized* 508,8 ms — **praktis tidak berbeda** (selisih 0,8 ms, jauh di dalam rentang simpangan baku ±15–22 ms kedua kelompok). Perbedaan tajam antara dua pengukuran ini menunjukkan bahwa pada aplikasi sesederhana *Company Profile*, dengan skala waktu muat hanya ratusan milidetik, *PerformanceObserver* dari satu sesi 5 repetisi terlalu rentan terhadap variasi kondisi mesin pengujian untuk dijadikan dasar klaim persentase yang presisi — sebuah ancaman terhadap validitas internal yang perlu diakui secara terbuka.

Bukti yang lebih dapat diandalkan datang dari Lighthouse (Tabel 3.7), yang simpangan bakunya jauh lebih kecil (mendekati 0 pada beberapa metrik) dan **konsisten pada dua kali pengukuran terpisah**: FCP *Company Profile* memburuk sekitar 15,9%–16,7% dan LCP sekitar 18,0%–17,9% pada versi *optimized*, baik sebelum maupun sesudah pengukuran ulang. Kesimpulan bahwa *code splitting* dapat memberi *overhead* kecil pada aplikasi sederhana **tetap didukung data**, tetapi bersandar pada bukti Lighthouse yang stabil — bukan pada angka 30,2% dari *PerformanceObserver* yang ternyata tidak *reproducible*.

**Tabel 3.8 Perbandingan Improvement antara SIMTA dan Company Profile (Kondisi CPU Throttled)**

| Metrik | Instrumen | SIMTA Improvement | CP Improvement | Keterangan |
|--------|-----------|-------------------|-----------------|------------|
| FCP | PerformanceObserver | +17,3% | -0,2% (~0, dalam noise) | SIMTA membaik jelas; CP tidak berbeda signifikan |
| FCP | Lighthouse | +34,5% | -15,9% (memburuk) | SIMTA membaik jelas; CP sedikit memburuk (stabil, SD kecil) |
| TBT | PerformanceObserver | +18,5% | +88,6% | Keduanya membaik (CP dari baseline yang sudah baik) |
| Load Time | PerformanceObserver | +13,0% | +24,5% | Keduanya membaik |
| JS Heap | PerformanceObserver | -2,3% (overhead) | -1,1% (overhead) | Overhead memori minimal, konsisten kecil |
| LH Score | Lighthouse | +32,0% | -1,0% | SIMTA naik besar; CP nyaris tidak berubah |

Kesimpulan dari tabel ini: **teknik *hybrid code splitting* + *lazy loading* + kompresi sangat efektif untuk aplikasi yang kompleks dan banyak menggunakan pustaka besar** (naik di semua metrik, termasuk Lighthouse Score +32,0%), **tetapi manfaatnya tipis — dan pada metrik Lighthouse yang stabil justru sedikit negatif pada FCP/LCP — untuk aplikasi sederhana** seperti *Company Profile*. Rekomendasi strategis tidak berubah: terapkan *code splitting* dan *lazy loading* hanya ketika *bundle* awal sudah melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak dibutuhkan di halaman utama; untuk aplikasi yang *bundle*-nya sudah kecil, biaya tambahan berupa beberapa kali *request* HTTP per *chunk* tidak sebanding dengan manfaatnya.

---

## 3.9 Verifikasi Mekanisme Prefetching

Sub-bab 3.2 menjelaskan bahwa *prefetching* ditambahkan untuk menutup kelemahan *lazy loading*, yaitu munculnya jeda pada setiap perpindahan halaman. Bagian ini menyajikan bukti bahwa mekanisme tersebut benar-benar berjalan pada aplikasi yang diuji, mulai dari perbandingan konsep, struktur *chunk* hasil *build*, hingga rekaman permintaan berkas yang sesungguhnya terjadi di peramban.

<div align="center">
  <img src="../chapters/images/diagram_strategi_pemuatan.png" alt="Perbandingan tiga strategi pemuatan" width="620" />
  <br>
  <i>Gambar 3.10 Perbandingan konseptual tiga strategi pemuatan modul.</i>
</div>

Gambar 3.10 di atas membandingkan tiga strategi secara berdampingan. Pada *eager loading*, seluruh kode diunduh sekaligus di awal sehingga perpindahan halaman memang terasa instan, tetapi beban pemuatan awal menjadi besar. Pada *lazy loading* murni, beban awal berhasil diperkecil, namun setiap klik menu memunculkan jeda karena *chunk* halaman baru diunduh pada saat itu juga. Strategi ketiga, yaitu *lazy loading* yang dilengkapi *prefetching*, mempertahankan *bundle* awal yang kecil sekaligus menghilangkan jeda tersebut dengan memindahkan pengunduhan ke waktu senggang peramban.

<div align="center">
  <img src="../chapters/images/diagram_arsitektur_chunk.png" alt="Peta chunk hasil build" width="620" />
  <br>
  <i>Gambar 3.11 Peta chunk hasil build SIMTA versi optimized beserta waktu pemuatannya.</i>
</div>

Gambar 3.11 di atas memetakan sembilan *chunk* hasil *build* ke dalam tiga kelompok berdasarkan kapan masing-masing diunduh. Kelompok pertama berisi berkas yang dibutuhkan halaman pertama dengan total **120,1 KB** setelah dikompresi. Kelompok kedua berisi dua *chunk* yang dijadwalkan melalui *prefetching*, hanya **5,4 KB** terkompresi — biaya yang sangat kecil dibanding beban pemuatan awal. Kelompok ketiga berisi *chunk* yang sengaja tidak di-*prefetch* dan baru diunduh apabila rutenya benar-benar diakses, sehingga *prefetching* tetap bersifat selektif dan tidak mengembalikan aplikasi ke pola *eager loading*.

<div align="center">
  <img src="../chapters/images/chart_prefetch_network.png" alt="Rekaman permintaan berkas JavaScript" width="620" />
  <br>
  <i>Gambar 3.12 Rekaman permintaan berkas JavaScript pada versi optimized tanpa interaksi klik (rata-rata 5 repetisi).</i>
</div>

Gambar 3.12 di atas merupakan rekaman permintaan berkas yang sesungguhnya terjadi ketika aplikasi dibuka lalu dibiarkan tanpa satu pun klik. Terlihat tiga tahap yang berurutan: berkas *entry* beserta `vendor-vue.js` dan `vendor-chart.js` diminta pada milidetik-milidetik pertama, `DashboardView.js` sebagai rute pembuka menyusul pada sekitar 129 ms, kemudian `DaftarJudulView.js` dan `DetailBimbinganView.js` diunduh pada sekitar 351 ms. Dua berkas terakhir inilah buktinya: keduanya masuk ke *cache* peramban meskipun menunya tidak pernah ditekan. Sebaliknya, `JadwalSeminarView.js` dan `PengaturanView.js` sama sekali tidak diminta, yang menunjukkan bahwa *prefetching* bekerja secara terarah pada rute yang diprediksi paling sering dituju, bukan mengunduh seluruh halaman tanpa pandang bulu. Rekaman ini dihasilkan oleh skrip `ukur_prefetch.cjs` dan datanya tersimpan pada `data_pengukuran/prefetch_network_log.json`.

---

# BAB IV PENUTUP

## 4.1 Kesimpulan

Berdasarkan hasil penelitian yang telah dilakukan pada dua model *Single Page Application* (SPA) — Sistem Informasi Manajemen Tugas Akhir (SIMTA) sebagai aplikasi kompleksitas tinggi, dan *Company Profile* sebagai aplikasi kompleksitas rendah — dengan menggunakan kombinasi instrumen pengukuran *W3C PerformanceObserver* dan Google Lighthouse, penelitian ini mengerucut pada kesimpulan berikut:

1. **Efektivitas *Code Splitting* dan kompresi dalam mengurangi beban muat awal (SIMTA).**
   Dengan memisahkan pustaka-pustaka besar (Vue/Pinia dan Chart.js) ke dalam *chunk* terpisah menggunakan fitur `manualChunks` di Vite, ditambah kompresi Brotli/Gzip pada setiap *chunk*, ukuran transfer jaringan berkurang signifikan dibanding satu berkas monolitik 346 KB pada *baseline*. Manfaatnya bukan dari menunda pengunduhan Chart.js — Dashboard sebagai halaman pertama tetap menampilkan grafik sejak awal — melainkan dari pengunduhan paralel beberapa *chunk* kecil dan ukuran transfer yang lebih kecil berkat kompresi.

2. ***Hybrid Lazy Loading*, *Code Splitting*, dan kompresi efektif mengurangi *Total Blocking Time* (TBT) tanpa *trade-off* berarti pada metrik lain.**
   Seluruh metrik yang diukur pada SIMTA — FCP, LCP, TTI, *Speed Index*, dan TBT — membaik pada versi *optimized*, baik lewat *PerformanceObserver* maupun Lighthouse. TBT turun 18,5%–24,9% menurut *PerformanceObserver* dan 30,6% menurut Lighthouse; Lighthouse Performance Score naik 32,0% (56,8 menjadi 75,0). Tidak ditemukan indikasi bahwa mekanisme pemuatan bertahap memperlambat metrik *loading* lain pada aplikasi ini.

3. **Manfaat terbesar terlihat pada perangkat dengan spesifikasi rendah.**
   Ketika diuji pada kondisi CPU diperlambat 4x, TBT SIMTA yang awalnya 710,4 ms (melampaui batas toleransi 300 ms) berhasil diturunkan menjadi 579,0 ms — perbaikan 18,5%. Ini berarti pengguna dengan perangkat lama yang mengakses SIMTA mengalami periode browser tidak responsif yang lebih singkat.

4. **_Prefetching_ diperlukan untuk menutup kelemahan bawaan _lazy loading_.**
   *Code splitting* dan *lazy loading* berhasil memperkecil beban muat awal, tetapi memindahkan sebagian biayanya ke waktu navigasi: setiap kali pengguna berpindah halaman, *chunk* halaman tersebut baru mulai diunduh saat itu juga. Untuk itu penelitian ini melengkapinya dengan *prefetching* berbasis `requestIdleCallback`, yang mengunduh halaman yang kemungkinan besar dituju berikutnya pada saat *main thread* sedang senggang. Dengan demikian keunggulan *bundle* awal yang kecil tetap dipertahankan tanpa memindahkan beban jeda ke pengalaman navigasi pengguna.

5. **Teknik ini tidak cocok untuk semua jenis website (*Diminishing Returns*).**
   Pada *Company Profile* (website sederhana), data Lighthouse yang stabil (simpangan baku mendekati nol, konsisten pada dua kali pengukuran terpisah) menunjukkan FCP dan LCP sedikit memburuk (masing-masing sekitar 16% dan 18%) pada versi *optimized*, akibat *overhead* beberapa *request* HTTP tambahan untuk *chunk* yang terpisah — biaya yang tidak sebanding pada aplikasi tanpa pustaka berat. (Pengukuran awal sempat mencatat degradasi FCP hingga 30,2% lewat *PerformanceObserver*; pengukuran ulang menunjukkan angka tersebut tidak *reproducible* pada instrumen itu — lihat catatan metodologis di Sub-bab 3.8 — sehingga kesimpulan ini disandarkan pada bukti Lighthouse yang terbukti stabil.) Penelitian ini membuktikan bahwa strategi optimasi harus mempertimbangkan tingkat kompleksitas aplikasi sebagai faktor penentu. Panduan praktis: terapkan *code splitting* hanya jika *bundle* awal sudah melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak digunakan di halaman pertama.

## 4.2 Saran untuk Penelitian Selanjutnya

1. **Integrasi dengan teknologi *Progressive Web App* (PWA):**
   File-file yang sudah diunduh bisa disimpan secara permanen di *cache* browser menggunakan *Service Workers*, sehingga pengguna yang membuka kembali website tidak perlu mengunduh file apa pun.

2. **Pengujian dengan *network throttling*:**
   Penelitian ini fokus pada *CPU throttling*. Penelitian lanjutan dapat menambahkan variabel *network throttling* (3G, 4G) untuk melihat dampak gabungan antara keterbatasan CPU dan jaringan, sesuai dengan rencana awal yang tercantum dalam proposal.

3. **Perbandingan dengan *Server-Side Rendering* (SSR):**
   Penelitian berikutnya bisa membandingkan apakah kerangka kerja SSR seperti Nuxt.js menghasilkan nilai FCP dan TBT yang lebih baik, karena HTML dikirimkan sudah matang dari server.

4. **Penanganan animasi yang berjalan terus-menerus:**
   Teknik `requestIdleCallback` yang digunakan untuk *prefetching* mungkin tidak bekerja optimal ketika halaman menampilkan animasi konstan. Penelitian lanjutan perlu mengembangkan mekanisme yang lebih cerdas.

5. **Penggunaan *Machine Learning* untuk *automated code splitting*:**
   Penelitian lanjutan dapat mengeksplorasi penggunaan *machine learning* untuk memprediksi *chunk grouping* yang optimal berdasarkan pola navigasi pengguna.

---

# DAFTAR PUSTAKA

Anggraeni, O. S. I., Sugiarto, L., & Agustin, T. (2024). "Studi Komparatif Performa Framework Javascript Modern dalam Pengembangan Aplikasi Web." *Modem: Jurnal Informatika dan Sains Teknologi*, 2(4), 162-177.

Bara, R.-M., Boiangiu, C.-A., & Tudose, C. (2024). "Analysing the Performance Impacts of Lazy Loading in Web Applications." *Journal of Information Systems & Operations Management*, 18(1), 1-15.

Bogner, J., & Merkel, M. (2022). "To Type or Not to Type? A Systematic Comparison of the Software Quality of JavaScript and TypeScript Applications on GitHub." *Proceedings of the 19th International Conference on Mining Software Repositories (MSR '22)*. ACM.

Donvir, A., Jain, A., & Saraswathi, P. K. (2024). "Application State Management (ASM) in the Modern Web and Mobile Applications: A Comprehensive Review." *arXiv preprint* arXiv:2407.19318.

Emmanni, P. S. (2023). "Comparative Analysis of Angular, React, and Vue.js in Single Page Application Development." *International Journal of Science and Research (IJSR)*, 12(6), 2971-2974.

Fauzi, A. Z. (2024). *Analisis Efisiensi Proses Build dan Performa Single-Page Application React, Vue, dan Svelte yang Dikembangkan Menggunakan Vite sebagai Build Tool* [Skripsi]. Yogyakarta: UIN Sunan Kalijaga.

Google. (2020). "Web Vitals: Essential metrics for a healthy site." Retrieved from https://web.dev/vitals/

Google Chrome Developers. (2023). "Core Web Vitals: Metric Definitions, Optimization Guidelines, and Lighthouse Methodologies." *Google Web Dev Official Documentation*. https://web.dev/vitals/

Hasanuddin, U. (2021). *Pedoman Penulisan Tesis dan Disertasi Mahasiswa Pascasarjana Fakultas Teknik Universitas Hasanuddin*. Makassar: Program Studi Magister Teknik Informatika, Universitas Hasanuddin.

Hermanto, R. R., & Engel, M. M. (2025). "Analisis Komparatif Kinerja Next.js, Nuxt.js, dan Remix.js dalam Implementasi Server Side Rendering Website Berita." *TIN: Terapan Informatika Nusantara*, 6(5), 450-463.

Jihadi, H., & Syarabil, A. F. (2023). "Perbandingan React JS dan Vue JS dalam Pengembangan Aplikasi Web Interaktif: Sebuah Studi Komparatif." *Jurnal Sistem Informasi Bisnis (JUNSIBI)*, 4(2), 70-79.

Johannes, D., Khomh, F., & Antoniol, G. (2019). "A Large-Scale Empirical Study of Code Smells in JavaScript Projects." *Software Quality Journal*, 27(3), 1271-1314.

Jonathan, R., & Suprihadi. (2023). "Development of Front-End Web Applications Utilizing Single Page Application Framework and React.js Library." *International Journal Software Engineering and Computer Science (IJSECS)*, 3(3), 529-536.

Khoirurrizal, M. F., Hidayat, C. R., & Ruuhwan. (2024). "Analisis Perbandingan Framework Front-End JavaScript SolidJS dan VueJS pada Pengembangan Website Interaktif." *Jurnal Informatika dan Teknik Elektro Terapan (JITET)*, 12(2).

Kowalczyk, K., & Szandała, T. (2024). "Enhancing SEO in Single-Page Web Applications in Contrast With Multi-Page Applications." *IEEE Access*, 12, 11597-11614. https://doi.org/10.1109/ACCESS.2024.3355740

Kumar, R., Singh, A., & Sharma, P. (2024). "Optimizing Web Performance with Lazy Loading and Code Splitting." *International Journal of Core Engineering & Management*, 11(3), 45-62.

Larissa, T. N., & Suartana, I M. (2026). "Perbandingan Teknik Pemuatan Awal Eager Loading dan Lazy Loading Intersection Observer terhadap Performa Website." *Journal of Informatics and Computer Science (JINACS)*, 7(4).

Noer, M. A., & Suartana, I M. (2024). "Perbandingan Mekanisme Rendering untuk Optimasi Website." *Journal of Informatics and Computer Science (JINACS)*, 6(2).

Piastou, M. (2023). "Comprehensive Performance and Scalability Assessment of Front-End Frameworks: React, Angular, and Vue.js." *World Journal of Advanced Engineering Technology and Sciences*, 9(2), 366-376.

Rezeki, A., Saputro, S. W., Saragih, T. H., Nugroho, R. A., & Abadi, F. (2026). "Empirical Performance of E2E Frameworks in React-Vue SPAs Using DIA." *International Journal of Advances in Data and Information Systems*, 7(1), 317-333.

Saboury, A., Musavi, P., Khomh, F., & Antoniol, G. (2017). "An Empirical Study of Code Smells in JavaScript Projects." *IEEE 24th International Conference on Software Analysis, Evolution and Reengineering (SANER)*, 294-305.

Setiawan, A. A., & Fauzi, E. (2025). "Analisis Komparatif Performa Implementasi Lazy Loading dan Code Splitting pada Framework React, Vue, dan Angular Berdasarkan Skor Lighthouse." *INTECOMS: Journal of Information Technology and Computer Science*, 8(3).

Sofi'ie, F. A. F., & Qoiriah, A. (2023). "Analisis Perbandingan Framework Front-End Javascript React dan Vue pada Pengembangan Website." *Journal of Informatics and Computer Science (JINACS)*, 5(2), 157-164.

Taivalsaari, A., & Mikkonen, T. (2021). "A Roadmap to the Programmable World: Software Challenges in the IoT Era." *IEEE Software*, 38(1), 53-61. https://doi.org/10.1109/MS.2020.3020616

Turcotte, A., Gokhale, S., & Tip, F. (2023). "Increasing the Responsiveness of Web Applications by Introducing Lazy Loading." *Proceedings of the 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)*, 459-470.

Vepsäläinen, J., Hellas, A., & Vuorimaa, P. (2023). "Overview of Web Application Performance Optimization Techniques." *Web Information Systems and Technologies (WEBIST 2023), Lecture Notes in Business Information Processing*. Springer.

Vite Team. (2024). "Why Vite: Next Generation Frontend Tooling." *Vite Official Documentation*. https://vitejs.dev/guide/why.html

W3C (World Wide Web Consortium). (2022). "Performance Timeline Level 2: Web APIs for Navigational Tracing." *W3C Working Draft*. https://www.w3.org/TR/performance-timeline-2/

Wijaya, I., & Farisi, A. (2025). "Analisis Perbandingan Kinerja dan Penggunaan Energi pada Framework React dan Vue." *Techno.Com*, 24(1), 104-116.

You, E., et al. (2023). "Vue.js 3: Design, Implementation, and Ecosystem." *Vue.js Official Documentation*. https://vuejs.org/

---

# LAMPIRAN

## Lampiran 1. Source Code, Data Pengukuran, dan Bahan Presentasi

Seluruh kode program aplikasi uji, skrip pengukuran, data mentah hasil pengujian, serta berkas presentasi tesis ini disimpan secara daring dan dapat diakses melalui tautan berikut:

**Tautan:** `[ISI LINK GOOGLE DRIVE DI SINI]`

Tautan tersebut mengarah pada satu folder Google Drive yang berisi dua berkas:

| No | Nama Berkas | Keterangan |
|----|-------------|------------|
| 1 | `mustari-pnup-main.zip` | Arsip repositori penelitian: seluruh kode program, konfigurasi *build*, skrip pengukuran, dan data mentah hasil pengujian |
| 2 | `Presentasi-Tesis-Mustari.pptx` | Berkas presentasi (slide) ujian tesis |

### Rincian Isi Berkas Arsip (ZIP)

Berkas arsip repositori tersusun dalam struktur berikut:

| Folder / Berkas | Isi |
|-----------------|-----|
| `src/` | Kode sumber aplikasi SIMTA (komponen Vue, *views*, *router*, *store* Pinia, dan lapisan layanan data asinkron) |
| `public/` | Berkas aset statis aplikasi |
| `index.baseline.html`, `index.optimized.html` | Titik masuk (*entry point*) aplikasi SIMTA versi *baseline* dan *optimized* |
| `index.cp.baseline.html`, `index.cp.optimized.html` | Titik masuk aplikasi *Company Profile* versi *baseline* dan *optimized* |
| `vite.config.baseline.js`, `vite.config.optimized.js` | Konfigurasi *build* Vite untuk SIMTA — berisi implementasi `manualChunks` sebagaimana dibahas pada Sub-bab 3.1 |
| `vite.config.cp.baseline.js`, `vite.config.cp.optimized.js` | Konfigurasi *build* Vite untuk *Company Profile* |
| `dist-baseline/`, `dist-optimized/` | Hasil kompilasi SIMTA kedua versi, sebagai bukti perbandingan ukuran *bundle* |
| `dist-cp-baseline/`, `dist-cp-optimized/` | Hasil kompilasi *Company Profile* kedua versi |
| `ukur_performa.cjs`, `ukur_performa_cp.cjs` | Skrip Puppeteer untuk pengukuran *PerformanceObserver* (uji tunggal) |
| `ukur_multirun.cjs`, `ukur_multirun_cp.cjs` | Skrip Puppeteer untuk pengukuran 5 repetisi per skenario |
| `ukur_lighthouse.cjs` | Skrip audit otomatis Google Lighthouse v11.x |
| `capture_screenshots.cjs` | Skrip pengambilan tangkapan layar untuk verifikasi kesamaan tampilan (Gambar 3.2 dan 3.3) |
| `analisis_statistik.py` | Skrip perhitungan rata-rata, standar deviasi, dan persentase perbaikan |
| `create_final_charts.py`, `process_visuals.py` | Skrip pembangkit grafik perbandingan (Gambar 3.4 sampai 3.9) |
| `laporan_tesis/data_pengukuran/` | Data mentah hasil pengukuran dalam format JSON (21 berkas) |
| `package.json`, `package-lock.json` | Daftar dependensi beserta versi terkunci, untuk menjamin reprodusibilitas |

### Rincian Data Mentah Pengukuran

Folder `data_pengukuran/` memuat data hasil pengujian yang menjadi dasar seluruh tabel dan grafik pada BAB III:

| Berkas | Isi |
|--------|-----|
| `multirun_baseline_ideal.json`, `multirun_optimized_ideal.json` | Data 5 repetisi SIMTA pada kondisi normal (Tabel 3.1, 3.2, 3.4) |
| `multirun_baseline_cpu_lambat.json`, `multirun_optimized_cpu_lambat.json` | Data 5 repetisi SIMTA pada kondisi CPU diperlambat 4x (Tabel 3.3, 3.4) |
| `multirun_cp_baseline_ideal.json`, `multirun_cp_optimized_ideal.json` | Data 5 repetisi *Company Profile* pada kondisi normal (Tabel 3.5) |
| `multirun_cp_baseline_cpu_lambat.json`, `multirun_cp_optimized_cpu_lambat.json` | Data 5 repetisi *Company Profile* pada kondisi CPU diperlambat 4x (Tabel 3.5) |
| `lighthouse_baseline.json`, `lighthouse_optimized.json` | Hasil audit Lighthouse SIMTA (Tabel 3.6) |
| `lighthouse_cp_baseline.json`, `lighthouse_cp_optimized.json` | Hasil audit Lighthouse *Company Profile* (Tabel 3.7) |
| `summary_stats.json` | Rekapitulasi rata-rata dan standar deviasi seluruh skenario |

### Cara Menjalankan Ulang Pengujian

Untuk mereproduksi hasil pengukuran pada BAB III, langkah-langkahnya adalah sebagai berikut:

```bash
# 1. Pasang seluruh dependensi
npm install

# 2. Kompilasi kedua versi aplikasi
npx vite build --config vite.config.baseline.js
npx vite build --config vite.config.optimized.js

# 3. Jalankan pengukuran PerformanceObserver (5 repetisi per skenario)
node ukur_multirun.cjs

# 4. Jalankan audit Lighthouse
node ukur_lighthouse.cjs

# 5. Hitung statistik dan bangkitkan grafik
python analisis_statistik.py
python create_final_charts.py
```

Hasil pengujian akan tersimpan dalam format JSON pada folder `data_pengukuran/`.

---


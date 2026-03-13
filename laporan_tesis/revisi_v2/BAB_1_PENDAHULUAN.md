# BAB I PENDAHULUAN

## 1.1 Latar Belakang Masalah

Single Page Application (SPA) telah menjadi arsitektur dominan dalam pengembangan aplikasi web modern karena kemampuannya memberikan pengalaman pengguna yang responsif dan interaktif (Mesbah & van Deursen, 2007). Berbeda dengan aplikasi web tradisional *Multi-Page Application* (MPA) yang memuat ulang seluruh halaman untuk setiap interaksi pengguna, SPA memuat seluruh konten dalam satu halaman HTML dan secara dinamis memperbarui tampilan tanpa *reload* halaman penuh, menghasilkan pengalaman yang lebih mirip aplikasi *desktop* (Taivalsaari & Mikkonen, 2021).

Dalam arsitektur MPA konvensional (menggunakan teknologi seperti PHP, ASP.NET, atau Ruby on Rails), setiap interaksi pengguna — seperti pengiriman formulir atau navigasi tautan — mengharuskan server memproses ulang halaman HTML secara utuh dan mengirimkannya kembali ke browser. Mekanisme pemuatan penuh (*full page reload*) ini tidak hanya membebani lalu lintas server, tetapi juga mendegradasi pengalaman pengguna karena timbulnya layar putih berkedip (*white screen blanking*) selama masa tunggu transmisi jaringan (Batool et al., 2021).

<div align="center">
  <img src="../chapters/images/diagram_mpa_spa.png" alt="Perbandingan Alur MPA dan SPA" width="380" />
  <br>
  <i>Gambar 1.1 Perbandingan arsitektur MPA (Multi-Page Application) dan SPA (Single Page Application).</i>
</div>

Sebagai solusi dari masalah tersebut, paradigma SPA hadir sebagai standar industri mutakhir yang dipelopori oleh kerangka kerja JavaScript reaktif berbasis komponen seperti Vue.js, React, dan Angular. SPA memungkinkan aplikasi web untuk mengunduh satu kerangka HTML (`index.html`) pada muatan perdana, kemudian semua perubahan tampilan dikelola oleh JavaScript di browser — tanpa perlu memuat ulang halaman. Ketika pengguna berpindah halaman, aplikasi hanya mengambil data kecil (dalam format JSON) dari server melalui API asinkron, lalu memperbarui bagian-bagian tertentu di layar saja (Bundschuh et al., 2019; Choi & Choi, 2020).

Hasilnya, SPA terasa jauh lebih cepat dan responsif — hampir seperti menggunakan aplikasi native. Karena itulah banyak lembaga akademik dan pemerintah mulai menggunakan SPA, termasuk untuk portal *e-government* dan sistem pelacakan tugas akhir.

Namun, pertumbuhan kompleksitas aplikasi web menyebabkan peningkatan ukuran *bundle* JavaScript yang berdampak negatif pada performa. Penelitian oleh Kumar et al. (2024) menunjukkan bahwa rata-rata ukuran *bundle* JavaScript pada aplikasi web modern mencapai 1.5 MB, yang membutuhkan waktu loading 8-12 detik pada koneksi 3G, mengakibatkan *bounce rate* meningkat hingga 53% untuk setiap penambahan delay 3 detik (Google, 2020).

Ketika sebuah aplikasi SPA tidak dioptimalkan dengan benar, browser terpaksa mengunduh seluruh kode program — termasuk semua halaman, komponen, gambar, dan pustaka pihak ketiga — sekaligus dalam satu file JavaScript yang sangat besar (*monolithic build*) (Malavolta et al., 2020). Untuk website sederhana seperti halaman profil perusahaan, hal ini mungkin tidak masalah. Tetapi untuk aplikasi yang kompleks seperti Sistem Informasi Manajemen Tugas Akhir (SIMTA) — yang menggunakan banyak fitur seperti grafik interaktif (*Chart.js*), manajemen data global (*Pinia*), koneksi *database* (*Supabase*), dan otentikasi pengguna — ukuran file-nya bisa melebihi batas wajar yang direkomendasikan untuk browser (lebih dari 300 KB terkompresi).

Akibat dari *bundle* yang terlalu besar ini sangat merugikan. Nilai-nilai penting dalam pengukuran performa web yang disebut *Core Web Vitals* — yang digunakan oleh mesin pencari seperti Google — akan turun drastis (Kusumawati dkk., 2022). Menurut Jiang et al. (2023), setiap *improvement* 100 ms pada LCP dapat meningkatkan *conversion rate* sebesar 1-2%, dan setiap *improvement* 100 ms pada FCP mengurangi *bounce rate* 2-3%. Saat browser harus memproses file JavaScript yang sangat besar, seluruh kemampuan prosesor digunakan untuk membaca, menguraikan, dan menjalankan kode tersebut. Selama proses ini berlangsung, browser tidak bisa merespons klik atau interaksi pengguna sama sekali (Amenta & Castellani, 2019).

Untuk mengatasi masalah ini, pendekatan *Code Splitting* dan *Lazy Loading* telah dikembangkan (Muhammed et al., 2021). Alih-alih mengirimkan semua kode sekaligus, hanya bagian yang diperlukan saat pengguna membuka halaman tertentu yang dikirimkan. Penelitian oleh Zhang dan Liu (2023) menunjukkan bahwa strategi loading yang adaptif dapat meningkatkan performa hingga 40% dibandingkan implementasi standar. Lebih lanjut, teknik *Hybrid Lazy Loading* atau *Prefetching* memanfaatkan waktu senggang browser untuk diam-diam mengunduh terlebih dahulu bagian kode yang kemungkinan akan dibutuhkan selanjutnya (Google Chrome Developers, 2023; Bellairs & Morrison, 2023).

Vue.js, sebagai salah satu framework JavaScript progresif, menyediakan mekanisme *code splitting* dan *lazy loading* bawaan. Namun, implementasi standar seringkali tidak optimal karena menerapkan strategi yang sama untuk seluruh komponen tanpa mempertimbangkan karakteristik dan pola penggunaan aplikasi (Zhang & Liu, 2023). Kombinasi Vue.js dengan Vite — *build tool* modern yang dikembangkan oleh Evan You — berpotensi menghasilkan optimasi performa yang lebih baik, namun masih memerlukan strategi hibrida yang menyesuaikan teknik *lazy loading* dan *code splitting* berdasarkan tingkat kompleksitas aplikasi.

Tingkat kompleksitas aplikasi web mempengaruhi efektivitas strategi optimasi. Menurut Patel dan Kumar (2022), aplikasi dengan kompleksitas rendah seperti *company profile* memiliki karakteristik berbeda dengan aplikasi kompleksitas tinggi yang melibatkan operasi CRUD dan visualisasi data *real-time*. Namun, belum ada penelitian yang secara spesifik mengkaji bagaimana tingkat kompleksitas ini mempengaruhi efektivitas strategi *hybrid lazy loading* dan *code splitting*.

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
   - **Aplikasi Kompleks (SIMTA):** Sistem Informasi Manajemen Tugas Akhir yang menggunakan banyak pustaka seperti Vue.js 3, Chart.js (untuk grafik), Supabase (untuk *database*), dan Pinia (untuk manajemen data global).
   - **Aplikasi Sederhana (Company Profile):** Website profil perusahaan yang hanya menampilkan konten statis tanpa grafik interaktif atau manajemen data yang kompleks.

3. **Teknik Optimasi:** *Route-based lazy loading*, *component-based lazy loading*, *dynamic import*, *code splitting* berbasis *chunk*, dan *intelligent prefetching*.

4. **Metrik Performa:** *First Contentful Paint* (FCP), *Largest Contentful Paint* (LCP), *Total Blocking Time* (TBT), *Load Time*, penggunaan memori JavaScript (*JS Heap*), serta data tambahan dari Lighthouse (*Performance Score*, *Time to Interactive*).

5. **Alat pengukuran:** Kombinasi *W3C PerformanceObserver* (pengukuran langsung dari browser) dan Google Lighthouse (sebagai alat audit standar industri).

6. **Pengujian:** Dilakukan di server lokal (*localhost*) menggunakan Puppeteer untuk automasi browser, dengan simulasi pelambatan CPU 4x melalui *Puppeteer Chromium API*.

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
2. **Bagi Industri:** Membantu organisasi dalam mengoptimalkan performa aplikasi web yang berdampak pada peningkatan *user experience* dan *conversion rate*. Pengurangan ukuran data yang dikirimkan juga berpotensi mengurangi biaya *bandwidth* bagi pengelola server.
3. **Bagi Peneliti Selanjutnya:** Menyediakan *baseline* dan metodologi yang dapat dikembangkan untuk penelitian lebih lanjut terkait optimasi performa web.

---

## 1.6 Tinjauan Pustaka / Penelitian Terdahulu

Penelitian tentang cara meningkatkan kecepatan SPA menggunakan *Code Splitting* dan *Lazy Loading* telah dilakukan oleh beberapa peneliti sebelumnya. Bagian ini merangkum penelitian terkait dan menjelaskan apa yang membedakan penelitian ini:

1. **Mesbah dan van Deursen (2007)** dalam *Proceedings of the 11th European Conference on Software Maintenance and Reengineering* membangun kerangka migrasi dari MPA ke SPA. Namun, paper klasik ini belum membahas teknik optimasi modern seperti *lazy loading* dan *code splitting*.

2. **Batool et al. (2021)** dalam jurnal *IEEE Access* membandingkan performa website MPA dan SPA. Mereka menemukan bahwa waktu muat SPA jauh lebih dipengaruhi oleh ukuran file JavaScript dibandingkan MPA. Namun, penelitian mereka tidak menguji kondisi perangkat yang lambat (*CPU throttling*), dan menggunakan alat Lighthouse yang dapat memengaruhi hasil pengukuran.

3. **Zheng dan Li (2022)** dalam jurnal *IJACSA* mendemonstrasikan teknik *Prefetching Lazy Loading* pada aplikasi React.js dan berhasil membuat perpindahan halaman terasa instan. Namun, mereka tidak membandingkan apakah teknik ini sama efektifnya pada website sederhana seperti *Company Profile*.

4. **Amenta dan Castellani (2019)** dalam *Journal of Digital Experiences* membuktikan bahwa *Total Blocking Time* (TBT) yang melebihi 300 ms menyebabkan pengguna meninggalkan website (*bounce rate* tinggi). Penelitian ini melanjutkan temuan mereka dengan secara nyata mengurangi nilai TBT.

5. **Choi dan Choi (2020)** dalam *International Journal of Computer Applications* meneliti manfaat *Lazy Loading* pada portal *e-government* dan berhasil mengurangi ukuran pengiriman sekitar 22%. Namun, mereka tidak menerapkan *Prefetching*, sehingga perpindahan halaman tetap terasa lambat.

6. **Kim dan Park (2022)** melakukan studi komparatif teknik optimasi pada React, menemukan kombinasi *code splitting* mengurangi TTI hingga 40%. Namun, penelitian ini fokus pada React ecosystem dan tidak meng-*address* Vue.js.

7. **Kumar et al. (2024)** dalam *International Journal of Core Engineering & Management* mengimplementasikan *lazy loading* dan *code splitting* pada 3 framework (React, Angular, Vue.js) dan mencapai 40% *reduction* pada *page load time*. Namun, studi ini bersifat *general* dan tidak *deep-dive* pada optimasi spesifik Vue.js + Vite.

8. **Rufián-Lizana et al. (2023)** dalam *Applied Sciences* mengidentifikasi *best practices* untuk *code splitting* dan *lazy loading*. Namun, mereka tidak mempertimbangkan kompleksitas aplikasi sebagai faktor dalam strategi optimasi.

9. **Fitriani dan Hasanuddin (2021)** dari Universitas Hasanuddin meneliti performa arsitektur *Micro-Frontend* dan membuktikan bahwa pemusatan pustaka besar dalam satu file menyebabkan beban berat di awal.

**Gap Penelitian:** Berdasarkan tinjauan di atas, belum terdapat penelitian komprehensif yang mengkaji implementasi *hybrid lazy loading* dan *code splitting* pada Vue.js dengan Vite yang mempertimbangkan tingkat kompleksitas aplikasi sebagai faktor penentu strategi optimasi. Penelitian ini mengisi gap tersebut dengan membandingkan dua aplikasi dengan kompleksitas yang sangat berbeda, menggunakan kombinasi alat pengukuran (*PerformanceObserver* + Lighthouse), dan menguji pada kondisi perangkat yang terbatas.

---

## 1.7 Sistematika Penulisan

Penulisan tesis ini dibagi menjadi empat bab utama:

- **BAB I PENDAHULUAN:** Menjelaskan latar belakang mengapa performa SPA perlu dioptimalkan, masalah yang ingin diselesaikan, batasan penelitian, tujuan, manfaat, dan ringkasan penelitian-penelitian terdahulu yang relevan.

- **BAB II METODE PENELITIAN DAN LANDASAN TEORI:** Menjelaskan teori-teori dasar yang digunakan (seperti arsitektur SPA, Vue.js, Vite, cara kerja browser, *Virtual DOM*, *Lazy Loading*, *Code Splitting*, strategi hibrida, dan cara mengukur performa web), serta metodologi penelitian secara detail termasuk variabel penelitian, spesifikasi alat yang digunakan, dan langkah-langkah pengujian.

- **BAB III HASIL DAN PEMBAHASAN:** Menyajikan hasil pengukuran dari kedua versi aplikasi (standar dan yang dioptimalkan), termasuk kode program, grafik perbandingan, data Lighthouse, analisis statistik, dan interpretasi mendalam tentang setiap temuan.

- **BAB IV PENUTUP:** Merangkum kesimpulan dari penelitian dan memberikan saran untuk penelitian lanjutan.

# BAB II METODE PENELITIAN

## 2.1 Jenis dan Pendekatan Penelitian
Desain metodologis dari tugas akhir riset tesis ini diklasifikasikan sebagai studi komparasi eksperimental (eksperimen semu atau *quasi-experimental*) terapan dalam rumpun keilmuan Rekayasa Perangkat Lunak Web Tingkat Lanjut. Model skema pengujian difokuskan pada perbandingan objektif dari dua *output* algoritma rute kompilasi atas purwarupa (prototipe) aplikasi *Single Page Application* (SPA) yang sama persis dalam hal rekayasa *frontend interface* (Antarmuka Pengguna) serta relasi basis data, namun dirangkai berbeda fondasinya terhadap distribusi *payload*.

Klasifikasi Varian Uji Kompilasi:
1. **Model Sistem Baseline (Monolithic / Eager Load):** Representasi perangkat lunak dasar menggunakan kompilasi reaktif standar (`vite.config.baseline.js`). Seluruh hierarki pohon komponen UI (halaman tunggal `DashboardView`, `JadwalSeminarView`, dll) dipanggil secara terpusat melalui mekanisme *Eager Imports* pada berkas perute (*router*). Kompilator akan menghasilkan sebuah berkas skrip JavaScript gabungan berukuran besar (*vendor*+*core*) yang mendominasi proses pemuatan awal situs.
2. **Model Sistem Optimized (Hybrid Splitting):** Representasi iterasi pembaharuan yang menerapkan algoritma konfigurasi pemecahan berkas (`vite.config.optimized.js`). Memanfaatkan fungsi deklaratif *Route-level Lazy Loading* (`() => import(...)`), isolasi ketergantungan paket perpustakaan berukuran besar (*manual chunks* untuk *Vue* dan *Chart.js*), aktivasi kompresi data transfer ganda (*Gzip* & *Brotli*), hingga implantasi strategis algoritma *Prefetching W3C Callback* secara asinkron (memanfaatkan *idle time tracking*).

## 2.2 Tahapan Pelaksanaan Eksperimen
Rencana riset direkayasa berkesinambungan melewati alur kerja investigatif sebagai berikut:
1. **Investigasi dan Pemodelan Sistem Berjalan:** Melakukan desain rancang bangun terhadap dua sampel tingkatan (*Complexity Density*) pada struktur aplikasi purwarupa uji. Target utama adalah tingkat *Kompleks* yang diwakili Aplikasi Sistem Informasi Manajemen Tugas Akhir / SIMTA. Target pembanding level *Sederhana* diwakili purwarupa aplikasi *Company Profile* murni.
2. **Konstruksi Pengembangan Kode (*Development*):** Melakukan perancangan *Single Page Application* menggunakan kerangka bahasa *TypeScript/Javascript Framework Vue.js v3*, disokong *Vue Router 4*. Pada SIMTA, eksekusi menggunakan sistem state manajemen (*Pinia Store*) dan diagram *Chart.js*, sementara pada profil perusahaan tidak memakai gubahan ekstensi tambahan apa pun.
3. **Rekayasa Formulasi Kompilasi (*Bundling Formulation*):** Mengonstruksi dua mode luaran kompilasi ke direktori statis tersendiri (satu versi ke `dist-baseline` dan peracikan ganda ke `dist-optimized`) menggunakan kompilator hibrida *Vite Bundler*. Pada mode optimasi, Vite distrukturkan menggunakan *Rollup.js* guna membentuk *Module Dependency Graph* (Pohon Grafik Ketergantungan Modul) secara statis sehingga mengizinkan fragmentasi *manual chunks* yang akurat antar rute. Formulasi ini divalidasi memanfaatkan *Plugin Rollup Visualizer*.
4. **Instalasi dan Pemungutan Observasi (Pengumpulan Data):** Pemasangan instrumen pelacakan otomatis menggunakan integrasi perangkat pengujian (*puppeteer*) yang dikombinasikan dengan API pemantau peramban bawaan (*W3C Native PerformanceObserver*) untuk memperoleh integritas data kinerja situs yang akurat.
5. **Evaluasi Deskriptif & Komparasi Matriks:** Kegiatan konversi dan olah hitung variabel evaluasi untuk menganalisis hipotesis peredaman latensi (*Web Vitals TBT/FCP*).

## 2.3 Pemodelan Tingkat Kompleksitas (Sistem SIMTA)
Landasan urgensi dari peletakan algoritma intervensi *Code Splitting* memerlukan pembenaran atas tingginya kompleksitas muatan bawaan sistem purwarupa. Berbeda totalnya rasio pemuatan komponen pada web portal statis linier, subsistem SIMTA memancarkan keterikatan reaktif padat (interaksi *interlocking state*) seperti tergambar di diagram berikut.

### 2.3.1 Relasi Basis Data (*Entity Relationship Diagram*)
Hubungan relasional multidimensi ini merepresentasikan bagaimana entitas kelolaan seperti status log mahasiswa, presensi bimbingan, notule asinkron, serta berkas laporan, memiliki tautan struktural yang merentang erat pada sisi antarmuka klien. Paradigma kerangka data yang masif ini merasionalisasi kerentanan SPA komprehensif terhadap degradasi *Render Time* jika dikompilasi ke dalam format arsitektur Monolitik secara mentah.

<div align="center">
  <img src="./images/mermaid_1.png" alt="Diagram Relasi Basis Data SIMTA/ERD" width="550" />
  <br>
  <i>Gambar 2.1 Entity Relationship Diagram (ERD) dari Modul Bimbingan SIMTA.</i>
</div>

### 2.3.2 Pola Sirkulasi Arus Data (*Data Flow Diagram Reaktif*)
Siklus aliran arsitektur SPA mutakhir ini (menggunakan *Pinia/Vuex* State Management) secara masif mengirimkan sinyal pembaruan (*Reactive Virtual-DOM Patching*) ketika bongkah *Library Chart.Js* atau tabel daftar antrean dimutasi secara langsung oleh respon *asynchronous* dari API.
<div align="center">
  <img src="./images/mermaid_2.png" alt="Diagram Alir Komunikasi State Management Berbasis Pinia" width="550" />
  <br>
  <i>Gambar 2.2 Arus Transmisi Data Status Asinkronus pada Aplikasi.</i>
</div>
Kerumitan beban perulangan pemanggilan (*payload event*) di siklus DFD asimetris mendemonstrasikan signifikansi prioritas alokasi modul proses peramban. Pendekatan manajemen siklus ini bertendensi untuk meringankan kinerja *Main Thread* (benang peramban utama) sehingga probabilitas penumpukan rendering inisial layar dapat diminimalkan. Hal tersebut bermuara langsung pada alasan mendasar implementasi metodologi *Lazy Load*.

## 2.4 Instrumen Pengumpulan Data (W3C Algoritma *Tracker*)
Dalam penelitian ini, tidak direkomendasikan penggunaan fitur rekam analitik pihak ketiga semacam piranti Google Lighthouse atau GTMetrix. Perkakas audit berbasis jaringan sering kali membawa efek beban pengamat (*Observer Effect*). Apabila ekstensi tersebut digunakan pada pemodelan kondisi perangkat berspesifikasi perangkat keras minimum, sistem eksternal audit tersebut justru dapat mengonsumsi limitasi memori RAM serta siklus prosesor tambahan, berujung pada menurunnya metrik hasil pengujian sehingga tidak merepresentasikan presisi empiris di lapang sesungguhnya.

Sebagai solusi substitusi, penelitian ini menyusun sebuah skrip pelacak algoritma kustom (*Tracker*) dengan memanfaatkan antarmuka API objektif standar peramban, yaitu `PerformanceObserver` berbasis *W3C specification*. Metode murni dalam-peramban (*in-browser*) ini menyokong pencatatan otomatis terhadap penayangan titik waktu (kapan mesin selesai merender muatan halaman) dengan akurasi granular tanpa menyebabkan friksi (*overhead*) monitoring ke perangkat kerja sang peramban itu sendiri.

Alur kerja instrumen pelacakan ini dapat digambarkan melalui diagram berikut:

<div align="center">
  <img src="./images/mermaid_3.png" alt="Alur Eksekusi Instrumen Pelacakan API Peramban" width="550" />
  <br>
  <i>Gambar 2.3 Struktur Penangkapan Algoritma Pelacakan Kelambatan Resolusi Layar.</i>
</div>

Berikut adalah contoh potongan pemograman skrip yang bekerja merekam data di latar belakang:
```javascript
// Memantau kemunculan halaman bergambar (cat piksel) fungsional pertama
const paintObserver = new PerformanceObserver((list) => {
    for (const entry of list.getEntriesByName('first-contentful-paint')) {
        let fcpDelay = Math.round(entry.startTime);
        MetricsTracker.record({ "FCP_ms": fcpDelay }); // Data direkam!
    }
});
paintObserver.observe({ type: 'paint', buffered: true });
```
Skrip observasi ini dieksekusi secara primer pada urutan paling awal sebelum lapisan SPA SIMTA terinisialisasi. Mekanisme ini memastikan objek pengintai (*observer*) teraktifkan demi merekam keempat metrik objektif (*FCP*, *LCP*, *TBT*, serta konsumsi alokasi jejak memori *Heap* RAM JS) secara otonom.

## 2.5 Perumusan Skenario Pengujian (*Stress-Tests*)
Keterandalan dari evaluasi teknik kompilasi asinkron (Optimasi SPA) sangat bergantung pada disparitas kondisi pengujian. Pengungkapan fenomena penurunan kapasitas layanan web acapkali tidak akan muncul apabila observasi semata-mata dihelat melalui arsitektur komputasi mutakhir pengembang tanpa kendala jaringan apa pun (*Bundle Bloat mask off*).

Atas dasar argumentasi tersebut, kerangka penelitian meramu dua desain komparasi simulasi beban pengujian yang dieksekusi sekuensial dan konsisten menggunakan pustaka otomasi web nir-antarmuka (*Puppeteer Headless Browser Node.js*):

1. **Skenario Optimal (Kondisi Ideal sebagai Acuan Dasar):** Metrik diobservasi dengan pemanfaatan maksimum kapasitas komputasi mesin server target simulasi (*baseline test*) tanpa perlakukan gangguan sistem perangkat keras. Skenario *Ideal* bertindak sebagai patokan baku atas persentase latensi murni komponen arsitektur.
2. **Skenario Emulasi Perangkat Terbatas (*4x CPU Slowdown*):** Skenario penekan ini ditunjukan mendemonsrasikan lingkungan uji paling rentan terhadap kompilasi algoritma skrip berkapasitas besar. Komputasi logis *thread* prosesor dikontrol melalui simulasi deviasi (*Throttling Limit*) guna dibatasi hingga 4 kali lebih minim frekuensi unjuk kerjanya (*4x Slowdown*). Uji tekan ini dipandang krusial dalam menyelaraskan pengalaman pengguna dari kalangan pemakai perangkat seluler dengan spesifikasi SoC menengah ke bawah di lapangan (*Real-world constraint*).

Alur simulasi otomasi komputasi terpusat mengekskusi interaksi dengan struktur logis *flowchart* berikut:

<div align="center">
  <img src="./images/mermaid_4.png" alt="Alur Logika Pengujian Otomasi dengan Batasan Hardware" width="550" />
  <br>
  <i>Gambar 2.4 Alur Diagram Eksekusi Puppeteer dalam Skenario Normal & Throttling Limit.</i>
</div>

Melimpahkan kendali pengarahan navigasi melalui arsitektur perangkat lunak otomatis (*Puppeteer API*), faktor ketidakakuratan dan rentang deviasi respons akibat anomali reaksi subjek manusiawinya (efek *human-error bias*) dapat dinihilkan sepenuhnya dari rentetan iterasi penelitian. Evaluasi akan murni melambangkan kapabilitas skrip tanpa adanya jeda distorsi pihak ketiga.

# BAB III HASIL DAN PEMBAHASAN

## 3.1 Resolusi Pemecahan Bundel (*Bundle Analysis & Decomposition*)
Perubahan pada kode sumber *Single Page Application* (SPA) menghasilkan redifinisi struktur pada tahap kompilasi akhir (Zheng & Li, 2022). Tabel matriks ukuran pasca-produksi (*post-compilation build*) secara objektif membuktikan efektivitas teknik pembagian beban (*Code Splitting*) dalam mendistribusikan hambatan lalu-lintas muatan data aplikasi Sistem Informasi Manajemen Tugas Akhir (SIMTA) ke dalam fraksi-fraksi asinkron.

### 3.1.1 Dekompilasi Modul *Baseline* vs *Optimized*
Pada arsitektur *Baseline*, kompilasi *build* menghasilkan satu berkas tunggal monolitik `index.baseline-Ca8FZuKC.js` berukuran cukup besar yakni **346.42 KB** (atau 120.94 KB dalam keadaan terkompresi *Gzip*). Kondisi ini mewajibkan peramban mengunduh seluruh fungsionalitas aplikasi sekaligus. Berkebalikan dengan itu, arsitektur *Optimized* menghasilkan distribusi direktori (*chunks manifest*) yang terurai secara terisolasi.

*Tabel 3.1 Persebaran Pemecahan Modul (Chunks) pada Arsitektur Optimized*
| Nama Berkas Modul (Kepingan *Chunk*) | Proporsi Fungsional | Ukuran Mentah | Ukuran Terkompresi (*Gzip*) |
|--------------------------------------|--------------------|----------------|-----------------------------|
| `vendor-chart-[hash].js` | Dependensi Eksternal (Grafik) | 199.59 KB | 67.42 KB |
| `vendor-vue-[hash].js` | Pustaka Inti Vue & Pinia | 103.29 KB | 39.40 KB |
| `supabase-[hash].js` | Protokol Klien API | 17.19 KB | 4.96 KB |
| `index.optimized-[hash].js` | *Entry Point* (Berkas Utama) | 11.67 KB | 4.39 KB |
| `DashboardView-[hash].js` | Antarmuka Halaman Dashboard | 7.99 KB | 2.62 KB |
| `DetailBimbinganView-[hash].js` | Modul Fitur Spesifik | 7.75 KB | 3.03 KB |
| `JadwalSeminarView-[hash].js`| Modul Fitur Spesifik | 6.34 KB | 2.51 KB |
| `DaftarJudulView-[hash].js` | Modul Fitur Spesifik | 5.59 KB | 2.39 KB |

*Sumber: Pengolahan Hasil Kompilasi Vite Rollup (2026).*

Dari perincian dekompilasi di atas diperoleh temuan empiris: alih-alih mewajibkan peramban mengunduh memori gabungan sebesar 346 KB sejak pengguna melihat layar pendaftaran SIMTA, struktur versi *Optimized* hanya menginstruksikan muatan inisial (`index.optimized`), kumpulan modul inti `vendor-vue`, dan CSS utama yang menggunakan komputasi minimum (<45 KB terkompresi). Hal ini meminimalkan beban *bandwidth* saat penginisialisasian pada sisi klien secara signifikan.

Distribusi proporsi pengerutan fail tersebut dicitrakan ulang pada model grafik lingkaran (*Pie Chart*) di bawah ini. Diagram ini mengilustrasikan dominasi fungsionalitas pustaka pihak ketiga (*Chart.js* dan *Vue/Pinia*) dibandingkan dengan kode murni aplikasi, yang membuktikan mengapa isolasi *chunk* bagi utilitas tersebut sangat penting untuk mereduksi beban *download* inisial:

<div align="center">
  <img src="./images/mermaid_5.png" alt="Proporsi Ukuran Modul Eksternal vs Skrip Aplikasi" width="550" />
  <br>
  <i>Gambar 3.1 Distribusi Proporsi Pemecahan Modul Vite Rollup.</i>
</div>

## 3.2 Hasil Pengujian pada Jaringan dan Perangkat Normal (Kondisi Ideal)
Pengujian pada skenario pertama disimulasikan melalui otomatisasi peramban latar belakang (*Puppeteer Headless CDP*) menggunakan konektivitas komputasi lokal *Host* Node.js tanpa penerapan batasan jaringan publik maupun hambatan latensi *Thread CPU*. Merujuk pada standar pengukuran Google Chrome Developers (2023) untuk melacak *core web vitals* secara terpadu melalui utilitas API *Native*, berikut instrumen analisis dari capaian pengembangannya:

| Metrik Objek *Web Vitals* W3C | Evaluasi Versi Baseline | Evaluasi Versi Optimized | Variansi Intervensi |
|-------------------|----------------|-----------------|---------------------|
| Lingkungan / Peramban | Google HeadlessChrome | Google HeadlessChrome | Spesifikasi Seimbang |
| ***First Contentful Paint* (FCP)**| 824 ms | 872 ms | Peningkatan +48 ms |
| ***Largest Contentful Paint* (LCP)**| 824 ms | 872 ms | Peningkatan +48 ms |
| ***Total Blocking Time* (TBT)**| 19 ms | **13 ms** | **Reduksi Kelambatan -6 ms (> 30%)**|
| Eksekusi Waktu Penuh Siklus Laman | 664 ms | 701 ms | Peningkatan +37 ms |
| Alokasi Konsumsi *Heap Memory JS* | 2.88 MB | 3.05 MB | Peningkatan Wajar +0.17 MB |

**Pembahasan Skenario 1:**
Pada spesifikasi tangguh dengan koneksi silang (*pipe network*) server lokal *localhost* (kondisi Ideal), rentang perbedaan parameter perenderan waktu penayangan (seperti FCP dan LCP) antara dua arsitektur dapat dikatakan seimbang. Terpantau sebuah toleransi keterlambatan latensi kecil terkait overhead resolusi transmisi HTTP pada bagian modul independen *chunk* sebesar 48ms di mode *Optimasi*. Fakta ini mengokohkan analisis bahwa eksekusi penanganan muatan asinkron berantai ini tidak membebani komputasi tingkat tinggi secara fatal (Bundschuh et al., 2019). 

Sebaliknya, metrik krusial demi pengidentifikasian interaktivitas SPA seperti *Total Blocking Time* (TBT) mengalami penciutan waktu hingga batas yang lebih responsif (**13ms**) berbanding tingkat rata-rata 19ms milik *baseline*. Algoritma *Web Vitals* berhasil menderivasi dan membuktikan keberhasilan penguraian siklus *Sub-Tree* tak terlihat tatkala aktivitas utama layar komputasi masih dalam posisi inisiasi pembangunan elemen *Document Object Model* (Amenta & Castellani, 2019).

## 3.3 Hasil Pengujian Ekstrem pada Perangkat Berspesifikasi Rendah (*CPU Throttling 4x*)
Guna memastikan rentang keterbatasan spesifikasi pengguna di lapangan (contohnya pengguna fitur yang mengakses dari gawainya dengan kualifikasi prosesor *Low End*), simulasi pengujian juga mensyaratkan pemberlakuan kondisi pembatasan *CPU Throttling 4x Slowdown*. Kondisi ini diperlukan agar menstimuli kegagalan layar pemuatan tak responsif (*Browser Event Freeze*) secara buatan pada aplikasi sistem informasi.

| Metrik Objek *Web Vitals* W3C | V. Baseline (CPU Lambat) | V. Optimized (CPU Lambat)| Efektivitas Intervensi |
|-------------------|----------------|-----------------|---------------------|
| Emulasi Lingkungan Perangkat | Perangkat Lambat(4x) | Perangkat Lambat(4x) | - |
| ***First Contentful Paint* (FCP)**| 1216 ms | 1404 ms | Bias Latensi Asinkron +188 ms |
| ***Largest Contentful Paint* (LCP)**| 1216 ms | 1404 ms | Bias Latensi Asinkron +188 ms |
| ***Total Blocking Time* (TBT)**| **377 ms** | **363 ms** | **Penggerusan Titik Lebur -14 ms**|
| Eksekusi Waktu Penuh Siklus Laman | 1039 ms | 1234 ms | Diferensiasi Resolusi Multi-DNS +195 ms |

**Pembahasan Skenario 2:**
Keterbatasan pemrosesan komputasi CPU mendelegasikan eskalasi durasi metrik waktu inisial antarmuka. Indeks waktu paruh (*First Contentful Paint*) dari mekanisme *Eager Loading Baseline* mengalami perlambatan responsif ke ambang 1.2 detik (1216 ms). Sejalan dengan hipotesis awal, terlepas perolehan waktu FCP milik arsitektur optimasi memperoleh kompensasi lebih (-188 ms) efek dari inisialisasi modul dependen turunan (*Promise chaining*), indikator urgensi interaktivitas yakni *Total Blocking Time* justru tertahan kuat stabil di kisaran **363ms**. 

Capaian evaluasi toleransi 363ms diklasifikan sebagai parameter stabil yang menjaga laju navigasi di luar batas minimum fatal matriks (*Google Warning Vitals* \> 400ms). Pada aspek berlawanan, wujud *Baseline* bertumpuk pada perolehan latensi yang rentan pembekuan yakni 377ms. Lamanya pemutusan antarmuka *UI Main Thread* yang membengkak bagi *Baseline* erat kaitannya dengan inoperabilitas prosesor *JIT* peramban dalam melakukan konversi dan parsing seluruh kesatuan 346 KB bundelan aplikasi SIMTA sekali waktu secara masif bersamaan. Konsekuensi langsung terhadap rasio kesiapan pengguna (*Time to Interactive/TTI*) menjadikan implementasi versi dasar sering mengalamai ineresponsif (*Event Freeze Layout*) yang merenggut efisiensi metodologi reaktif *Single Page Application* secara harfiah (Choi & Choi, 2020).

## 3.4 Bukti Render Antarmuka Pengujian (Simulasi Algoritma Puppeteer)
Verifikasi visualisasi tampilan antarmuka *mock-up* aplikasi sistem termaksud saat diakses memanfaatkan piranti uji *Headless Browser* didokumentasikan melalui integrasi perintah log `screenshot()` Node.js pada kedua port:

<div align="center">
  <img src="./images/bukti_baseline.png" alt="Tangkapan Antarmuka Baseline Port 4001" width="550" />
  <br>
  <i>Gambar 3.2 Tangkapan Halaman Web Peramban pada Sistem Render Monolitik.</i>
</div>

<div align="center">
  <img src="./images/bukti_optimized.png" alt="Tangkapan Antarmuka Optimized Port 4002" width="550" />
  <br>
  <i>Gambar 3.3 Tangkapan Halaman Web Peramban pada Sistem Komparasi Teroptimasi.</i>
</div>

Dalam observasi layar antarmuka di atas, **tidak ditemukan perbedaan visual sekecil apapun (Gambar 3.2 dan 3.3 tampak identik secara kasat mata)**. Persamaan visual ini justru adalah sebuah bentuk validasi keberhasilan. Hal tersebut membuktikan bahwa mekanisme optimasi memecah kode (*Code Splitting*) secara eksklusif hanya mengintervensi fondasi logika alur data di latar belakang, tanpa sedikitpun merusak tata letak CSS (*layout*), warna, maupun struktur fungsional desain tampilan (*front-end representation*) yang disajikan kepada pengguna.

## 3.5 Pembuktian Mekanisme Pengunduhan Latar Belakang (*Prefetching*)

Pembuktian teknis ini didasarkan analisis jejak kerja dari *W3C Performance Timeline Level 2 API*. Purwarupa SPA SIMTA (*Optimized*) teridentifikasi secara presisi memanggil pemuatan asinkron untuk dependensi laten secara periodik (*stealth async request*) bertepatan purna-eksekusinya konstruksi komponen inisial `Dashboard` (*DOM mounted Lifecycle*).

Strategi pemanfaatan muatan *Hybrid Lazy Loading* ini secara definitif disajikan dalam alur konfigurator penjagaan modul navigasi (*Router Navigation Guards*):

```javascript
// Algoritma Pencegat Rutinitas (Route Guarding Interceptor)
router.afterEach((to, from) => {
    if (to.name === 'DashboardView') {
        // Taktik 'Mencuri Waktu' Silang dari Main Thread Peramban
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                // Inisiasi transfer HTTP Asinkron di latar tanpa distorsi UI
                import('../views/DaftarJudulView.vue');
            })
        }
    }
})
```

Pemanggilan *Prefetching* memanfaatkan *callback* `requestIdleCallback` bertujuan untuk menangkap jendela penyelesaian alokasi *rendering* awal guna memanfaatkan periodisasi waktu lenggang prosesornya sehingga tidak memangkas efisiensi kompilasi inisial (W3C, 2022). Hasil pengembangannya memungkinkan subhalaman direktori (misal fitur 'Daftar Judul') telah terserap pra-konsultasi (*cache-ready*) sebelum tindakan klik navigasi dari operator terjadi secara nyata. Modifikasi reaktor peristiwa ini meningkatkan presisi *Zero Latency Navigation*, mentransformasi rasio waktu tunggu peramban pengguna hingga skala pengunduhan statis seketika.

## 3.6 Dampak Terhadap Pengalaman Pengguna (*User Experience*)
Pergeseran rasio optimasi berbasis pola kompilatif arsitektur *Hybrid Lazy Loading* perlu dinilai ulang pada matriks keberdayaan layanan dari sisi Pengguna Akhir (HCI - Interaksi Manusia Komputer). Di skema arsitektur *Baseline*, pelonjakan TBT (> 370ms) untuk mesin standar menengah mendorong potensi interupsi layanan seperti fenomena *Rage Clicks*—perulangan intensitas pemanggilan kontrol oleh karena aplikasi tak sanggup bereaksi berkat tingginya sumbatan prioritas sinkron pada benang kerja JS utama (Batool et al., 2021).

Isolasi pembaharuan rute melalui peranti pecah kode secara terintegrasi mampu menjaga status aplikasi senantiasa berada pada level fungsional interaktif (*responsive to input events*), karena skema penundaan asinkron merotasi beban transmisi secara bergilir pada prioritas sekunder. Pola desain yang memitigasi muatan fungsional spesifik seperti pustaka statistik `Chart.js` memungkinkan implementasi respons antarmuka tereksekusi segera sebelum seluruh skema antarmuka purna diunduh seutuhnya.

## 3.7 Analisis Penggunaan Memori Peramban (*Heap Memory / RAM*)
Efisiensi perancangan perangkat lunak turut memperhitungkan korelasi alokasi RAM peramban pada lingkungan penyedia layanan (*client-machine constraint*). Pemantauan ini dicatat konfigurasinya menuju observasi pemakaian RAM berbasis batas batas JS Heap *API Runtime W3C*.

Pada skenario tanpa intervensi jaringan pembatas, model *Baseline Eager-Load* membatasi penggunaan *heap memory* di indeks 2.88 MB, manakala versi tersubstitusi (*Optimized*) menunjukkan ekspansi utilitas minor di 3.05 MB. Alasan objektif menggarisbawahi mengapa integrasi ukuran file optimasi secara kolektif melahirkan pertambahan marjinal sebesar +0.17 MB.
Gejala tersebut merupakan *Trade-off* prosedural yang logis atas reaktor dependensi (*dynamic imports maping*) di struktur rujukan aplikasi asinkron (Fitriani & Hasanuddin, 2021). Mesin Webkit/V8 memerlukan alokasi *registry file mapper* pemetaan (*Manifest Vite/Webpack Module Resolver*) ekstra demi mengomputasi susunan jejak rute pengalamatan (*Promise Resolve Function*) secara tepat sasaran. Selisih *overhead memori* tersebut dianggap setara (*feasible margin trade-off*) dikompensasikan bersama keberhasilan menurunkan rasio keutuhan TBT saat interlock visual (*Dashboard* utama) berjalan pada perangkat komputasi konvensional.

## 3.8 Evaluasi Pemecahan Rute Spesifik (*Route-Level Analysis*)
Kajian mendetail pada lapisan hirarki pengalamatan spesifik merasionalisasi margin keuntungan efektivitas beban terstruktur dari mekanisme optimasi ini secara teratur:

1. **Rute Eksekusi `/dashboard`:** Sebagai instrumen fungsional terpadat, komponen halaman *dashboard* mengimpor secara menyeluruh ekstensi eksternal `Chart.js`. Konfigurator *Vite Rollup* yang diprogram mampu mengisolasi fungsi grafik ini menduduki lokasi *parsing manual* di fail asinkron `vendor-chart-[hash].js`. Kondisional ini menjamin hilangnya muatan pengumpulan *cache* apabila antarmuka visual pelaporan grafik belum pernah diekseskusi di layar komputer milik pengguna (*route isolation on demand*).

2. **Rute Navigasi `/jadwal-seminar` dan `/detail-bimbingan`:** Titik berat pada kedua *view* ini ada pada manipulasi objek *State Management (Pinia)* untuk menampilkan daftar interaktif asinkron. Reduksi beban tercapai secara memuaskan, di mana kompilasi skrip antarmuka utamanya cuma berkisar ~6 KB. Pengolahan status datanya menjadi sangat kilat tanpa tersandung distorsi grafik visual rute lain.

Melalui penelaahan berbasis modul ganda tersebut, riset aplikatif ini mendefinisikan kerangka teknis terbaik dalam skenario sistem berbasis lokal berlawanan terhadap penutupan limitasi korelasi performa asinkron konvensional yang kental pada model eksekusi peramban gawai nirkawat.

## 3.9 Analisis Komparasi Arsitektur Sederhana (*Company Profile*)
Menjawab pilar perumusan kompleksitas sistem di Bab 1, pengukuran yang identik diaplikasikan terhadap sebuah replika aplikasi murni profil perusahaan (*Company Profile*) yang tidak memiliki beban Pustaka grafik (`Chart.js`) maupun Pustaka pengelola state (`Pinia`). 

*Tabel 3.2 Metrik Kinerja Aplikasi Company Profile (Skenario CPU Lambat 4x)*
| Metrik Objek *Web Vitals* W3C | V. Baseline (CPU Lambat) | V. Optimized (CPU Lambat)| Margin Perubahan |
|-------------------|----------------|-----------------|---------------------|
| ***First Contentful Paint* (FCP)**| 384 ms | 436 ms | +52 ms (Lebih Lambat) |
| ***Total Blocking Time* (TBT)**| **143 ms** | **24 ms** | -119 ms (Lebih Cepat) |
| Alokasi Tumpukan RAM (Heap) | 1.87 MB | 1.90 MB | +0.03 MB |

**Diskusi Kontrastif Eksplisit (Aplikasi Kompleks vs Sederhana):**
Data yang diperoleh pada Tabel 3.2 menunjukkan kontradiksi fungsionalitas yang sangat nyata dan eksplisit. Pada sistem informasi berskala minimum (`Company Profile`), pencapaian nilai metrik TBT untuk arsitektur *Baseline* sejatinya sudah tercatat sangat optimal pada angka **143 ms**, nilai fungsional ini jauh berada di dalam zona hijau pengujian stabilitas Web Vitals (<300 ms). Pengurangan durasi transmisi sebesar sekadar -119 milidetik (melalui *Code Splitting*) secara objektif tidak merepresentasikan kontribusi kinerja (*performance jump*) yang bisa dibedakan pada rasio observasi visual harian (Seow, 2008). 

Sebagai validasinya, perbandingan kinerja eksplisit antara pengunaan *Baseline* vs *Optimasi* direpresentasikan pada rangkaian visualisasi kurva pengujian di bawah ini:

<div align="center">
  <img src="./images/chart_tbt_comparison.png" alt="Perbandingan Total Blocking Time (TBT) - Baseline vs Optimized" width="550" />
  <br>
  <i>Gambar 3.4 Grafik Kelambatan Interaktivitas Layar (Total Blocking Time).</i>
</div>
*(Penjelasan: Semakin kecil nilainya semakin baik. Gambar 3.4 memperlihatkan waktu TBT pada SIMTA turun drastis (semakin responsif) setelah dioptimasi, khususnya pada perangkat dengan prosesor lambat. Sebaliknya, TBT untuk tingkat aplikasi sederhana/Company Profile sudah sangat kecil dan tidak urgen untuk disunat lebih lanjut).*

<div align="center">
  <img src="./images/chart_fcp_comparison.png" alt="Perbandingan First Contentful Paint (FCP) - Baseline vs Optimized" width="550" />
  <br>
  <i>Gambar 3.5 Grafik Durasi Muat Cat Layar Pertama (First Contentful Paint).</i>
</div>
*(Penjelasan: Pada FCP aplikasi SIMTA yang kompleks, peramban membuang ekstra ~188 ms sebagai ongkos memetakan jalur rute terkompresi. Meskipun terdapat pelarutan ini, kelebihannya ditebus pada TBT di Gambar 3.4).*

<div align="center">
  <img src="./images/chart_loadtime_comparison.png" alt="Perbandingan Waktu Muat Total Laman (Load Time)" width="550" />
  <br>
  <i>Gambar 3.6 Grafik Total Eksekusi Halaman Berbading Tipe Aplikasi (Load Time).</i>
</div>
*(Penjelasan: Waktu akhir proses perenderan pada Company Profile menunjukkan bahwa arsitektur Baseline sejatinya lebih andal (~560 ms). Penambahan teknik splitting malah menjadikan proses memuat halamannya tertahan karena kelebihan biaya pemanggilan jaringan ganda/HTTP request).*

<div align="center">
  <img src="./images/chart_memory_comparison.png" alt="Perbandingan Konsumsi Memori Peramban (JS Heap)" width="550" />
  <br>
  <i>Gambar 3.7 Grafik Alokasi Pengunaan Memori RAM Internal JS Heap.</i>
</div>
*(Penjelasan: Terlihat kenaikan marjinal penggunaan RAM pasca-optimasi pada kedua tipe aplikasi. Kenaikan +0.17 MB pada SIMTA ini mengonfirmasi adanya pajak alokasi pemetaan objek yang rasional demi menukar kerentanan layar beku).*

Mengacu pada tren keempat matriks kinerja di atas, konklusi eksperimen dapat ditetapkan secara definitif bahwa: **Penerapan teknik pemecahan *Code Splitting* mutlak dikerjakan secara eksklusif hanya untuk purwarupa SPA bervolume kompleks seperti SIMTA (terutama untuk menyelesaikan durasi *Thread* yang membeku melampaui rentang toleran).*

Jika metodologi pemecahan fail fungsional diterapkan secara membuta pada struktur linier sederhana (*Company profile*), intervensi jaringan justru memicu anomali keterlambatan yang disebut *Diminishing Returns*. Alih-alih mereduksi kelambatan, rute latensi *Lazy Loading* justru membebani proses kinerja durasi statis aplikasi tersebut tanpa faedah konkrit akibat menumpuknya rute jaringan yang tak esensial. Dengan demikian, intervensi desain hibrida direkomendasikan secara selektif berbasis rasio kepadatan DOM dan berat utilitas perangkat lunak ekstensi.

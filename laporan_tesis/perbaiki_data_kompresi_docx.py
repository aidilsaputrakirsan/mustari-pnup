# -*- coding: utf-8 -*-
"""Memperbaiki angka BAB III/BAB IV di Revisi-Tesis-Mustari.docx menyusul
perbaikan bug pengukuran (kompresi Brotli/Gzip tidak aktif saat pengujian,
Lighthouse memakai Chrome sistem yang menyebabkan interstitial) dan
pengukuran ulang penuh. Lihat laporan_tesis/revisi_v2/BAB_3_HASIL_PEMBAHASAN.md
untuk versi markdown yang menjadi rujukan angka baru di skrip ini.

Jalankan saat Revisi-Tesis-Mustari.docx tertutup:
    python perbaiki_data_kompresi_docx.py
"""
import os
import shutil
from docx import Document
from docx.table import Table

BASE = os.path.dirname(os.path.abspath(__file__))
DOCX = os.path.join(BASE, 'Revisi-Tesis-Mustari.docx')
BACKUP = os.path.join(BASE, 'Revisi-Tesis-Mustari.SEBELUM-PERBAIKAN-KOMPRESI.docx')

# ---------------------------------------------------------------- prosa ----

GANTI = [
    ("Gambar 3.1 di atas secara visual mengkonfirmasi temuan kuantitatif yang menjadi landasan penerapan code splitting dalam penelitian ini. Dominasi pustaka vendor — khususnya Chart.js yang menyumbang hampir sepertiga dari total ukuran bundle — menjelaskan mengapa strategi pemisahan chunk menjadi intervensi yang tepat sasaran. Ketika Chart.js dipisahkan ke dalam chunk vendor-charts.js dan hanya dimuat saat pengguna mengakses halaman yang menampilkan grafik, browser tidak perlu lagi memuat beban besar tersebut pada saat pembukaan pertama aplikasi.",
     "Gambar 3.1 di atas secara visual mengkonfirmasi temuan kuantitatif yang menjadi landasan penerapan code splitting dalam penelitian ini. Dominasi pustaka vendor — khususnya Chart.js yang menyumbang hampir sepertiga dari total ukuran bundle — menjelaskan mengapa strategi pemisahan chunk menjadi intervensi yang tepat sasaran. Perlu diluruskan bahwa manfaatnya bukan berasal dari menunda pengunduhan Chart.js sampai pengguna membuka halaman tertentu — halaman Dashboard yang menjadi rute pertama sudah menampilkan grafik sejak awal, sehingga vendor-chart.js tetap ikut diunduh pada kunjungan pertama. Manfaat nyatanya berasal dari pengunduhan beberapa chunk kecil secara paralel, kemampuan cache terpisah untuk pustaka vendor, dan chunk yang tidak pernah diunduh sama sekali pada navigasi yang tidak dimulai dari Dashboard."),

    ("Hasilnya: ukuran file yang harus diunduh saat pertama kali membuka website turun dari 346 KB menjadi sekitar 195 KB — bahkan hanya sekitar 65 KB setelah dikompresi. Chart.js kini tersimpan di file terpisah vendor-charts.js dan hanya diunduh ketika pengguna benar-benar membuka halaman yang menampilkan grafik.",
     "Hasilnya, total ukuran JavaScript SIMTA versi optimized terpecah menjadi delapan berkas terpisah (vendor-vue.js, vendor-chart.js, lima chunk per halaman, dan satu chunk layanan data), dibandingkan satu berkas tunggal 346,53 KB pada baseline. Setiap chunk dikompresi otomatis dengan Gzip dan Brotli saat build, dan server pengujian disiapkan agar peramban benar-benar menerima varian terkompresi ini sesuai header Accept-Encoding, sehingga manfaat kompresi ikut terukur pada metrik jaringan di sub-bab berikutnya."),

    ("Pada aplikasi SIMTA dalam kondisi ideal (no throttling), versi baseline menampilkan konten visual pertama dalam waktu rata-rata 1144,0 ms (SD = 17,1), sedangkan versi yang telah dioptimasi mencatatkan waktu 881,6 ms (SD = 35,5). Selisih sebesar 262,4 ms ini merepresentasikan perbaikan 22,9%, yang secara teknis disebabkan oleh berkurangnya volume JavaScript yang harus diunduh dan di-parse oleh mesin V8 sebelum browser dapat melakukan first paint.",
     "Pada aplikasi SIMTA dalam kondisi ideal (no throttling), versi baseline menampilkan konten visual pertama dalam waktu rata-rata 1103,2 ms (SD = 179,4), sedangkan versi yang telah dioptimasi mencatatkan waktu 842,4 ms (SD = 20,0). Selisih sebesar 260,8 ms ini merepresentasikan perbaikan 23,6%, yang secara teknis disebabkan oleh berkurangnya volume JavaScript yang harus diunduh dan di-parse oleh mesin V8 sebelum browser dapat melakukan first paint, ditambah manfaat kompresi Brotli/Gzip yang mengecilkan ukuran transfer setiap chunk."),

    ('Pada aplikasi Company Profile, versi baseline mencatat FCP sebesar 367,2 ms (SD = 16,2) dan versi optimasi 364,0 ms (SD = 44,1). Selisih yang hampir dapat diabaikan (3,2 ms) ini mengindikasikan bahwa pada aplikasi dengan kompleksitas rendah — di mana bundle JavaScript sejak awal sudah berukuran kecil dan tidak mengandung pustaka berat — penerapan Code Splitting tidak memberikan kontribusi signifikan terhadap percepatan FCP. Temuan ini konsisten dengan adanya trade-off penerapan lazy loading pada aplikasi sederhana yang dilaporkan Bara, Boiangiu, dan Tudose (2024).',
     'Pada aplikasi Company Profile, versi baseline mencatat FCP sebesar 511,2 ms (SD = 31,7) dan versi optimasi 483,2 ms (SD = 18,8) — perbaikan kecil sebesar 5,5%. Selisih ini jauh lebih tipis dibanding SIMTA, mengindikasikan bahwa pada aplikasi dengan kompleksitas rendah — di mana bundle JavaScript sejak awal sudah berukuran kecil dan tidak mengandung pustaka berat — penerapan Code Splitting tidak memberikan kontribusi sebesar pada aplikasi kompleks terhadap percepatan FCP.'),

    ("Gambar 3.4 di atas memvisualisasikan perbedaan FCP yang terjadi akibat penerapan code splitting. Pada SIMTA, penurunan FCP sebesar 22,9% (dari 1144,0 ms menjadi 881,6 ms) terjadi karena berkurangnya volume JavaScript yang harus di-parse oleh mesin V8 sebelum browser dapat melakukan first paint. Sementara itu, hampir tidak ada perbedaan pada Company Profile (367,2 ms vs 364,0 ms), yang mengindikasikan bahwa manfaat code splitting terhadap FCP hanya signifikan ketika bundle awal sudah cukup besar untuk menyebabkan keterlambatan parsing yang terukur.",
     "Gambar 3.4 di atas memvisualisasikan perbedaan FCP yang terjadi akibat penerapan code splitting, lazy loading, dan kompresi. Pada SIMTA, penurunan FCP sebesar 23,6% (dari 1103,2 ms menjadi 842,4 ms) terjadi karena berkurangnya volume JavaScript yang harus di-parse oleh mesin V8 sebelum browser dapat melakukan first paint, ditambah transfer chunk yang lebih kecil berkat kompresi. Sementara itu, perbedaan pada Company Profile jauh lebih tipis (511,2 ms vs 483,2 ms, perbaikan 5,5%), yang mengindikasikan bahwa manfaat code splitting terhadap FCP jauh lebih terasa ketika bundle awal sudah cukup besar untuk menyebabkan keterlambatan parsing dan transfer yang terukur."),

    ("Pada SIMTA dalam kondisi ideal, versi baseline mencatatkan TBT sebesar 111,8 ms (SD = 41,0), sementara versi yang telah dioptimasi mencatatkan angka sedikit lebih tinggi yaitu 137,2 ms (SD = 50,7). Kenaikan sebesar 25,4 ms ini pada pandangan pertama tampak kontraintuitif, namun dapat dijelaskan melalui mekanisme Event Loop. Pada kondisi ideal di mana kemampuan prosesor tidak dibatasi, proses resolusi dynamic import dan registrasi callback untuk lazy-loaded modules menambahkan sejumlah microtask ke dalam Callback Queue yang turut dihitung sebagai waktu pemblokiran. Namun, perbedaan ini masih berada di bawah ambang batas 200 ms yang ditetapkan oleh standar Core Web Vitals, sehingga tidak terasa oleh pengguna akhir. Dampak sesungguhnya dari teknik optimasi baru terlihat jelas pada skenario CPU yang diperlambat.",
     "Pada SIMTA dalam kondisi ideal, versi baseline mencatatkan TBT sebesar 139,2 ms (SD = 77,0), sementara versi yang telah dioptimasi mencatatkan angka lebih rendah yaitu 104,6 ms (SD = 34,6) — perbaikan 24,9%. Kedua nilai ini masih berada di bawah ambang batas 200 ms yang ditetapkan oleh standar Core Web Vitals, sehingga tidak terlalu terasa oleh pengguna akhir pada kondisi perangkat yang mumpuni. Dampak sesungguhnya dari teknik optimasi ini terlihat jauh lebih jelas pada skenario CPU yang diperlambat."),

    ("Gambar 3.5 di atas memperlihatkan temuan yang sekilas tampak kontraintuitif: TBT SIMTA versi optimized sedikit lebih tinggi (137,2 ms) dibanding baseline (111,8 ms) pada kondisi normal. Hal ini disebabkan oleh overhead administratif dari mekanisme lazy loading itu sendiri — registrasi dynamic import handler menambah microtask kecil ke dalam Event Loop. Namun, kedua nilai masih jauh di bawah ambang batas 200 ms Core Web Vitals. Pada Company Profile, TBT tercatat 0 ms pada kedua versi, mengkonfirmasi bahwa bundle yang sudah kecil tidak menghasilkan blocking time yang terukur.",
     "Gambar 3.5 di atas memperlihatkan TBT SIMTA versi optimized konsisten lebih rendah dibanding baseline, baik pada kondisi normal (104,6 ms vs 139,2 ms) maupun pada kondisi CPU diperlambat. Kedua nilai pada kondisi normal masih berada di bawah ambang batas 200 ms Core Web Vitals. Pada Company Profile, TBT tercatat 0 ms pada kedua versi, mengkonfirmasi bahwa bundle yang sudah kecil tidak menghasilkan blocking time yang terukur pada kondisi ideal."),

    ("Pada SIMTA, waktu muat versi baseline meningkat dari 726,0 ms (kondisi ideal) menjadi 1095,2 ms (SD = 26,9), sedangkan versi optimasi meningkat dari 743,6 ms menjadi 1031,8 ms (SD = 64,6). Perbedaan antara kedua versi pada kondisi throttled menunjukkan perbaikan sebesar 5,8%. Untuk Company Profile, versi optimasi menghasilkan Load Time yang lebih cepat (97,4 ms vs 171,2 ms pada baseline), dengan perbaikan sebesar 43,1%.",
     "Pada SIMTA, waktu muat versi baseline meningkat dari 694,2 ms (kondisi ideal) menjadi 1121,6 ms (SD = 218,5), sedangkan versi optimasi meningkat dari 688,6 ms menjadi 975,8 ms (SD = 45,5). Perbedaan antara kedua versi pada kondisi throttled menunjukkan perbaikan sebesar 13,0%. Untuk Company Profile, versi optimasi juga menghasilkan Load Time yang lebih cepat (106,0 ms vs 140,4 ms pada baseline), dengan perbaikan sebesar 24,5%."),

    ("Gambar 3.6 di atas menampilkan perbandingan Load Time pada kondisi CPU yang diperlambat 4x — skenario yang paling merepresentasikan kondisi pengguna dengan perangkat rendah. Penurunan Load Time pada SIMTA sebesar 5,8% (dari 1095,2 ms menjadi 1031,8 ms) lebih moderat dibanding penurunan FCP karena Load Time mencakup seluruh siklus pemuatan termasuk resolusi modul dinamis. Yang menarik, penurunan Company Profile jauh lebih tajam (43,1%) karena efektivitas kompresi Brotli/Gzip lebih optimal pada fragmen-fragmen file kecil hasil pemecahan.",
     "Gambar 3.6 di atas menampilkan perbandingan Load Time pada kondisi CPU yang diperlambat 4x — skenario yang paling merepresentasikan kondisi pengguna dengan perangkat rendah. Penurunan Load Time pada SIMTA sebesar 13,0% (dari 1121,6 ms menjadi 975,8 ms) berasal dari kombinasi code splitting, lazy loading, dan kompresi Brotli/Gzip yang kini benar-benar aktif tersaji ke peramban. Company Profile turut membaik sebesar 24,5%, murni dari code splitting dan lazy loading — konfigurasi build Company Profile tidak menyertakan kompresi Brotli/Gzip, sehingga perbaikannya tidak dapat dikaitkan dengan kompresi."),

    ('Analisis: Nilai TBT pada versi standar yang mencapai 1023,0 ± 75,6 ms sudah melampaui batas toleransi Google Web Vitals (300 ms). Dengan Code Splitting, nilai TBT turun menjadi 790,8 ± 46,5 ms — meskipun masih di atas batas ideal, sudah menunjukkan perbaikan signifikan sebesar 22,7% bagi pengguna perangkat rendah. Ini berarti browser yang sebelumnya tidak bisa merespons klik selama lebih dari 1 detik, kini responsivitasnya meningkat hampir seperempat.',
     'Analisis: Nilai TBT pada versi standar yang mencapai 710,4 ± 89,2 ms sudah melampaui batas toleransi Google Web Vitals (300 ms). Dengan Code Splitting, Lazy Loading, dan kompresi, nilai TBT turun menjadi 579,0 ± 63,1 ms — meskipun masih di atas batas ideal, sudah menunjukkan perbaikan signifikan sebesar 18,5% bagi pengguna perangkat rendah.'),

    ('Perbedaan metodologi pengukuran inilah yang menyebabkan nilai absolut FCP dan LCP pada Lighthouse jauh lebih tinggi dibandingkan hasil PerformanceObserver (misalnya FCP Lighthouse 5093 ms vs FCP PerformanceObserver 1144 ms).',
     'Perbedaan metodologi pengukuran inilah yang menyebabkan nilai absolut FCP dan LCP pada Lighthouse jauh lebih tinggi dibandingkan hasil PerformanceObserver (misalnya FCP Lighthouse 4960 ms vs FCP PerformanceObserver 1103 ms).'),

    ("Gambar 3.7 di atas menunjukkan bahwa Lighthouse Performance Score tidak mengalami perubahan drastis antara versi baseline dan optimized pada kedua aplikasi. SIMTA berada di kisaran 64-66 dan Company Profile di 99-100. Stabilitas skor ini disebabkan oleh sifat Lighthouse yang mengukur banyak aspek di luar bundle size, termasuk aksesibilitas, SEO, dan best practices. Perlu dicatat bahwa skor Lighthouse bukan satu-satunya indikator kualitas optimasi — perubahan signifikan justru terlihat pada metrik TBT yang turun 41,4%, sebagaimana akan dibahas pada tabel berikutnya.",
     "Gambar 3.7 di atas menunjukkan bahwa Lighthouse Performance Score SIMTA naik cukup besar dari baseline ke optimized (56,8 menjadi 75,0, kenaikan 32,0%), sementara Company Profile nyaris tidak berubah (100 menjadi 99). Pola ini konsisten dengan hipotesis utama penelitian: manfaat code splitting dan lazy loading jauh lebih terasa pada aplikasi kompleks dengan pustaka berat, dan nyaris tidak berpengaruh pada aplikasi yang bundle awalnya sudah kecil."),

    ("Interpretasi Hasil Lighthouse SIMTA: Hasil Lighthouse menunjukkan bahwa FCP dan LCP versi optimized lebih lambat dari baseline. Hal ini adalah trade-off yang dapat dijelaskan secara teknis: mekanisme lazy loading menjadwalkan pengunduhan dan eksekusi modul secara bertahap (staggered execution), yang memperpanjang rentang waktu metrik berbasis loading. Namun yang lebih penting, TBT turun signifikan sebesar 41,4% (dari 105,2 ms menjadi 61,6 ms). Ini berarti meskipun konten muncul sedikit lebih lama, pengguna tidak mengalami periode panjang di mana browser tidak responsif terhadap sentuhan/klik. Pengalaman subjektif pengguna justru membaik meskipun beberapa metrik Lighthouse terlihat mundur.",
     "Interpretasi Hasil Lighthouse SIMTA: Berbeda dengan dugaan awal bahwa lazy loading akan memperlambat metrik berbasis loading (FCP, LCP, TTI) sebagai trade-off dari eksekusi modul yang bertahap, hasil pengukuran menunjukkan seluruh metrik Lighthouse membaik pada versi optimized — termasuk FCP, LCP, dan TTI yang pada pengukuran sebelumnya (sebelum kompresi Brotli/Gzip diperbaiki agar benar-benar tersaji ke peramban) sempat terlihat memburuk. Setelah kompresi berfungsi sebagaimana mestinya, ukuran transfer setiap chunk mengecil cukup jauh sehingga manfaat code splitting tidak lagi tertutupi oleh biaya tambahan request jaringan per chunk. Simpangan baku pada versi optimized (misalnya TBT 315,4 ± 241,5 ms) juga jauh lebih besar dibanding baseline — ini wajar karena Lighthouse mengukur seluruh rangkaian pemuatan modul dinamis yang waktunya lebih bervariasi dibanding satu berkas monolitik, namun rata-ratanya tetap menunjukkan perbaikan yang jelas."),

    ("Gambar 3.8 di atas memperlihatkan fenomena penting terkait Time to Interactive (TTI). Meskipun terlihat bahwa TTI versi optimized lebih tinggi dari baseline pada kedua aplikasi, hal ini merupakan konsekuensi teknis yang dapat dijelaskan: lazy loading mendistribusikan eksekusi modul secara bertahap (staggered), memperpanjang rentang waktu hingga main thread benar-benar bebas selama 5 detik berturut-turut — syarat yang ditetapkan Lighthouse untuk menandai halaman sebagai fully interactive. Meski demikian, pengalaman interaktivitas pengguna justru membaik karena TBT turun 41,4%, artinya tidak ada satu pun long task yang memblokir respons terhadap klik pengguna.",
     "Gambar 3.8 di atas memperlihatkan TTI SIMTA membaik dari 5566,8 ms menjadi 3964,0 ms (28,8%) — sejalan dengan perbaikan pada FCP, LCP, TBT, dan Speed Index. Artinya, pada SIMTA, optimasi tidak hanya membuat halaman lebih responsif terhadap klik (TBT turun), tetapi juga membuat main thread lebih cepat mencapai kondisi benar-benar bebas dan interaktif secara keseluruhan."),

    ("Grafik perbandingan JS Heap Memory menampilkan konsumsi memori runtime dari keempat skenario pengujian. Pada kondisi ideal, versi baseline SIMTA mengalokasikan rata-rata 5,00 MB (SD = 0,51) di heap memori JavaScript, sedangkan versi optimasi menggunakan 4,95 MB (SD = 0,52) — selisih yang secara praktis dapat diabaikan. Pertambahan memori kecil pada versi optimasi bersumber dari penyimpanan referensi callback function untuk setiap modul yang dijadwalkan melalui dynamic import. Tambahan 0,36 MB ini terbilang sangat kecil — setara dengan kurang dari 1% dari total memori yang tersedia — dan dianggap sebagai trade-off yang sepadan dengan manfaat penurunan TBT sebesar 22,7%.",
     "Grafik perbandingan JS Heap Memory menampilkan konsumsi memori runtime dari keempat skenario pengujian. Pada kondisi ideal, versi baseline SIMTA mengalokasikan rata-rata 5,09 MB (SD = 0,42) di heap memori JavaScript, sedangkan versi optimasi menggunakan 5,40 MB (SD = 0,08) — tambahan 0,31 MB. Pada kondisi CPU diperlambat, polanya konsisten: baseline 4,81 MB (SD = 0,13) vs optimized 4,92 MB (SD = 0,12), tambahan 0,11 MB. Pertambahan memori kecil dan konsisten pada versi optimasi ini bersumber dari penyimpanan referensi callback function untuk setiap modul yang dijadwalkan melalui dynamic import, termasuk modul yang dijadwalkan lewat mekanisme prefetching."),

    ("Gambar 3.9 di atas mengkonfirmasi bahwa penerapan code splitting tidak menambah beban memori yang signifikan. Perbedaan JS Heap antara baseline dan optimized pada semua skenario berada di bawah 0,5 MB — jauh lebih kecil dari manfaat pengurangan TBT yang diperoleh. Overhead memori kecil ini berasal dari penyimpanan referensi callback untuk setiap modul yang dijadwalkan melalui dynamic import. Dengan demikian, trade-off antara sedikit tambahan memori dan penurunan TBT sebesar 22,7% sangat menguntungkan, dan implementasi hybrid lazy loading dapat direkomendasikan tanpa kekhawatiran terhadap konsumsi memori berlebih.",
     "Gambar 3.9 di atas mengkonfirmasi bahwa penerapan code splitting tidak menambah beban memori yang signifikan. Perbedaan JS Heap antara baseline dan optimized pada semua skenario SIMTA berada di bawah 0,35 MB — jauh lebih kecil dari manfaat pengurangan TBT yang diperoleh (18,5%–24,9%). Dengan demikian, trade-off antara sedikit tambahan memori dan penurunan TBT yang jauh lebih besar tetap menguntungkan, dan implementasi hybrid lazy loading dapat direkomendasikan tanpa kekhawatiran terhadap konsumsi memori berlebih."),

    ("Analisis komparatif antara SIMTA dan Company Profile menghasilkan temuan yang memperkuat hipotesis utama penelitian ini tentang pengaruh tingkat kompleksitas terhadap efektivitas strategi optimasi. Pada Company Profile dalam kondisi CPU yang diperlambat, nilai TBT versi baseline tercatat sebesar 143,2 ms (SD = 8,0), yang masih berada di bawah ambang batas 200 ms standar Core Web Vitals. Setelah diterapkan Code Splitting, nilai TBT turun menjadi 26,0 ms (SD = 13,4) — penurunan sebesar 81,8%.",
     "Analisis komparatif antara SIMTA dan Company Profile menghasilkan temuan yang memperkuat hipotesis utama penelitian ini tentang pengaruh tingkat kompleksitas terhadap efektivitas strategi optimasi — dengan satu catatan metodologis penting yang perlu disampaikan secara jujur. Pada Company Profile dalam kondisi CPU yang diperlambat, nilai TBT versi baseline tercatat sebesar 66,6 ms (SD = 4,4), yang masih berada jauh di bawah ambang batas 200 ms standar Core Web Vitals. Setelah diterapkan Code Splitting, nilai TBT turun menjadi 7,6 ms (SD = 4,6) — penurunan sebesar 88,6%."),

    ('Namun penting untuk dicatat: meskipun penurunan persentase TBT pada Company Profile tampak lebih besar (81,8% vs 22,7% pada SIMTA), konteks penggunaannya berbeda. Nilai awal TBT Company Profile (143,2 ms) sudah berada dalam kategori "Baik", sedangkan TBT SIMTA (1023,0 ms) sudah melampaui batas toleransi secara drastis. Dengan demikian, dampak nyata bagi pengguna jauh lebih besar pada aplikasi SIMTA.',
     'Sebagaimana SIMTA (18,5%–24,9%), TBT Company Profile juga konsisten membaik, meski nilai awalnya sudah tergolong baik sehingga dampak praktis bagi pengguna jauh lebih kecil dibanding SIMTA yang TBT baseline-nya (710,4 ms) sudah melampaui batas toleransi secara drastis.'),

    ('Di sisi lain, metrik FCP pada Company Profile justru mengalami degradasi dari 373,6 ms menjadi 486,4 ms pada kondisi throttled — sebuah peningkatan negatif sebesar 30,2%. Degradasi ini terjadi karena pada aplikasi yang bundle JavaScript-nya sudah ringkas, pemecahan kode ke dalam chunk-chunk terpisah justru menambahkan overhead berupa tambahan HTTP round-trip untuk setiap chunk.',
     'Catatan metodologis mengenai FCP Company Profile: pengukuran awal penelitian ini pada kondisi throttled sempat mencatat FCP baseline 373,6 ms dan optimized 486,4 ms — memberi kesan code splitting men-degradasi FCP sebesar 30,2% pada aplikasi sederhana. Pengukuran ulang dengan metodologi yang telah diperbaiki mencatat FCP baseline 508,0 ms dan optimized 508,8 ms — praktis tidak berbeda (selisih 0,8 ms, jauh di dalam rentang simpangan baku ±15–22 ms kedua kelompok). Ini menunjukkan bahwa pada aplikasi sesederhana Company Profile, dengan skala waktu muat hanya ratusan milidetik, PerformanceObserver dari satu sesi 5 repetisi terlalu rentan terhadap variasi kondisi mesin pengujian untuk dijadikan dasar klaim persentase yang presisi. Bukti yang lebih dapat diandalkan datang dari Lighthouse, yang simpangan bakunya jauh lebih kecil dan konsisten pada dua kali pengukuran terpisah: FCP Company Profile memburuk sekitar 15,9%–16,7% dan LCP sekitar 18,0%–17,9% pada versi optimized, baik sebelum maupun sesudah pengukuran ulang. Kesimpulan bahwa code splitting dapat memberi overhead kecil pada aplikasi sederhana tetap didukung data, tetapi bersandar pada bukti Lighthouse yang stabil — bukan pada angka 30,2% dari PerformanceObserver yang ternyata tidak reproducible.'),

    ('Kesimpulan dari tabel ini: teknik Hybrid Code Splitting sangat efektif untuk aplikasi yang kompleks dan banyak menggunakan pustaka besar, tetapi tidak diperlukan — bahkan bisa merugikan FCP — untuk website sederhana. Rekomendasi strategis: terapkan code splitting hanya ketika bundle awal sudah melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak dibutuhkan di halaman utama.',
     'Kesimpulan dari tabel ini: teknik hybrid code splitting, lazy loading, dan kompresi sangat efektif untuk aplikasi yang kompleks dan banyak menggunakan pustaka besar (naik di semua metrik, termasuk Lighthouse Score +32,0%), tetapi manfaatnya tipis — dan pada metrik Lighthouse yang stabil justru sedikit negatif pada FCP/LCP — untuk aplikasi sederhana seperti Company Profile. Rekomendasi strategis tidak berubah: terapkan code splitting dan lazy loading hanya ketika bundle awal sudah melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak dibutuhkan di halaman utama.'),

    ("Efektivitas Code Splitting dalam mengurangi ukuran bundle awal (SIMTA). Dengan memisahkan pustaka-pustaka besar (seperti Chart.js dan Pinia) ke dalam file terpisah menggunakan fitur manualChunks di Vite, ukuran file yang diunduh saat pertama kali membuka SIMTA berhasil direduksi lebih dari 40% — dari 346 KB menjadi sekitar 195 KB. Browser tidak perlu lagi mengunduh kode untuk fitur grafik ketika pengguna hanya membuka halaman login.",
     "Efektivitas Code Splitting dan kompresi dalam mengurangi beban muat awal (SIMTA). Dengan memisahkan pustaka-pustaka besar (Vue/Pinia dan Chart.js) ke dalam chunk terpisah menggunakan fitur manualChunks di Vite, ditambah kompresi Brotli/Gzip pada setiap chunk, ukuran transfer jaringan berkurang signifikan dibanding satu berkas monolitik 346 KB pada baseline. Manfaatnya bukan dari menunda pengunduhan Chart.js — Dashboard sebagai halaman pertama tetap menampilkan grafik sejak awal — melainkan dari pengunduhan paralel beberapa chunk kecil dan ukuran transfer yang lebih kecil berkat kompresi."),

    ("Hybrid Lazy Loading efektif mengurangi Total Blocking Time (TBT). Meskipun beberapa metrik berbasis loading (FCP, LCP) sedikit bertambah pada Lighthouse karena overhead resolusi rute dinamis, manfaat nyata terlihat pada TBT yang berkurang signifikan: turun 22,7% pada kondisi CPU normal (PerformanceObserver) dan 41,4% menurut simulasi Lighthouse. Ini berarti browser lebih responsif terhadap interaksi pengguna meskipun konten muncul sedikit lebih lambat. Trade-off ini menguntungkan pengguna karena responsivitas sering dirasakan lebih penting dari kecepatan kemunculan konten pertama.",
     "Hybrid Lazy Loading, Code Splitting, dan kompresi efektif mengurangi Total Blocking Time (TBT) tanpa trade-off berarti pada metrik lain. Seluruh metrik yang diukur pada SIMTA — FCP, LCP, TTI, Speed Index, dan TBT — membaik pada versi optimized, baik lewat PerformanceObserver maupun Lighthouse. TBT turun 18,5%–24,9% menurut PerformanceObserver dan 30,6% menurut Lighthouse; Lighthouse Performance Score naik 32,0% (56,8 menjadi 75,0). Tidak ditemukan indikasi bahwa mekanisme pemuatan bertahap memperlambat metrik loading lain pada aplikasi ini."),

    ("Manfaat terbesar terlihat pada perangkat dengan spesifikasi rendah. Ketika diuji pada kondisi CPU diperlambat 4x, TBT SIMTA yang awalnya 1023,0 ms (melampaui batas toleransi 300 ms secara drastis) berhasil diturunkan menjadi 790,8 ms — perbaikan 22,7%. Ini berarti pengguna dengan perangkat lama yang mengakses SIMTA mengalami periode browser tidak responsif yang jauh lebih singkat.",
     "Manfaat terbesar terlihat pada perangkat dengan spesifikasi rendah. Ketika diuji pada kondisi CPU diperlambat 4x, TBT SIMTA yang awalnya 710,4 ms (melampaui batas toleransi 300 ms) berhasil diturunkan menjadi 579,0 ms — perbaikan 18,5%. Ini berarti pengguna dengan perangkat lama yang mengakses SIMTA mengalami periode browser tidak responsif yang lebih singkat."),

    ("Teknik ini tidak cocok untuk semua jenis website (Diminishing Returns). Pada Company Profile (website sederhana), FCP justru mengalami degradasi 30,2% pada kondisi CPU lambat karena overhead HTTP request tambahan dari chunk-chunk yang dipecah. Penelitian ini membuktikan bahwa strategi optimasi harus mempertimbangkan tingkat kompleksitas aplikasi sebagai faktor penentu. Panduan praktis: terapkan code splitting hanya jika bundle awal sudah melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak digunakan di halaman pertama.",
     "Teknik ini tidak cocok untuk semua jenis website (Diminishing Returns). Pada Company Profile (website sederhana), data Lighthouse yang stabil menunjukkan FCP dan LCP sedikit memburuk (masing-masing sekitar 16% dan 18%) pada versi optimized, akibat overhead beberapa request HTTP tambahan untuk chunk yang terpisah — biaya yang tidak sebanding pada aplikasi tanpa pustaka berat. (Pengukuran awal sempat mencatat degradasi FCP hingga 30,2% lewat PerformanceObserver; pengukuran ulang menunjukkan angka tersebut tidak reproducible pada instrumen itu, sehingga kesimpulan ini disandarkan pada bukti Lighthouse yang terbukti stabil.) Penelitian ini membuktikan bahwa strategi optimasi harus mempertimbangkan tingkat kompleksitas aplikasi sebagai faktor penentu. Panduan praktis: terapkan code splitting hanya jika bundle awal sudah melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak digunakan di halaman pertama."),
]

# --------------------------------------------------------------- tabel ----
# (header_row_signature, {(row_index, col_index): (old_text, new_text)})
TABLE_EDITS = [
    (("Aplikasi", "Baseline (ms)", "Optimized (ms)", "Selisih"), {
        (1, 1): ("1144,0 ± 17,1", "1103,2 ± 179,4"),
        (1, 2): ("881,6 ± 35,5", "842,4 ± 20,0"),
        (1, 3): ("-262,4 ms", "-260,8 ms (-23,6%)"),
        (2, 1): ("367,2 ± 16,2", "511,2 ± 31,7"),
        (2, 2): ("364,0 ± 44,1", "483,2 ± 18,8"),
        (2, 3): ("-3,2 ms", "-28,0 ms (-5,5%)"),
    }),
    (("Aplikasi", "Baseline (ms)", "Optimized (ms)", "Selisih", "%"), {
        (1, 1): ("111,8 ± 41,0", "139,2 ± 77,0"),
        (1, 2): ("137,2 ± 50,7", "104,6 ± 34,6"),
        (1, 3): ("+25,4 ms", "-34,6 ms"),
        (1, 4): ("-22,7%", "-24,9%"),
    }),
    (("Metrik (SIMTA)", "Baseline (CPU Lambat)", "Optimized (CPU Lambat)", ""), {
        (1, 1): ("1523,2 ± 38,7 ms", "1371,2 ± 49,4 ms"),
        (1, 2): ("1182,4 ± 24,9 ms", "1134,4 ± 47,1 ms"),
        (2, 1): ("1023,0 ± 75,6 ms", "710,4 ± 89,2 ms"),
        (2, 2): ("790,8 ± 46,5 ms", "579,0 ± 63,1 ms"),
    }),
    (("Metrik", "Baseline Normal", "Optimized Normal", "Baseline Throttled", "Optimized Throttled"), {
        # tabel 3.4 SIMTA (baris 1=FCP, 2=LCP, 3=TBT, 4=Load Time, 5=JS Heap)
        (1, 1): ("1144,0 ± 17,1", "1103,2 ± 179,4"), (1, 2): ("881,6 ± 35,5", "842,4 ± 20,0"),
        (1, 3): ("1523,2 ± 38,7", "1371,2 ± 49,4"), (1, 4): ("1182,4 ± 24,9", "1134,4 ± 47,1"),
        (2, 1): ("1144,0 ± 17,1", "1103,2 ± 179,4"), (2, 2): ("881,6 ± 35,5", "842,4 ± 20,0"),
        (2, 3): ("1523,2 ± 38,7", "1371,2 ± 49,4"), (2, 4): ("1182,4 ± 24,9", "1134,4 ± 47,1"),
        (3, 1): ("111,8 ± 41,0", "139,2 ± 77,0"), (3, 2): ("137,2 ± 50,7", "104,6 ± 34,6"),
        (3, 3): ("1023,0 ± 75,6", "710,4 ± 89,2"), (3, 4): ("790,8 ± 46,5", "579,0 ± 63,1"),
        (4, 1): ("726,0 ± 12,1", "694,2 ± 22,2"), (4, 2): ("743,6 ± 30,0", "688,6 ± 17,6"),
        (4, 3): ("1095,2 ± 26,9", "1121,6 ± 218,5"), (4, 4): ("1031,8 ± 64,6", "975,8 ± 45,5"),
        (5, 1): ("5,00 ± 0,51", "5,09 ± 0,42"), (5, 2): ("4,95 ± 0,52", "5,40 ± 0,08"),
        (5, 3): ("4,53 ± 0,17", "4,81 ± 0,13"), (5, 4): ("4,89 ± 0,14", "4,92 ± 0,12"),
    }),
]

TABLE_EDITS_CP_PERF = (
    ("Metrik", "Baseline Normal", "Optimized Normal", "Baseline Throttled", "Optimized Throttled"), {
        (1, 1): ("367,2 ± 16,2", "511,2 ± 31,7"), (1, 2): ("364,0 ± 44,1", "483,2 ± 18,8"),
        (1, 3): ("373,6 ± 57,6", "508,0 ± 15,2"), (1, 4): ("486,4 ± 64,7", "508,8 ± 22,4"),
        (2, 1): ("367,2 ± 16,2", "511,2 ± 31,7"), (2, 2): ("364,0 ± 44,1", "483,2 ± 18,8"),
        (2, 3): ("373,6 ± 57,6", "508,0 ± 15,2"), (2, 4): ("486,4 ± 64,7", "508,8 ± 22,4"),
        (3, 3): ("143,2 ± 8,0", "66,6 ± 4,4"), (3, 4): ("26,0 ± 13,4", "7,6 ± 4,6"),
        (4, 1): ("44,0 ± 3,5", "58,8 ± 7,6"), (4, 2): ("35,6 ± 3,7", "45,2 ± 5,5"),
        (4, 3): ("171,2 ± 15,5", "140,4 ± 7,4"), (4, 4): ("97,4 ± 7,3", "106,0 ± 13,6"),
        (5, 1): ("1,88 ± 0,02", "1,87 ± 0,00"), (5, 2): ("1,89 ± 0,00", "1,90 ± 0,00"),
        (5, 3): ("1,87 ± 0,00", "1,88 ± 0,02"), (5, 4): ("1,90 ± 0,00", "1,90 ± 0,00"),
    })

TABLE_EDITS_LH_SIMTA = (
    ("Metrik", "Baseline", "Optimized", "Selisih"), {
        (1, 1): ("66,2 ± 0,4", "56,8 ± 4,2"), (1, 2): ("64,0 ± 0,0", "75,0 ± 13,3"), (1, 3): ("-2,2", "+18,2 (+32,0%)"),
        (2, 1): ("5093,0 ± 42,4", "4960,4 ± 56,4"), (2, 2): ("5434,8 ± 37,1", "3250,2 ± 404,6"), (2, 3): ("+341,8", "-1710,2 (-34,5%)"),
        (3, 1): ("5198,4 ± 40,7", "5228,4 ± 60,6"), (3, 2): ("5909,8 ± 40,1", "3790,8 ± 774,3"), (3, 3): ("+711,4", "-1437,6 (-27,5%)"),
        (4, 1): ("5273,4 ± 39,9", "5566,8 ± 181,9"), (4, 2): ("5909,8 ± 40,1", "3964,0 ± 918,3"), (4, 3): ("+636,4", "-1602,8 (-28,8%)"),
        (5, 1): ("105,2 ± 8,1", "454,8 ± 152,0"), (5, 2): ("61,6 ± 3,7", "315,4 ± 241,5"), (5, 3): ("-43,6 (-41,4%)", "-139,4 (-30,6%)"),
        (6, 1): ("5588,6 ± 37,8", "4960,4 ± 56,4"), (6, 2): ("5855,8 ± 9,3", "3265,2 ± 386,8"), (6, 3): ("+267,2", "-1695,2 (-34,2%)"),
    })

TABLE_EDITS_LH_CP = (
    ("Metrik", "Baseline", "Optimized", "Selisih"), {
        (2, 1): ("1352,8 ± 0,4", "1361,4 ± 16,8"), (2, 2): ("1579,0 ± 1,1", "1578,2 ± 1,0"), (2, 3): ("+226,2", "+216,8 (+15,9%)"),
        (3, 1): ("1531,4 ± 2,8", "1528,8 ± 8,2"), (3, 2): ("1804,6 ± 1,2", "1804,4 ± 1,4"), (3, 3): ("+273,2", "+275,6 (+18,0%)"),
        (4, 1): ("1560,2 ± 5,6", "1530,6 ± 7,4"), (4, 2): ("1804,6 ± 1,2", "1804,4 ± 1,4"), (4, 3): ("+244,4", "+273,8 (+17,9%)"),
        (5, 1): ("7,4 ± 5,6", "0,0 ± 0,0"), (5, 3): ("-7,4", "0,0"),
        (6, 1): ("1352,8 ± 0,4", "1361,4 ± 16,8"), (6, 2): ("1579,0 ± 1,1", "1578,2 ± 1,0"), (6, 3): ("+226,2", "+216,8 (+15,9%)"),
    })

TABLE_EDITS_TABEL38 = (
    ("Metrik", "SIMTA Improvement", "CP Improvement", "Keterangan"), {
        (1, 1): ("+22,4%", "+17,3%"), (1, 2): ("-30,2% (turun)", "-0,2% (~0, dalam noise)"),
        (1, 3): ("SIMTA membaik, CP memburuk", "SIMTA membaik jelas; CP tidak berbeda signifikan (lihat catatan Lighthouse di bawah)"),
        (2, 1): ("+22,7%", "+18,5%"), (2, 2): ("+81,8%", "+88,6%"),
        (3, 1): ("+5,8%", "+13,0%"), (3, 2): ("+43,1%", "+24,5%"),
        (4, 1): ("-7,9% (overhead)", "-2,3% (overhead)"), (4, 2): ("-1,6%", "-1,1%"),
        (5, 1): ("-3,3%", "+32,0%"), (5, 2): ("-1,0%", "-1,0%"),
        (5, 3): ("Perubahan minimal (karena trade-off TTI)", "SIMTA naik besar; CP nyaris tidak berubah"),
    })


def ganti_di_paragraf(par, cari, ganti):
    runs = par.runs
    if not runs:
        return False
    penuh = ''.join(r.text for r in runs)
    idx = penuh.find(cari)
    if idx == -1:
        return False
    batas, pos = [], 0
    for r in runs:
        batas.append((pos, pos + len(r.text), r))
        pos += len(r.text)
    akhir = idx + len(cari)
    sudah_ditulis = False
    for mulai_r, akhir_r, r in batas:
        if akhir_r <= idx or mulai_r >= akhir:
            continue
        sisa_kiri = r.text[:max(0, idx - mulai_r)]
        sisa_kanan = r.text[max(0, akhir - mulai_r):] if akhir_r > akhir else ''
        if not sudah_ditulis:
            r.text = sisa_kiri + ganti + sisa_kanan
            sudah_ditulis = True
        else:
            r.text = sisa_kiri + sisa_kanan
    return True


def semua_paragraf_dokumen(doc):
    for p in doc.paragraphs:
        yield p


def terapkan_tabel(doc, ganti_list_of_tuples):
    """Beberapa tabel di naskah ini berbagi header yang persis sama (mis.
    Tabel 3.4 SIMTA dan Tabel 3.5 Company Profile). `_dipakai` melacak tabel
    (berdasarkan id objek) yang sudah dipasangkan ke satu edit-set, supaya
    pencarian berikutnya dengan header sama lanjut ke tabel berikutnya,
    bukan menimpa tabel yang sama dua kali."""
    hasil = {'cocok': 0, 'tidak': []}
    _dipakai = set()
    for header_sig, edits in ganti_list_of_tuples:
        table_found = None
        for t in doc.tables:
            if len(t.rows) == 0 or id(t) in _dipakai:
                continue
            header_cells = tuple(c.text.strip() for c in t.rows[0].cells)
            if header_cells[:len(header_sig)] == header_sig:
                table_found = t
                _dipakai.add(id(t))
                break
        if table_found is None:
            hasil['tidak'].append(('TABEL TIDAK DITEMUKAN', header_sig))
            continue
        for (r, c), (old, new) in edits.items():
            try:
                cell = table_found.rows[r].cells[c]
            except IndexError:
                hasil['tidak'].append((f'sel ({r},{c}) di luar jangkauan', header_sig))
                continue
            done = False
            for p in cell.paragraphs:
                if ganti_di_paragraf(p, old, new):
                    done = True
                    break
            if done:
                hasil['cocok'] += 1
            else:
                hasil['tidak'].append((f'({r},{c}) "{old}" -> tidak ketemu di sel "{cell.text}"', header_sig))
    return hasil


def main():
    if not os.path.exists(BACKUP):
        shutil.copy2(DOCX, BACKUP)
        print('Cadangan dibuat:', os.path.basename(BACKUP))

    doc = Document(DOCX)

    # 1. prosa
    hitung = {c: 0 for c, _ in GANTI}
    for par in semua_paragraf_dokumen(doc):
        for cari, ganti in GANTI:
            if ganti_di_paragraf(par, cari, ganti):
                hitung[cari] += 1

    print('Hasil penggantian prosa:')
    for cari, jml in hitung.items():
        status = 'OK  ' if jml else 'TIDAK KETEMU'
        print(f'  [{status}] {jml}x  {cari[:70]}...')

    # 2. tabel
    semua_tabel = TABLE_EDITS + [TABLE_EDITS_CP_PERF, TABLE_EDITS_LH_SIMTA, TABLE_EDITS_LH_CP, TABLE_EDITS_TABEL38]
    hasil = terapkan_tabel(doc, semua_tabel)
    print(f"\nHasil penggantian tabel: {hasil['cocok']} sel berhasil diganti.")
    if hasil['tidak']:
        print('Sel yang GAGAL diganti (perlu dicek manual):')
        for msg, sig in hasil['tidak']:
            print('  -', msg, '| tabel:', sig)

    doc.save(DOCX)
    print('\nSelesai. Disimpan ke', os.path.basename(DOCX))


if __name__ == '__main__':
    main()

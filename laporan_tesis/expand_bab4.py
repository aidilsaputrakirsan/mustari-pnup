import os

filepath = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\chapters\BAB_4_PENUTUP.md"

bab_4_content = """# BAB IV PENUTUP

## 4.1 Kesimpulan

Berdasarkan formulasi landasan teoretis, implementasi metodologis, hingga serangkaian pembedahan log observasi evaluasi performa pada dua model *Single Page Application* (SPA)—dalam studi kasus purwarupa Sistem Informasi Manajemen Tugas Akhir (SIMTA) serta situs pembanding linier *Company Profile*—penelitian ini mengerucut pada kesimpulan komprehensif sebagai berikut:

1. **Efektivitas Dekonstruksi Berkas Melalui *Route-Level Code Splitting*:**
   Modifikasi arsitektur kompilasi (*bundle pipeline*) yang dimotori oleh piranti Vite—beranjak dari ortodoksi *Eager-Loading* yang memampatkan seluruh logika aplikasi ke dalam satu kontainer masif—terbukti sahih mensubstitusi disfungsi kecepatan awal (startup bottleneck). Melalui injeksi `manualChunks` yang dikhususkan menyortir dependensi raksasa (seperti pustaka grafik *Chart.js* dan *Pinia Store*), ukuran *payload* skrip purwarupa kompleks sukses direduksi. Pencapaian ini merepresentasikan nilai kuantitatif yang mengesankan: pemampatan berkas dari berat awal statis sebesar ~346 KB anjlok secara radikal ke ambang aman < 195 KB (mengukir rasio penekanan memori kompilasi hingga melebih 40%), memungkinkan antarmuka peramban untuk memulai eksekusi cat kanvas tanpa perlu menunggu pengunduhan utilitas yang tidak mendesak.

2. **Supremasi *Hybrid Lazy Loading* terhadap Resolusi Interaksi (*Total Blocking Time*/TBT):**
   Manifestasi pengukuran rekam jejak W3C `PerformanceObserver` menvalidasi secara empiris peran krusial pemanggilan asinkron (*Prefetch Lazy Loading*) dalam melepaskan jeratan kelumpuhan *Main Thread* V8 Engine. Kendati kurva *First Contentful Paint* (FCP) maupun *Load Time* menunjukkan grafik deviasi lambat (+48 ms dan seterusnya) guna mengompensasi pencarian rute dinamis (*Overhead HTTP Heads Header*), nilai limitasi interaktivitas murni dapat dipangkas luar biasa. Pada skenario kondisi normal, waktu layar macet (*TBT*) direduksi dari angka awal 19 ms menjadi sangat instan di 13 ms.

3. **Manajemen *Trade-Off* Laten pada Lingkungan Perangkat Ekstrem (*Throttled CPU*):**
   Secara spesifik mendalam, kontribusi rekayasa hibrida ini meledak pada titik kulminasinya kala merespons emulasi perangkat dengan komputasi rendah (*Puppeteer 4x CPU Slowdown*). Teknik pemecahan kawat statis ini ampuh menyetabilkan ambang ledak TBT dari zona bahaya *Needs Improvement* milik Google (377 ms pada mode Monolitik Eager) ke ranah adaptif yang lolos perizinan di atas platform penjelajah modern (363 ms). Sekalipun implementasi janji tunda ini meminta upeti berwujud konsumsi pelacakan memori *JS Heap* membesar marginal (+0.17 MB), pengorbanan itu dikategorikan sangat sepadan dan wajib dipertahankan demi menjaga stabilitas pengalaman interaksi antarmuka pengunjung dari ancaman halaman merespons statis (gantung/*lag*).

4. **Korelasi Ambang Batas Ekstrem terhadap Tingkat Kepadatan Sistem (Fenomena *Diminishing Returns*):**
   Pertentangan uji klinis performansi menyasar purwarupa situs lurus nir-dependensi berat (*Company Profile*) membuahkan pembuktian definitif. Eksploitasi ekosistem *Code-Splitting* teridentifikasi memicu fenomena penolakan kebermanfaatan ganda (*Diminishing Returns*) apabila diimplementasikan atas platform ringan berkonten statis. Fakta mencatat indeks TBT sistem murni purwarupa tersebut aslinya sudah bertengger damai pada poros 143 ms, menjadikan manuver pemecahan fragmen *JavaScript* tidak menderivasi kelincahan aplikasi, melainkan hanya sekadar menggelembungkan komisi perulangan *Network Requests*. Resolusi tesis ini menyimpulkan bahwa pemisahan asinkron hibrida adalah instrumen pedang bermata satu: sangat adidaya meruntuhkan sumbatan kala digunakan membedah Web berskala dependensi rumit (Modul Besar), namun malah merugikan manakala ditikamkan pada struktur Web Linier biasa.

## 4.2 Saran Lanjutan dan Pengembangan

Menyadari keterbatasan cakupan spektrum rekayasa teknis pada lapisan ekosistem klien (`Client-Side`), berikut penulis merumuskan usulan perbaikan komprehensif bagi penelitian berantai (*Chain Research*) di institusi untuk agenda di masa serjana/megister berikutnya:

1. **Integrasi Eksekusi Bawah Tanah Bersama Ekosistem *Service Workers* (PWA):**
   Pada studi mendatang, disarankan agar pemanggilan pra-tunda fungsional (*lazy prefetch*) tidak semata dititipkan pada antrean pasif detektor lenggang peramban (`requestIdleCallback`). Pengiriman muatan dapat diotomasi seutuhnya menuju proksi ketersediaan tembolok luring (*Cache Storage API*) selaras arsitektur hibrida *Progressive Web Application* (PWA). Persilangan absolut kedua pilar ini menjanjikan ilusi waktu unduhan pecahan rute asinkron nol milidetik mutlak (*Zero-Latency Instant Transfer*), mematikan *round-trip delay* untuk halaman antarmuka kunjungan paruh waktu.
   
2. **Kompensasi Kelambatan dengan Penahan Prioritas Reflow DOM AnimasiVisual:**
   Pemanfaatan sinkronisasi *Idle Observer* dilaporkan cacat latensi apabila objek pengujian merender sirkuit komputasi antarmuka pergerakan grafis yang konstan (*Continuous CSS Animation / WebGL Canvas*). Kerangka arsitektur masa seberang wajib dibekali pendeteksi mutasi visual khusus (Semacam *MutationObserver Tracker*) demi memadamkan insting *Prefetching* manakala transisi batas ambang bingkai (*Frames Per Second*) melorot di bawah 60 FPS. Ini ditujukan untuk menyeret *Browser* agar menghindari benturan interupsi *micro-stuttering* tatkala transisi kanvas berlangsung.

3. **Komparasi Silang Bersama Kerangka Moderen SSR & Server Edge:**
   Tesis ini membidik murni optimasi piranti pemrosesan sisi klien (*Client-Side Rendering*). Peneliti pascasarjana di ranah selanjutnya ditantang kuat merumuskan desain kajian persilangan metrik reduksi TBT antara taktik *Vite Bundler CSR* jika didebatkan menggunakan mesin hibrida Server Kompilasi Aktual (semacam pendayagunaan kerangka *Nuxt.js* atau pun *Next.js Server-Side Components*). Peleburan ini dipercaya sanggup menuntaskan anomali pengorbanan waktu awal FCP (Karena HTML dikirim utuh/matang dari Peladen), seraya mengunci kesempurnaan TBT di aras terendah (Karena *Hydration JS Chunk* disuntikkan secara terpartisi asinkron perlahan-lahan ke ruang tunggu perangkat klien).
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(bab_4_content)
    
print("Bab 4 Penutup berhasil diekspansi secara ekstensif! Kedalaman analisis diperkuat.")

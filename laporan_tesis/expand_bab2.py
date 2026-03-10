import os

filepath = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\chapters\BAB_2_METODE_PENELITIAN.md"

bab_2_content = """# BAB II METODE PENELITIAN DAN LANDASAN TEORI

## 2.1 Landasan Teori

Berdasarkan kajian pendahuluan dan rumusan masalah yang ditetapkan, kerangka penelitian ini bersandar pada sejumlah teori fondasional di bidang rekayasa perangkat lunak web. Teori-teori ini berfungsi sebagai pisau bedah analitik untuk menguraikan kompleksitas kinerja *Single Page Application* (SPA) dan efektivitas intervensi teknik kompilator.

### 2.1.1 Arsitektur *Single Page Application* dan *Virtual DOM*
Aplikasi Laman Tunggal (*Single Page Application/SPA*) merepresentasikan loncatan revolusioner dalam ekosistem desain antarmuka web. Pendekatan ini melepaskan diri dari paradigma pemuatan halaman tradisional (*Multi-Page Application*) dengan cara mentransfer beban kerja konstruksi antarmuka (rendering UI) serta fungsionalitas pengurutan layar (*routing*) sepenuhnya dari peladen menuju ranah *Browser* milik pengguna (Batool et al., 2021). Secara topologis, peramban klien hanya akan mengunduh sehelai dokumen struktur statis—biasanya dibaptis dengan nama `index.html`—yang berfungsi sebagai raga kosong atau bingkai dasar (*shell*) pada saat persentuhan *hyperlink* awal terjadi.

Keunggulan SPA ditopang teguh oleh konsep *Virtual-DOM (Document Object Model)*. Ekosistem kerangka kerja seperti *Vue.js* tidak memanipulasi *DOM* pohon hierarki HTML secara kasar yang terkenal lelet dan rakus daya komputasi; sebaliknya, memori *JavaScript* menyimpan representasi maya komprehensif dari *DOM* tersebut di latar belakang. Ketika terjadi perubahan kondisi data dari klien (semisal pengguna mengetik sebaris input atau API peladen memuntahkan merespons JSON baru), *Vue.js* akan terlebih dulu mengonstruksi *Virtual DOM* baru, lalu memperhitungkan selisih perbedaan mutasinya (*Diffing/Patching Algorhytm*) terhadap susunan *Virtual DOM* terdahulu. Hasil pembeda matematis tesebut barulah dilunturkan ke dalam *Real-DOM* (DOM fisik) peramban. Pembaruan bedah presisi inilah yang sanggup mengurangi ongkos siklus *repaint* dan *reflow* layar monitor secara parsial tanpa mewajibkan pemuatan utuh halaman (Zheng & Li, 2022). Sayangnya, mekanisme cerdas dan reaktif ini membutuhkan harga mahal: Kebutuhan kapasitas berkas JavaScript (*bundler size*) yang harus diunduh dan diparsing di awal sebelum *Virtual DOM* dapat aktif.

### 2.1.2 Kompilasi Kawat JavaScript dan Pemrosesan *V8 Engine / Webkit*
Berkas raksasa *JavaScript* SPA tidak dapat secara magis terwujud menjadi antarmuka visual peramban tanpa bantuan sang penterjemah sintaks: *JavaScript Engine*. Konsep eksekusi peramban mutakhir (Bermesin Google V8 Chromium, SpiderMonkey Firefox, atau Webkit Safari) bersandar kuat pada siklus hidup leksikal (*Lexical Lifecycle Execution*) yang dirumuskan ketat sesuai konsensus algoritma JIT (*Just In Time Compiler*) (Hasanuddin, 2021). 

Berbeda dengan bahasa kompilasi absolut murni seperti C++ atau Java yang memproduksi *byte-code binary* matang sebelum diantarkan kepada komputer peramban, *JavaScript* di ranah klien diunduh berupa kode sumber mentah (*abstract format*). Langkah demi langkah peramban wajib merekonstruksinya lewat serangkaian tahapan intensif:
1. **Resolution & Downloading:** Peramban menjalin kontak *Transport Control Protocol* (TCP) via *HTTP Request* menuju CDN peladen penampung sistem guna mengunduh bongkahan fail. Di tahap kompilasi konvensional (*Eager-Loading*), bongkahan fail ini terkompresi di satu struktur `.js` raksasa yang menyita durasi panjang untuk diterima utuh oleh jaringan.
2. **Lexical Parsing & AST:** Susunan kata-kata *JavaScript* diurai silabel per silabel (Tokenisasi) oleh komponen *parser* demi membentuk sintaks logis *Abstract Syntax Tree (AST)*. Pemrosesan rumit sintaks ini seratus persen menyedot kemampuan inti (Thread tunggal / *Main Thread*) unit pemroses prosesor klien.
3. **Ignition Interpreter & TurboFan JIT Compilation:** Format pepohonan logika abstrak disulap oleh *engine* peramban menjadi struktur mesin level menengah, yang selanjutnya digodok menjadi bahasa pelatuk mesin biner yang sanggup diintervensi oleh sistem operasi gawai perangkat pengguna.
4. **Execution & Memory Allocation:** Seluruh fungsi, deklarasi peubah, maupun panggilan pustaka eksternal (*Chart.js*, dan state *Pinia*) ditempatkan pada blok-lokasi alokasi RAM peramban (*JS Heap*), lantas kode reaktif *Vue* berhak mulai menggambar (*Painting*) layar di *Frame-buffer* monitor operator.

Dikarenakan arsitektur pembangun eksekusi bawaan *JavaScript Client* berifat *Single-Threaded* (tersusun lurus dari atas ke bawah tanpa paralel komputasi pada *thread browser*), segala gempuran penguraian file JS raksasa yang masuk di urutan inisial pertama akan memblokir siklus komputasi dari menangani interaksi penting lainnya (Amenta & Castellani, 2019). Fenomena ini dikenal dengan sumbatan benang penyula (*Event Loop Blocking*).

### 2.1.3 Mekanika Transmisi Asinkronus dan *Event Loop*
Meresahkan hakikat ketergantungan pada *Single-Thread*, ranah arsitektur peramban melengkapi persenjataannya melalui piranti bawaan bernama *Web APIs*, selaras dengan antrean fungsi delegasi penundaan eksekusi yang dijuluki *Event Loop* (Choi & Choi, 2020). *Event Loop* adalah manifestasi penjaga gawang (*Supervisor*) sistem yang tak pernah jeda memonitor antrean tumpukan perintah sinkronus (*Call Stack*) maupun perintah asinkron yang dititipkan terpisah pada keranjang peramban (*Callback/Microtask Queue*).

Mekanika transmisi asinkron merupakan roh dasar yang menopang efektivitas *Single Page Application* maupun intervensi skrip pemecah kompilasi (*Lazy Loading Chunk*). Melalui jaring struktur *Promises* JavaScript `(() => import(...).then(...))`, aplikasi web menyingkirkan fungsi raksasa semacam pengunduhan modul "Daftar Dosen" beserta interaksi *database*-nya dari blokade urutan tumpukan eksekusi antarmuka urutan prioritas awal (*Main thread stack*). Modul berat berstatus asinkron ini diparkir secara cerdik di bilik ruang tunggu (*Callback Queue*). Segera usai layar antarmuka dasar selesai tergambar di monitor (*Call stack* kosong), sang *Event Loop* baru mengomandoi pemanggilan antrian tunggu tersebut untuk ditarik masuk mengeksekusi sisa sintaks tanpa membekukan layar (W3C, 2022). 

### 2.1.4 Arsitektur *Virtual Bundler (Vite)* dan Fragmentasi *Code Splitting* 
Ekosistem pengembangan modern mengusir dominasi arsitektur penyatuan kompilasi kuno (termasuk *Webpack* klasik) dengan mempersembahkan kompilator modul Hibrida yang efisien bertaraf mutakhir, *Vite.js*. Dinahkodai lewat arsitektur rakitan balik *Rollup.js*, kompilasi masa pra-produksi (*Build-Time*) Vite merangkai ikatan statis modul *JavaScript* menjadi sebuah representasi Peta Ranting Pohon (*Dependency Graph*) berpedoman pada format tata bahasa murni *ESModules (ESM)* (Zheng & Li, 2022).

Dalam kondisi alami (*Eager default*), Vite meringkas seluruh simpul pohon (*Entry Point Modules*) yang dirakit oleh pakar baris pemograman menjadi berkumpulan fail ringkas padat `vendor.js` berstempel waktu (*Hash*). Intervensi arsitektural terjadi melalui sintaks rekayasa pisau bedah *Code Splitting* di akar *Router Vue*. Pendekatan fragmentasi berlevel sub-halaman (*Route-level Chunking*) dideskripsikan memecah ikatan batang pohon kompilasi Vite tersebut ke tingkat cabang, melokalisir impor *Library Pinia, Dashboard*, maupun *Form Bimbingan* ke wujud puluhan ekstensi keping terpisah tak bersinergi absolut (*Isolated Async Chunks*). 

Meneruskan skema pemisahan (*Chunking*), arsitektur hibrida mendayagunakan rutinitas pelacakan waktu jeda layar (`window.requestIdleCallback`) guna mendelegasikan perintah tebak-awal pengunduhan berkas kepingan tersebut di sela-sela relaksasi komputasi *CPU*. Manuver perampasan sela waktu rahasia ini diistilahkan sebagai taktik *Prefetching Lazy Load*, perisai utama penyusutan letupan *Network-Round-Trips* selagi menjamin instanisasi pindah sirkuit memori laman web tanpa batas tunggu di masa mendatang.

### 2.1.5 Variabel Uji Web Vitals (FCP, LCP, dan TBT)
Keselarasan optimasi skrip bukan diukur berdasarkan perasaan subjektif respons navigasi tatap muka semata, sebaliknya harus tunduk pada konvensi audit numerik interaktivitas layar berbasis matriks Google Chromium Foundation (2023) yang dinamai *Core Web Vitals*:
1. **First Contentful Paint (FCP):** Jangka jeda milidetik absolut (*ms*) yang dicatat sejak momentum pertama pakar mengetik rentetan URL di rute penjelajah (*Navigation Start Time*) menuju detik eksak tatkala elemen tekstual, struktur kotak *Canvas*, atau grafis apa pun dilukis (*Pixel mapped rendering*) untuk kali perdananya merubah layar putih penjelajah. Batas kelayakan FCP untuk indeks mesin pencarian bermutu premium (SEO) wajib melampaui nilai < 1.8 detik (1800 ms).
2. **Largest Contentful Paint (LCP):** Berbeda halangannya dengan FCP perdana, LCP merujuk batas toleransi titik ukur selesainya elemen terbesar (baik *Hero-Image Banner*, tabel raksasa visual, paragraf artikel utama, dsb) memuat ke layar secara tuntas tanpa pecah piksel. Acuan kompetensi web mendiktekan durasi yang mumpuni dikualifikasikan pada kecepatan kilat < 2.5 detik (2500 ms).
3. **Total Blocking Time (TBT):** Tolok ukur keandalan fungsional *Single Page Application* yang mengalkulasi keseluruhan nilai rekam durasi pembekuan utas komputasi. Kalkulasi diukur dari jumlah mutlak jeda di mana eksekusi rute tugas JavaScript (*Long Task* > 50 ms) mengebiri kapabilitas reaksi peramban (*Main Thread Freeze*) di ruang rentang antara penyelesaian pelukisan awal (FCP) menuju penahbisan matang antarmuka interaktif total (*Time To Interactive*). TBT merepresentasikan "Keputusasaan Pengguna"—yakni lamanya waktu di mana pengguna menekan tombol aplikasi web tanpa mendapati satupun tanggapan merespon balik. Nilai toleransi kognitif rasional manusia mengharuskan sumbangan TBT harus dieksekusi tuntas di bawah garis rawan < 200 ms hingga mentok 300 ms (Amenta & Castellani, 2019).


---

## 2.2 Jenis dan Pendekatan Penelitian
Desain metodologis dari tugas akhir riset tesis ini diklasifikasikan sebagai studi komparasi eksperimental terapan (eksperimen semu atau *quasi-experimental*) dalam tataran rekayasa peranti lunak lapis *Front-end*. Model parameter pengujian akan mengkonfrontasi pengukuran dua struktur purwarupa keluaran (Hasil varian perakitan/kompilasi *Build Output*) berbasis fungsionalitas visual tingkat homogen.  

Pembagian Klasterisasi Varian Kompilasi Penilaian meliputi:
1. **Model Sistem Baseline (Monolithic / Eager Load):** Representasi perangkat lunak standar konvensional tersusun melalui injeksi gabungan fail padat. Mengemulasikan sifat impor statik biasa yang melucuti probabilitas peramban merepresentasikan tata letak modul secara efisien pada pemicuan berderet antarmuka awal situs web. 
2. **Model Sistem Optimized (Hybrid Splitting):** Pengaplikasian metodologi penyelarasan pemisahan serangkai berkas JavaScript independen yang dibalut mekanisme instruksi asinkronus iteratif (*Manual Chunks*, *Route Lazy Import*, kompresi transfer data sekunder algoritma Brotli/Gzip ganda, diorkestrasi *Prefetching API* berdikari).

## 2.3 Spesifikasi Instrumen Perangkat Penelitian (Hardware & Software)
Studi perbandingan arsitektur pemrosesan ini dirangkai di dalam kapabilitas ruang ekosistem yang terkontrol presisi demi meredam distorsi variabel eksternal. Perancangan konstruksi aplikasi (*Development Build*), pelaksanaan peladen inang HTTP proksi, sekaligus stasiun pengukur jejak *Performance Tracking* menggunakan sarana otomasi peramban merujuk pada standar laboratorium dengan spesifikasi terdaftar di bawah:

**Stasiun Pengerjaan Keras Klien Independen Lokal (Hardware Base Station):**
- Sistem Dasar Operasional: Windows 10/11 Architecture 64-Bit Microprocessor X86-64
- Unit Prosesor Tunggal Tuan Rumah: Kapasitas Setara Generasi Konvensional Quad Core/Octa Core Modifikasi Minimum untuk memastikan rasio Throttling berjalan mumpuni.
- Pemetaan Kapasitas Memori (RAM): Ketersediaan *Random Access Memory* ≥ 8 GB.
- Distribusi Data Jaringan: Komunikasi tertutup interkal antar port *Localhost HTTP Service Loopback Subnet Mask Local*.

**Daftar Peralatan Perangkat Lunak Inti (Software Technical Stack):**
1. Mesin Inti Kruntime Eksekutor: *Node.js* (Versi stabil LTS v18/20.x+) men-support *Interpreter V8 Asynchronous Native File System*.
2. Kerangka Konstruksi Visual Purwarupa Frontend: *Vue.js Versi 3.x (Composition Script Paradigm)*.
3. Kerangka Manajemen Sub Modul Berkas/Bawaan Reaktif: Ekstensi *Vue-Router 4*, *Pinia Store Ecosystem v2*, Pengolahan Grafis *Chart.js*.
4. Perakit Kompilasi Silang Masa Pra-Produksi/Transpiler Tesis: *Vite.js* dengan Sokongan Kompilasi Hibrida *Rollup Compiler*.
5. Piranti Pengendali Uji Tanpa Muka Peramban Automasi: Paket modul eksternal *Puppeteer Node JS Layer* (Versi 20+) menyandera kontrol jarak jauh mesin penampil Webkit *Chromium Headless Browser Engine*.

## 2.4 Tahapan Pelaksanaan Eksperimen
Rencana riset rekayasa dikerucutkan berlapis serangkaian peta transisi sekuensial taktis guna menyajikan keaslian rasio perbandingan:
1. **Investigasi dan Pemodelan Tingkat Kepadatan Sistem (Complexity Architecture):** Merakit diferensiasi tajam terhadap kapabilitas purwarupa. Menjadikan portal interaktif rumit Sistem Informasi Manajemen Tugas Akhir (SIMTA/Memuat beban diagram, basis data tersentral, *Store Router*) sebagai parameter "Aplikasi Skala Kompleks". Disandingkan paralel bersama portal representatif lurus *Company Profile* murni HTML/VUE reaktif selaku pilar bandingan "Aplikasi Skala Sederhana".
2. **Restrukturisasi Penulisan Sandi Modul (*Development Initialization*):** Menginjeksi purwarupa basis sistem kode ke dalam algoritma penulisan terstruktur dan memastikan *Deployment Frontend Vue.Js* yang matang (Bebas *Compiler Error*).
3. **Rekayasa Penggandaan Kompilator Varian (Dual Bundling Formulations):** Melakukan eksekusi *Compile Build* ke ranah fail bundel produksi (direktori *dist*). Menyiplin satu varian kompilasi standar ke wadah pengujian komplit (*baseline*) seraya menyemburkan ramuan *plugin splitting* dan *lazy route binding Vite* menempati repositori (*optimized-dist*). 
4. **Instalasi Modul Pemungutan Performa (W3C Tracker Observer):** Merancang penempat skrip tangkapan algoritma evaluasi bawaan peramban (*Custom PerformanceObserver Script Tracker in JS Vanilla*) diselundupkan di hulu komponen awal sebelum pemancangan aplikasi purwarupa berjalan (*pre-mounted script initializations*).
5. **Eksekusi Bot Peniru Hambatan Spek Gawai (Puppeteer Runner Environment):** Meluncurkan bot komputasi di port asinkron lokal guna merekam metrik numerikal (LCP, TBT) dalam kondisi Normal, lalu menginjeksikan secara brutal pembatasan kecepatan pemroses sentral sebanyak empat lapis kelipatan pelambatan (*CPU Slowdown 4x Profile/Network Simulation Disable*).
6. **Ekstraksi Hasil dan Analisis Evaluasi Log:** Mendulang metadatum dari bonggol penyajian format struktur JSON. Pembuatan bagan chart kurva Matplotlib dan rasionalisasi implikasi fungsional (Konfirmasi rasio perbedaan antara Varian Sederhana dan Ekstrem Kompleks SIMTA).

## 2.5 Pemodelan Tingkat Kompleksitas (Sistem SIMTA)
Landasan urgensi dari peletakan algoritma intervensi *Code Splitting* memerlukan pembenaran atas tingginya kompleksitas muatan bawaan sistem purwarupa. Berbeda totalnya rasio pemuatan komponen pada web portal statis linier, subsistem SIMTA memancarkan keterikatan reaktif padat (interaksi *interlocking state*) seperti tergambar di diagram berikut.

### 2.5.1 Relasi Basis Data (*Entity Relationship Diagram*)
Hubungan relasional multidimensi ini merepresentasikan bagaimana entitas kelolaan seperti status log mahasiswa, presensi bimbingan, notule asinkron, serta berkas laporan, memiliki tautan struktural yang merentang erat pada sisi antarmuka klien. Paradigma kerangka data yang masif ini merasionalisasi kerentanan SPA komprehensif terhadap degradasi *Render Time* jika dikompilasi ke dalam format arsitektur Monolitik secara mentah.

<div align="center">
  <img src="./chapters/images/mermaid_1.png" alt="Diagram Relasi Basis Data SIMTA/ERD" width="550" />
  <br>
  <i>Gambar 2.1 Entity Relationship Diagram (ERD) dari Modul Bimbingan SIMTA.</i>
</div>

### 2.5.2 Pola Sirkulasi Arus Data (*Data Flow Diagram Reaktif*)
Siklus aliran arsitektur SPA mutakhir ini (menggunakan *Pinia/Vuex* State Management) secara masif mengirimkan sinyal pembaruan (*Reactive Virtual-DOM Patching*) ketika bongkah *Library Chart.Js* atau tabel daftar antrean dimutasi secara langsung oleh respon *asynchronous* dari API.

<div align="center">
  <img src="./chapters/images/mermaid_2.png" alt="Diagram Alir Komunikasi State Management Berbasis Pinia" width="550" />
  <br>
  <i>Gambar 2.2 Arus Transmisi Data Status Asinkronus pada Aplikasi.</i>
</div>

Kerumitan beban perulangan pemanggilan (*payload event*) di siklus DFD asimetris mendemonstrasikan signifikansi prioritas alokasi modul proses peramban. Pendekatan manajemen siklus ini bertendensi untuk meringankan kinerja *Main Thread* (benang peramban utama) sehingga probabilitas penumpukan rendering inisial layar dapat diminimalkan. Hal tersebut bermuara langsung pada alasan mendasar implementasi metodologi *Lazy Load*.

## 2.6 Instrumen Pengumpulan Data (W3C Algoritma *Tracker*)
Dalam penelitian ini, tidak direkomendasikan penggunaan fitur rekam analitik pihak ketiga semacam piranti Google Lighthouse atau GTMetrix. Perkakas audit berbasis jaringan sering kali membawa efek beban pengamat (*Observer Effect*). Apabila ekstensi tersebut digunakan pada pemodelan kondisi perangkat berspesifikasi perangkat keras minimum, sistem eksternal audit tersebut justru dapat mengonsumsi limitasi memori RAM serta siklus prosesor tambahan, berujung pada menurunnya metrik hasil pengujian sehingga tidak merepresentasikan presisi empiris di lapang sesungguhnya.

Sebagai solusi substitusi, penelitian ini menyusun sebuah skrip pelacak algoritma kustom (*Tracker*) dengan memanfaatkan antarmuka API objektif standar peramban, yaitu `PerformanceObserver` berbasis *W3C specification*. Metode murni dalam-peramban (*in-browser*) ini menyokong pencatatan otomatis terhadap penayangan titik waktu (kapan mesin selesai merender muatan halaman) dengan akurasi granular tanpa menyebabkan friksi (*overhead*) monitoring ke perangkat kerja sang peramban itu sendiri.

Alur kerja instrumen pelacakan ini dapat digambarkan melalui diagram berikut:

<div align="center">
  <img src="./chapters/images/mermaid_3.png" alt="Alur Eksekusi Instrumen Pelacakan API Peramban" width="550" />
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

## 2.7 Perumusan Skenario Pengujian (*Stress-Tests*)
Keterandalan dari evaluasi teknik kompilasi asinkron (Optimasi SPA) sangat bergantung pada disparitas kondisi pengujian. Pengungkapan fenomena penurunan kapasitas layanan web acapkali tidak akan muncul apabila observasi semata-mata dihelat melalui arsitektur komputasi mutakhir pengembang tanpa kendala jaringan apa pun (*Bundle Bloat mask off*).

Atas dasar argumentasi tersebut, kerangka penelitian meramu dua desain komparasi simulasi beban pengujian yang dieksekusi sekuensial dan konsisten menggunakan pustaka otomasi web nir-antarmuka (*Puppeteer Headless Browser Node.js*):

1. **Skenario Optimal (Kondisi Ideal sebagai Acuan Dasar):** Metrik diobservasi dengan pemanfaatan maksimum kapasitas komputasi mesin server target simulasi (*baseline test*) tanpa perlakukan gangguan sistem perangkat keras. Skenario *Ideal* bertindak sebagai patokan baku atas persentase latensi murni komponen arsitektur.
2. **Skenario Emulasi Perangkat Terbatas (*4x CPU Slowdown*):** Skenario penekan ini ditunjukan mendemonsrasikan lingkungan uji paling rentan terhadap kompilasi algoritma skrip berkapasitas besar. Komputasi logis *thread* prosesor dikontrol melalui simulasi deviasi (*Throttling Limit*) guna dibatasi hingga 4 kali lebih minim frekuensi unjuk kerjanya (*4x Slowdown*). Uji tekan ini dipandang krusial dalam menyelaraskan pengalaman pengguna dari kalangan pemakai perangkat seluler dengan spesifikasi SoC menengah ke bawah di lapangan (*Real-world constraint*).

Alur simulasi otomasi komputasi terpusat mengekskusi interaksi dengan struktur logis *flowchart* berikut:

<div align="center">
  <img src="./chapters/images/mermaid_4.png" alt="Alur Logika Pengujian Otomasi dengan Batasan Hardware" width="550" />
  <br>
  <i>Gambar 2.4 Alur Diagram Eksekusi Puppeteer dalam Skenario Normal & Throttling Limit.</i>
</div>

Melimpahkan kendali pengarahan navigasi melalui arsitektur perangkat lunak otomatis (*Puppeteer API*), faktor ketidakakuratan dan rentang deviasi respons akibat anomali reaksi subjek manusiawinya (efek *human-error bias*) dapat dinihilkan sepenuhnya dari rentetan iterasi penelitian. Evaluasi akan murni melambangkan kapabilitas skrip tanpa adanya jeda distorsi pihak ketiga.
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(bab_2_content)
    
print("Bab 2 Berhasil diekspansi dan diselipkan teori-teori secara ekstensif! Target halaman terdongkrak.")

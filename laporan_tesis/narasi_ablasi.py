"""
Narasi pembahasan Sub-bab 3.10 dan kesimpulan studi ablasi.
Angka diambil dari data ringkasan; kalimat interpretasi ditulis berdasarkan
hasil pengukuran riil (ukur_ablasi.cjs) dan uji Welch t-test (analisis_ablasi.py).
"""

TEKNIK = {
    "A1-splitting": "code splitting",
    "A2-lazy": "lazy loading",
    "A4-gzip": "Gzip",
}


def buat_narasi(H, po, lh, angka, pct_po, pct_lh, NAMA):
    def m(v, s, k):
        return po(v, s, k)["mean"]

    def rel(v, s, k, acuan="A0-kontrol"):
        return (m(v, s, k) - m(acuan, s, k)) / m(acuan, s, k) * 100

    def p(x):
        return angka(abs(x)) + "%"

    def arah(x, ambang=5):
        if x <= -ambang:
            return f"turun {p(x)}"
        if x >= ambang:
            return f"naik {p(x)}"
        return f"praktis tidak berubah ({'+' if x > 0 else '−'}{p(x)})"

    def L(v, k):
        return lh(v, k)["mean"]

    lh_rel = {v: L(v, "PerformanceScore") - L("A0-kontrol", "PerformanceScore") for v in NAMA}

    # Skor kontribusi: rata-rata perbaikan TBT (CPU 4x), Load Time (jaringan lambat), dan Lighthouse Score
    def skor(v):
        return (-rel(v, "cpu_lambat", "TBT_ms") - rel(v, "jaringan_lambat", "LoadTime_ms")
                + lh_rel[v] / L("A0-kontrol", "PerformanceScore") * 100) / 3

    tunggal = sorted(TEKNIK, key=skor, reverse=True)
    terbaik, kedua, ketiga = tunggal
    nav_a0 = m("A0-kontrol", "jaringan_lambat", "Navigasi_ms")
    nav_lazy = m("A2-lazy", "jaringan_lambat", "Navigasi_ms")
    nav_pref = m("A3-prefetch", "jaringan_lambat", "Navigasi_ms")
    t = lambda v, s, k: angka(m(v, s, k))  # noqa: E731
    kb = lambda v: angka(m(v, "ideal", "transfer_js_KB"))  # noqa: E731
    sc = lambda v: angka(L(v, "PerformanceScore"))  # noqa: E731
    gz_hemat = (1 - m("A4-gzip", "ideal", "transfer_js_KB") / m("A0-kontrol", "ideal", "transfer_js_KB")) * 100
    jl = "jaringan_lambat"

    n = {}
    n["pembuka"] = (
        "Sub-bab ini menjawab pertanyaan teknik mana yang paling berkontribusi terhadap perbaikan performa SIMTA. "
        "Setiap varian dibandingkan dengan varian kontrol A0 (tanpa optimasi apa pun); persentase negatif pada metrik "
        "waktu (FCP, TBT, _Load Time_, navigasi) berarti lebih cepat. Perbedaan terhadap kontrol diuji dengan Welch "
        "_t-test_ (α = 0,05). Desain varian dijelaskan pada Sub-bab 2.8.1."
    )

    n["ukuran"] = (
        f"Tabel 3.9 menunjukkan bahwa total ukuran JavaScript mentah hampir sama pada semua varian "
        f"({angka(min(H['ukuran'][v]['total_mentah_KB'] for v in NAMA))}–"
        f"{angka(max(H['ukuran'][v]['total_mentah_KB'] for v in NAMA))} KB): _code splitting_ dan _lazy loading_ hanya "
        f"memindahkan kode ke berkas lain, tidak menghapusnya. Yang berubah adalah berapa banyak yang dikirim di awal. "
        f"_Code splitting_ saja (A1) tetap mentransfer {kb('A1-splitting')} KB karena ketiga _chunk_-nya dibutuhkan halaman "
        f"pertama. _Lazy loading_ (A2) hanya sedikit mengurangi transfer menjadi {kb('A2-lazy')} KB, karena Chart.js ikut "
        f"masuk ke _chunk_ Dashboard yang memang dibuka pertama. Penurunan terbesar datang dari Gzip (A4): "
        f"{kb('A0-kontrol')} KB menjadi {kb('A4-gzip')} KB, hemat {angka(gz_hemat)}% tanpa mengubah struktur kode sama "
        f"sekali. Pada A3, transfer naik menjadi {kb('A3-prefetch')} KB karena dua _chunk_ halaman di-_prefetch_ saat idle — "
        f"biaya yang memang disengaja dan terjadi setelah halaman tampil."
    )

    n["muatan_awal"] = (
        f"Pada **kondisi normal** (Tabel 3.10), perbedaan antarvarian umumnya berada dalam rentang simpangan baku dan tidak "
        f"signifikan, kecuali FCP varian _code splitting_ saja (A1) yang justru {arah(rel('A1-splitting', 'ideal', 'FCP_ms'))} "
        f"({t('A0-kontrol', 'ideal', 'FCP_ms')} → {t('A1-splitting', 'ideal', 'FCP_ms')} ms; p < 0,01). Pada perangkat yang "
        f"cepat dan tanpa hambatan jaringan, satu berkas besar diproses cukup cepat sehingga tidak ada teknik yang "
        f"memberi keuntungan berarti, dan pemecahan berkas tanpa penundaan pemuatan hanya menambah permintaan HTTP.\n"
        f"Pada **CPU diperlambat 4x** (Tabel 3.11), _lazy loading_ (A2) adalah satu-satunya teknik tunggal yang menurunkan "
        f"TBT secara signifikan: {t('A0-kontrol', 'cpu_lambat', 'TBT_ms')} → {t('A2-lazy', 'cpu_lambat', 'TBT_ms')} ms "
        f"({p(rel('A2-lazy', 'cpu_lambat', 'TBT_ms'))}, p < 0,05), disertai _Load Time_ "
        f"{arah(rel('A2-lazy', 'cpu_lambat', 'LoadTime_ms'))}. _Code splitting_ (A1, "
        f"{arah(rel('A1-splitting', 'cpu_lambat', 'TBT_ms'))}) dan Gzip (A4, {arah(rel('A4-gzip', 'cpu_lambat', 'TBT_ms'))}) "
        f"tidak berbeda signifikan dari kontrol. Hal ini sesuai mekanisme pada Sub-bab 2.1.6 dan 2.1.10: TBT ditentukan "
        f"oleh banyaknya kode yang dieksekusi dalam satu _task_ panjang. _Lazy loading_ memecah eksekusi menjadi beberapa "
        f"_task_ yang lebih pendek, sedangkan Gzip hanya memperkecil berkas di jaringan — setelah didekompresi, mesin V8 "
        f"tetap memproses kode yang sama besarnya. TBT terendah dicapai varian gabungan A5 "
        f"({t('A5-gabungan', 'cpu_lambat', 'TBT_ms')} ms, {p(rel('A5-gabungan', 'cpu_lambat', 'TBT_ms'))} lebih rendah; "
        f"p < 0,05).\n"
        f"Pada **CPU 4x + jaringan lambat** (Tabel 3.12), FCP dan _Load Time_ seluruh varian kecuali A1 membaik secara "
        f"signifikan (p < 0,001). FCP kontrol mencapai {t('A0-kontrol', jl, 'FCP_ms')} ms karena peramban harus menunggu satu berkas "
        f"{kb('A0-kontrol')} KB selesai diunduh sebelum menggambar apa pun. _Lazy loading_ (A2) menurunkan FCP menjadi "
        f"{t('A2-lazy', jl, 'FCP_ms')} ms ({p(rel('A2-lazy', jl, 'FCP_ms'))}) dan _Load Time_ menjadi "
        f"{t('A2-lazy', jl, 'LoadTime_ms')} ms ({p(rel('A2-lazy', jl, 'LoadTime_ms'))}), sedikit lebih baik daripada Gzip "
        f"(A4: FCP {t('A4-gzip', jl, 'FCP_ms')} ms, {p(rel('A4-gzip', jl, 'FCP_ms'))}; _Load Time_ "
        f"{t('A4-gzip', jl, 'LoadTime_ms')} ms, {p(rel('A4-gzip', jl, 'LoadTime_ms'))}). _Lazy loading_ unggul karena kerangka "
        f"aplikasi (_sidebar_ dan _header_) sudah dapat digambar sebelum _chunk_ Dashboard selesai diunduh, sedangkan Gzip "
        f"unggul pada TBT ({t('A4-gzip', jl, 'TBT_ms')} ms) karena berkas tiba lebih cepat sehingga eksekusinya tidak "
        f"bertumpuk. Varian gabungan A5 mencatat FCP terendah ({t('A5-gabungan', jl, 'FCP_ms')} ms) dan TBT terendah "
        f"({t('A5-gabungan', jl, 'TBT_ms')} ms) dari semua varian."
    )

    n["anomali"] = (
        f"Satu hasil perlu dicermati: _Load Time_ A5 pada jaringan lambat ({t('A5-gabungan', jl, 'LoadTime_ms')} ms) "
        f"justru lebih lambat daripada A3 yang tidak memakai _code splitting_ maupun Gzip ({t('A3-prefetch', jl, 'LoadTime_ms')} "
        f"ms; p < 0,001). Penelusuran pada hasil _build_ menunjukkan penyebabnya ada pada konfigurasi `manualChunks`. "
        f"Aturan `id.includes('node_modules/vue')` juga cocok dengan `node_modules/vue-chartjs`, sehingga "
        f"`vue-chartjs` ikut masuk ke `vendor-vue`. Karena `vendor-vue` dimuat sejak awal dan `vue-chartjs` meng-_import_ "
        f"Chart.js, Vite menambahkan `<link rel=\"modulepreload\">` untuk `vendor-chart` pada HTML awal (A1 dan A5). "
        f"Akibatnya Chart.js menjadi bagian dari pemuatan sinkron yang menahan _event load_, walaupun halaman Dashboard "
        f"sudah di-_lazy load_. Pada A2 dan A3 (tanpa `manualChunks`), Chart.js berada di dalam _chunk_ Dashboard yang dimuat "
        f"dinamis sehingga tidak menahan _event load_. Konfigurasi yang sama dipakai pada versi _optimized_ di Sub-bab 3.1, "
        f"sehingga temuan ini juga menjelaskan pengamatan pada Gambar 3.12 bahwa `vendor-chart.js` sudah diminta pada "
        f"milidetik-milidetik pertama. Artinya, _code splitting_ yang tidak dikonfigurasi dengan cermat dapat mengurangi "
        f"manfaat _lazy loading_; urutan aturan perlu diperbaiki agar pustaka grafik dicek lebih dulu daripada pustaka Vue."
    )

    n["navigasi"] = (
        f"Tabel 3.13 memperlihatkan konsekuensi _lazy loading_ yang telah dibahas secara konseptual pada Sub-bab 3.2. Pada "
        f"jaringan lambat, perpindahan Dashboard → Daftar Judul pada varian A2 membutuhkan {angka(nav_lazy)} ms, hampir "
        f"{angka(nav_lazy / nav_a0, 0)} kali lebih lambat daripada kontrol ({angka(nav_a0)} ms), karena _chunk_ halaman baru "
        f"diunduh saat menu ditekan. Penambahan _prefetching_ (A3) menurunkan latensi ini menjadi {angka(nav_pref)} ms "
        f"({p((nav_pref - nav_lazy) / nav_lazy * 100)} lebih cepat dari A2; p < 0,001), mendekati varian tanpa _lazy loading_, "
        f"karena _chunk_ sudah berada di _cache_ peramban sebelum menu ditekan. Sebaliknya, metrik muatan awal A3 dan A2 "
        f"hampir sama (Tabel 3.10–3.12). Artinya, kontribusi _prefetching_ tidak terletak pada kecepatan halaman pertama, "
        f"melainkan pada menghilangkan biaya navigasi yang ditimbulkan _lazy loading_."
    )

    n["lighthouse"] = (
        f"Lighthouse, yang mensimulasikan perangkat seluler kelas menengah dengan jaringan _Slow 4G_, memberi gambaran yang "
        f"berbeda dari _PerformanceObserver_. Skor kontrol {sc('A0-kontrol')}; _code splitting_ ({sc('A1-splitting')}), "
        f"_lazy loading_ ({sc('A2-lazy')}), dan _lazy loading_ + _prefetching_ ({sc('A3-prefetch')}) tidak berbeda signifikan "
        f"dari kontrol, sedangkan Gzip saja langsung menaikkan skor menjadi {sc('A4-gzip')} (p < 0,01) dan gabungan menjadi "
        f"{sc('A5-gabungan')} (p < 0,01). Penyebabnya terlihat pada LCP: _lazy loading_ memang mempercepat FCP Lighthouse "
        f"({angka(L('A0-kontrol', 'FCP_ms'), 0)} → {angka(L('A2-lazy', 'FCP_ms'), 0)} ms), tetapi LCP — elemen terbesar, yaitu "
        f"konten Dashboard beserta grafiknya — tetap {angka(L('A2-lazy', 'LCP_ms'), 0)} ms karena _chunk_ Dashboard yang "
        f"berisi Chart.js tetap harus diunduh utuh. Gzip memperkecil seluruh berkas sehingga LCP turun menjadi "
        f"{angka(L('A4-gzip', 'LCP_ms'), 0)} ms. Karena LCP dan FCP berbobot besar dalam skor Lighthouse, teknik yang "
        f"mengurangi ukuran transfer paling menentukan skor ini. Skor gabungan ({sc('A5-gabungan')}) tidak berbeda "
        f"signifikan dari Gzip saja ({sc('A4-gzip')}), namun TBT Lighthouse-nya lebih rendah "
        f"({angka(L('A4-gzip', 'TBT_ms'), 0)} → {angka(L('A5-gabungan', 'TBT_ms'), 0)} ms) berkat kontribusi _lazy loading_.\n"
        f"Sebagai pembanding, versi _baseline_ dan _optimized_ dari Bab III yang diukur ulang pada sesi yang sama mencatat "
        f"skor {sc('R-baseline')} dan {sc('R-optimized')}. Skor _optimized_ lebih tinggi daripada A5 karena memakai Brotli di "
        f"samping Gzip, yang menghasilkan berkas lebih kecil lagi. Nilai absolut ini berbeda dari Tabel 3.6 (56,8 dan 75,0) "
        f"karena Lighthouse sensitif terhadap kondisi mesin pada tiap sesi pengukuran; oleh karena itu perbandingan "
        f"antarvarian hanya dilakukan di dalam satu sesi yang sama."
    )

    n["sintesis_pembuka"] = (
        "Berdasarkan Tabel 3.9–3.14, tidak ada satu teknik tunggal yang unggul di semua metrik, karena masing-masing bekerja "
        "pada lapisan yang berbeda. Tabel 3.15 merangkum kontribusinya; peringkat disusun dari rata-rata perbaikan tiga "
        "indikator utama (TBT pada CPU 4x, _Load Time_ pada jaringan lambat, dan Lighthouse Score) terhadap kontrol."
    )

    def dampak(v):
        return (f"TBT CPU 4x {arah(rel(v, 'cpu_lambat', 'TBT_ms'))}; Load jaringan lambat "
                f"{arah(rel(v, jl, 'LoadTime_ms'))}; Score {'+' if lh_rel[v] >= 0 else '−'}{angka(abs(lh_rel[v]))}")

    peringkat = {v: str(i + 1) for i, v in enumerate(tunggal)}
    n["tabel_rangkuman"] = [
        ["Gzip", "Ukuran transfer jaringan", "Transfer JS, LCP, Lighthouse Score", dampak("A4-gzip"), peringkat["A4-gzip"]],
        ["Lazy loading", "Kapan kode dieksekusi", "TBT pada CPU lambat, FCP & Load pada jaringan lambat", dampak("A2-lazy"),
         peringkat["A2-lazy"]],
        ["Code splitting", "Cara kode dikemas", "Caching pustaka; prasyarat pemisahan vendor", dampak("A1-splitting"),
         peringkat["A1-splitting"]],
        ["Prefetching", "Waktu navigasi", "Latensi navigasi",
         f"Navigasi jaringan lambat {arah((nav_pref - nav_lazy) / nav_lazy * 100)} vs A2", "Pelengkap"],
        ["**Gabungan (A5)**", "Semua lapisan", "TBT, FCP, Lighthouse Score", dampak("A5-gabungan"), "**Paling optimal**"],
    ]

    n["sintesis_poin"] = [
        f"**Gzip adalah teknik tunggal dengan kontribusi terbesar secara keseluruhan.** Gzip memangkas transfer JavaScript "
        f"{angka(gz_hemat)}% dan satu-satunya teknik tunggal yang menaikkan Lighthouse Score secara signifikan "
        f"({sc('A0-kontrol')} → {sc('A4-gzip')}). Biaya penerapannya juga paling rendah karena tidak mengubah kode aplikasi.",
        f"**Lazy loading berada di peringkat kedua, tetapi paling unggul ketika hambatannya CPU.** Hanya _lazy loading_ yang "
        f"menurunkan TBT secara signifikan pada CPU 4x ({p(rel('A2-lazy', 'cpu_lambat', 'TBT_ms'))}), dan pada jaringan lambat "
        f"memberi FCP serta _Load Time_ terbaik di antara teknik tunggal. Gzip dan _lazy loading_ saling melengkapi: "
        f"yang satu mengurangi kerja jaringan, yang lain mengurangi kerja CPU.",
        f"**Code splitting berdiri sendiri memberi manfaat paling kecil** dan pada kondisi normal bahkan memperlambat FCP, "
        f"karena halaman pertama SIMTA tetap membutuhkan seluruh _chunk_ sehingga hanya menambah permintaan HTTP. Perannya "
        f"adalah memisahkan pustaka agar dapat di-_cache_ terpisah, dengan catatan aturan `manualChunks` harus disusun "
        f"cermat agar tidak menarik pustaka berat kembali ke jalur muat awal.",
        "**Prefetching tidak mempercepat muatan awal, tetapi wajib menyertai lazy loading**, karena menghapus jeda "
        f"navigasi yang muncul akibat _lazy loading_ murni ({angka(nav_lazy)} → {angka(nav_pref)} ms pada jaringan lambat).",
        f"**Kombinasi keempatnya (A5) adalah konfigurasi paling optimal secara keseluruhan**: Lighthouse Score tertinggi "
        f"({sc('A5-gabungan')}), TBT terendah pada CPU 4x ({t('A5-gabungan', 'cpu_lambat', 'TBT_ms')} ms) dan jaringan lambat "
        f"({t('A5-gabungan', jl, 'TBT_ms')} ms), FCP terendah pada jaringan lambat, tanpa jeda navigasi. Satu-satunya metrik "
        f"yang tidak terbaik adalah _Load Time_ jaringan lambat, akibat konfigurasi `manualChunks` yang dibahas di atas.",
    ]

    n["sintesis_penutup"] = (
        f"Dengan demikian, jawaban atas pertanyaan teknik mana yang membuat SIMTA paling optimal adalah: secara individual "
        f"{TEKNIK[terbaik]} memberi kontribusi terbesar, diikuti {TEKNIK[kedua]}, sedangkan {TEKNIK[ketiga]} dan "
        f"_prefetching_ berperan sebagai pendukung. Urutan Gzip dan _lazy loading_ bergantung pada sumber hambatan: bila "
        f"hambatannya jaringan, Gzip paling menentukan; bila hambatannya CPU perangkat, _lazy loading_ paling menentukan. "
        f"Hasil terbaik hanya dicapai bila keempatnya dipakai bersama, karena masing-masing menutup kelemahan yang tidak "
        f"dapat ditangani teknik lain. Temuan ini sekaligus menjelaskan komposisi perbaikan versi _optimized_ yang "
        f"dilaporkan pada Sub-bab 3.4–3.6."
    )

    n["kesimpulan"] = (
        f"**Kontribusi tiap teknik berbeda, dan kombinasi keempatnya yang paling optimal.** Studi ablasi pada SIMTA "
        f"(Sub-bab 3.10) menunjukkan bahwa {TEKNIK[terbaik]} adalah teknik tunggal dengan kontribusi terbesar, diikuti "
        f"{TEKNIK[kedua]}. Gzip paling berpengaruh pada ukuran transfer ({angka(gz_hemat)}% lebih kecil) dan Lighthouse "
        f"Score ({sc('A0-kontrol')} → {sc('A4-gzip')}); _lazy loading_ satu-satunya teknik tunggal yang menurunkan TBT secara "
        f"signifikan pada CPU lambat ({p(rel('A2-lazy', 'cpu_lambat', 'TBT_ms'))}); _code splitting_ hampir tidak berdampak "
        f"bila berdiri sendiri; dan _prefetching_ tidak memengaruhi muatan awal tetapi memangkas latensi navigasi pada "
        f"jaringan lambat dari {angka(nav_lazy)} ms menjadi {angka(nav_pref)} ms. Kombinasi keempatnya memberikan "
        f"Lighthouse Score tertinggi ({sc('A5-gabungan')}) dan TBT terendah."
    )

    n["saran"] = (
        "**Perbaikan konfigurasi code splitting dan studi ablasi lanjutan.** Studi ablasi menemukan bahwa aturan "
        "`manualChunks` yang memeriksa `node_modules/vue` lebih dulu ikut menangkap `vue-chartjs`, sehingga Chart.js "
        "kembali ke jalur muat awal. Penelitian lanjutan disarankan memperbaiki urutan aturan tersebut (memeriksa pustaka "
        "grafik lebih dulu), lalu mengulang pengukuran. Studi ablasi juga dapat diperluas ke _Company Profile_, jaringan "
        "seluler sungguhan, serta perbandingan terpisah antara Gzip dan Brotli."
    )
    return n

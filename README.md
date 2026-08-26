# Optimasi Performa Single Page Application Menggunakan Hybrid Lazy Loading dan Code Splitting Berdasarkan Tingkat Kompleksitas Sistem

Repositori ini berisi kode program, konfigurasi *build*, skrip pengukuran, dan data mentah hasil pengujian dari penelitian tesis dengan judul di atas.

**Peneliti:** Mustari Muhiddin (D082241013)
**Program Studi:** Magister Teknik Informatika, Fakultas Teknik, Universitas Hasanuddin

---

## Ringkasan Penelitian

Penelitian ini menguji apakah efektivitas *hybrid lazy loading* dan *code splitting* pada SPA berbasis Vue.js + Vite dipengaruhi oleh tingkat kompleksitas aplikasi. Dua aplikasi dibandingkan:

| Objek Uji | Tingkat Kompleksitas | Karakteristik |
|-----------|---------------------|---------------|
| **SIMTA** (Sistem Informasi Manajemen Tugas Akhir) | Tinggi | 15+ rute, 50+ komponen, Chart.js + Pinia + Vue Router, operasi CRUD, visualisasi data |
| **Company Profile** | Rendah | Konten dominan statis, tanpa grafik interaktif maupun *state management* terpusat |

Masing-masing dikompilasi dalam dua versi — **baseline** (*monolithic / eager load*) dan **optimized** (*code splitting*, *lazy loading*, kompresi Brotli/Gzip, *prefetching*) — lalu diukur dengan W3C `PerformanceObserver` dan Google Lighthouse melalui Puppeteer, sebanyak 5 repetisi per skenario, pada kondisi normal dan CPU diperlambat 4x.

### Hasil Utama

| Temuan | SIMTA (kompleksitas tinggi) | Company Profile (kompleksitas rendah) |
|--------|------------------------------|----------------------------------------|
| Lighthouse Performance Score | 56,8 → 75,0 (**naik 32,0%**) | 100,0 → 99,0 (nyaris tidak berubah) |
| FCP — PerformanceObserver (kondisi normal) | 1103,2 → 842,4 ms (**−23,6%**) | 511,2 → 483,2 ms (−5,5%) |
| FCP — Lighthouse | 4960,4 → 3250,2 ms (**−34,5%**) | 1361,4 → 1578,2 ms (memburuk 15,9%) |
| TBT — PerformanceObserver (CPU 4x) | 710,4 → 579,0 ms (**−18,5%**) | 66,6 → 7,6 ms (−88,6%) |

**Kesimpulan:** *code splitting* + *lazy loading* + kompresi Brotli/Gzip sangat efektif pada aplikasi kompleks dengan pustaka berat (naik di semua metrik), tetapi manfaatnya tipis — dan pada metrik Lighthouse yang stabil justru sedikit negatif di FCP/LCP — pada aplikasi sederhana. Ambang praktis yang direkomendasikan: terapkan hanya bila *bundle* awal melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak dibutuhkan di halaman pertama. Lihat catatan metodologis di `laporan_tesis/revisi_v2/BAB_3_HASIL_PEMBAHASAN.md` Sub-bab 3.8 mengenai satu klaim (degradasi FCP Company Profile) dari pengukuran awal yang tidak *reproducible* dan telah dikoreksi.

---

## Struktur Repositori

```
src/                          Kode sumber aplikasi SIMTA (Vue 3, Pinia, Chart.js, Vue Router)
public/                       Aset statis
index.baseline.html           Entry point SIMTA versi baseline
index.optimized.html          Entry point SIMTA versi optimized
index.cp.baseline.html        Entry point Company Profile versi baseline
index.cp.optimized.html       Entry point Company Profile versi optimized
vite.config.baseline.js       Build SIMTA tanpa optimasi
vite.config.optimized.js      Build SIMTA dengan manualChunks + kompresi
vite.config.cp.*.js           Build Company Profile kedua versi
dist-baseline/                Hasil build SIMTA baseline (bukti ukuran bundle)
dist-optimized/               Hasil build SIMTA optimized
dist-cp-baseline/             Hasil build Company Profile baseline
dist-cp-optimized/            Hasil build Company Profile optimized
ukur_performa.cjs             Pengukuran PerformanceObserver, uji tunggal (SIMTA)
ukur_performa_cp.cjs          Pengukuran PerformanceObserver, uji tunggal (Company Profile)
ukur_multirun.cjs             Pengukuran 5 repetisi (SIMTA)
ukur_multirun_cp.cjs          Pengukuran 5 repetisi (Company Profile)
ukur_lighthouse.cjs           Audit Google Lighthouse v11.x
capture_screenshots.cjs       Tangkapan layar untuk verifikasi kesamaan tampilan
analisis_statistik.py         Rata-rata, standar deviasi, persentase perbaikan
create_final_charts.py        Pembangkit grafik perbandingan
process_visuals.py            Pemrosesan diagram dan visual naskah
laporan_tesis/                Naskah tesis, slide presentasi, dan data pengukuran
  data_pengukuran/            Data mentah hasil pengujian (JSON)
  revisi_v2/                  Naskah tesis dalam format Markdown per bab
```

## Cara Menjalankan Ulang Pengujian

### Prasyarat

| Kebutuhan | Versi | Catatan |
|-----------|-------|---------|
| Node.js | v20 atau v22 | diuji pada v22.12.0 |
| Python | 3.9+ | diuji pada 3.11.6 |
| Paket Python | `numpy`, `matplotlib` | `pip install numpy matplotlib` |
| Koneksi internet | saat `npm install` saja | Puppeteer mengunduh Chromium (~150 MB) |

Puppeteer, Lighthouse, dan http-server sudah terdaftar di `devDependencies`, sehingga
`npm install` cukup — tidak ada unduhan tambahan saat pengukuran berjalan.

### Verifikasi cepat (satu perintah)

```bash
npm install
npm run verifikasi
```

Perintah `verifikasi` menjalankan seluruh rantai: build 4 varian → pengukuran
PerformanceObserver → audit Lighthouse → analisis statistik → pembangkitan grafik.
Total durasi ± 25–35 menit.

> **Peringatan.** Menjalankan pengukuran akan **menimpa** berkas JSON di
> `laporan_tesis/data_pengukuran/` — yaitu data mentah yang dilaporkan pada naskah
> tesis. Untuk membandingkan hasil baru dengan data asli tanpa kehilangan apa pun,
> cadangkan lebih dulu atau pulihkan dengan `git checkout -- laporan_tesis/data_pengukuran/`.

### Verifikasi bertahap

```bash
# 1. Pasang dependensi (Node + Python)
npm install
pip install numpy matplotlib

# 2. Kompilasi keempat varian aplikasi
npm run build:baseline        # SIMTA baseline      -> dist-baseline/
npm run build:optimized       # SIMTA optimized     -> dist-optimized/
npm run build:cp:baseline     # Company Profile baseline  -> dist-cp-baseline/
npm run build:cp:optimized    # Company Profile optimized -> dist-cp-optimized/
# atau sekaligus:  npm run build:all

# 3. Pengukuran PerformanceObserver
#    (5 repetisi x 2 skenario: normal dan CPU throttled 4x)
npm run ukur:simta            # ± 8 menit,  port 4001/4002
npm run ukur:cp               # ± 2 menit,  port 4005/4006

# 4. Audit Lighthouse (5 repetisi x 4 target)
npm run ukur:lighthouse       # ± 15 menit, port 4001/4002/4005/4006

# 5. Hitung statistik dan bangkitkan grafik
python analisis_statistik.py  # -> data_pengukuran/summary_stats.json
python create_final_charts.py # -> chapters/images/chart_*.png
```

Setiap skrip menyalakan server statisnya sendiri lalu mematikannya kembali; tidak perlu
menjalankan server secara manual. Pastikan port 4001, 4002, 4005, dan 4006 tidak terpakai
sebelum memulai.

### Cara membaca hasilnya

| Berkas | Isi |
|--------|-----|
| `laporan_tesis/data_pengukuran/multirun_*.json` | Data mentah per-repetisi: FCP, LCP, TBT, LoadTime, Memory |
| `laporan_tesis/data_pengukuran/lighthouse_*.json` | Data mentah Lighthouse: Score, FCP, LCP, TTI, TBT, Speed Index |
| `laporan_tesis/data_pengukuran/summary_stats.json` | Rerata dan simpangan baku seluruh metrik |
| Keluaran konsol `analisis_statistik.py` | Tabel `mean ± SD` + persentase perbaikan SIMTA |
| `laporan_tesis/chapters/images/chart_*.png` | Grafik perbandingan yang dipakai pada BAB III |

Angka pada BAB III berasal dari `summary_stats.json`. Sebagai contoh, klaim
"FCP SIMTA turun 23,6% pada kondisi normal" dapat dilacak ke baris
`FCP_ms Improvement` pada keluaran `analisis_statistik.py`, yang dihitung dari
`multirun_baseline_ideal.json` dan `multirun_optimized_ideal.json`.

Ukuran *bundle* yang dilaporkan dapat diperiksa langsung dari keluaran `npm run build:*`
atau dari isi folder `dist-*` yang disertakan.

### Catatan reproduktibilitas

Nilai absolut (mis. FCP dalam milidetik) **akan berbeda** antar mesin karena bergantung
pada kecepatan CPU penguji. Yang harus tetap konsisten adalah **arah dan besaran relatif**
perbandingan baseline vs optimized, yaitu kesimpulan penelitian ini. Versi Node.js,
Chromium bawaan Puppeteer, dan Lighthouse juga memengaruhi nilai absolut, sehingga
versi paket dikunci pada `package-lock.json` — gunakan `npm ci` alih-alih `npm install`
bila ingin lingkungan yang identik.

Dua perbaikan penting pada skrip pengukuran, ditemukan saat audit reproduktibilitas:

- `ukur_lighthouse.cjs` kini memaksa Lighthouse memakai Chrome yang sama dengan
  yang dikelola Puppeteer (`process.env.CHROME_PATH`), bukan Chrome sistem yang
  terdeteksi otomatis oleh `chrome-launcher` — Chrome sistem (dengan profil dan
  ekstensi pengguna) dapat menampilkan *interstitial* yang menggagalkan seluruh
  audit.
- `ukur_multirun.cjs`, `ukur_multirun_cp.cjs`, dan `ukur_lighthouse.cjs` kini
  menjalankan `http-server` dengan *flag* `-g -b` agar varian `.gz`/`.br` hasil
  `vite.config.optimized.js` benar-benar tersaji ke peramban sesuai
  `Accept-Encoding` — tanpa ini, manfaat kompresi Brotli/Gzip tidak pernah
  benar-benar terukur meski berkasnya ada di `dist-optimized/`.

Selain itu, aplikasi *Company Profile* memuat halaman dalam skala ratusan
milidetik, sehingga metrik `PerformanceObserver`-nya (khususnya FCP pada
kondisi CPU diperlambat) terbukti cukup sensitif terhadap variasi kondisi
mesin antar-sesi pengukuran, meski dijalankan pada mesin yang sama. Gunakan
data Lighthouse (simpangan baku jauh lebih kecil) sebagai rujukan utama untuk
klaim persentase pada aplikasi ini — lihat catatan metodologis di
Sub-bab 3.8 naskah tesis.

## Catatan Metodologis

- **Lapisan data.** `src/services/supabase.js` adalah *service layer* asinkron yang meniru pola pemanggilan Supabase (*promise-based* dengan penundaan jaringan tersimulasi, sumber data di `src/services/mockData.js`), **bukan** koneksi ke basis data daring. Pilihan ini diambil agar pengujian sepenuhnya *CPU-bound* dan dapat direproduksi tanpa bergantung pada layanan pihak ketiga maupun latensi jaringan. Karena *code splitting* bekerja pada lapisan pemuatan modul JavaScript, hal ini tidak memengaruhi validitas perbandingan *baseline* vs *optimized*.
- **Kondisi pengujian.** Seluruh pengukuran dijalankan di `localhost` dengan *CPU throttling* 4x melalui Puppeteer Chromium API, sehingga variabel jaringan tereliminasi. *Network throttling* tidak diterapkan dan dicatat sebagai saran penelitian lanjutan.
- **Folder `dist-*` sengaja diikutsertakan** dalam repositori sebagai bukti perbandingan ukuran *bundle* yang dilaporkan pada BAB III, meskipun umumnya hasil *build* tidak disertakan dalam kontrol versi.

## Lisensi dan Penggunaan

Repositori ini disertakan sebagai lampiran tesis untuk keperluan verifikasi dan reproduksi hasil penelitian. Silakan merujuk pada tesis terkait bila menggunakan bagian mana pun dari kode atau data di dalamnya.

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

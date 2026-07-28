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
| Ukuran *bundle* awal | 346 KB → ~195 KB (**turun >40%**) | sudah kecil sejak awal |
| FCP (kondisi normal) | 1144,0 → 881,6 ms (**−22,9%**) | 367,2 → 364,0 ms (tidak berarti) |
| TBT (CPU 4x) | 1023,0 → 790,8 ms (**−22,7%**) | 143,2 → 26,0 ms |
| FCP (CPU 4x) | membaik | **memburuk 30,2%** |

**Kesimpulan:** *code splitting* sangat efektif pada aplikasi kompleks dengan pustaka berat, tetapi kontraproduktif pada aplikasi sederhana. Ambang praktis yang direkomendasikan: terapkan hanya bila *bundle* awal melebihi 200 KB terkompresi dan terdapat pustaka berat yang tidak dibutuhkan di halaman pertama.

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

Prasyarat: Node.js LTS (v18/v20) dan Python 3.

```bash
# 1. Pasang dependensi
npm install

# 2. Kompilasi kedua versi aplikasi
npx vite build --config vite.config.baseline.js
npx vite build --config vite.config.optimized.js

# 3. Pengukuran PerformanceObserver (5 repetisi per skenario,
#    kondisi normal dan CPU throttled 4x)
node ukur_multirun.cjs
node ukur_multirun_cp.cjs

# 4. Audit Lighthouse
node ukur_lighthouse.cjs

# 5. Hitung statistik dan bangkitkan grafik
python analisis_statistik.py
python create_final_charts.py
```

Hasil pengukuran tersimpan sebagai JSON di `laporan_tesis/data_pengukuran/`.

## Catatan Metodologis

- **Lapisan data.** `src/services/supabase.js` adalah *service layer* asinkron yang meniru pola pemanggilan Supabase (*promise-based* dengan penundaan jaringan tersimulasi, sumber data di `src/services/mockData.js`), **bukan** koneksi ke basis data daring. Pilihan ini diambil agar pengujian sepenuhnya *CPU-bound* dan dapat direproduksi tanpa bergantung pada layanan pihak ketiga maupun latensi jaringan. Karena *code splitting* bekerja pada lapisan pemuatan modul JavaScript, hal ini tidak memengaruhi validitas perbandingan *baseline* vs *optimized*.
- **Kondisi pengujian.** Seluruh pengukuran dijalankan di `localhost` dengan *CPU throttling* 4x melalui Puppeteer Chromium API, sehingga variabel jaringan tereliminasi. *Network throttling* tidak diterapkan dan dicatat sebagai saran penelitian lanjutan.
- **Folder `dist-*` sengaja diikutsertakan** dalam repositori sebagai bukti perbandingan ukuran *bundle* yang dilaporkan pada BAB III, meskipun umumnya hasil *build* tidak disertakan dalam kontrol versi.

## Lisensi dan Penggunaan

Repositori ini disertakan sebagai lampiran tesis untuk keperluan verifikasi dan reproduksi hasil penelitian. Silakan merujuk pada tesis terkait bila menggunakan bagian mana pun dari kode atau data di dalamnya.

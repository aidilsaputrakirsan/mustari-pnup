# BAB 4: Hasil Pengujian dan Analisis Performa

## 4.1 Metodologi Pengujian
Pengujian dilakukan dengan melakukan proses *build* produksi pada kedua versi aplikasi menggunakan Vite. Ukuran berkas (Bundle Size) diukur setelah proses minifikasi.

**Lingkungan Pengujian:**
- **Build Tool**: Vite v8.0.0-beta
- **Framework**: Vue 3.5.25
- **Node.js**: v22.12.0
- **Mode Build**: Production Mode (Minified)

---

## 4.2 Analisis Ukuran Bundle (Bundle Size)

Berikut adalah perbandingan ukuran berkas JavaScript yang harus diunduh browser pada saat pertama kali aplikasi dibuka (Initial Load).

### Tabel 4.1: Perbandingan Ukuran Bundle Utama

| Metrik | Versi 1A (Baseline) | Versi 1B (Optimized) | Selisih/Reduksi |
|--------|---------------------|----------------------|-----------------|
| **Total Entry File** | **336.89 KB** | **~127 KB*** | **62% Lebih Kecil** |
| struktur File | 1 File Raksasa | Modular (20+ Files) | - |

*\*Catatan: Versi 1B hanya memuat `index.optimized.js` (10KB), `vendor-vue.js` (100KB), dan `DashboardView.js` (7.8KB) di awal.*

### Grafik 4.1: Distribusi Ukuran File (Versi 1B)
Pada Versi 1B, pustaka berat berhasil dipisahkan dari bundle utama:

1.  **vendor-chart.js** (194.91 KB)
    - *Status*: **Lazy Loaded**.
    - *Keterangan*: Hanya diunduh jika pengguna membuka Dashboard. Tidak membebani halaman Login atau Pengaturan.

2.  **Halaman (Views)**
    - Rata-rata ukuran per halaman: **~5-8 KB**.
    - Diunduh secara on-demand saat navigasi.

---

## 4.3 Analisis Efisiensi Pemuatan

### Skenario 1: Pengguna Membuka Halaman "Pengaturan"
- **Versi 1A**: Browser mengunduh **336 KB** (termasuk Chart.js dan semua data tabel Skripsi yang tidak dibutuhkan di halaman pengaturan).
- **Versi 1B**: Browser mengunduh **~116 KB** (Core + Halaman Pengaturan). Chart.js (195 KB) **TIDAK** diunduh.
- **Hasil**: Versi 1B menghemat **~220 KB** bandwidth data pada skenario ini.

### Skenario 2: Update Kode Aplikasi
- **Versi 1A**: Jika ada perubahan kecil pada kode logika, seluruh file **336 KB** berubah hash-nya dan harus diunduh ulang oleh user (Cache Miss).
- **Versi 1B**: Jika logika aplikasi berubah, user hanya mengunduh ulang file aplikasi yang kecil (~10-20 KB). File `vendor-vue` dan `vendor-chart` tetap diambil dari **Cache Browser**.

---

## 4.4 Kesimpulan Hasil
Berdasarkan data di atas, arsitektur **Optimized (1B)** terbukti jauh lebih efisien dibandingkan Baseline (1A). Penerapan *Code Splitting* dan *Lazy Loading* berhasil mengurangi beban awal aplikasi hingga **62%**, yang akan berdampak langsung pada kecepatan akses pengguna (First Contentful Paint) dan skor performa SEO (Lighthouse).

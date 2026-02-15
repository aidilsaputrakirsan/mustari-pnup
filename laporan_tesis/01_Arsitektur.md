# BAB 3: Analisis Arsitektur Aplikasi SIMTA

## 3.1 Tinjauan Arsitektur

Aplikasi SIMTA dibangun dengan dua pendekatan arsitektur frontend yang berbeda untuk menguji efisiensi pemuatan halaman dan manajemen sumber daya.

### 3.1.1 Arsitektur Baseline (Versi 1A)
Pendekatan ini menggunakan pola **Monolithic Bundle** yang umum ditemukan pada aplikasi Vue.js standar tanpa optimasi.

**Karakteristik Utama:**
- **Eager Loading**: Semua komponen halaman (Dashboard, Jadwal, Bimbingan) diimpor secara statis pada saat inisialisasi aplikasi.
- **Single Entry Point**: Seluruh kode aplikasi, termasuk pustaka pihak ketiga yang besar seperti `Chart.js`, dibundel menjadi satu berkas JavaScript (`index.baseline.js`).
- **Global Registration**: Komponen berat diregistrasi secara global di `main.js`, memaksa browser mengunduh kodenya meskipun pengguna tidak sedang membuka halaman yang menggunakannya.

**Kelemahan Teoretis:**
- Waktu muat awal (Initial Load Time) tinggi karena ukuran berkas yang besar.
- Penggunaan bandwidth tidak efisien (mengunduh fitur yang tidak dipakai).
- Kinerja menurun pada perangkat dengan koneksi lambat.

### 3.1.2 Arsitektur Optimized (Versi 1B)
Pendekatan ini menerapkan teknik **Code Splitting** dan **Lazy Loading** modern untuk memecah aplikasi menjadi bagian-bagian kecil (chunks).

**Karakteristik Utama:**
- **Route-Level Code Splitting**: Setiap halaman (View) hanya dimuat kodenya saat pengguna menavigasi ke rute tersebut.
- **Async Components**: Komponen berat seperti `ChartStatistik` dan `CalendarJadwal` dimuat secara asinkron (`defineAsyncComponent`) hanya saat dirender di layar.
- **Vendor Splitting**: Pustaka pihak ketiga dipisahkan ke dalam chunk tersendiri (`vendor-vue`, `vendor-chart`) untuk memaksimalkan caching browser.
- **Prefetching**: Strategi `prefetch` diterapkan pada halaman populer (misal: dari Dashboard memuat Daftar Judul di latar belakang) untuk transisi instan.

**Keunggulan Teoretis:**
- Waktu muat awal sangat cepat (hanya memuat kerangka aplikasi).
- Efisiensi sumber daya tinggi (On-Demand Loading).
- Pengalaman pengguna (UX) lebih responsif.

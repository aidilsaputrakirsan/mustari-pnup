# LAMPIRAN C: Panduan Replikasi Eksperimen

Panduan ini ditujukan bagi penguji atau peneliti lain yang ingin mereplikasi hasil eksperimen perbandingan arsitektur SIMTA.

## C.1 Persiapan Lingkungan
Pastikan Node.js (minimal v18) dan NPM sudah terinstal.

1.  **Clone Repository** (jika ada) atau ekstrak kode sumber.
2.  **Install Dependencies**:
    ```bash
    npm install
    ```

## C.2 Menjalankan Mode Pengembangan
Untuk memverifikasi fungsionalitas fitur secara visual:

- **Versi Baseline (1A)**:
  ```bash
  npm run dev:baseline
  ```
  Akses di: `http://localhost:3001`

- **Versi Optimized (1B)**:
  ```bash
  npm run dev:optimized
  ```
  Akses di: `http://localhost:3002`

## C.3 Melakukan Build Produksi
Untuk mendapatkan data ukuran bundle yang akurat (minified & compressed):

1.  Jalankan perintah build untuk kedua versi:
    ```bash
    npm run build:baseline
    npm run build:optimized
    ```
2.  Hasil build akan tersimpan di folder:
    - `dist-baseline/`
    - `dist-optimized/`

## C.4 Menganalisis Ukuran File
Gunakan perintah berikut (PowerShell) untuk melihat total ukuran file JavaScript:

```powershell
Get-ChildItem -Recurse dist-baseline -Include *.js | Measure-Object -Property Length -Sum
Get-ChildItem -Recurse dist-optimized -Include *.js | Measure-Object -Property Length -Sum
```

## C.5 Visualisasi Bundle (Hanya Versi 1B)
Untuk melihat visualisasi *treemap* dari modul-modul yang ada:

```bash
npm run analyze
```
Buka file `stats.html` yang terbentuk di browser untuk melihat proporsi ukuran library (Chart.js vs Vue vs Code Aplikasi).

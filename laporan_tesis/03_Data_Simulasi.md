# LAMPIRAN A: Spesifikasi Data Simulasi

Untuk memastikan validitas pengujian tanpa ketergantungan pada koneksi database eksternal, aplikasi menggunakan dataset simulasi yang komprehensif.

## A.1 Struktur Mock Data
Berkas: `src/services/mockData.js`

Data simulasi dirancang untuk mencerminkan volume data nyata di lingkungan akademik:

1.  **Data Judul Skripsi**: 50+ entri
    - Status bervariasi: *Diajukan, Disetujui, Revisi, Ditolak, Selesai*.
    - Mencakup berbagai bidang minat (Web, Mobile, AI, IoT).
    - Atribut lengkap: Judul, Mahasiswa, Pembimbing 1 & 2, Abstrak.

2.  **Data Bimbingan**: Rekam jejak bimbingan detail
    - Log aktivitas bimbingan (tanggal, topik, status, catatan dosen).
    - Progres bar dinamis berdasarkan jumlah bimbingan yang disetujui.

3.  **Data Jadwal Seminar**: Simulasi kalender akademik
    - Jenis: *Seminar Proposal* dan *Sidang Akhir*.
    - Status: *Terjadwal, Menunggu Konfirmasi, Selesai*.
    - Terintegrasi dengan komponen Kalender Visual.

4.  **Riwayat Chat**: Simulasi komunikasi realtime
    - Pesan teks antara dosen dan mahasiswa.
    - Timestamp dan status baca.

## A.2 Mekanisme Simulasi Latency
Berkas: `src/services/supabase.js`

Untuk meniru perilaku jaringan nyata (Real World API), service layer dilengkapi dengan penundaan buatan (artificial delay):

```javascript
// Simulasi latency jaringan 200ms - 1500ms
const simulateDelay = () => {
  return new Promise(resolve => 
    setTimeout(resolve, 200 + Math.random() * 1300)
  )
}
```

Hal ini memastikan bahwa *loading states* (spinner, skeleton loader) dapat diuji secara visual, memberikan pengalaman pengguna yang realistis meskipun tanpa backend sesungguhnya.

/**
 * ============================================
 * SIMTA - Mock Data Service
 * Data simulasi untuk menggantikan koneksi Supabase
 * ============================================
 */

// Daftar dosen pembimbing
export const dosenList = [
    { id: 1, nama: 'Dr. Ahmad Ridwan, M.Kom.', bidang: 'Rekayasa Perangkat Lunak', email: 'ahmad.ridwan@univ.ac.id' },
    { id: 2, nama: 'Prof. Siti Nurhaliza, Ph.D.', bidang: 'Kecerdasan Buatan', email: 'siti.nurhaliza@univ.ac.id' },
    { id: 3, nama: 'Dr. Bambang Sutrisno, M.T.', bidang: 'Jaringan Komputer', email: 'bambang.s@univ.ac.id' },
    { id: 4, nama: 'Dr. Dewi Puspita, M.Cs.', bidang: 'Data Science', email: 'dewi.puspita@univ.ac.id' },
    { id: 5, nama: 'Dr. Hendra Wijaya, M.Kom.', bidang: 'Sistem Informasi', email: 'hendra.w@univ.ac.id' },
]

// Daftar mahasiswa
export const mahasiswaList = [
    { id: 1, nim: '2021001', nama: 'Andi Pratama', angkatan: 2021, prodi: 'Teknik Informatika' },
    { id: 2, nim: '2021002', nama: 'Budi Santoso', angkatan: 2021, prodi: 'Teknik Informatika' },
    { id: 3, nim: '2021003', nama: 'Citra Dewi', angkatan: 2021, prodi: 'Sistem Informasi' },
    { id: 4, nim: '2021004', nama: 'Dian Permata', angkatan: 2021, prodi: 'Teknik Informatika' },
    { id: 5, nim: '2021005', nama: 'Eko Saputra', angkatan: 2021, prodi: 'Sistem Informasi' },
    { id: 6, nim: '2020001', nama: 'Fitri Handayani', angkatan: 2020, prodi: 'Teknik Informatika' },
    { id: 7, nim: '2020002', nama: 'Gunawan Hidayat', angkatan: 2020, prodi: 'Teknik Informatika' },
    { id: 8, nim: '2020003', nama: 'Hana Safitri', angkatan: 2020, prodi: 'Sistem Informasi' },
    { id: 9, nim: '2022001', nama: 'Irfan Maulana', angkatan: 2022, prodi: 'Teknik Informatika' },
    { id: 10, nim: '2022002', nama: 'Joko Widodo', angkatan: 2022, prodi: 'Sistem Informasi' },
]

// Status judul yang mungkin
const statusJudul = ['Diajukan', 'Disetujui', 'Revisi', 'Ditolak', 'Sedang Berjalan', 'Selesai']
const statusWarna = {
    'Diajukan': 'badge-info',
    'Disetujui': 'badge-success',
    'Revisi': 'badge-warning',
    'Ditolak': 'badge-danger',
    'Sedang Berjalan': 'badge-info',
    'Selesai': 'badge-success',
}

// Generate 50+ judul skripsi
export const judulSkripsiList = [
    { id: 1, judul: 'Implementasi Machine Learning untuk Prediksi Kelulusan Mahasiswa', mahasiswa_id: 1, dosen_id: 2, status: 'Sedang Berjalan', tanggal_ajuan: '2025-09-15', bidang: 'Kecerdasan Buatan' },
    { id: 2, judul: 'Rancang Bangun Sistem E-Voting Berbasis Blockchain', mahasiswa_id: 2, dosen_id: 1, status: 'Disetujui', tanggal_ajuan: '2025-08-20', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 3, judul: 'Analisis Sentimen Media Sosial Menggunakan NLP', mahasiswa_id: 3, dosen_id: 4, status: 'Revisi', tanggal_ajuan: '2025-10-01', bidang: 'Data Science' },
    { id: 4, judul: 'Pengembangan Aplikasi IoT untuk Smart Campus', mahasiswa_id: 4, dosen_id: 3, status: 'Sedang Berjalan', tanggal_ajuan: '2025-07-12', bidang: 'Jaringan Komputer' },
    { id: 5, judul: 'Sistem Rekomendasi Buku Perpustakaan dengan Collaborative Filtering', mahasiswa_id: 5, dosen_id: 2, status: 'Diajukan', tanggal_ajuan: '2025-11-05', bidang: 'Kecerdasan Buatan' },
    { id: 6, judul: 'Deteksi Penyakit Tanaman Padi Menggunakan CNN', mahasiswa_id: 6, dosen_id: 2, status: 'Selesai', tanggal_ajuan: '2025-03-10', bidang: 'Kecerdasan Buatan' },
    { id: 7, judul: 'Implementasi CI/CD Pipeline untuk Aplikasi Microservice', mahasiswa_id: 7, dosen_id: 1, status: 'Sedang Berjalan', tanggal_ajuan: '2025-06-22', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 8, judul: 'Aplikasi Mobile Absensi Berbasis Face Recognition', mahasiswa_id: 8, dosen_id: 5, status: 'Revisi', tanggal_ajuan: '2025-09-28', bidang: 'Sistem Informasi' },
    { id: 9, judul: 'Optimasi Query Database dengan Teknik Indexing pada PostgreSQL', mahasiswa_id: 9, dosen_id: 4, status: 'Diajukan', tanggal_ajuan: '2025-12-01', bidang: 'Data Science' },
    { id: 10, judul: 'Perancangan Network Monitoring System Berbasis SNMP', mahasiswa_id: 10, dosen_id: 3, status: 'Ditolak', tanggal_ajuan: '2025-10-15', bidang: 'Jaringan Komputer' },
    { id: 11, judul: 'Sistem Pendeteksi Plagiarisme Menggunakan Algoritma Rabin-Karp', mahasiswa_id: 1, dosen_id: 1, status: 'Diajukan', tanggal_ajuan: '2025-11-20', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 12, judul: 'Pengembangan Chatbot Akademik dengan GPT API', mahasiswa_id: 2, dosen_id: 2, status: 'Sedang Berjalan', tanggal_ajuan: '2025-08-05', bidang: 'Kecerdasan Buatan' },
    { id: 13, judul: 'Analisis Performa GraphQL vs REST API pada Aplikasi Real-Time', mahasiswa_id: 3, dosen_id: 1, status: 'Disetujui', tanggal_ajuan: '2025-09-10', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 14, judul: 'Implementasi Data Warehouse untuk Analisis Akademik', mahasiswa_id: 4, dosen_id: 4, status: 'Sedang Berjalan', tanggal_ajuan: '2025-07-25', bidang: 'Data Science' },
    { id: 15, judul: 'Sistem Manajemen Inventaris Laboratorium Berbasis Web', mahasiswa_id: 5, dosen_id: 5, status: 'Selesai', tanggal_ajuan: '2025-04-15', bidang: 'Sistem Informasi' },
    { id: 16, judul: 'Klasifikasi Citra Satelit untuk Identifikasi Lahan Pertanian', mahasiswa_id: 6, dosen_id: 2, status: 'Diajukan', tanggal_ajuan: '2025-12-10', bidang: 'Kecerdasan Buatan' },
    { id: 17, judul: 'Pengembangan Game Edukasi Pemrograman untuk Anak-Anak', mahasiswa_id: 7, dosen_id: 1, status: 'Revisi', tanggal_ajuan: '2025-10-20', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 18, judul: 'Sistem Parkir Cerdas dengan Sensor Ultrasonik dan ESP32', mahasiswa_id: 8, dosen_id: 3, status: 'Sedang Berjalan', tanggal_ajuan: '2025-08-15', bidang: 'Jaringan Komputer' },
    { id: 19, judul: 'Prediksi Harga Saham dengan Model LSTM', mahasiswa_id: 9, dosen_id: 4, status: 'Disetujui', tanggal_ajuan: '2025-09-05', bidang: 'Data Science' },
    { id: 20, judul: 'Dashboard Analitik Kinerja Karyawan Berbasis Web', mahasiswa_id: 10, dosen_id: 5, status: 'Selesai', tanggal_ajuan: '2025-05-20', bidang: 'Sistem Informasi' },
    { id: 21, judul: 'Implementasi SSO (Single Sign-On) untuk Portal Akademik', mahasiswa_id: 1, dosen_id: 3, status: 'Sedang Berjalan', tanggal_ajuan: '2025-07-01', bidang: 'Jaringan Komputer' },
    { id: 22, judul: 'Sistem Deteksi Intrusi Jaringan Berbasis Deep Learning', mahasiswa_id: 2, dosen_id: 3, status: 'Diajukan', tanggal_ajuan: '2025-11-15', bidang: 'Jaringan Komputer' },
    { id: 23, judul: 'Aplikasi Pengelolaan Keuangan Pribadi dengan Fitur OCR', mahasiswa_id: 3, dosen_id: 5, status: 'Revisi', tanggal_ajuan: '2025-10-05', bidang: 'Sistem Informasi' },
    { id: 24, judul: 'Segmentasi Pelanggan E-Commerce dengan K-Means Clustering', mahasiswa_id: 4, dosen_id: 4, status: 'Disetujui', tanggal_ajuan: '2025-08-30', bidang: 'Data Science' },
    { id: 25, judul: 'Framework Testing Otomatis untuk Aplikasi Vue.js', mahasiswa_id: 5, dosen_id: 1, status: 'Sedang Berjalan', tanggal_ajuan: '2025-06-15', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 26, judul: 'Sistem E-Learning Adaptif Berbasis Profil Belajar Mahasiswa', mahasiswa_id: 6, dosen_id: 5, status: 'Diajukan', tanggal_ajuan: '2025-12-05', bidang: 'Sistem Informasi' },
    { id: 27, judul: 'Optimasi Algoritma Dijkstra untuk Navigasi Indoor', mahasiswa_id: 7, dosen_id: 2, status: 'Sedang Berjalan', tanggal_ajuan: '2025-09-20', bidang: 'Kecerdasan Buatan' },
    { id: 28, judul: 'Pengembangan API Gateway untuk Arsitektur Microservice', mahasiswa_id: 8, dosen_id: 1, status: 'Disetujui', tanggal_ajuan: '2025-07-10', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 29, judul: 'Visualisasi Data COVID-19 Interaktif dengan D3.js', mahasiswa_id: 9, dosen_id: 4, status: 'Selesai', tanggal_ajuan: '2025-02-28', bidang: 'Data Science' },
    { id: 30, judul: 'Implementasi WebSocket untuk Aplikasi Chat Real-Time', mahasiswa_id: 10, dosen_id: 3, status: 'Sedang Berjalan', tanggal_ajuan: '2025-08-10', bidang: 'Jaringan Komputer' },
    { id: 31, judul: 'Perbandingan Performa Vue.js dan React.js pada SPA', mahasiswa_id: 1, dosen_id: 1, status: 'Revisi', tanggal_ajuan: '2025-10-25', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 32, judul: 'Sistem Pakar Diagnosis Penyakit Hewan Ternak', mahasiswa_id: 2, dosen_id: 2, status: 'Diajukan', tanggal_ajuan: '2025-11-30', bidang: 'Kecerdasan Buatan' },
    { id: 33, judul: 'Aplikasi Manajemen Proyek Agile Berbasis Kanban Board', mahasiswa_id: 3, dosen_id: 5, status: 'Sedang Berjalan', tanggal_ajuan: '2025-06-28', bidang: 'Sistem Informasi' },
    { id: 34, judul: 'Analisis Big Data Transportasi Publik Kota Makassar', mahasiswa_id: 4, dosen_id: 4, status: 'Disetujui', tanggal_ajuan: '2025-09-12', bidang: 'Data Science' },
    { id: 35, judul: 'Implementasi Load Balancer dengan Nginx pada Cloud Server', mahasiswa_id: 5, dosen_id: 3, status: 'Selesai', tanggal_ajuan: '2025-04-01', bidang: 'Jaringan Komputer' },
    { id: 36, judul: 'Pengenalan Wajah Real-Time dengan OpenCV dan TensorFlow', mahasiswa_id: 6, dosen_id: 2, status: 'Sedang Berjalan', tanggal_ajuan: '2025-08-22', bidang: 'Kecerdasan Buatan' },
    { id: 37, judul: 'Sistem Informasi Tracer Study Alumni', mahasiswa_id: 7, dosen_id: 5, status: 'Revisi', tanggal_ajuan: '2025-10-08', bidang: 'Sistem Informasi' },
    { id: 38, judul: 'Pengembangan PWA untuk Aplikasi Jadwal Kuliah', mahasiswa_id: 8, dosen_id: 1, status: 'Diajukan', tanggal_ajuan: '2025-12-15', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 39, judul: 'ETL Pipeline untuk Data Akademik Menggunakan Apache Airflow', mahasiswa_id: 9, dosen_id: 4, status: 'Sedang Berjalan', tanggal_ajuan: '2025-07-18', bidang: 'Data Science' },
    { id: 40, judul: 'Implementasi VPN Site-to-Site dengan WireGuard', mahasiswa_id: 10, dosen_id: 3, status: 'Disetujui', tanggal_ajuan: '2025-09-25', bidang: 'Jaringan Komputer' },
    { id: 41, judul: 'Sistem Rekomendasi Film dengan Content-Based Filtering', mahasiswa_id: 1, dosen_id: 2, status: 'Sedang Berjalan', tanggal_ajuan: '2025-06-05', bidang: 'Kecerdasan Buatan' },
    { id: 42, judul: 'Pengembangan Design System untuk Aplikasi Enterprise', mahasiswa_id: 2, dosen_id: 1, status: 'Selesai', tanggal_ajuan: '2025-03-15', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 43, judul: 'Analisis Performa NoSQL vs SQL pada Aplikasi Skala Besar', mahasiswa_id: 3, dosen_id: 4, status: 'Diajukan', tanggal_ajuan: '2025-11-25', bidang: 'Data Science' },
    { id: 44, judul: 'Sistem Monitoring Server dengan Prometheus dan Grafana', mahasiswa_id: 4, dosen_id: 3, status: 'Revisi', tanggal_ajuan: '2025-10-30', bidang: 'Jaringan Komputer' },
    { id: 45, judul: 'Aplikasi Penjualan Online dengan Payment Gateway Midtrans', mahasiswa_id: 5, dosen_id: 5, status: 'Sedang Berjalan', tanggal_ajuan: '2025-08-08', bidang: 'Sistem Informasi' },
    { id: 46, judul: 'Deteksi Objek pada Citra Drone menggunakan YOLOv8', mahasiswa_id: 6, dosen_id: 2, status: 'Disetujui', tanggal_ajuan: '2025-09-18', bidang: 'Kecerdasan Buatan' },
    { id: 47, judul: 'Implementasi Serverless Architecture dengan AWS Lambda', mahasiswa_id: 7, dosen_id: 1, status: 'Sedang Berjalan', tanggal_ajuan: '2025-07-30', bidang: 'Rekayasa Perangkat Lunak' },
    { id: 48, judul: 'Time Series Forecasting Konsumsi Energi Listrik', mahasiswa_id: 8, dosen_id: 4, status: 'Diajukan', tanggal_ajuan: '2025-12-20', bidang: 'Data Science' },
    { id: 49, judul: 'Pengembangan SDN Controller untuk Jaringan Kampus', mahasiswa_id: 9, dosen_id: 3, status: 'Selesai', tanggal_ajuan: '2025-05-10', bidang: 'Jaringan Komputer' },
    { id: 50, judul: 'Sistem Informasi Geografis Pemetaan Fasilitas Kampus', mahasiswa_id: 10, dosen_id: 5, status: 'Sedang Berjalan', tanggal_ajuan: '2025-08-25', bidang: 'Sistem Informasi' },
]

// Data bimbingan
export const bimbinganList = [
    { id: 1, judul_id: 1, tanggal: '2025-10-01', topik: 'Pembahasan BAB I - Pendahuluan', catatan: 'Perbaiki latar belakang masalah, tambahkan data statistik kelulusan', status: 'Selesai', progres: 15 },
    { id: 2, judul_id: 1, tanggal: '2025-10-15', topik: 'Review Tinjauan Pustaka', catatan: 'Tambahkan 5 referensi jurnal internasional terbaru (2023-2025)', status: 'Selesai', progres: 25 },
    { id: 3, judul_id: 1, tanggal: '2025-11-01', topik: 'Metodologi Penelitian', catatan: 'Gunakan metode CRISP-DM, jelaskan setiap fase dengan jelas', status: 'Selesai', progres: 40 },
    { id: 4, judul_id: 1, tanggal: '2025-11-15', topik: 'Desain Arsitektur Sistem', catatan: 'Buat diagram UML: use case, activity, dan class diagram', status: 'Selesai', progres: 55 },
    { id: 5, judul_id: 1, tanggal: '2025-12-01', topik: 'Progress Implementasi', catatan: 'Demo prototype model ML, akurasi masih 72%, perlu tuning hyperparameter', status: 'Sedang Berjalan', progres: 65 },
    { id: 6, judul_id: 2, tanggal: '2025-09-05', topik: 'Konsultasi Judul & Ruang Lingkup', catatan: 'Judul disetujui, fokuskan pada aspek keamanan blockchain', status: 'Selesai', progres: 10 },
    { id: 7, judul_id: 2, tanggal: '2025-09-20', topik: 'Studi Literatur Blockchain', catatan: 'Bandingkan Ethereum vs Hyperledger untuk use case voting', status: 'Selesai', progres: 20 },
    { id: 8, judul_id: 2, tanggal: '2025-10-10', topik: 'Smart Contract Design', catatan: 'Draft smart contract menggunakan Solidity, review keamanan', status: 'Sedang Berjalan', progres: 35 },
    { id: 9, judul_id: 4, tanggal: '2025-08-01', topik: 'Pemilihan Sensor IoT', catatan: 'Gunakan DHT22 untuk suhu, MQ-135 untuk kualitas udara', status: 'Selesai', progres: 20 },
    { id: 10, judul_id: 4, tanggal: '2025-09-01', topik: 'Arsitektur MQTT', catatan: 'Setup broker Mosquitto, tentukan topic hierarchy', status: 'Selesai', progres: 40 },
    { id: 11, judul_id: 7, tanggal: '2025-07-10', topik: 'Setup Jenkins Pipeline', catatan: 'Konfigurasi Jenkins dengan Docker, buat Jenkinsfile awal', status: 'Selesai', progres: 30 },
    { id: 12, judul_id: 7, tanggal: '2025-08-15', topik: 'Unit Testing Strategy', catatan: 'Capai minimal 80% code coverage, gunakan Jest + Supertest', status: 'Sedang Berjalan', progres: 50 },
]

// Chat history bimbingan
export const chatHistory = [
    { id: 1, bimbingan_id: 5, sender: 'mahasiswa', pesan: 'Pak, saya sudah meningkatkan akurasi model menjadi 78% setelah tuning hyperparameter.', waktu: '2025-12-01 09:15:00' },
    { id: 2, bimbingan_id: 5, sender: 'dosen', pesan: 'Bagus! Coba gunakan teknik cross-validation 10-fold untuk validasi yang lebih robust.', waktu: '2025-12-01 09:30:00' },
    { id: 3, bimbingan_id: 5, sender: 'mahasiswa', pesan: 'Baik Pak. Apakah perlu saya tambahkan confusion matrix di laporan?', waktu: '2025-12-01 09:35:00' },
    { id: 4, bimbingan_id: 5, sender: 'dosen', pesan: 'Ya, wajib ada confusion matrix, classification report (precision, recall, F1-score), dan ROC curve.', waktu: '2025-12-01 09:40:00' },
    { id: 5, bimbingan_id: 5, sender: 'mahasiswa', pesan: 'Siap Pak, saya akan kerjakan dan upload hasilnya minggu depan.', waktu: '2025-12-01 09:45:00' },
    { id: 6, bimbingan_id: 8, sender: 'mahasiswa', pesan: 'Bu, draft smart contract sudah selesai. Mohon review.', waktu: '2025-10-10 14:00:00' },
    { id: 7, bimbingan_id: 8, sender: 'dosen', pesan: 'Saya sudah review. Ada potensi reentrancy attack di fungsi vote(). Perlu pakai ReentrancyGuard.', waktu: '2025-10-10 16:30:00' },
    { id: 8, bimbingan_id: 8, sender: 'mahasiswa', pesan: 'Terima kasih Bu. Saya akan perbaiki dan tambahkan unit test untuk security.', waktu: '2025-10-10 17:00:00' },
]

// Jadwal seminar
export const jadwalSeminar = [
    { id: 1, jenis: 'Seminar Proposal', mahasiswa_id: 1, judul_id: 1, tanggal: '2026-01-15', waktu: '09:00', ruangan: 'Lab RPL Lt. 3', penguji: [1, 4], status: 'Terjadwal' },
    { id: 2, jenis: 'Sidang Akhir', mahasiswa_id: 6, judul_id: 6, tanggal: '2026-01-20', waktu: '10:00', ruangan: 'Aula Gedung B', penguji: [1, 3], status: 'Terjadwal' },
    { id: 3, jenis: 'Seminar Proposal', mahasiswa_id: 4, judul_id: 4, tanggal: '2026-01-22', waktu: '13:00', ruangan: 'Lab Jarkom Lt. 2', penguji: [2, 5], status: 'Terjadwal' },
    { id: 4, jenis: 'Sidang Akhir', mahasiswa_id: 7, judul_id: 7, tanggal: '2026-02-05', waktu: '09:00', ruangan: 'Lab RPL Lt. 3', penguji: [3, 4], status: 'Menunggu Konfirmasi' },
    { id: 5, jenis: 'Seminar Proposal', mahasiswa_id: 2, judul_id: 12, tanggal: '2026-02-10', waktu: '14:00', ruangan: 'Lab AI Lt. 4', penguji: [1, 5], status: 'Terjadwal' },
    { id: 6, jenis: 'Sidang Akhir', mahasiswa_id: 5, judul_id: 15, tanggal: '2026-02-15', waktu: '10:00', ruangan: 'Aula Gedung B', penguji: [2, 3], status: 'Selesai' },
    { id: 7, jenis: 'Seminar Proposal', mahasiswa_id: 9, judul_id: 19, tanggal: '2026-02-20', waktu: '09:00', ruangan: 'Lab DS Lt. 3', penguji: [1, 2], status: 'Terjadwal' },
    { id: 8, jenis: 'Sidang Akhir', mahasiswa_id: 10, judul_id: 20, tanggal: '2026-02-25', waktu: '13:00', ruangan: 'Lab SI Lt. 2', penguji: [3, 5], status: 'Menunggu Konfirmasi' },
]

// Profil user (simulasi user yang login)
export const currentUser = {
    id: 1,
    nama: 'Andi Pratama',
    nim: '2021001',
    email: 'andi.pratama@student.univ.ac.id',
    prodi: 'Teknik Informatika',
    angkatan: 2021,
    telepon: '081234567890',
    alamat: 'Jl. Perintis Kemerdekaan No. 45, Makassar',
    foto: null,
    role: 'mahasiswa',
    dosen_pembimbing_id: 2,
}

// Statistik dashboard
export const dashboardStats = {
    totalBimbingan: 12,
    bimbinganBulanIni: 3,
    totalJudul: 50,
    judulDisetujui: 12,
    judulRevisi: 8,
    judulDitolak: 2,
    judulSedangBerjalan: 15,
    judulSelesai: 7,
    judulDiajukan: 6,
    seminarTerjadwal: 5,
    seminarSelesai: 1,
    progresRataRata: 42,
}

// Helper: cari data relasional
export function getMahasiswaById(id) {
    return mahasiswaList.find(m => m.id === id)
}

export function getDosenById(id) {
    return dosenList.find(d => d.id === id)
}

export function getJudulById(id) {
    return judulSkripsiList.find(j => j.id === id)
}

export function getBimbinganByJudulId(judulId) {
    return bimbinganList.filter(b => b.judul_id === judulId)
}

export function getChatByBimbinganId(bimbinganId) {
    return chatHistory.filter(c => c.bimbingan_id === bimbinganId)
}

export { statusWarna }

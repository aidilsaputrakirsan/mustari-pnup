/**
 * ============================================
 * SIMTA DEMO - SEEDER DATA
 * ============================================
 * Data simulasi arsip Tugas Akhir lintas semester.
 * Tidak ada database: seluruh isi dibangkitkan di sini
 * secara DETERMINISTIK, sehingga angka yang tampil
 * selalu sama di setiap build maupun setiap perangkat.
 * ============================================
 */

/** PRNG mulberry32 — deterministik, tidak memakai Math.random(). */
function buatAcak(benih) {
    let a = benih >>> 0
    return function () {
        a = (a + 0x6d2b79f5) >>> 0
        let t = Math.imul(a ^ (a >>> 15), 1 | a)
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296
    }
}

const acak = buatAcak(20260818)
const pilih = (arr) => arr[Math.floor(acak() * arr.length)]
const antara = (min, maks) => Math.floor(acak() * (maks - min + 1)) + min

/* ============================================
   REFERENSI
   ============================================ */

export const daftarSemester = [
    { kode: '20231', label: '2023/2024 Ganjil', urut: 1, aktif: false },
    { kode: '20232', label: '2023/2024 Genap', urut: 2, aktif: false },
    { kode: '20241', label: '2024/2025 Ganjil', urut: 3, aktif: false },
    { kode: '20242', label: '2024/2025 Genap', urut: 4, aktif: false },
    { kode: '20251', label: '2025/2026 Ganjil', urut: 5, aktif: false },
    { kode: '20252', label: '2025/2026 Genap', urut: 6, aktif: true },
]

export const daftarProdi = [
    { kode: 'D4TI', nama: 'D4 Teknik Informatika' },
    { kode: 'D4TKJ', nama: 'D4 Teknik Komputer dan Jaringan' },
    { kode: 'D3TI', nama: 'D3 Teknik Informatika' },
]

export const daftarBidang = [
    'Rekayasa Perangkat Lunak',
    'Kecerdasan Buatan',
    'Jaringan & Keamanan',
    'Sains Data',
    'Sistem Informasi',
    'Sistem Tertanam & IoT',
]

export const daftarDosen = [
    { id: 1, nidn: '0012057801', nama: 'Dr. Ahmad Ridwan, S.T., M.Kom.', bidang: 'Rekayasa Perangkat Lunak', jabatan: 'Lektor Kepala', kuota: 8 },
    { id: 2, nidn: '0025098102', nama: 'Prof. Dr. Siti Nurhaliza, M.Eng.', bidang: 'Kecerdasan Buatan', jabatan: 'Guru Besar', kuota: 6 },
    { id: 3, nidn: '0003117903', nama: 'Dr. Bambang Sutrisno, S.Kom., M.T.', bidang: 'Jaringan & Keamanan', jabatan: 'Lektor Kepala', kuota: 8 },
    { id: 4, nidn: '0018038404', nama: 'Dr. Dewi Puspita, S.Si., M.Cs.', bidang: 'Sains Data', jabatan: 'Lektor', kuota: 8 },
    { id: 5, nidn: '0007068005', nama: 'Dr. Hendra Wijaya, S.T., M.Kom.', bidang: 'Sistem Informasi', jabatan: 'Lektor Kepala', kuota: 8 },
    { id: 6, nidn: '0029128506', nama: 'Muh. Ilham Akbar, S.T., M.T.', bidang: 'Sistem Tertanam & IoT', jabatan: 'Lektor', kuota: 10 },
    { id: 7, nidn: '0014078707', nama: 'Nurul Fadhilah, S.Kom., M.Kom.', bidang: 'Rekayasa Perangkat Lunak', jabatan: 'Lektor', kuota: 10 },
    { id: 8, nidn: '0021048808', nama: 'Rahmat Hidayat, S.T., M.Eng.', bidang: 'Jaringan & Keamanan', jabatan: 'Asisten Ahli', kuota: 10 },
    { id: 9, nidn: '0009098309', nama: 'Dr. Andi Tenri Ola, S.Si., M.Si.', bidang: 'Sains Data', jabatan: 'Lektor', kuota: 8 },
    { id: 10, nidn: '0002028610', nama: 'Fajar Ramadhan, S.Kom., M.T.', bidang: 'Kecerdasan Buatan', jabatan: 'Lektor', kuota: 10 },
    { id: 11, nidn: '0016118911', nama: 'Ir. Hasnawati Malik, M.T.', bidang: 'Sistem Informasi', jabatan: 'Lektor', kuota: 8 },
    { id: 12, nidn: '0027059012', nama: 'Zulkifli Nurdin, S.T., M.Kom.', bidang: 'Sistem Tertanam & IoT', jabatan: 'Asisten Ahli', kuota: 10 },
    { id: 13, nidn: '0011088213', nama: 'Dr. Sri Wahyuni, S.Kom., M.Cs.', bidang: 'Rekayasa Perangkat Lunak', jabatan: 'Lektor Kepala', kuota: 8 },
    { id: 14, nidn: '0023039114', nama: 'Ridwan Saputra, S.Kom., M.Kom.', bidang: 'Jaringan & Keamanan', jabatan: 'Asisten Ahli', kuota: 10 },
]

const depanPria = ['Andi', 'Muh.', 'Ahmad', 'Rizky', 'Fajar', 'Ilham', 'Yusuf', 'Bayu', 'Dimas', 'Arif', 'Hendra', 'Reza', 'Aldi', 'Fikri', 'Taufik', 'Irfan', 'Agus', 'Rahmat', 'Zulfikar', 'Bagus']
const depanWanita = ['Nur', 'Siti', 'Dewi', 'Putri', 'Anisa', 'Fitri', 'Indah', 'Rani', 'Sari', 'Ayu', 'Melati', 'Hasna', 'Alya', 'Citra', 'Wulan', 'Nabila', 'Salsa', 'Intan', 'Zahra', 'Karina']
const belakang = ['Pratama', 'Santoso', 'Wijaya', 'Nugroho', 'Ramadhan', 'Maulana', 'Hidayat', 'Saputra', 'Kurniawan', 'Permata', 'Lestari', 'Anggraini', 'Handayani', 'Safitri', 'Rahmawati', 'Mahendra', 'Tenri', 'Baso', 'Sulaiman', 'Amelia', 'Fauziah', 'Wardana', 'Setiawan', 'Utami']

const polaJudul = {
    'Rekayasa Perangkat Lunak': [
        'Rancang Bangun Sistem Informasi {objek} Berbasis Web',
        'Penerapan Arsitektur Microservice pada Aplikasi {objek}',
        'Pengembangan Aplikasi Mobile {objek} dengan Flutter',
        'Implementasi CI/CD Pipeline pada Pengembangan {objek}',
        'Rancang Bangun Progressive Web App untuk {objek}',
        'Penerapan Metode Scrum dalam Pengembangan {objek}',
    ],
    'Kecerdasan Buatan': [
        'Klasifikasi {objek} Menggunakan Convolutional Neural Network',
        'Penerapan Algoritma Naive Bayes untuk Prediksi {objek}',
        'Sistem Pakar Diagnosis {objek} Berbasis Forward Chaining',
        'Deteksi {objek} Secara Real-Time Menggunakan YOLO',
        'Implementasi Model LSTM untuk Peramalan {objek}',
        'Optimasi Hyperparameter pada Model Prediksi {objek}',
    ],
    'Jaringan & Keamanan': [
        'Analisis Kinerja Jaringan {objek} Menggunakan Metode QoS',
        'Implementasi VLAN dan Routing Dinamis pada Jaringan {objek}',
        'Rancang Bangun Sistem Deteksi Intrusi pada {objek}',
        'Penerapan VPN Site-to-Site untuk {objek}',
        'Audit Keamanan Sistem {objek} Menggunakan Standar ISO 27001',
        'Optimasi Load Balancing pada Server {objek}',
    ],
    'Sains Data': [
        'Analisis Sentimen {objek} Menggunakan Natural Language Processing',
        'Segmentasi {objek} dengan Algoritma K-Means Clustering',
        'Perancangan Data Warehouse untuk {objek}',
        'Visualisasi Data {objek} Berbasis Dashboard Interaktif',
        'Penerapan Association Rule Mining pada Data {objek}',
        'Analisis Prediktif {objek} Menggunakan Random Forest',
    ],
    'Sistem Informasi': [
        'Perancangan Sistem Informasi Manajemen {objek}',
        'Evaluasi Usability Sistem {objek} Menggunakan Metode SUS',
        'Implementasi ERP Modul {objek} pada UMKM',
        'Analisis dan Perancangan Sistem {objek} dengan Metode Waterfall',
        'Pengukuran Tingkat Kematangan Tata Kelola TI pada {objek}',
        'Rancang Bangun Sistem Pendukung Keputusan {objek} Metode SAW',
    ],
    'Sistem Tertanam & IoT': [
        'Rancang Bangun Sistem Monitoring {objek} Berbasis IoT',
        'Prototipe Kendali Otomatis {objek} Menggunakan ESP32',
        'Implementasi Protokol MQTT pada Sistem {objek}',
        'Sistem Peringatan Dini {objek} Berbasis Mikrokontroler',
        'Rancang Bangun Smart {objek} dengan Sensor Terintegrasi',
        'Penerapan LoRa untuk Komunikasi Data {objek}',
    ],
}

const objekJudul = [
    'Perpustakaan Kampus', 'Koperasi Mahasiswa', 'Presensi Perkuliahan', 'Inventaris Laboratorium',
    'Penjadwalan Kuliah', 'Pengelolaan Beasiswa', 'Layanan Akademik', 'Praktik Kerja Lapangan',
    'Kualitas Air Tambak', 'Kesehatan Tanaman Padi', 'Konsumsi Energi Listrik', 'Kemacetan Lalu Lintas',
    'Sampah Perkotaan', 'Produksi UMKM', 'Distribusi Logistik', 'Rumah Sakit Daerah',
    'Pariwisata Sulawesi Selatan', 'Kualitas Udara Kampus', 'Penjualan Ritel', 'Peternakan Ayam',
    'Parkir Kendaraan', 'Ruang Kelas', 'Alumni Politeknik', 'Tagihan Uang Kuliah',
]

const topikBimbingan = [
    'Konsultasi Judul dan Ruang Lingkup', 'Penyusunan Latar Belakang Masalah', 'Review Tinjauan Pustaka',
    'Penetapan Metodologi Penelitian', 'Perancangan Arsitektur Sistem', 'Review Diagram UML',
    'Progres Implementasi Tahap I', 'Progres Implementasi Tahap II', 'Pengujian dan Validasi Sistem',
    'Analisis Hasil Pengujian', 'Penyusunan Pembahasan', 'Penyusunan Kesimpulan dan Saran',
    'Persiapan Seminar Proposal', 'Perbaikan Pasca Seminar', 'Finalisasi Naskah',
]

const catatanBimbingan = [
    'Perjelas rumusan masalah agar sejalan dengan tujuan penelitian.',
    'Tambahkan minimal lima referensi jurnal terindeks lima tahun terakhir.',
    'Perbaiki sitasi, gunakan gaya IEEE secara konsisten di seluruh naskah.',
    'Lengkapi diagram alir sistem dan sesuaikan dengan implementasi aktual.',
    'Hasil pengujian perlu disajikan dalam tabel beserta analisis statistiknya.',
    'Perbaiki tata tulis pada BAB III, banyak kalimat yang belum efektif.',
    'Tambahkan pembanding dengan penelitian terdahulu pada bagian pembahasan.',
    'Dataset perlu diperbesar agar hasil pelatihan model lebih representatif.',
    'Sudah baik, lanjutkan ke tahap pengujian dengan responden sesungguhnya.',
    'Siapkan slide presentasi maksimal 15 halaman untuk seminar.',
]

const ruangan = ['Lab RPL Lt. 3', 'Lab Jaringan Lt. 2', 'Lab Sains Data Lt. 3', 'Aula Teknik Lt. 1', 'Ruang Sidang TI', 'Lab Multimedia Lt. 4']

/* ============================================
   PEMBANGKIT DATA
   ============================================ */

function namaAcak() {
    const depan = acak() > 0.5 ? pilih(depanPria) : pilih(depanWanita)
    return depan + ' ' + pilih(belakang)
}

function judulAcak(bidang) {
    return pilih(polaJudul[bidang]).replace('{objek}', pilih(objekJudul))
}

// Berapa mahasiswa TA per semester (semester berjalan lebih ramai)
const kuotaPerSemester = { 20231: 36, 20232: 41, 20241: 38, 20242: 44, 20251: 40, 20252: 47 }

export const daftarMahasiswa = []
export const daftarTugasAkhir = []
export const daftarBimbingan = []
export const daftarSeminar = []

let idMhs = 0
let idTa = 0
let idBimbingan = 0
let idSeminar = 0

for (const semester of daftarSemester) {
    const tahun = Number(semester.kode.slice(0, 4))
    const ganjil = semester.kode.endsWith('1')
    const jumlah = kuotaPerSemester[semester.kode]

    for (let i = 0; i < jumlah; i++) {
        idMhs++
        idTa++

        const prodi = pilih(daftarProdi)
        const angkatan = tahun - (prodi.kode.startsWith('D4') ? 3 : 2)
        const urutProdi = prodi.kode === 'D4TI' ? '2' : prodi.kode === 'D4TKJ' ? '3' : '1'
        const nim = String(angkatan).slice(2) + urutProdi + String(idMhs).padStart(3, '0')
        const nama = namaAcak()

        const mahasiswa = {
            id: idMhs,
            nim,
            nama,
            prodi: prodi.nama,
            prodiKode: prodi.kode,
            angkatan,
            email: nama.toLowerCase().replace(/[^a-z]/g, '.') + '@student.poliupg.ac.id',
            ipk: Number((2.9 + acak() * 1.1).toFixed(2)),
        }
        daftarMahasiswa.push(mahasiswa)

        const bidang = pilih(daftarBidang)
        // Pembimbing utama diusahakan sebidang, pendamping bebas
        const sebidang = daftarDosen.filter((d) => d.bidang === bidang)
        const pembimbing1 = pilih(sebidang.length ? sebidang : daftarDosen)
        let pembimbing2 = pilih(daftarDosen)
        while (pembimbing2.id === pembimbing1.id) pembimbing2 = pilih(daftarDosen)

        // Semester lampau sudah tuntas; semester berjalan masih bergerak
        let status
        let progres
        let nilaiHuruf = null
        let nilaiAngka = null

        if (semester.aktif) {
            const undi = acak()
            if (undi < 0.14) { status = 'Diajukan'; progres = antara(0, 10) }
            else if (undi < 0.26) { status = 'Revisi Judul'; progres = antara(5, 15) }
            else if (undi < 0.52) { status = 'Bimbingan'; progres = antara(20, 55) }
            else if (undi < 0.74) { status = 'Seminar Proposal'; progres = antara(55, 70) }
            else if (undi < 0.90) { status = 'Penelitian'; progres = antara(70, 88) }
            else { status = 'Siap Sidang'; progres = antara(90, 98) }
        } else {
            const undi = acak()
            if (undi < 0.90) { status = 'Lulus'; progres = 100 }
            else if (undi < 0.97) { status = 'Perpanjangan'; progres = antara(75, 95) }
            else { status = 'Mengundurkan Diri'; progres = antara(15, 45) }
        }

        if (status === 'Lulus') {
            nilaiAngka = Number((78 + acak() * 20).toFixed(1))
            nilaiHuruf = nilaiAngka >= 91 ? 'A' : nilaiAngka >= 86 ? 'A-' : nilaiAngka >= 81 ? 'B+' : 'B'
        }

        const bulanMulai = ganjil ? 8 : 2
        const tahunAjuan = tahun + (ganjil ? 0 : 1)
        const tanggalAjuan = tahunAjuan + '-' + String(bulanMulai + antara(0, 1)).padStart(2, '0') + '-' + String(antara(1, 28)).padStart(2, '0')

        const ta = {
            id: idTa,
            kode: 'TA-' + semester.kode + '-' + String(i + 1).padStart(3, '0'),
            judul: judulAcak(bidang),
            bidang,
            status,
            progres,
            nilaiHuruf,
            nilaiAngka,
            semester: semester.kode,
            semesterLabel: semester.label,
            semesterAktif: semester.aktif,
            tanggalAjuan,
            mahasiswaId: mahasiswa.id,
            nim: mahasiswa.nim,
            namaMahasiswa: mahasiswa.nama,
            prodi: mahasiswa.prodi,
            prodiKode: mahasiswa.prodiKode,
            angkatan: mahasiswa.angkatan,
            ipk: mahasiswa.ipk,
            pembimbing1Id: pembimbing1.id,
            pembimbing1: pembimbing1.nama,
            pembimbing2Id: pembimbing2.id,
            pembimbing2: pembimbing2.nama,
        }
        daftarTugasAkhir.push(ta)

        // Log bimbingan — makin tinggi progres, makin banyak pertemuan
        const jumlahBimbingan = Math.max(1, Math.round((progres / 100) * 14))
        for (let b = 0; b < jumlahBimbingan; b++) {
            idBimbingan++
            const bulan = bulanMulai + Math.floor((b / jumlahBimbingan) * 5)
            const tahunBimbingan = tahunAjuan + (bulan > 12 ? 1 : 0)
            const bulanNormal = ((bulan - 1) % 12) + 1
            daftarBimbingan.push({
                id: idBimbingan,
                taId: ta.id,
                kodeTa: ta.kode,
                nim: ta.nim,
                namaMahasiswa: ta.namaMahasiswa,
                judul: ta.judul,
                pertemuanKe: b + 1,
                tanggal: tahunBimbingan + '-' + String(bulanNormal).padStart(2, '0') + '-' + String(antara(1, 28)).padStart(2, '0'),
                topik: topikBimbingan[Math.min(b, topikBimbingan.length - 1)],
                catatan: pilih(catatanBimbingan),
                pembimbing: b % 2 === 0 ? ta.pembimbing1 : ta.pembimbing2,
                semester: semester.kode,
                semesterLabel: semester.label,
                disetujui: !(semester.aktif && b === jumlahBimbingan - 1 && acak() < 0.4),
            })
        }

        // Seminar proposal & sidang akhir
        const sudahSempro = progres >= 55 || status === 'Lulus'
        if (sudahSempro) {
            idSeminar++
            daftarSeminar.push({
                id: idSeminar,
                taId: ta.id,
                jenis: 'Seminar Proposal',
                kodeTa: ta.kode,
                nim: ta.nim,
                namaMahasiswa: ta.namaMahasiswa,
                judul: ta.judul,
                prodi: ta.prodi,
                tanggal: tahunAjuan + '-' + String(bulanMulai + 2).padStart(2, '0') + '-' + String(antara(1, 28)).padStart(2, '0'),
                waktu: pilih(['08:00', '09:30', '11:00', '13:00', '14:30']),
                ruangan: pilih(ruangan),
                penguji: [pilih(daftarDosen).nama, pilih(daftarDosen).nama],
                status: semester.aktif ? pilih(['Terjadwal', 'Selesai', 'Menunggu Konfirmasi']) : 'Selesai',
                nilai: semester.aktif ? null : Number((78 + acak() * 20).toFixed(1)),
                semester: semester.kode,
                semesterLabel: semester.label,
            })
        }
        if (status === 'Lulus' || status === 'Siap Sidang') {
            idSeminar++
            daftarSeminar.push({
                id: idSeminar,
                taId: ta.id,
                jenis: 'Sidang Akhir',
                kodeTa: ta.kode,
                nim: ta.nim,
                namaMahasiswa: ta.namaMahasiswa,
                judul: ta.judul,
                prodi: ta.prodi,
                tanggal: tahunAjuan + '-' + String(bulanMulai + 4).padStart(2, '0') + '-' + String(antara(1, 28)).padStart(2, '0'),
                waktu: pilih(['08:00', '09:30', '11:00', '13:00', '14:30']),
                ruangan: pilih(ruangan),
                penguji: [pilih(daftarDosen).nama, pilih(daftarDosen).nama],
                status: status === 'Lulus' ? 'Selesai' : 'Terjadwal',
                nilai: nilaiAngka,
                semester: semester.kode,
                semesterLabel: semester.label,
            })
        }
    }
}

/* ============================================
   AKUN DEMO
   ============================================ */

export const akunDemo = {
    email: 'koorpro@poliupg.ac.id',
    sandi: 'simta2026',
    profil: {
        nama: 'Dr. Ahmad Ridwan, S.T., M.Kom.',
        inisial: 'AR',
        nidn: '0012057801',
        peran: 'Koordinator Program Studi',
        peranSingkat: 'Koorpro',
        unit: 'Program Studi D4 Teknik Informatika',
        institusi: 'Politeknik Negeri Ujung Pandang',
        email: 'koorpro@poliupg.ac.id',
    },
}

/* ============================================
   TURUNAN / AGREGASI
   ============================================ */

export const semesterAktif = daftarSemester.find((s) => s.aktif)

export const statusAktifUrut = ['Diajukan', 'Revisi Judul', 'Bimbingan', 'Seminar Proposal', 'Penelitian', 'Siap Sidang']

/** Severity badge PrimeVue per status. */
export const severityStatus = {
    'Diajukan': 'secondary',
    'Revisi Judul': 'warn',
    'Bimbingan': 'info',
    'Seminar Proposal': 'info',
    'Penelitian': 'contrast',
    'Siap Sidang': 'success',
    'Lulus': 'success',
    'Perpanjangan': 'warn',
    'Mengundurkan Diri': 'danger',
    'Terjadwal': 'info',
    'Selesai': 'success',
    'Menunggu Konfirmasi': 'warn',
}

/** Rekap jumlah TA & kelulusan per semester. */
export const rekapSemester = daftarSemester.map((s) => {
    const isi = daftarTugasAkhir.filter((t) => t.semester === s.kode)
    const lulus = isi.filter((t) => t.status === 'Lulus')
    const nilaiRerata = lulus.length
        ? Number((lulus.reduce((a, t) => a + t.nilaiAngka, 0) / lulus.length).toFixed(2))
        : null
    return {
        kode: s.kode,
        label: s.label,
        aktif: s.aktif,
        total: isi.length,
        lulus: lulus.length,
        berjalan: isi.filter((t) => !['Lulus', 'Mengundurkan Diri'].includes(t.status)).length,
        mundur: isi.filter((t) => t.status === 'Mengundurkan Diri').length,
        persenLulus: Number(((lulus.length / isi.length) * 100).toFixed(1)),
        nilaiRerata,
    }
})

/** Beban bimbingan tiap dosen pada semester berjalan. */
export const bebanDosen = daftarDosen.map((d) => {
    const utama = daftarTugasAkhir.filter((t) => t.semesterAktif && t.pembimbing1Id === d.id)
    const pendamping = daftarTugasAkhir.filter((t) => t.semesterAktif && t.pembimbing2Id === d.id)
    const sepanjangMasa = daftarTugasAkhir.filter((t) => t.pembimbing1Id === d.id || t.pembimbing2Id === d.id)
    const diluluskan = sepanjangMasa.filter((t) => t.status === 'Lulus')
    return {
        ...d,
        bimbinganUtama: utama.length,
        bimbinganPendamping: pendamping.length,
        totalAktif: utama.length + pendamping.length,
        persenKuota: Math.round(((utama.length + pendamping.length) / d.kuota) * 100),
        totalSepanjangMasa: sepanjangMasa.length,
        diluluskan: diluluskan.length,
        rerataNilai: diluluskan.length
            ? Number((diluluskan.reduce((a, t) => a + t.nilaiAngka, 0) / diluluskan.length).toFixed(2))
            : null,
    }
})

/** Sebaran bidang penelitian sepanjang arsip. */
export const sebaranBidang = daftarBidang.map((b) => ({
    bidang: b,
    jumlah: daftarTugasAkhir.filter((t) => t.bidang === b).length,
    aktif: daftarTugasAkhir.filter((t) => t.bidang === b && t.semesterAktif).length,
}))

/** Sebaran status TA pada semester berjalan. */
export const sebaranStatusAktif = statusAktifUrut.map((s) => ({
    status: s,
    jumlah: daftarTugasAkhir.filter((t) => t.semesterAktif && t.status === s).length,
}))

const taAktif = daftarTugasAkhir.filter((t) => t.semesterAktif)

export const ringkasan = {
    totalArsip: daftarTugasAkhir.length,
    totalMahasiswa: daftarMahasiswa.length,
    totalBimbingan: daftarBimbingan.length,
    totalSeminar: daftarSeminar.length,
    taAktif: taAktif.length,
    perluTindakan: taAktif.filter((t) => ['Diajukan', 'Revisi Judul'].includes(t.status)).length,
    siapSidang: taAktif.filter((t) => t.status === 'Siap Sidang').length,
    progresRerata: Math.round(taAktif.reduce((a, t) => a + t.progres, 0) / taAktif.length),
    lulusSepanjangMasa: daftarTugasAkhir.filter((t) => t.status === 'Lulus').length,
    bimbinganBelumDisetujui: daftarBimbingan.filter((b) => !b.disetujui).length,
    seminarMendatang: daftarSeminar.filter((s) => s.status === 'Terjadwal' || s.status === 'Menunggu Konfirmasi').length,
}

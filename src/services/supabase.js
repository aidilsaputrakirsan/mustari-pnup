/**
 * ============================================
 * SIMTA - Supabase Service (Simulasi)
 * Simulasi panggilan API ke Supabase
 * Menggunakan mock data dengan delay artifisial
 * ============================================
 */

import {
    judulSkripsiList,
    bimbinganList,
    chatHistory,
    jadwalSeminar,
    dashboardStats,
    currentUser,
    dosenList,
    mahasiswaList,
    getMahasiswaById,
    getDosenById,
} from './mockData.js'

// Simulasi network delay (200-500ms)
const simulateDelay = (ms = null) => {
    const delay = ms || Math.floor(Math.random() * 300) + 200
    return new Promise(resolve => setTimeout(resolve, delay))
}

/**
 * Service: Daftar Judul Skripsi
 */
export const judulService = {
    // Ambil semua judul dengan relasi
    async getAll(filters = {}) {
        await simulateDelay()
        let data = [...judulSkripsiList].map(j => ({
            ...j,
            mahasiswa: getMahasiswaById(j.mahasiswa_id),
            dosen: getDosenById(j.dosen_id),
        }))

        // Filter status
        if (filters.status) {
            data = data.filter(j => j.status === filters.status)
        }
        // Filter bidang
        if (filters.bidang) {
            data = data.filter(j => j.bidang === filters.bidang)
        }
        // Pencarian
        if (filters.search) {
            const q = filters.search.toLowerCase()
            data = data.filter(j =>
                j.judul.toLowerCase().includes(q) ||
                j.mahasiswa?.nama.toLowerCase().includes(q)
            )
        }

        return { data, error: null }
    },

    // Ambil judul berdasarkan ID
    async getById(id) {
        await simulateDelay()
        const judul = judulSkripsiList.find(j => j.id === id)
        if (!judul) return { data: null, error: 'Judul tidak ditemukan' }
        return {
            data: {
                ...judul,
                mahasiswa: getMahasiswaById(judul.mahasiswa_id),
                dosen: getDosenById(judul.dosen_id),
            },
            error: null,
        }
    },
}

/**
 * Service: Bimbingan
 */
export const bimbinganService = {
    // Ambil bimbingan berdasarkan judul_id
    async getByJudulId(judulId) {
        await simulateDelay()
        const data = bimbinganList
            .filter(b => b.judul_id === judulId)
            .sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal))
        return { data, error: null }
    },

    // Tambah bimbingan baru (simulasi)
    async create(bimbingan) {
        await simulateDelay(300)
        const newBimbingan = {
            id: bimbinganList.length + 1,
            ...bimbingan,
            status: 'Sedang Berjalan',
        }
        bimbinganList.push(newBimbingan)
        return { data: newBimbingan, error: null }
    },

    // Ambil chat history
    async getChatHistory(bimbinganId) {
        await simulateDelay()
        const data = chatHistory
            .filter(c => c.bimbingan_id === bimbinganId)
            .sort((a, b) => new Date(a.waktu) - new Date(b.waktu))
        return { data, error: null }
    },

    // Kirim pesan chat (simulasi)
    async sendMessage(bimbinganId, pesan, sender = 'mahasiswa') {
        await simulateDelay(200)
        const newChat = {
            id: chatHistory.length + 1,
            bimbingan_id: bimbinganId,
            sender,
            pesan,
            waktu: new Date().toISOString().replace('T', ' ').slice(0, 19),
        }
        chatHistory.push(newChat)
        return { data: newChat, error: null }
    },
}

/**
 * Service: Jadwal Seminar
 */
export const seminarService = {
    async getAll() {
        await simulateDelay()
        const data = jadwalSeminar.map(s => ({
            ...s,
            mahasiswa: getMahasiswaById(s.mahasiswa_id),
            judul: judulSkripsiList.find(j => j.id === s.judul_id),
            dosen_penguji: s.penguji.map(id => getDosenById(id)),
        }))
        return { data, error: null }
    },
}

/**
 * Service: Dashboard
 */
export const dashboardService = {
    async getStats() {
        await simulateDelay()
        return { data: { ...dashboardStats }, error: null }
    },

    async getRecentActivity() {
        await simulateDelay()
        return {
            data: [
                { jenis: 'bimbingan', deskripsi: 'Bimbingan BAB III dengan Dr. Siti Nurhaliza', waktu: '2 jam lalu' },
                { jenis: 'judul', deskripsi: 'Judul "Implementasi ML untuk Prediksi" diupdate', waktu: '5 jam lalu' },
                { jenis: 'seminar', deskripsi: 'Jadwal Seminar Proposal dikonfirmasi', waktu: '1 hari lalu' },
                { jenis: 'chat', deskripsi: 'Pesan baru dari Dosen Pembimbing', waktu: '2 hari lalu' },
                { jenis: 'bimbingan', deskripsi: 'Progres updated: 65%', waktu: '3 hari lalu' },
            ],
            error: null,
        }
    },
}

/**
 * Service: User / Profil
 */
export const userService = {
    async getProfile() {
        await simulateDelay()
        return { data: { ...currentUser }, error: null }
    },

    async updateProfile(updates) {
        await simulateDelay(400)
        Object.assign(currentUser, updates)
        return { data: { ...currentUser }, error: null }
    },
}

/**
 * Service: Data Referensi
 */
export const referensiService = {
    async getDosen() {
        await simulateDelay()
        return { data: [...dosenList], error: null }
    },

    async getMahasiswa() {
        await simulateDelay()
        return { data: [...mahasiswaList], error: null }
    },
}

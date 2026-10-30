/**
 * ROUTER ABLASI - EAGER (tanpa lazy loading)
 * Semua halaman di-import statis, sama seperti router baseline.
 */
import { createRouter, createWebHashHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import DaftarJudulView from '../views/DaftarJudulView.vue'
import DetailBimbinganView from '../views/DetailBimbinganView.vue'
import JadwalSeminarView from '../views/JadwalSeminarView.vue'
import PengaturanView from '../views/PengaturanView.vue'

const routes = [
    { path: '/', name: 'Dashboard', component: DashboardView },
    { path: '/daftar-judul', name: 'DaftarJudul', component: DaftarJudulView },
    { path: '/bimbingan', name: 'DetailBimbingan', component: DetailBimbinganView },
    { path: '/jadwal-seminar', name: 'JadwalSeminar', component: JadwalSeminarView },
    { path: '/pengaturan', name: 'Pengaturan', component: PengaturanView },
]

export default createRouter({ history: createWebHashHistory(), routes })

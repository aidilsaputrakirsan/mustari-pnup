/**
 * ROUTER ABLASI - LAZY LOADING MURNI (tanpa prefetching)
 * Setiap halaman di-import dinamis dan baru diunduh saat rutenya diakses.
 */
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    { path: '/', name: 'Dashboard', component: () => import('../views/DashboardView.vue') },
    { path: '/daftar-judul', name: 'DaftarJudul', component: () => import('../views/DaftarJudulView.vue') },
    { path: '/bimbingan', name: 'DetailBimbingan', component: () => import('../views/DetailBimbinganView.vue') },
    { path: '/jadwal-seminar', name: 'JadwalSeminar', component: () => import('../views/JadwalSeminarView.vue') },
    { path: '/pengaturan', name: 'Pengaturan', component: () => import('../views/PengaturanView.vue') },
]

export default createRouter({ history: createWebHashHistory(), routes })

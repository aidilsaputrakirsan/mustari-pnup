/**
 * ============================================
 * ROUTER - VERSI 1A (BASELINE)
 * ============================================
 * Pendekatan: EAGER LOADING
 *
 * SEMUA komponen halaman di-import di atas file (static import).
 * Artinya, semua kode halaman akan dimuat sekaligus saat
 * aplikasi pertama kali dibuka, meskipun user hanya
 * mengakses halaman Dashboard.
 *
 * Dampak:
 * - Bundle size besar (semua kode jadi satu file)
 * - Initial load time lebih lama
 * - Tight coupling: router "tahu" semua komponen
 * ============================================
 */
import { createRouter, createWebHistory } from 'vue-router'

// ❌ BAD PRACTICE: Semua komponen di-import secara EAGER
// Semua file ini akan masuk ke bundle utama
import DashboardView from '../views/DashboardView.vue'
import DaftarJudulView from '../views/DaftarJudulView.vue'
import DetailBimbinganView from '../views/DetailBimbinganView.vue'
import JadwalSeminarView from '../views/JadwalSeminarView.vue'
import PengaturanView from '../views/PengaturanView.vue'

const routes = [
    {
        path: '/',
        name: 'Dashboard',
        component: DashboardView, // Eager: langsung di-assign
    },
    {
        path: '/daftar-judul',
        name: 'DaftarJudul',
        component: DaftarJudulView, // Eager
    },
    {
        path: '/bimbingan',
        name: 'DetailBimbingan',
        component: DetailBimbinganView, // Eager
    },
    {
        path: '/jadwal-seminar',
        name: 'JadwalSeminar',
        component: JadwalSeminarView, // Eager
    },
    {
        path: '/pengaturan',
        name: 'Pengaturan',
        component: PengaturanView, // Eager
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router

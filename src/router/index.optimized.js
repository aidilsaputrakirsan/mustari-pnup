/**
 * ============================================
 * ROUTER - VERSI 1B (OPTIMIZED)
 * ============================================
 * Pendekatan: LAZY LOADING + PREFETCHING
 *
 * Komponen halaman di-import secara DINAMIS menggunakan
 * () => import(...). Vite akan otomatis membuat chunk
 * terpisah untuk setiap halaman.
 *
 * Tambahan:
 * - webpackChunkName equivalent (Vite magic comments tidak perlu)
 * - Prefetching: Saat di Dashboard, prefetch halaman Daftar Judul
 * - Route-level code splitting
 *
 * Dampak:
 * - Bundle utama kecil (hanya kode yang dibutuhkan)
 * - Halaman dimuat on-demand saat diakses
 * - Loose coupling: router hanya "tahu" path ke module
 * ============================================
 */
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Dashboard',
        // ✅ BEST PRACTICE: Lazy loading via dynamic import
        // Vite akan membuat chunk terpisah: DashboardView.[hash].js
        component: () => import('../views/DashboardView.vue'),
    },
    {
        path: '/daftar-judul',
        name: 'DaftarJudul',
        // Lazy loaded: chunk terpisah untuk Daftar Judul
        component: () => import('../views/DaftarJudulView.vue'),
    },
    {
        path: '/bimbingan',
        name: 'DetailBimbingan',
        // Lazy loaded: chunk terpisah untuk Detail Bimbingan
        component: () => import('../views/DetailBimbinganView.vue'),
    },
    {
        path: '/jadwal-seminar',
        name: 'JadwalSeminar',
        // Lazy loaded: chunk terpisah untuk Jadwal Seminar
        component: () => import('../views/JadwalSeminarView.vue'),
    },
    {
        path: '/pengaturan',
        name: 'Pengaturan',
        // Lazy loaded: chunk terpisah untuk Pengaturan
        component: () => import('../views/PengaturanView.vue'),
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

/**
 * ============================================
 * PREFETCHING STRATEGY
 * ============================================
 * Saat user berada di halaman Dashboard, kita proaktif
 * memuat (prefetch) halaman "Daftar Judul" di background.
 *
 * Alasan: Dashboard → Daftar Judul adalah navigasi paling umum.
 * Dengan prefetch, transisi antar halaman terasa instan.
 *
 * Teknik: afterEach guard + dynamic import saat idle.
 * ============================================
 */
router.afterEach((to) => {
    // Prefetch halaman yang kemungkinan besar dikunjungi berikutnya
    if (to.name === 'Dashboard') {
        // Gunakan requestIdleCallback jika tersedia, fallback ke setTimeout
        const prefetch = () => {
            // Prefetch Daftar Judul (navigasi paling umum dari Dashboard)
            import('../views/DaftarJudulView.vue')
            // Prefetch Detail Bimbingan (navigasi kedua paling umum)
            import('../views/DetailBimbinganView.vue')
        }

        if ('requestIdleCallback' in window) {
            requestIdleCallback(prefetch)
        } else {
            setTimeout(prefetch, 1000) // Fallback: delay 1 detik
        }
    }

    // Saat di Daftar Judul, prefetch Detail Bimbingan
    if (to.name === 'DaftarJudul') {
        const prefetch = () => {
            import('../views/DetailBimbinganView.vue')
        }
        if ('requestIdleCallback' in window) {
            requestIdleCallback(prefetch)
        } else {
            setTimeout(prefetch, 1000)
        }
    }
})

export default router

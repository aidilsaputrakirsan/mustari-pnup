/**
 * ============================================
 * ROUTER - VARIAN DEMO
 * ============================================
 * Seluruh halaman dalam dimuat secara lazy sehingga
 * berkas masuk (login) tetap ringan bagi pengunjung
 * yang belum masuk.
 * ============================================
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const routes = [
    {
        path: '/masuk',
        name: 'Masuk',
        component: () => import('../views/LoginView.vue'),
        meta: { publik: true, judul: 'Masuk' },
    },
    {
        path: '/',
        component: () => import('../layout/AppLayout.vue'),
        children: [
            {
                path: '',
                name: 'Dasbor',
                component: () => import('../views/DashboardView.vue'),
                meta: { judul: 'Dasbor', anak: 'Ringkasan penyelenggaraan Tugas Akhir' },
            },
            {
                path: 'tugas-akhir',
                name: 'TugasAkhir',
                component: () => import('../views/TugasAkhirView.vue'),
                meta: { judul: 'Arsip Tugas Akhir', anak: 'Seluruh judul lintas semester' },
            },
            {
                path: 'bimbingan',
                name: 'Bimbingan',
                component: () => import('../views/BimbinganView.vue'),
                meta: { judul: 'Log Bimbingan', anak: 'Rekam jejak pertemuan mahasiswa dan pembimbing' },
            },
            {
                path: 'seminar',
                name: 'Seminar',
                component: () => import('../views/SeminarView.vue'),
                meta: { judul: 'Seminar & Sidang', anak: 'Penjadwalan proposal dan sidang akhir' },
            },
            {
                path: 'dosen',
                name: 'Dosen',
                component: () => import('../views/DosenView.vue'),
                meta: { judul: 'Beban Pembimbing', anak: 'Distribusi bimbingan terhadap kuota dosen' },
            },
            {
                path: 'rekap',
                name: 'Rekap',
                component: () => import('../views/RekapView.vue'),
                meta: { judul: 'Rekap Semester', anak: 'Perbandingan capaian antar semester' },
            },
        ],
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/',
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior: () => ({ top: 0 }),
})

/** Penjaga rute: halaman dalam hanya untuk sesi yang sudah masuk. */
router.beforeEach((to) => {
    const auth = useAuthStore()

    if (!to.meta.publik && !auth.sudahMasuk) {
        return { name: 'Masuk', query: { lanjut: to.fullPath } }
    }
    if (to.name === 'Masuk' && auth.sudahMasuk) {
        return { name: 'Dasbor' }
    }
    return true
})

export default router

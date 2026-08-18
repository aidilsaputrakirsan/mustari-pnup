/**
 * ============================================
 * SIMTA DEMO - ENTRY POINT
 * ============================================
 * Varian khusus untuk demo publik (Netlify).
 * Terpisah dari varian Baseline (1A) & Optimized (1B)
 * agar pengukuran pada laporan tesis tetap utuh.
 * ============================================
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import Tooltip from 'primevue/tooltip'
import { definePreset } from '@primevue/themes'
import Aura from '@primevue/themes/aura'

import App from './App.vue'
import router from './router/index.js'

import 'primeicons/primeicons.css'
import './style.css'

/**
 * Preset warna SIMTA — indigo institusional di atas netral slate.
 * Aura bawaan memakai emerald; kita ganti agar terasa akademik
 * dan tidak seperti template mentah.
 */
const PresetSimta = definePreset(Aura, {
    semantic: {
        primary: {
            50: '#eef2ff',
            100: '#e0e7ff',
            200: '#c7d2fe',
            300: '#a5b4fc',
            400: '#818cf8',
            500: '#6366f1',
            600: '#4f46e5',
            700: '#4338ca',
            800: '#3730a3',
            900: '#312e81',
            950: '#1e1b4b',
        },
        colorScheme: {
            light: {
                surface: {
                    0: '#ffffff',
                    50: '#f8fafc',
                    100: '#f1f5f9',
                    200: '#e2e8f0',
                    300: '#cbd5e1',
                    400: '#94a3b8',
                    500: '#64748b',
                    600: '#475569',
                    700: '#334155',
                    800: '#1e293b',
                    900: '#0f172a',
                    950: '#020617',
                },
            },
        },
    },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: PresetSimta,
        options: {
            // Tema TERANG sebagai bawaan. Mode gelap hanya aktif
            // bila kelas .app-dark dipasang di <html> lewat tombol alih tema.
            darkModeSelector: '.app-dark',
            cssLayer: {
                name: 'primevue',
                order: 'theme, base, primevue',
            },
        },
    },
    ripple: true,
    locale: {
        startsWith: 'Diawali dengan',
        contains: 'Mengandung',
        notContains: 'Tidak mengandung',
        endsWith: 'Diakhiri dengan',
        equals: 'Sama dengan',
        notEquals: 'Tidak sama dengan',
        noFilter: 'Tanpa filter',
        clear: 'Bersihkan',
        apply: 'Terapkan',
        matchAll: 'Cocok semua',
        matchAny: 'Cocok salah satu',
        addRule: 'Tambah aturan',
        removeRule: 'Hapus aturan',
        emptyMessage: 'Tidak ada data',
        emptyFilterMessage: 'Tidak ada hasil yang cocok',
        dayNames: ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'],
        dayNamesShort: ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'],
        dayNamesMin: ['M', 'S', 'S', 'R', 'K', 'J', 'S'],
        monthNames: ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'],
        monthNamesShort: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
        today: 'Hari ini',
        weekHeader: 'Mg',
        firstDayOfWeek: 1,
        dateFormat: 'dd/mm/yy',
    },
})
app.use(ToastService)
app.use(ConfirmationService)
app.directive('tooltip', Tooltip)

app.mount('#app')

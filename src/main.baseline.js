/**
 * ============================================
 * MAIN.JS - VERSI 1A (BASELINE)
 * ============================================
 * Pendekatan: INISIALISASI "KOTOR"
 *
 * Semua plugin, store, dan dependensi di-import dan
 * diregistrasi secara SINKRON di satu file.
 *
 * Masalah:
 * - File ini menjadi "god file" yang tahu segalanya
 * - Semua dependensi harus di-resolve sebelum app bisa render
 * - Tidak ada lazy initialization
 * ============================================
 */

// Import SEMUA yang dibutuhkan di top-level (tight coupling)
import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Import router versi baseline (eager loading)
import router from './router/index.baseline.js'

// Import App versi baseline
import App from './App.baseline.vue'

// Import CSS
import './style.css'

// ❌ BAD PRACTICE: Import store instances di main.js
// Meskipun belum dipakai, ini menambah ukuran entry bundle
import { useJudulStore } from './stores/judulStore.js'
import { useBimbinganStore } from './stores/bimbinganStore.js'
import { useSeminarStore } from './stores/seminarStore.js'
import { useUserStore } from './stores/userStore.js'

// ❌ BAD PRACTICE: Import komponen berat di entry point
// Ini memaksa Chart.js (~200KB) masuk ke bundle utama
import ChartStatistik from './components/ChartStatistik.vue'
import CalendarJadwal from './components/CalendarJadwal.vue'

// Buat app instance
const app = createApp(App)

// Pasang semua plugin sekaligus
const pinia = createPinia()
app.use(pinia)
app.use(router)

// Mount app
app.mount('#app')

// ❌ BAD PRACTICE: Pre-fetch SEMUA data di main.js
// Ini menambah waktu inisialisasi meskipun data mungkin belum dibutuhkan
const judulStore = useJudulStore()
const bimbinganStore = useBimbinganStore()
const seminarStore = useSeminarStore()
const userStore = useUserStore()

// Load semua data sekaligus (bloking user experience)
judulStore.fetchJudul()
bimbinganStore.fetchBimbingan(1)
seminarStore.fetchSeminar()
userStore.fetchProfile()

console.log('[BASELINE] Semua komponen dan data dimuat sekaligus')
console.log('[BASELINE] ChartStatistik dan CalendarJadwal sudah di-import:', !!ChartStatistik, !!CalendarJadwal)

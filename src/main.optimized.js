/**
 * ============================================
 * MAIN.JS - VERSI 1B (OPTIMIZED)
 * ============================================
 * Pendekatan: INISIALISASI BERSIH
 *
 * Prinsip:
 * - Import hanya yang BENAR-BENAR dibutuhkan untuk bootstrap
 * - TIDAK ada global component registration
 * - TIDAK ada pre-fetching data di entry point
 * - Setiap halaman mengelola data sendiri (loose coupling)
 * ============================================
 */

// ✅ BEST PRACTICE: Hanya import core dependencies
import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Import router versi optimized (lazy loading)
import router from './router/index.optimized.js'

// Import App versi optimized
import App from './App.optimized.vue'

// Import CSS
import './style.css'

// Import PerformanceTracker
import { initPerformanceTracker } from './services/PerformanceTracker.js'

// Inisialisasi Tracker (Akan mengukur FCP, LCP, Loader, dll)
initPerformanceTracker('Optimized (Lazy Load + Split)')

// ✅ BEST PRACTICE: Inisialisasi minimalis
// Tidak ada import store, tidak ada import komponen berat
const app = createApp(App)

// Plugin registration — hanya yang essential
app.use(createPinia())
app.use(router)

// Mount — selesai. Clean & minimal.
app.mount('#app')

console.log('[OPTIMIZED] App dimuat dengan minimal footprint')

// ✅ Tidak ada pre-fetching di sini
// Setiap halaman akan fetch data sendiri saat dibutuhkan (on-demand)
// Komponen berat (ChartStatistik, CalendarJadwal) dimuat via defineAsyncComponent

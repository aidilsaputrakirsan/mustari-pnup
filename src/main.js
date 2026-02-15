/**
 * ============================================
 * MAIN.JS - DEFAULT ENTRY POINT
 * ============================================
 * Default: menggunakan versi OPTIMIZED (1B)
 *
 * Untuk menjalankan versi spesifik:
 *   npm run dev:baseline   → Versi 1A (Eager Loading)
 *   npm run dev:optimized  → Versi 1B (Lazy Loading)
 * ============================================
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router/index.optimized.js'
import App from './App.optimized.vue'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

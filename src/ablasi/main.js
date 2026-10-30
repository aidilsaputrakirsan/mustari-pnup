/**
 * MAIN.JS - STUDI ABLASI
 * Entry point yang sama untuk semua varian ablasi. Router yang dipakai
 * dipilih saat build lewat alias `@ablasi-router` (lihat vite.config.ablasi.js),
 * sehingga satu-satunya perbedaan antarvarian adalah teknik yang diuji.
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from '@ablasi-router'
import App from '../App.baseline.vue'
import '../style.css'
import { initPerformanceTracker } from '../services/PerformanceTracker.js'

initPerformanceTracker(__VARIAN_ABLASI__)

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

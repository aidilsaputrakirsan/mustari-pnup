# LAMPIRAN B: Cuplikan Kode Implementasi

## B.1 Konfigurasi Vite (Code Splitting)
Perbedaan utama konfigurasi build terletak pada `rollupOptions` di `vite.config.optimized.js`:

```javascript
// vite.config.optimized.js
build: {
  rollupOptions: {
    output: {
      manualChunks(id) {
        // Memisahkan Vue Core (Vue, Router, Pinia)
        if (id.includes('node_modules/vue')) {
            return 'vendor-vue'
        }
        // Memisahkan Library Berat (Chart.js)
        if (id.includes('node_modules/chart.js')) {
            return 'vendor-chart'
        }
      }
    }
  }
}
```

## B.2 Implementasi Router (Lazy Loading)
Perbedaan cara impor komponen di Router:

**Versi 1A (Baseline):**
```javascript
import DashboardView from '../views/DashboardView.vue' // Eager import
{ path: '/', component: DashboardView }
```

**Versi 1B (Optimized):**
```javascript
// Lazy dynamic import
{ path: '/', component: () => import('../views/DashboardView.vue') }
```

## B.3 Implementasi Async Component
Cara memuat komponen berat di dalam View (`src/views/DashboardView.vue`):

**Versi 1B (Optimized):**
```javascript
import { defineAsyncComponent } from 'vue'

// ChartStatistik hanya diunduh saat komponen dirender
const ChartStatistik = defineAsyncComponent(() => 
  import('../components/ChartStatistik.vue')
)
```

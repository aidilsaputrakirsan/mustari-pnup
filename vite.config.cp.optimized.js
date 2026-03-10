import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// Konfigurasi CODE SPLITTING untuk Company Profile (Aplikasi Sederhana)
export default defineConfig({
    plugins: [vue()],
    root: '.',
    build: {
        outDir: 'dist-cp-optimized',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: path.resolve(__dirname, 'index.cp.optimized.html')
            },
            output: {
                // Memisahkan Vue core karena ini aplikasi sederhana tanpa Chart.js
                manualChunks(id) {
                    if (id.includes('node_modules/vue') || id.includes('node_modules/vue-router') || id.includes('node_modules/@vue')) {
                        return 'vendor-vue'
                    }
                }
            }
        }
    }
})

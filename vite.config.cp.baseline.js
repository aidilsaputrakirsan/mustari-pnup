import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// Konfigurasi EAGER LOADING untuk Company Profile (Aplikasi Sederhana)
export default defineConfig({
    plugins: [vue()],
    root: '.',
    build: {
        outDir: 'dist-cp-baseline',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: path.resolve(__dirname, 'index.cp.baseline.html')
            },
            output: {
                // Semuanya digabung menjadi 1 file raksasa (Eager Loading)
            }
        }
    }
})

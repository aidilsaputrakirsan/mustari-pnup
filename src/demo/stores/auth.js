/**
 * ============================================
 * STORE AUTENTIKASI (SIMULASI)
 * ============================================
 * Tidak ada server maupun basis data. Kredensial
 * dicocokkan dengan akun demo dari seeder, lalu
 * sesi disimpan di sessionStorage agar bertahan
 * saat halaman dimuat ulang.
 * ============================================
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { akunDemo } from '../data/seed.js'

const KUNCI_SESI = 'simta.sesi'

export const useAuthStore = defineStore('auth', () => {
    const profil = ref(bacaSesi())
    const sedangProses = ref(false)
    const pesanGalat = ref('')

    const sudahMasuk = computed(() => profil.value !== null)

    function bacaSesi() {
        try {
            const mentah = sessionStorage.getItem(KUNCI_SESI)
            return mentah ? JSON.parse(mentah) : null
        } catch {
            return null
        }
    }

    /**
     * Simulasi proses masuk, lengkap dengan jeda jaringan
     * supaya keadaan memuat pada tombol benar-benar terlihat.
     */
    async function masuk(email, sandi) {
        sedangProses.value = true
        pesanGalat.value = ''

        await new Promise((resolve) => setTimeout(resolve, 650))

        const cocok =
            email.trim().toLowerCase() === akunDemo.email &&
            sandi === akunDemo.sandi

        if (!cocok) {
            pesanGalat.value = 'Email atau kata sandi tidak sesuai. Gunakan akun demo yang tertera.'
            sedangProses.value = false
            return false
        }

        profil.value = akunDemo.profil
        sessionStorage.setItem(KUNCI_SESI, JSON.stringify(akunDemo.profil))
        sedangProses.value = false
        return true
    }

    function keluar() {
        profil.value = null
        pesanGalat.value = ''
        sessionStorage.removeItem(KUNCI_SESI)
    }

    return { profil, sudahMasuk, sedangProses, pesanGalat, masuk, keluar }
})

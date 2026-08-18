/**
 * ============================================
 * ALIH TEMA TERANG / GELAP
 * ============================================
 * Tema TERANG adalah bawaan. Mode gelap aktif hanya
 * bila kelas .app-dark dipasang pada elemen <html> —
 * selaras dengan darkModeSelector di main.js.
 *
 * Pilihan pengguna disimpan di localStorage; bila belum
 * pernah memilih, tema terang tetap dipakai (tidak
 * mengikuti preferensi sistem, sesuai permintaan bahwa
 * terang menjadi bawaan).
 * ============================================
 */
import { ref } from 'vue'

const KUNCI = 'simta.tema'
const gelap = ref(localStorage.getItem(KUNCI) === 'gelap')

function terapkan() {
    document.documentElement.classList.toggle('app-dark', gelap.value)
}

terapkan()

export function useTema() {
    function alihTema() {
        gelap.value = !gelap.value
        localStorage.setItem(KUNCI, gelap.value ? 'gelap' : 'terang')
        terapkan()
    }

    return { gelap, alihTema }
}

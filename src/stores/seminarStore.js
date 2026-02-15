/**
 * Store: Seminar
 * Mengelola jadwal seminar proposal dan sidang akhir
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { seminarService } from '../services/supabase.js'

export const useSeminarStore = defineStore('seminar', () => {
    // State
    const seminarList = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Getters
    const seminarTerjadwal = computed(() =>
        seminarList.value.filter(s => s.status === 'Terjadwal')
    )
    const seminarMenunggu = computed(() =>
        seminarList.value.filter(s => s.status === 'Menunggu Konfirmasi')
    )
    const seminarSelesai = computed(() =>
        seminarList.value.filter(s => s.status === 'Selesai')
    )

    // Kelompokkan jadwal seminar per bulan untuk tampilan kalender
    const jadwalPerBulan = computed(() => {
        const grouped = {}
        seminarList.value.forEach(s => {
            const bulan = s.tanggal.slice(0, 7) // YYYY-MM
            if (!grouped[bulan]) grouped[bulan] = []
            grouped[bulan].push(s)
        })
        return grouped
    })

    // Actions
    async function fetchSeminar() {
        loading.value = true
        error.value = null
        try {
            const { data, error: err } = await seminarService.getAll()
            if (err) throw new Error(err)
            seminarList.value = data
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    return {
        seminarList, loading, error,
        seminarTerjadwal, seminarMenunggu, seminarSelesai, jadwalPerBulan,
        fetchSeminar,
    }
})

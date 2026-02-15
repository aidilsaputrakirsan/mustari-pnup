/**
 * Store: Judul Skripsi
 * Mengelola daftar judul, pencarian, dan filter
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { judulService } from '../services/supabase.js'

export const useJudulStore = defineStore('judul', () => {
    // State
    const judulList = ref([])
    const loading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')
    const filterStatus = ref('')
    const filterBidang = ref('')

    // Getters
    const filteredJudul = computed(() => {
        let hasil = [...judulList.value]
        if (searchQuery.value) {
            const q = searchQuery.value.toLowerCase()
            hasil = hasil.filter(j =>
                j.judul.toLowerCase().includes(q) ||
                j.mahasiswa?.nama.toLowerCase().includes(q)
            )
        }
        if (filterStatus.value) {
            hasil = hasil.filter(j => j.status === filterStatus.value)
        }
        if (filterBidang.value) {
            hasil = hasil.filter(j => j.bidang === filterBidang.value)
        }
        return hasil
    })

    const totalJudul = computed(() => judulList.value.length)
    const jumlahPerStatus = computed(() => {
        const counts = {}
        judulList.value.forEach(j => {
            counts[j.status] = (counts[j.status] || 0) + 1
        })
        return counts
    })

    // Actions
    async function fetchJudul() {
        loading.value = true
        error.value = null
        try {
            const { data, error: err } = await judulService.getAll()
            if (err) throw new Error(err)
            judulList.value = data
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    function setSearch(query) {
        searchQuery.value = query
    }

    function setFilterStatus(status) {
        filterStatus.value = status
    }

    function setFilterBidang(bidang) {
        filterBidang.value = bidang
    }

    function resetFilters() {
        searchQuery.value = ''
        filterStatus.value = ''
        filterBidang.value = ''
    }

    return {
        judulList, loading, error, searchQuery, filterStatus, filterBidang,
        filteredJudul, totalJudul, jumlahPerStatus,
        fetchJudul, setSearch, setFilterStatus, setFilterBidang, resetFilters,
    }
})

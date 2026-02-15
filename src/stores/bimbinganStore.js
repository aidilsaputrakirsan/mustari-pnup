/**
 * Store: Bimbingan
 * Mengelola data bimbingan, progres, dan chat
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { bimbinganService } from '../services/supabase.js'

export const useBimbinganStore = defineStore('bimbingan', () => {
    // State
    const bimbinganList = ref([])
    const chatMessages = ref([])
    const loading = ref(false)
    const chatLoading = ref(false)
    const error = ref(null)
    const selectedBimbinganId = ref(null)

    // Getters
    const sortedBimbingan = computed(() =>
        [...bimbinganList.value].sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal))
    )

    const latestProgres = computed(() => {
        if (bimbinganList.value.length === 0) return 0
        return Math.max(...bimbinganList.value.map(b => b.progres))
    })

    const totalBimbingan = computed(() => bimbinganList.value.length)

    // Actions
    async function fetchBimbingan(judulId) {
        loading.value = true
        error.value = null
        try {
            const { data, error: err } = await bimbinganService.getByJudulId(judulId)
            if (err) throw new Error(err)
            bimbinganList.value = data
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    async function fetchChat(bimbinganId) {
        chatLoading.value = true
        selectedBimbinganId.value = bimbinganId
        try {
            const { data, error: err } = await bimbinganService.getChatHistory(bimbinganId)
            if (err) throw new Error(err)
            chatMessages.value = data
        } catch (e) {
            error.value = e.message
        } finally {
            chatLoading.value = false
        }
    }

    async function sendMessage(pesan) {
        if (!selectedBimbinganId.value || !pesan.trim()) return
        try {
            const { data, error: err } = await bimbinganService.sendMessage(
                selectedBimbinganId.value, pesan
            )
            if (err) throw new Error(err)
            chatMessages.value.push(data)
        } catch (e) {
            error.value = e.message
        }
    }

    async function tambahBimbingan(dataBimbingan) {
        try {
            const { data, error: err } = await bimbinganService.create(dataBimbingan)
            if (err) throw new Error(err)
            bimbinganList.value.push(data)
            return data
        } catch (e) {
            error.value = e.message
            return null
        }
    }

    return {
        bimbinganList, chatMessages, loading, chatLoading, error, selectedBimbinganId,
        sortedBimbingan, latestProgres, totalBimbingan,
        fetchBimbingan, fetchChat, sendMessage, tambahBimbingan,
    }
})

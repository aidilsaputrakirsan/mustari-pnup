/**
 * Store: User / Profil
 * Mengelola data profil pengguna yang sedang login
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userService } from '../services/supabase.js'

export const useUserStore = defineStore('user', () => {
    // State
    const profile = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const saveSuccess = ref(false)

    // Actions
    async function fetchProfile() {
        loading.value = true
        error.value = null
        try {
            const { data, error: err } = await userService.getProfile()
            if (err) throw new Error(err)
            profile.value = data
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    async function updateProfile(updates) {
        loading.value = true
        error.value = null
        saveSuccess.value = false
        try {
            const { data, error: err } = await userService.updateProfile(updates)
            if (err) throw new Error(err)
            profile.value = data
            saveSuccess.value = true
            setTimeout(() => { saveSuccess.value = false }, 3000)
        } catch (e) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    return {
        profile, loading, error, saveSuccess,
        fetchProfile, updateProfile,
    }
})

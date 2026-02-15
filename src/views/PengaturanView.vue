<template>
  <!-- Halaman Pengaturan: Profil user -->
  <div class="pengaturan">
    <div class="settings-container">
      <!-- Profil Card -->
      <div class="profile-card card">
        <div class="profile-header">
          <div class="profile-avatar">
            <span>{{ initials }}</span>
          </div>
          <div class="profile-info">
            <h3>{{ profile?.nama || 'Loading...' }}</h3>
            <p>{{ profile?.nim }} • {{ profile?.prodi }}</p>
            <span class="badge badge-info">{{ profile?.role }}</span>
          </div>
        </div>
      </div>

      <!-- Form Pengaturan -->
      <div class="settings-form card">
        <h3 class="form-section-title">✏️ Edit Profil</h3>

        <div v-if="saveSuccess" class="success-alert">
          ✅ Profil berhasil diperbarui!
        </div>

        <form @submit.prevent="simpanProfil" class="edit-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Nama Lengkap</label>
              <input v-model="form.nama" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">NIM</label>
              <input v-model="form.nim" type="text" class="form-input" disabled />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">No. Telepon</label>
              <input v-model="form.telepon" type="tel" class="form-input" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Program Studi</label>
              <input v-model="form.prodi" type="text" class="form-input" disabled />
            </div>
            <div class="form-group">
              <label class="form-label">Angkatan</label>
              <input v-model="form.angkatan" type="number" class="form-input" disabled />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Alamat</label>
            <textarea v-model="form.alamat" class="form-input" rows="3"></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="loading">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                <polyline points="17 21 17 13 7 13 7 21"/>
                <polyline points="7 3 7 8 15 8"/>
              </svg>
              {{ loading ? 'Menyimpan...' : 'Simpan Perubahan' }}
            </button>
            <button type="button" class="btn-secondary" @click="resetForm">
              Batal
            </button>
          </div>
        </form>
      </div>

      <!-- Info Section -->
      <div class="info-card card">
        <h3 class="form-section-title">ℹ️ Informasi Akun</h3>
        <div class="info-list">
          <div class="info-item">
            <span class="info-label">Dosen Pembimbing</span>
            <span class="info-value">Dr. Siti Nurhaliza, Ph.D.</span>
          </div>
          <div class="info-item">
            <span class="info-label">Status Akun</span>
            <span class="badge badge-success">Aktif</span>
          </div>
          <div class="info-item">
            <span class="info-label">Terakhir Login</span>
            <span class="info-value">{{ new Date().toLocaleDateString('id-ID') }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '../stores/userStore.js'

const store = useUserStore()

const profile = computed(() => store.profile)
const loading = computed(() => store.loading)
const saveSuccess = computed(() => store.saveSuccess)

const form = ref({
  nama: '',
  nim: '',
  email: '',
  telepon: '',
  prodi: '',
  angkatan: '',
  alamat: '',
})

const initials = computed(() => {
  if (!profile.value?.nama) return '??'
  return profile.value.nama.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
})

// Sinkronkan form dengan profil yang di-fetch
watch(profile, (val) => {
  if (val) {
    form.value = { ...val }
  }
}, { immediate: true })

function simpanProfil() {
  store.updateProfile({
    nama: form.value.nama,
    email: form.value.email,
    telepon: form.value.telepon,
    alamat: form.value.alamat,
  })
}

function resetForm() {
  if (profile.value) {
    form.value = { ...profile.value }
  }
}

onMounted(() => {
  store.fetchProfile()
})
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Profile Card */
.profile-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}
.profile-avatar {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 800;
  color: white;
}
.profile-info h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #f1f5f9;
}
.profile-info p {
  font-size: 0.8125rem;
  color: #64748b;
  margin: 4px 0;
}

/* Form */
.form-section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 1.25rem;
}
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}
.form-label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #94a3b8;
}
.form-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 0.5rem;
}

/* Success */
.success-alert {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #4ade80;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

/* Info */
.info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #1e293b;
}
.info-item:last-child { border-bottom: none; }
.info-label {
  font-size: 0.8125rem;
  color: #64748b;
}
.info-value {
  font-size: 0.8125rem;
  color: #e2e8f0;
  font-weight: 500;
}
</style>

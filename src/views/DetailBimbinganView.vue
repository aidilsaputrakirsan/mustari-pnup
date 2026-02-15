<template>
  <!-- Halaman Detail Bimbingan: Form input & chat -->
  <div class="detail-bimbingan">
    <div class="bimbingan-layout">
      <!-- Panel Kiri: Daftar Bimbingan + Form -->
      <div class="bimbingan-left">
        <!-- Progress Bar -->
        <div class="progress-section card">
          <div class="progress-header">
            <h3>📈 Progres Keseluruhan</h3>
            <span class="progress-pct">{{ latestProgres }}%</span>
          </div>
          <div class="big-progress-bar">
            <div class="big-progress-fill" :style="{ width: latestProgres + '%' }"></div>
          </div>
        </div>

        <!-- Form Tambah Bimbingan -->
        <div class="form-section card">
          <h3 class="form-title">➕ Catatan Bimbingan Baru</h3>
          <form @submit.prevent="submitBimbingan" class="bimbingan-form">
            <div class="form-group">
              <label class="form-label">Tanggal</label>
              <input v-model="formData.tanggal" type="date" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Topik Bimbingan</label>
              <input v-model="formData.topik" type="text" class="form-input" placeholder="Misal: Review BAB III" required />
            </div>
            <div class="form-group">
              <label class="form-label">Catatan / Hasil</label>
              <textarea v-model="formData.catatan" class="form-input form-textarea" rows="3" placeholder="Catatan dari sesi bimbingan..." required></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Progres (%)</label>
              <input v-model.number="formData.progres" type="number" class="form-input" min="0" max="100" required />
            </div>
            <button type="submit" class="btn-primary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                <polyline points="17 21 17 13 7 13 7 21"/>
                <polyline points="7 3 7 8 15 8"/>
              </svg>
              Simpan Catatan
            </button>
          </form>
        </div>

        <!-- Timeline Bimbingan -->
        <div class="timeline-section card">
          <h3 class="timeline-title">📋 Riwayat Bimbingan</h3>
          <div v-if="loading" class="loading-timeline">
            <div v-for="i in 3" :key="i" class="skeleton" style="height: 80px; margin-bottom: 12px;"></div>
          </div>
          <div v-else class="timeline">
            <div v-for="item in sortedBimbingan" :key="item.id" class="timeline-item" :class="{ active: selectedBimbinganId === item.id }" @click="selectBimbingan(item.id)">
              <div class="timeline-dot" :class="item.status === 'Selesai' ? 'done' : 'in-progress'"></div>
              <div class="timeline-content">
                <div class="timeline-header">
                  <span class="timeline-date">{{ formatTanggal(item.tanggal) }}</span>
                  <span class="badge" :class="item.status === 'Selesai' ? 'badge-success' : 'badge-info'">{{ item.status }}</span>
                </div>
                <h4 class="timeline-topik">{{ item.topik }}</h4>
                <p class="timeline-catatan">{{ item.catatan }}</p>
                <div class="timeline-progres">
                  <div class="mini-progress">
                    <div class="mini-fill" :style="{ width: item.progres + '%' }"></div>
                  </div>
                  <span>{{ item.progres }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel Kanan: Chat History -->
      <div class="bimbingan-right">
        <ChatHistory
          :messages="chatMessages"
          :loading="chatLoading"
          @send="handleSendMessage"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBimbinganStore } from '../stores/bimbinganStore.js'
import ChatHistory from '../components/ChatHistory.vue'

const store = useBimbinganStore()

const formData = ref({
  tanggal: new Date().toISOString().slice(0, 10),
  topik: '',
  catatan: '',
  progres: 0,
})

const loading = computed(() => store.loading)
const chatLoading = computed(() => store.chatLoading)
const sortedBimbingan = computed(() => store.sortedBimbingan)
const chatMessages = computed(() => store.chatMessages)
const latestProgres = computed(() => store.latestProgres)
const selectedBimbinganId = computed(() => store.selectedBimbinganId)

function selectBimbingan(id) {
  store.fetchChat(id)
}

async function submitBimbingan() {
  await store.tambahBimbingan({
    judul_id: 1, // Default ke judul pertama (simulasi)
    ...formData.value,
  })
  // Reset form
  formData.value = {
    tanggal: new Date().toISOString().slice(0, 10),
    topik: '',
    catatan: '',
    progres: 0,
  }
}

function handleSendMessage(pesan) {
  store.sendMessage(pesan)
}

function formatTanggal(tanggal) {
  return new Date(tanggal).toLocaleDateString('id-ID', { day: '2-digit', month: 'long', year: 'numeric' })
}

onMounted(() => {
  // Load bimbingan untuk judul pertama (simulasi user yang login)
  store.fetchBimbingan(1)
  // Load chat bimbingan terbaru
  store.fetchChat(5)
})
</script>

<style scoped>
.bimbingan-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 1.5rem;
  align-items: start;
}
.bimbingan-left {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Progress */
.progress-section {
  padding: 1.25rem;
}
.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.progress-header h3 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #e2e8f0;
}
.progress-pct {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.big-progress-bar {
  height: 10px;
  background: #0f172a;
  border-radius: 5px;
  overflow: hidden;
}
.big-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 5px;
  transition: width 1s ease;
}

/* Form */
.form-title { font-size: 0.9375rem; font-weight: 600; color: #e2e8f0; margin-bottom: 1rem; }
.bimbingan-form { display: flex; flex-direction: column; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.375rem; }
.form-label { font-size: 0.8125rem; font-weight: 500; color: #94a3b8; }
.form-textarea { resize: vertical; min-height: 80px; }

/* Timeline */
.timeline-title { font-size: 0.9375rem; font-weight: 600; color: #e2e8f0; margin-bottom: 1rem; }
.timeline { display: flex; flex-direction: column; gap: 0; }
.timeline-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-left: 2px solid #334155;
  margin-left: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 0 8px 8px 0;
}
.timeline-item:hover { background: rgba(59, 130, 246, 0.05); }
.timeline-item.active { background: rgba(59, 130, 246, 0.08); border-left-color: #3b82f6; }
.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-left: -23px;
  margin-top: 4px;
  flex-shrink: 0;
}
.timeline-dot.done { background: #4ade80; }
.timeline-dot.in-progress { background: #60a5fa; animation: pulse-glow 2s infinite; }
.timeline-content { flex: 1; }
.timeline-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.375rem; }
.timeline-date { font-size: 0.75rem; color: #64748b; }
.timeline-topik { font-size: 0.875rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.25rem; }
.timeline-catatan { font-size: 0.8125rem; color: #94a3b8; line-height: 1.5; }
.timeline-progres {
  display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;
  font-size: 0.75rem; color: #64748b;
}
.mini-progress { width: 100px; height: 4px; background: #0f172a; border-radius: 2px; overflow: hidden; }
.mini-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 2px; }

@media (max-width: 900px) {
  .bimbingan-layout {
    grid-template-columns: 1fr;
  }
}
</style>

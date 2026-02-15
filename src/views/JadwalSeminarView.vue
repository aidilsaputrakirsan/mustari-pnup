<template>
  <!-- Halaman Jadwal Seminar -->
  <div class="jadwal-seminar">
    <!-- Summary Cards -->
    <div class="jadwal-summary">
      <div class="summary-card">
        <span class="summary-count">{{ terjadwal }}</span>
        <span class="summary-label">Terjadwal</span>
      </div>
      <div class="summary-card menunggu">
        <span class="summary-count">{{ menunggu }}</span>
        <span class="summary-label">Menunggu Konfirmasi</span>
      </div>
      <div class="summary-card selesai">
        <span class="summary-count">{{ selesai }}</span>
        <span class="summary-label">Selesai</span>
      </div>
    </div>

    <!-- Kalender -->
    <div class="calendar-wrapper">
      <h3 class="section-title">📅 Kalender Seminar</h3>
      <CalendarJadwal :jadwal-list="seminarList" />
    </div>

    <!-- List Detail Jadwal -->
    <div class="jadwal-list-section">
      <h3 class="section-title">📋 Detail Jadwal</h3>
      <div v-if="loading" class="loading-list">
        <div v-for="i in 4" :key="i" class="skeleton" style="height: 100px; margin-bottom: 12px;"></div>
      </div>
      <div v-else class="jadwal-list">
        <div v-for="jadwal in seminarList" :key="jadwal.id" class="jadwal-card">
          <div class="jadwal-type" :class="jadwal.jenis === 'Seminar Proposal' ? 'type-sempro' : 'type-sidang'">
            {{ jadwal.jenis === 'Seminar Proposal' ? 'SP' : 'SA' }}
          </div>
          <div class="jadwal-info">
            <h4 class="jadwal-jenis">{{ jadwal.jenis }}</h4>
            <p class="jadwal-mahasiswa">{{ jadwal.mahasiswa?.nama }} — {{ jadwal.judul?.judul }}</p>
            <div class="jadwal-details">
              <span class="detail-item">
                📅 {{ formatTanggal(jadwal.tanggal) }}
              </span>
              <span class="detail-item">
                🕐 {{ jadwal.waktu }} WITA
              </span>
              <span class="detail-item">
                🏫 {{ jadwal.ruangan }}
              </span>
            </div>
            <div class="jadwal-penguji">
              <span class="penguji-label">Penguji:</span>
              <span v-for="(p, idx) in jadwal.dosen_penguji" :key="p.id" class="penguji-name">
                {{ p.nama }}{{ idx < jadwal.dosen_penguji.length - 1 ? ', ' : '' }}
              </span>
            </div>
          </div>
          <div class="jadwal-status-badge">
            <span class="badge" :class="getStatusBadge(jadwal.status)">{{ jadwal.status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useSeminarStore } from '../stores/seminarStore.js'
import CalendarJadwal from '../components/CalendarJadwal.vue'

const store = useSeminarStore()

const loading = computed(() => store.loading)
const seminarList = computed(() => store.seminarList)
const terjadwal = computed(() => store.seminarTerjadwal.length)
const menunggu = computed(() => store.seminarMenunggu.length)
const selesai = computed(() => store.seminarSelesai.length)

function formatTanggal(tanggal) {
  return new Date(tanggal).toLocaleDateString('id-ID', {
    weekday: 'long', day: '2-digit', month: 'long', year: 'numeric',
  })
}

function getStatusBadge(status) {
  const map = {
    'Terjadwal': 'badge-info',
    'Menunggu Konfirmasi': 'badge-warning',
    'Selesai': 'badge-success',
  }
  return map[status] || 'badge-info'
}

onMounted(() => {
  store.fetchSeminar()
})
</script>

<style scoped>
.jadwal-seminar {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.jadwal-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
.summary-card {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
}
.summary-card.menunggu {
  background: linear-gradient(135deg, rgba(234, 179, 8, 0.1), rgba(234, 179, 8, 0.05));
  border-color: rgba(234, 179, 8, 0.2);
}
.summary-card.selesai {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
  border-color: rgba(34, 197, 94, 0.2);
}
.summary-count {
  font-size: 2rem;
  font-weight: 800;
  color: #f1f5f9;
  display: block;
}
.summary-label {
  font-size: 0.8125rem;
  color: #64748b;
}
.section-title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 1.25rem;
}
.jadwal-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.jadwal-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.25rem;
  transition: all 0.2s;
}
.jadwal-card:hover {
  border-color: #475569;
  transform: translateX(4px);
}
.jadwal-type {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 800;
  flex-shrink: 0;
}
.type-sempro {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}
.type-sidang {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}
.jadwal-info {
  flex: 1;
}
.jadwal-jenis {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}
.jadwal-mahasiswa {
  font-size: 0.8125rem;
  color: #94a3b8;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}
.jadwal-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
}
.detail-item {
  font-size: 0.75rem;
  color: #64748b;
}
.jadwal-penguji {
  font-size: 0.75rem;
  color: #64748b;
}
.penguji-label {
  font-weight: 600;
  color: #94a3b8;
}
.jadwal-status-badge {
  flex-shrink: 0;
}
</style>

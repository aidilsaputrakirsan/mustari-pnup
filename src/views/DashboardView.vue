<template>
  <!-- Halaman Dashboard: Statistik ringkas -->
  <div class="dashboard">
    <!-- Loading State -->
    <div v-if="loading" class="loading-grid">
      <div v-for="i in 4" :key="i" class="skeleton stat-skeleton"></div>
    </div>

    <template v-else>
      <!-- Stat Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-label">Total Bimbingan</span>
            <div class="stat-icon blue">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats.totalBimbingan }}</div>
          <div class="stat-footer">
            <span class="stat-change positive">+{{ stats.bimbinganBulanIni }}</span>
            <span class="stat-period">bulan ini</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-label">Judul Disetujui</span>
            <div class="stat-icon green">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats.judulDisetujui }}</div>
          <div class="stat-footer">
            <span>dari {{ stats.totalJudul }} total judul</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-label">Progres Rata-rata</span>
            <div class="stat-icon purple">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats.progresRataRata }}%</div>
          <div class="stat-footer">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: stats.progresRataRata + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-label">Seminar Terjadwal</span>
            <div class="stat-icon cyan">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats.seminarTerjadwal }}</div>
          <div class="stat-footer">
            <span>{{ stats.seminarSelesai }} selesai</span>
          </div>
        </div>
      </div>

      <!-- Status Judul Quick View -->
      <div class="status-overview">
        <h3 class="section-title">📋 Ringkasan Status Judul</h3>
        <div class="status-pills">
          <div class="status-pill">
            <span class="pill-dot green"></span>
            <span class="pill-label">Disetujui</span>
            <span class="pill-count">{{ stats.judulDisetujui }}</span>
          </div>
          <div class="status-pill">
            <span class="pill-dot blue"></span>
            <span class="pill-label">Sedang Berjalan</span>
            <span class="pill-count">{{ stats.judulSedangBerjalan }}</span>
          </div>
          <div class="status-pill">
            <span class="pill-dot yellow"></span>
            <span class="pill-label">Revisi</span>
            <span class="pill-count">{{ stats.judulRevisi }}</span>
          </div>
          <div class="status-pill">
            <span class="pill-dot purple"></span>
            <span class="pill-label">Diajukan</span>
            <span class="pill-count">{{ stats.judulDiajukan }}</span>
          </div>
          <div class="status-pill">
            <span class="pill-dot red"></span>
            <span class="pill-label">Ditolak</span>
            <span class="pill-count">{{ stats.judulDitolak }}</span>
          </div>
          <div class="status-pill">
            <span class="pill-dot cyan"></span>
            <span class="pill-label">Selesai</span>
            <span class="pill-count">{{ stats.judulSelesai }}</span>
          </div>
        </div>
      </div>

      <!-- Chart Section -->
      <div class="chart-section">
        <h3 class="section-title">📊 Statistik Visual</h3>
        <ChartStatistik />
      </div>

      <!-- Aktivitas Terbaru -->
      <div class="recent-activity">
        <h3 class="section-title">🕐 Aktivitas Terbaru</h3>
        <div class="activity-list">
          <div v-for="(activity, idx) in recentActivity" :key="idx" class="activity-item">
            <div class="activity-icon" :class="activity.jenis">
              {{ activityEmoji(activity.jenis) }}
            </div>
            <div class="activity-content">
              <p class="activity-desc">{{ activity.deskripsi }}</p>
              <span class="activity-time">{{ activity.waktu }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dashboardService } from '../services/supabase.js'
import ChartStatistik from '../components/ChartStatistik.vue'

const stats = ref({})
const recentActivity = ref([])
const loading = ref(true)

function activityEmoji(jenis) {
  const emojis = { bimbingan: '📝', judul: '📄', seminar: '🎓', chat: '💬' }
  return emojis[jenis] || '📌'
}

onMounted(async () => {
  const [statsRes, activityRes] = await Promise.all([
    dashboardService.getStats(),
    dashboardService.getRecentActivity(),
  ])
  stats.value = statsRes.data
  recentActivity.value = activityRes.data
  loading.value = false
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Loading */
.loading-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}
.stat-skeleton {
  height: 130px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}
.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}
.stat-label {
  font-size: 0.8125rem;
  color: #64748b;
  font-weight: 500;
}
.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.stat-icon.blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.stat-icon.green { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.stat-icon.purple { background: rgba(139, 92, 246, 0.15); color: #a78bfa; }
.stat-icon.cyan { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }
.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #f1f5f9;
  line-height: 1;
  margin-bottom: 0.5rem;
}
.stat-footer {
  font-size: 0.75rem;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}
.stat-change.positive {
  color: #4ade80;
  font-weight: 600;
}
.progress-bar {
  flex: 1;
  height: 6px;
  background: #0f172a;
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  border-radius: 3px;
  transition: width 1s ease;
}

/* Section titles */
.section-title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Status Overview */
.status-overview {
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.5rem;
}
.status-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.status-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid #334155;
  border-radius: 999px;
  padding: 0.5rem 1rem;
}
.pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.pill-dot.green { background: #4ade80; }
.pill-dot.blue { background: #60a5fa; }
.pill-dot.yellow { background: #facc15; }
.pill-dot.purple { background: #a78bfa; }
.pill-dot.red { background: #f87171; }
.pill-dot.cyan { background: #22d3ee; }
.pill-label {
  font-size: 0.8125rem;
  color: #94a3b8;
}
.pill-count {
  font-size: 0.8125rem;
  font-weight: 700;
  color: #e2e8f0;
}

/* Chart Section */
.chart-section {
  /* Chart akan dirender via slot */
}

/* Activity */
.recent-activity {
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.5rem;
}
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.3);
  border-radius: 10px;
  transition: background 0.2s;
}
.activity-item:hover {
  background: rgba(59, 130, 246, 0.05);
}
.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  background: rgba(59, 130, 246, 0.1);
}
.activity-desc {
  font-size: 0.8125rem;
  color: #e2e8f0;
}
.activity-time {
  font-size: 0.6875rem;
  color: #64748b;
}
</style>

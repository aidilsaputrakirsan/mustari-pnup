<template>
  <!-- Halaman Daftar Judul Skripsi: List panjang -->
  <div class="daftar-judul">
    <!-- Filter & Search Bar -->
    <div class="filter-bar">
      <div class="search-wrapper">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          class="form-input search-field"
          placeholder="Cari judul atau nama mahasiswa..."
          @input="handleSearch"
        />
      </div>
      <select v-model="filterStatus" class="form-input filter-select" @change="handleFilter">
        <option value="">Semua Status</option>
        <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
      </select>
      <select v-model="filterBidang" class="form-input filter-select" @change="handleFilter">
        <option value="">Semua Bidang</option>
        <option v-for="b in bidangOptions" :key="b" :value="b">{{ b }}</option>
      </select>
      <div class="result-count">
        <span class="count-number">{{ filteredJudul.length }}</span>
        <span class="count-label">judul ditemukan</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-list">
      <div v-for="i in 8" :key="i" class="skeleton list-skeleton"></div>
    </div>

    <!-- Daftar Judul -->
    <div v-else class="judul-list">
      <div
        v-for="judul in paginatedJudul"
        :key="judul.id"
        class="judul-card"
      >
        <div class="judul-main">
          <div class="judul-number">#{{ judul.id }}</div>
          <div class="judul-content">
            <h4 class="judul-title">{{ judul.judul }}</h4>
            <div class="judul-meta">
              <span class="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                {{ judul.mahasiswa?.nama || '-' }}
              </span>
              <span class="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                </svg>
                {{ judul.bidang }}
              </span>
              <span class="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
                {{ formatTanggal(judul.tanggal_ajuan) }}
              </span>
            </div>
          </div>
        </div>
        <div class="judul-status">
          <span class="badge" :class="getStatusClass(judul.status)">{{ judul.status }}</span>
          <span class="judul-dosen">Pembimbing: {{ judul.dosen?.nama || '-' }}</span>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredJudul.length === 0 && !loading" class="empty-state">
        <p>😔 Tidak ada judul yang sesuai filter.</p>
        <button class="btn-secondary" @click="resetFilters">Reset Filter</button>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="currentPage--"
      >← Sebelumnya</button>
      <div class="page-numbers">
        <button
          v-for="p in visiblePages"
          :key="p"
          class="page-num"
          :class="{ active: p === currentPage }"
          @click="currentPage = p"
        >{{ p }}</button>
      </div>
      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >Selanjutnya →</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useJudulStore } from '../stores/judulStore.js'
import { statusWarna } from '../services/mockData.js'

const store = useJudulStore()

const searchQuery = ref('')
const filterStatus = ref('')
const filterBidang = ref('')
const currentPage = ref(1)
const perPage = 10

const statusOptions = ['Diajukan', 'Disetujui', 'Revisi', 'Ditolak', 'Sedang Berjalan', 'Selesai']
const bidangOptions = ['Rekayasa Perangkat Lunak', 'Kecerdasan Buatan', 'Jaringan Komputer', 'Data Science', 'Sistem Informasi']

const loading = computed(() => store.loading)
const filteredJudul = computed(() => store.filteredJudul)

const totalPages = computed(() => Math.ceil(filteredJudul.value.length / perPage))
const paginatedJudul = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredJudul.value.slice(start, start + perPage)
})
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

function handleSearch() {
  store.setSearch(searchQuery.value)
  currentPage.value = 1
}

function handleFilter() {
  store.setFilterStatus(filterStatus.value)
  store.setFilterBidang(filterBidang.value)
  currentPage.value = 1
}

function resetFilters() {
  searchQuery.value = ''
  filterStatus.value = ''
  filterBidang.value = ''
  store.resetFilters()
  currentPage.value = 1
}

function getStatusClass(status) {
  return statusWarna[status] || 'badge-info'
}

function formatTanggal(tanggal) {
  return new Date(tanggal).toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(() => {
  store.fetchJudul()
})
</script>

<style scoped>
.daftar-judul {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Filter */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.25rem;
}
.search-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  min-width: 240px;
  color: #64748b;
}
.search-field {
  flex: 1;
}
.filter-select {
  width: 180px;
  cursor: pointer;
}
.result-count {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-left: auto;
}
.count-number {
  font-size: 1.25rem;
  font-weight: 800;
  color: #60a5fa;
}
.count-label {
  font-size: 0.75rem;
  color: #64748b;
}

/* Loading */
.loading-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.list-skeleton { height: 80px; }

/* Judul cards */
.judul-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.judul-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  transition: all 0.2s;
  cursor: pointer;
}
.judul-card:hover {
  border-color: #3b82f6;
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
}
.judul-main {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}
.judul-number {
  font-size: 0.75rem;
  font-weight: 700;
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  padding: 4px 8px;
  border-radius: 6px;
  white-space: nowrap;
}
.judul-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}
.judul-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: #64748b;
}
.judul-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  flex-shrink: 0;
}
.judul-dosen {
  font-size: 0.6875rem;
  color: #64748b;
  max-width: 180px;
  text-align: right;
}

/* Empty */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding-top: 1rem;
}
.page-btn {
  background: #1e293b;
  border: 1px solid #334155;
  color: #94a3b8;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all 0.2s;
}
.page-btn:hover:not(:disabled) {
  border-color: #3b82f6;
  color: #60a5fa;
}
.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.page-numbers {
  display: flex;
  gap: 4px;
}
.page-num {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: transparent;
  border: 1px solid transparent;
  color: #94a3b8;
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all 0.2s;
}
.page-num:hover {
  background: #1e293b;
}
.page-num.active {
  background: #3b82f6;
  color: white;
  font-weight: 600;
}
</style>

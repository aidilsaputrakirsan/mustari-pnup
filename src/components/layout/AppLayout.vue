<template>
  <!-- Layout Utama Aplikasi SIMTA -->
  <div class="app-layout">
    <SidebarNav />
    <main class="main-content">
      <!-- Header -->
      <header class="main-header">
        <div class="header-left">
          <h2 class="page-title">{{ pageTitle }}</h2>
          <p class="page-subtitle">{{ pageSubtitle }}</p>
        </div>
        <div class="header-right">
          <div class="search-box">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input type="text" placeholder="Cari..." class="search-input" />
          </div>
          <button class="notification-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            <span class="notif-dot"></span>
          </button>
        </div>
      </header>

      <!-- Konten Halaman (router-view) -->
      <div class="page-content">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SidebarNav from './SidebarNav.vue'

const route = useRoute()

// Judul halaman berdasarkan route
const pageTitles = {
  '/': { title: 'Dashboard', subtitle: 'Ringkasan aktivitas Tugas Akhir Anda' },
  '/daftar-judul': { title: 'Daftar Judul Skripsi', subtitle: 'Kelola dan pantau semua judul yang diajukan' },
  '/bimbingan': { title: 'Detail Bimbingan', subtitle: 'Progres bimbingan dan konsultasi' },
  '/jadwal-seminar': { title: 'Jadwal Seminar', subtitle: 'Jadwal Seminar Proposal & Sidang Akhir' },
  '/pengaturan': { title: 'Pengaturan', subtitle: 'Kelola profil dan preferensi akun' },
}

const pageTitle = computed(() => pageTitles[route.path]?.title || 'SIMTA')
const pageSubtitle = computed(() => pageTitles[route.path]?.subtitle || '')
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}
.main-content {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
}

/* Header */
.main-header {
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #1e293b;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 40;
}
.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
}
.page-subtitle {
  font-size: 0.8125rem;
  color: #64748b;
  margin-top: 2px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 0.5rem 1rem;
  color: #64748b;
}
.search-input {
  background: transparent;
  border: none;
  color: #e2e8f0;
  font-size: 0.8125rem;
  outline: none;
  width: 180px;
}
.search-input::placeholder {
  color: #64748b;
}
.notification-btn {
  position: relative;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 0.5rem;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s;
}
.notification-btn:hover {
  border-color: #3b82f6;
  color: #e2e8f0;
}
.notif-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid #1e293b;
}

/* Konten */
.page-content {
  padding: 2rem;
}
</style>

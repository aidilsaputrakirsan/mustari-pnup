<template>
  <!-- Sidebar Navigasi SIMTA -->
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Logo & Header -->
    <div class="sidebar-header">
      <div class="logo-wrapper">
        <div class="logo-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            <path d="M8 7h8M8 11h6" />
          </svg>
        </div>
        <transition name="fade">
          <div v-if="!isCollapsed" class="logo-text">
            <h1>SIMTA</h1>
            <span>Manajemen Tugas Akhir</span>
          </div>
        </transition>
      </div>
      <button class="toggle-btn" @click="toggleCollapse" :title="isCollapsed ? 'Expand' : 'Collapse'">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path v-if="isCollapsed" d="M9 18l6-6-6-6" />
          <path v-else d="M15 18l-6-6 6-6" />
        </svg>
      </button>
    </div>

    <!-- Menu Navigasi -->
    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ active: $route.path === item.path }"
      >
        <div class="nav-icon" v-html="item.icon"></div>
        <transition name="fade">
          <span v-if="!isCollapsed" class="nav-label">{{ item.label }}</span>
        </transition>
        <transition name="fade">
          <span v-if="!isCollapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
        </transition>
      </router-link>
    </nav>

    <!-- Footer Sidebar -->
    <div class="sidebar-footer">
      <div class="user-info">
        <div class="avatar">AP</div>
        <transition name="fade">
          <div v-if="!isCollapsed" class="user-details">
            <span class="user-name">Andi Pratama</span>
            <span class="user-role">Mahasiswa</span>
          </div>
        </transition>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'

const isCollapsed = ref(false)

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

// Item menu navigasi
const menuItems = [
  {
    path: '/',
    label: 'Dashboard',
    badge: null,
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
  },
  {
    path: '/daftar-judul',
    label: 'Daftar Judul',
    badge: '50',
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8M16 17H8M10 9H8"/></svg>',
  },
  {
    path: '/bimbingan',
    label: 'Detail Bimbingan',
    badge: '3',
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
  },
  {
    path: '/jadwal-seminar',
    label: 'Jadwal Seminar',
    badge: '5',
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
  },
  {
    path: '/pengaturan',
    label: 'Pengaturan',
    badge: null,
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
  },
]
</script>

<style scoped>
.sidebar {
  width: 260px;
  min-height: 100vh;
  background: linear-gradient(180deg, #0f172a 0%, #1a1f3a 100%);
  border-right: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 50;
}
.sidebar.collapsed {
  width: 72px;
}

/* Header */
.sidebar-header {
  padding: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #1e293b;
}
.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}
.logo-text h1 {
  font-size: 1.125rem;
  font-weight: 800;
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
}
.logo-text span {
  font-size: 0.625rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.toggle-btn {
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s;
}
.toggle-btn:hover {
  background: #1e293b;
  color: #e2e8f0;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  position: relative;
}
.nav-item:hover {
  background: rgba(59, 130, 246, 0.08);
  color: #e2e8f0;
}
.nav-item.active {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.1));
  color: #60a5fa;
  font-weight: 600;
}
.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: linear-gradient(180deg, #3b82f6, #8b5cf6);
  border-radius: 0 3px 3px 0;
}
.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.nav-badge {
  margin-left: auto;
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
}

/* Footer */
.sidebar-footer {
  padding: 1rem 0.75rem;
  border-top: 1px solid #1e293b;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
}
.avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}
.user-details {
  display: flex;
  flex-direction: column;
}
.user-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #e2e8f0;
}
.user-role {
  font-size: 0.6875rem;
  color: #64748b;
}
</style>

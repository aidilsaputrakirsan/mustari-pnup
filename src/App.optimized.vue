<template>
  <!--
    ============================================
    APP.VUE - VERSI 1B (OPTIMIZED)
    ============================================
    Pendekatan: Lazy Loading via router
    Komponen berat dimuat secara LAZY oleh masing-masing view.
    Transition memberikan UX yang smooth antar halaman.
    ============================================
  -->
  <AppLayout>
    <router-view v-slot="{ Component, route }">
      <transition name="fade" mode="out-in">
        <component :is="Component" :key="route.path" />
      </transition>
    </router-view>
  </AppLayout>
</template>

<script setup>
/**
 * ✅ BEST PRACTICE: App.vue yang bersih
 *
 * - Tidak ada import komponen berat di sini
 * - ChartStatistik & CalendarJadwal dimuat oleh views masing-masing
 * - Router melakukan code splitting via dynamic import
 * - Transition memberikan UX smooth saat navigasi
 */
import AppLayout from './components/layout/AppLayout.vue'
</script>

<style>
/* Transition animation untuk perpindahan halaman */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<template>
  <!--
    ============================================
    APP.VUE - VERSI 1A (BASELINE)
    ============================================
    Pendekatan: EAGER IMPORT semua komponen
    Semua komponen berat langsung di-import via views.
    ============================================
  -->
  <AppLayout>
    <router-view />
  </AppLayout>
</template>

<script setup>
/**
 * ❌ BAD PRACTICE: Pendekatan baseline
 * Semua halaman dan komponen di-import eager via router
 * dan views. Tidak ada code splitting atau lazy loading.
 */
import AppLayout from './components/layout/AppLayout.vue'
</script>

<style>
/* Tidak ada style khusus - semua ada di style.css */
</style>

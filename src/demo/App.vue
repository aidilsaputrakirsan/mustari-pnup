<template>
  <router-view v-slot="{ Component, route }">
    <transition name="halaman" mode="out-in">
      <component :is="Component" :key="route.path" />
    </transition>
  </router-view>
  <Toast position="bottom-right" />
</template>

<script setup>
import Toast from 'primevue/toast'
</script>

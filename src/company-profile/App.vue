<template>
  <div class="cp-layout">
    <nav class="cp-nav">
      <h2>Perusahaan X</h2>
      <ul>
        <li><router-link to="/">Beranda</router-link></li>
        <li><router-link to="/tentang">Tentang Kami</router-link></li>
        <li><router-link to="/layanan">Layanan</router-link></li>
      </ul>
    </nav>
    <main class="cp-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<style scoped>
.cp-layout { font-family: Arial, sans-serif; }
.cp-nav { display: flex; justify-content: space-between; padding: 1rem 2rem; background: #2c3e50; color: white; }
.cp-nav ul { list-style: none; display: flex; gap: 1rem; }
.cp-nav a { color: white; text-decoration: none; }
.cp-content { padding: 2rem; }
</style>

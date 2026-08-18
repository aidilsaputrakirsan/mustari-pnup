<template>
  <div class="kerangka">
    <!-- ============ SIDEBAR ============ -->
    <aside class="sisi" :class="{ ringkas: ringkas }">
      <div class="sisi-kepala">
        <div class="merek">
          <div class="merek-lambang">
            <i class="pi pi-graduation-cap"></i>
          </div>
          <div v-if="!ringkas" class="merek-teks">
            <strong>SIMTA</strong>
            <span>Politeknik Negeri Ujung Pandang</span>
          </div>
        </div>
      </div>

      <nav class="sisi-menu">
        <p v-if="!ringkas" class="menu-label">Penyelenggaraan</p>
        <router-link
          v-for="item in menu"
          :key="item.to"
          :to="item.to"
          class="menu-item"
          :class="{ aktif: rute.path === item.to }"
          v-tooltip.right="ringkas ? item.label : null"
        >
          <i :class="item.ikon"></i>
          <span v-if="!ringkas">{{ item.label }}</span>
          <Badge
            v-if="!ringkas && item.jumlah"
            :value="item.jumlah"
            :severity="item.tegas ? 'danger' : 'secondary'"
            class="menu-jumlah"
          />
        </router-link>
      </nav>

      <div class="sisi-kaki">
        <div v-if="!ringkas" class="semester-kini">
          <span class="semester-label">Semester berjalan</span>
          <strong>{{ semesterAktif.label }}</strong>
        </div>
        <Button
          :icon="ringkas ? 'pi pi-angle-double-right' : 'pi pi-angle-double-left'"
          text
          severity="secondary"
          size="small"
          :aria-label="ringkas ? 'Lebarkan menu' : 'Ringkaskan menu'"
          @click="ringkas = !ringkas"
        />
      </div>
    </aside>

    <!-- ============ ISI ============ -->
    <div class="isi">
      <header class="bilah">
        <div class="bilah-kiri">
          <Button
            icon="pi pi-bars"
            text
            severity="secondary"
            class="tombol-menu-mobil"
            aria-label="Buka menu"
            @click="laciTampil = true"
          />
          <div>
            <h1 class="bilah-judul">{{ rute.meta.judul }}</h1>
            <p class="bilah-anak">{{ rute.meta.anak }}</p>
          </div>
        </div>

        <div class="bilah-kanan">
          <Button
            :icon="gelap ? 'pi pi-sun' : 'pi pi-moon'"
            text
            severity="secondary"
            rounded
            :aria-label="gelap ? 'Gunakan tema terang' : 'Gunakan tema gelap'"
            v-tooltip.bottom="gelap ? 'Tema terang' : 'Tema gelap'"
            @click="alihTema"
          />
          <Button
            icon="pi pi-bell"
            text
            severity="secondary"
            rounded
            aria-label="Notifikasi"
            v-tooltip.bottom="ringkasan.perluTindakan + ' judul menunggu tindakan'"
            :badge="String(ringkasan.perluTindakan)"
            badgeSeverity="danger"
          />

          <button class="pengguna" @click="menuPengguna.toggle($event)">
            <Avatar :label="profil.inisial" shape="circle" class="pengguna-avatar" />
            <span class="pengguna-teks">
              <strong>{{ ringkasNama(profil.nama) }}</strong>
              <small>{{ profil.peranSingkat }}</small>
            </span>
            <i class="pi pi-chevron-down pengguna-panah"></i>
          </button>
          <Menu ref="menuPengguna" :model="menuAkun" :popup="true" />
        </div>
      </header>

      <main class="lembar">
        <router-view v-slot="{ Component, route }">
          <transition name="halaman" mode="out-in">
            <component :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- ============ LACI (MOBIL) ============ -->
    <Drawer v-model:visible="laciTampil" header="SIMTA" class="laci">
      <nav class="laci-menu">
        <router-link
          v-for="item in menu"
          :key="item.to"
          :to="item.to"
          class="menu-item"
          :class="{ aktif: rute.path === item.to }"
          @click="laciTampil = false"
        >
          <i :class="item.ikon"></i>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </Drawer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Avatar from 'primevue/avatar'
import Badge from 'primevue/badge'
import Button from 'primevue/button'
import Drawer from 'primevue/drawer'
import Menu from 'primevue/menu'
import { useToast } from 'primevue/usetoast'

import { useAuthStore } from '../stores/auth.js'
import { useTema } from '../composables/useTema.js'
import { ringkasan, semesterAktif } from '../data/seed.js'

const rute = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const { gelap, alihTema } = useTema()

const ringkas = ref(false)
const laciTampil = ref(false)
const menuPengguna = ref()

const profil = computed(() => auth.profil ?? {})

const menu = [
  { to: '/', label: 'Dasbor', ikon: 'pi pi-chart-pie' },
  { to: '/tugas-akhir', label: 'Arsip Tugas Akhir', ikon: 'pi pi-book', jumlah: ringkasan.totalArsip },
  { to: '/bimbingan', label: 'Log Bimbingan', ikon: 'pi pi-comments', jumlah: ringkasan.bimbinganBelumDisetujui, tegas: true },
  { to: '/seminar', label: 'Seminar & Sidang', ikon: 'pi pi-calendar', jumlah: ringkasan.seminarMendatang },
  { to: '/dosen', label: 'Beban Pembimbing', ikon: 'pi pi-users' },
  { to: '/rekap', label: 'Rekap Semester', ikon: 'pi pi-chart-bar' },
]

/** "Dr. Ahmad Ridwan, S.T., M.Kom." → "Dr. Ahmad Ridwan" */
function ringkasNama(nama = '') {
  return nama.split(',')[0]
}

const menuAkun = [
  { label: profil.value.unit, disabled: true },
  { separator: true },
  {
    label: 'Profil saya',
    icon: 'pi pi-user',
    command: () => toast.add({ severity: 'info', summary: 'Mode demo', detail: 'Halaman profil tidak tersedia pada versi demo.', life: 3000 }),
  },
  {
    label: 'Keluar',
    icon: 'pi pi-sign-out',
    command: () => {
      auth.keluar()
      router.push({ name: 'Masuk' })
    },
  },
]
</script>

<style scoped>
.kerangka {
  display: flex;
  min-height: 100vh;
}

/* ============ SIDEBAR ============ */
.sisi {
  width: 264px;
  flex-shrink: 0;
  background: var(--simta-sidebar);
  border-right: 1px solid var(--simta-garis);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  transition: width .2s ease;
}

.sisi.ringkas {
  width: 76px;
}

.sisi-kepala {
  padding: 1.125rem 1rem;
  border-bottom: 1px solid var(--simta-garis);
}

.merek {
  display: flex;
  align-items: center;
  gap: .75rem;
}

.merek-lambang {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--p-primary-500), var(--p-primary-700));
  color: #fff;
  display: grid;
  place-items: center;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.merek-teks {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.merek-teks strong {
  font-size: 1.0625rem;
  font-weight: 800;
  letter-spacing: -.02em;
}

.merek-teks span {
  font-size: .625rem;
  color: var(--simta-teks-lembut);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sisi-menu {
  flex: 1;
  padding: 1rem .75rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.menu-label {
  font-size: .625rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--simta-teks-lembut);
  font-weight: 700;
  padding: 0 .75rem;
  margin-bottom: .5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .625rem .75rem;
  border-radius: 8px;
  color: var(--simta-teks-lembut);
  text-decoration: none;
  font-size: .8125rem;
  font-weight: 500;
  transition: background .15s ease, color .15s ease;
}

.sisi.ringkas .menu-item {
  justify-content: center;
}

.menu-item i {
  font-size: 1rem;
  flex-shrink: 0;
}

.menu-item:hover {
  background: var(--p-primary-50);
  color: var(--p-primary-700);
}

html.app-dark .menu-item:hover {
  background: rgba(99, 102, 241, .12);
  color: var(--p-primary-300);
}

.menu-item.aktif {
  background: var(--p-primary-600);
  color: #fff;
  font-weight: 600;
  box-shadow: var(--simta-bayang);
}

.menu-item.aktif:hover {
  background: var(--p-primary-600);
  color: #fff;
}

.menu-jumlah {
  margin-left: auto;
}

.sisi-kaki {
  padding: .75rem;
  border-top: 1px solid var(--simta-garis);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: .5rem;
}

.semester-kini {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.semester-label {
  font-size: .625rem;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: var(--simta-teks-lembut);
  font-weight: 600;
}

.semester-kini strong {
  font-size: .8125rem;
  white-space: nowrap;
}

/* ============ ISI ============ */
.isi {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.bilah {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: .875rem 1.5rem;
  background: var(--simta-permukaan);
  border-bottom: 1px solid var(--simta-garis);
  position: sticky;
  top: 0;
  z-index: 20;
}

.bilah-kiri {
  display: flex;
  align-items: center;
  gap: .5rem;
  min-width: 0;
}

.bilah-judul {
  font-size: 1.1875rem;
  font-weight: 700;
  letter-spacing: -.02em;
}

.bilah-anak {
  font-size: .75rem;
  color: var(--simta-teks-lembut);
  margin-top: 1px;
}

.bilah-kanan {
  display: flex;
  align-items: center;
  gap: .25rem;
}

.tombol-menu-mobil {
  display: none;
}

.pengguna {
  display: flex;
  align-items: center;
  gap: .5rem;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 999px;
  padding: .25rem .625rem .25rem .25rem;
  cursor: pointer;
  color: inherit;
  font: inherit;
  margin-left: .25rem;
  transition: background .15s ease, border-color .15s ease;
}

.pengguna:hover {
  background: var(--p-surface-100);
  border-color: var(--simta-garis);
}

html.app-dark .pengguna:hover {
  background: var(--p-surface-800);
}

.pengguna-avatar {
  background: var(--p-primary-600);
  color: #fff;
  font-size: .75rem;
  font-weight: 700;
  width: 32px;
  height: 32px;
}

.pengguna-teks {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.2;
}

.pengguna-teks strong {
  font-size: .8125rem;
  font-weight: 600;
}

.pengguna-teks small {
  font-size: .6875rem;
  color: var(--simta-teks-lembut);
}

.pengguna-panah {
  font-size: .625rem;
  color: var(--simta-teks-lembut);
}

.lembar {
  padding: 1.5rem;
  flex: 1;
}

.laci-menu {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* ============ RESPONSIF ============ */
@media (max-width: 1024px) {
  .sisi {
    display: none;
  }

  .tombol-menu-mobil {
    display: inline-flex;
  }

  .pengguna-teks {
    display: none;
  }

  .lembar {
    padding: 1rem;
  }

  .bilah {
    padding: .75rem 1rem;
  }
}
</style>

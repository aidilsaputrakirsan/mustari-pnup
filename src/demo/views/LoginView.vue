<template>
  <div class="masuk">
    <!-- ============ PANEL KIRI: IDENTITAS ============ -->
    <section class="sisi-merek">
      <div class="merek-atas">
        <div class="merek-lambang"><i class="pi pi-graduation-cap"></i></div>
        <div>
          <strong>SIMTA</strong>
          <span>Sistem Informasi Manajemen Tugas Akhir</span>
        </div>
      </div>

      <div class="merek-tengah">
        <h2>Satu tempat untuk seluruh siklus Tugas Akhir.</h2>
        <p>
          Pengajuan judul, log bimbingan, penjadwalan seminar, hingga rekap kelulusan —
          terpantau dari satu dasbor koordinator.
        </p>

        <dl class="statistik">
          <div>
            <dt>{{ ringkasan.totalArsip }}</dt>
            <dd>Judul terarsip</dd>
          </div>
          <div>
            <dt>{{ daftarSemester.length }}</dt>
            <dd>Semester tercatat</dd>
          </div>
          <div>
            <dt>{{ ringkasan.totalBimbingan.toLocaleString('id-ID') }}</dt>
            <dd>Log bimbingan</dd>
          </div>
        </dl>
      </div>

      <p class="merek-bawah">
        Politeknik Negeri Ujung Pandang &middot; Program Studi D4 Teknik Informatika
      </p>
    </section>

    <!-- ============ PANEL KANAN: FORMULIR ============ -->
    <section class="sisi-form">
      <div class="form-bungkus">
        <div class="form-kepala">
          <h1>Masuk ke SIMTA</h1>
          <p>Gunakan akun sivitas untuk mengakses dasbor.</p>
        </div>

        <!-- Kartu akun demo, sengaja di LUAR formulir -->
        <div class="kartu-demo">
          <div class="demo-kepala">
            <span class="demo-titik" aria-hidden="true"></span>
            <strong>Akun demo — Koordinator Program Studi</strong>
          </div>
          <dl class="demo-isi">
            <div>
              <dt>Email</dt>
              <dd>
                <code>{{ akunDemo.email }}</code>
                <Button
                  icon="pi pi-copy"
                  text
                  rounded
                  size="small"
                  aria-label="Salin email"
                  @click="salin(akunDemo.email, 'Email')"
                />
              </dd>
            </div>
            <div>
              <dt>Kata sandi</dt>
              <dd>
                <code>{{ akunDemo.sandi }}</code>
                <Button
                  icon="pi pi-copy"
                  text
                  rounded
                  size="small"
                  aria-label="Salin kata sandi"
                  @click="salin(akunDemo.sandi, 'Kata sandi')"
                />
              </dd>
            </div>
          </dl>
          <Button
            label="Isi otomatis lalu masuk"
            icon="pi pi-bolt"
            size="small"
            severity="secondary"
            outlined
            class="demo-tombol"
            :loading="auth.sedangProses"
            @click="masukDemo"
          />
        </div>

        <form class="form" @submit.prevent="kirim">
          <div class="ruas">
            <label for="email">Email</label>
            <InputText
              id="email"
              v-model="email"
              type="email"
              placeholder="nama@poliupg.ac.id"
              autocomplete="username"
              :invalid="Boolean(auth.pesanGalat)"
              fluid
            />
          </div>

          <div class="ruas">
            <label for="sandi">Kata sandi</label>
            <Password
              id="sandi"
              v-model="sandi"
              placeholder="Masukkan kata sandi"
              autocomplete="current-password"
              :feedback="false"
              toggleMask
              :invalid="Boolean(auth.pesanGalat)"
              fluid
            />
          </div>

          <div class="ruas-baris">
            <div class="ingat">
              <Checkbox v-model="ingat" inputId="ingat" binary />
              <label for="ingat">Ingat saya</label>
            </div>
            <a href="#" class="tautan-lupa" @click.prevent="beriTahuDemo">Lupa kata sandi?</a>
          </div>

          <Message v-if="auth.pesanGalat" severity="error" size="small" variant="simple" class="galat">
            {{ auth.pesanGalat }}
          </Message>

          <Button
            type="submit"
            label="Masuk"
            icon="pi pi-sign-in"
            :loading="auth.sedangProses"
            fluid
          />
        </form>

        <p class="catatan-kaki">
          Aplikasi demo tanpa basis data — seluruh data bersifat simulasi
          dan tidak merepresentasikan data akademik sesungguhnya.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'
import { useToast } from 'primevue/usetoast'

import { useAuthStore } from '../stores/auth.js'
import { akunDemo, ringkasan, daftarSemester } from '../data/seed.js'

const auth = useAuthStore()
const router = useRouter()
const rute = useRoute()
const toast = useToast()

const email = ref('')
const sandi = ref('')
const ingat = ref(true)

async function kirim() {
  const berhasil = await auth.masuk(email.value, sandi.value)
  if (berhasil) {
    toast.add({
      severity: 'success',
      summary: 'Selamat datang',
      detail: auth.profil.nama.split(',')[0],
      life: 2500,
    })
    router.push(rute.query.lanjut || { name: 'Dasbor' })
  }
}

/** Jalan pintas demo: isi kredensial lalu langsung masuk. */
async function masukDemo() {
  email.value = akunDemo.email
  sandi.value = akunDemo.sandi
  await kirim()
}

async function salin(teks, label) {
  try {
    await navigator.clipboard.writeText(teks)
    toast.add({ severity: 'success', summary: label + ' disalin', life: 1800 })
  } catch {
    toast.add({ severity: 'warn', summary: 'Gagal menyalin', detail: 'Salin manual dari kartu demo.', life: 2500 })
  }
}

function beriTahuDemo() {
  toast.add({
    severity: 'info',
    summary: 'Mode demo',
    detail: 'Pemulihan kata sandi tidak tersedia. Gunakan akun demo yang tertera.',
    life: 3200,
  })
}
</script>

<style scoped>
.masuk {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1.05fr 1fr;
}

/* ============ PANEL MEREK ============ */
.sisi-merek {
  background:
    radial-gradient(120% 120% at 0% 0%, #4338ca 0%, #312e81 45%, #1e1b4b 100%);
  color: #e0e7ff;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

/* Garis halus sebagai tekstur latar */
.sisi-merek::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, .05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, .05) 1px, transparent 1px);
  background-size: 56px 56px;
  mask-image: radial-gradient(80% 80% at 70% 30%, #000 20%, transparent 75%);
  pointer-events: none;
}

.merek-atas,
.merek-tengah,
.merek-bawah {
  position: relative;
  z-index: 1;
}

.merek-atas {
  display: flex;
  align-items: center;
  gap: .75rem;
}

.merek-atas strong {
  display: block;
  font-size: 1.125rem;
  font-weight: 800;
  letter-spacing: -.02em;
  color: #fff;
}

.merek-atas span {
  font-size: .6875rem;
  color: #a5b4fc;
}

.merek-lambang {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  background: rgba(255, 255, 255, .12);
  border: 1px solid rgba(255, 255, 255, .2);
  display: grid;
  place-items: center;
  font-size: 1.25rem;
  color: #fff;
}

.merek-tengah h2 {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -.03em;
  line-height: 1.2;
  color: #fff;
  max-width: 15ch;
}

.merek-tengah p {
  margin-top: 1rem;
  font-size: .9375rem;
  line-height: 1.65;
  color: #c7d2fe;
  max-width: 46ch;
}

.statistik {
  display: flex;
  gap: 2.5rem;
  margin-top: 2.5rem;
  padding-top: 1.75rem;
  border-top: 1px solid rgba(255, 255, 255, .14);
}

.statistik dt {
  font-size: 1.75rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -.02em;
  font-variant-numeric: tabular-nums;
}

.statistik dd {
  margin: 2px 0 0;
  font-size: .75rem;
  color: #a5b4fc;
}

.merek-bawah {
  font-size: .75rem;
  color: #a5b4fc;
}

/* ============ PANEL FORMULIR ============ */
.sisi-form {
  display: grid;
  place-items: center;
  padding: 2rem;
  background: var(--simta-permukaan);
}

.form-bungkus {
  width: 100%;
  max-width: 400px;
}

.form-kepala h1 {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -.02em;
}

.form-kepala p {
  margin-top: .375rem;
  font-size: .875rem;
  color: var(--simta-teks-lembut);
}

/* ============ KARTU DEMO ============ */
.kartu-demo {
  margin: 1.5rem 0;
  padding: 1rem;
  border: 1px dashed var(--p-primary-300);
  border-radius: 12px;
  background: var(--p-primary-50);
}

html.app-dark .kartu-demo {
  background: rgba(99, 102, 241, .1);
  border-color: var(--p-primary-700);
}

.demo-kepala {
  display: flex;
  align-items: center;
  gap: .5rem;
  font-size: .75rem;
  color: var(--p-primary-800);
}

html.app-dark .demo-kepala {
  color: var(--p-primary-200);
}

.demo-titik {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, .2);
  flex-shrink: 0;
}

.demo-isi {
  margin: .75rem 0 0;
  display: flex;
  flex-direction: column;
  gap: .25rem;
}

.demo-isi>div {
  display: flex;
  align-items: center;
  gap: .5rem;
}

.demo-isi dt {
  font-size: .75rem;
  color: var(--simta-teks-lembut);
  width: 86px;
  flex-shrink: 0;
}

.demo-isi dd {
  margin: 0;
  display: flex;
  align-items: center;
  gap: .125rem;
  min-width: 0;
}

.demo-isi code {
  font-size: .78125rem;
  font-weight: 600;
  color: var(--simta-teks);
  background: transparent;
  overflow-wrap: anywhere;
}

.demo-tombol {
  margin-top: .75rem;
  width: 100%;
}

/* ============ FORMULIR ============ */
.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ruas {
  display: flex;
  flex-direction: column;
  gap: .375rem;
}

.ruas label {
  font-size: .8125rem;
  font-weight: 600;
}

.ruas-baris {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ingat {
  display: flex;
  align-items: center;
  gap: .5rem;
}

.ingat label {
  font-size: .8125rem;
  color: var(--simta-teks-lembut);
  cursor: pointer;
}

.tautan-lupa {
  font-size: .8125rem;
  color: var(--p-primary-600);
  text-decoration: none;
  font-weight: 500;
}

.tautan-lupa:hover {
  text-decoration: underline;
}

.galat {
  margin-top: -.25rem;
}

.catatan-kaki {
  margin-top: 1.5rem;
  font-size: .6875rem;
  line-height: 1.6;
  color: var(--simta-teks-lembut);
  text-align: center;
}

/* ============ RESPONSIF ============ */
@media (max-width: 900px) {
  .masuk {
    grid-template-columns: 1fr;
  }

  .sisi-merek {
    padding: 1.75rem;
  }

  .merek-tengah {
    display: none;
  }

  .merek-bawah {
    display: none;
  }

  .sisi-form {
    padding: 1.5rem;
    align-items: start;
  }
}
</style>

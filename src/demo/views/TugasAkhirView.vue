<template>
  <div class="panel">
    <DataTable
      v-model:filters="filter"
      v-model:expandedRows="barisTerbuka"
      :value="daftarTugasAkhir"
      data-key="id"
      paginator
      :rows="15"
      :rows-per-page-options="[15, 25, 50, 100]"
      filter-display="menu"
      sort-mode="multiple"
      removable-sort
      :global-filter-fields="['kode', 'judul', 'nim', 'namaMahasiswa', 'pembimbing1', 'pembimbing2']"
      size="small"
      striped-rows
      scrollable
      scroll-height="calc(100vh - 320px)"
      paginator-template="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink RowsPerPageDropdown"
      current-page-report-template="{first}–{last} dari {totalRecords} judul"
      state-storage="session"
      state-key="simta.tabel.ta"
    >
      <!-- ============ BILAH ALAT ============ -->
      <template #header>
        <div class="alat">
          <div class="alat-kiri">
            <IconField>
              <InputIcon class="pi pi-search" />
              <InputText
                v-model="filter.global.value"
                placeholder="Cari judul, NIM, nama, atau pembimbing…"
                class="pencarian"
              />
            </IconField>

            <Select
              v-model="filter.semesterLabel.value"
              :options="opsiSemester"
              placeholder="Semua semester"
              show-clear
              class="saring"
            />
            <MultiSelect
              v-model="filter.status.value"
              :options="opsiStatus"
              placeholder="Semua status"
              :max-selected-labels="1"
              selected-items-label="{0} status"
              class="saring"
            />
            <MultiSelect
              v-model="filter.bidang.value"
              :options="daftarBidang"
              placeholder="Semua bidang"
              :max-selected-labels="1"
              selected-items-label="{0} bidang"
              class="saring"
            />
          </div>

          <div class="alat-kanan">
            <Button
              v-if="adaSaringan"
              label="Bersihkan"
              icon="pi pi-filter-slash"
              severity="secondary"
              text
              size="small"
              @click="resetFilter"
            />
            <Button
              label="Ekspor CSV"
              icon="pi pi-download"
              severity="secondary"
              outlined
              size="small"
              @click="ekspor"
            />
          </div>
        </div>
      </template>

      <template #empty>
        <div class="kosong">
          <i class="pi pi-inbox"></i>
          <p>Tidak ada judul yang cocok dengan saringan.</p>
          <Button label="Bersihkan saringan" text size="small" @click="resetFilter" />
        </div>
      </template>

      <!-- ============ KOLOM ============ -->
      <Column expander style="width: 42px" />

      <Column field="kode" header="Kode" sortable style="min-width: 108px">
        <template #body="{ data }">
          <span class="kode angka-tabular">{{ data.kode }}</span>
        </template>
      </Column>

      <Column field="namaMahasiswa" header="Mahasiswa" sortable style="min-width: 168px">
        <template #body="{ data }">
          <div class="sel-mhs">
            <strong>{{ data.namaMahasiswa }}</strong>
            <small class="angka-tabular">{{ data.nim }} · {{ data.prodiKode }}</small>
          </div>
        </template>
      </Column>

      <Column field="judul" header="Judul Tugas Akhir" sortable style="min-width: 250px">
        <template #body="{ data }">
          <span class="judul" :title="data.judul">{{ data.judul }}</span>
        </template>
      </Column>

      <Column field="bidang" header="Bidang" sortable style="min-width: 140px">
        <template #body="{ data }">
          <span class="bidang">{{ data.bidang }}</span>
        </template>
      </Column>

      <Column field="semesterLabel" header="Semester" sortable style="min-width: 120px">
        <template #body="{ data }">
          <span class="semester">{{ pendekSemester(data.semesterLabel) }}</span>
        </template>
      </Column>

      <Column field="status" header="Status" sortable style="min-width: 128px">
        <template #body="{ data }">
          <Tag :value="data.status" :severity="severityStatus[data.status]" />
        </template>
      </Column>

      <Column field="progres" header="Progres" sortable style="min-width: 108px">
        <template #body="{ data }">
          <div class="progres">
            <ProgressBar :value="data.progres" :show-value="false" style="height: 6px" />
            <span class="angka-tabular">{{ data.progres }}%</span>
          </div>
        </template>
      </Column>

      <Column field="nilaiHuruf" header="Nilai" sortable style="min-width: 76px">
        <template #body="{ data }">
          <span v-if="data.nilaiHuruf" class="nilai">
            {{ data.nilaiHuruf }}
            <small class="angka-tabular">{{ data.nilaiAngka }}</small>
          </span>
          <span v-else class="kosong-sel">—</span>
        </template>
      </Column>

      <!-- ============ BARIS RINCIAN ============ -->
      <template #expansion="{ data }">
        <div class="rincian">
          <div class="rincian-kolom">
            <h4>Pembimbing</h4>
            <ul class="daftar-pembimbing">
              <li>
                <Avatar :label="inisial(data.pembimbing1)" shape="circle" size="normal" class="avatar-dosen" />
                <div>
                  <strong>{{ data.pembimbing1 }}</strong>
                  <small>Pembimbing I</small>
                </div>
              </li>
              <li>
                <Avatar :label="inisial(data.pembimbing2)" shape="circle" size="normal" class="avatar-dosen" />
                <div>
                  <strong>{{ data.pembimbing2 }}</strong>
                  <small>Pembimbing II</small>
                </div>
              </li>
            </ul>
          </div>

          <div class="rincian-kolom">
            <h4>Administrasi</h4>
            <dl class="ringkas-data">
              <div><dt>Program studi</dt><dd>{{ data.prodi }}</dd></div>
              <div><dt>Angkatan</dt><dd class="angka-tabular">{{ data.angkatan }}</dd></div>
              <div><dt>IPK</dt><dd class="angka-tabular">{{ data.ipk.toFixed(2) }}</dd></div>
              <div><dt>Tanggal ajuan</dt><dd class="angka-tabular">{{ data.tanggalAjuan }}</dd></div>
            </dl>
          </div>

          <div class="rincian-kolom lebar">
            <h4>Riwayat bimbingan terakhir</h4>
            <Timeline :value="bimbinganTerakhir(data.id)" class="linimasa">
              <template #opposite="{ item }">
                <small class="angka-tabular linimasa-tanggal">{{ item.tanggal }}</small>
              </template>
              <template #content="{ item }">
                <strong class="linimasa-topik">{{ item.topik }}</strong>
                <p class="linimasa-catatan">{{ item.catatan }}</p>
              </template>
            </Timeline>
            <p v-if="!bimbinganTerakhir(data.id).length" class="kosong-sel">
              Belum ada catatan bimbingan.
            </p>
          </div>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import MultiSelect from 'primevue/multiselect'
import ProgressBar from 'primevue/progressbar'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Timeline from 'primevue/timeline'
import { useToast } from 'primevue/usetoast'

import {
  daftarTugasAkhir,
  daftarBimbingan,
  daftarBidang,
  daftarSemester,
  severityStatus,
} from '../data/seed.js'

const toast = useToast()
const barisTerbuka = ref({})

const opsiSemester = daftarSemester.map((s) => s.label)
const opsiStatus = [...new Set(daftarTugasAkhir.map((t) => t.status))]

function filterAwal() {
  return {
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    semesterLabel: { value: null, matchMode: FilterMatchMode.EQUALS },
    status: { value: null, matchMode: FilterMatchMode.IN },
    bidang: { value: null, matchMode: FilterMatchMode.IN },
    judul: {
      operator: FilterOperator.AND,
      constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }],
    },
    progres: {
      operator: FilterOperator.AND,
      constraints: [{ value: null, matchMode: FilterMatchMode.GREATER_THAN_OR_EQUAL_TO }],
    },
  }
}

const filter = ref(filterAwal())

const adaSaringan = computed(() =>
  Boolean(
    filter.value.global.value ||
    filter.value.semesterLabel.value ||
    filter.value.status.value?.length ||
    filter.value.bidang.value?.length
  )
)

function resetFilter() {
  filter.value = filterAwal()
}

/** Tiga catatan bimbingan terbaru untuk baris yang dibuka. */
function bimbinganTerakhir(taId) {
  return daftarBimbingan
    .filter((b) => b.taId === taId)
    .slice(-3)
    .reverse()
}

/** "2023/2024 Ganjil" → "23/24 Ganjil", agar kolom tetap ramping. */
function pendekSemester(label = '') {
  const [tahun, jenis] = label.split(' ')
  const [awal, akhir] = tahun.split('/')
  return awal.slice(2) + '/' + akhir.slice(2) + ' ' + jenis
}

function inisial(nama = '') {
  return nama
    .replace(/(Dr\.|Prof\.|Ir\.|S\.T\.|S\.Kom\.|S\.Si\.|M\.Kom\.|M\.T\.|M\.Eng\.|M\.Cs\.|M\.Si\.)/g, '')
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((k) => k[0])
    .join('')
    .toUpperCase()
}

/** Ekspor sisi-klien: tidak ada server, berkas dirakit di browser. */
function ekspor() {
  const kolom = ['kode', 'nim', 'namaMahasiswa', 'prodi', 'judul', 'bidang', 'semesterLabel', 'status', 'progres', 'nilaiHuruf', 'nilaiAngka', 'pembimbing1', 'pembimbing2']
  const kepala = ['Kode', 'NIM', 'Nama', 'Prodi', 'Judul', 'Bidang', 'Semester', 'Status', 'Progres', 'Nilai Huruf', 'Nilai Angka', 'Pembimbing I', 'Pembimbing II']

  const bungkus = (v) => '"' + String(v ?? '').replace(/"/g, '""') + '"'
  const baris = daftarTugasAkhir.map((t) => kolom.map((k) => bungkus(t[k])).join(','))
  const isi = '﻿' + [kepala.map(bungkus).join(','), ...baris].join('\r\n')

  const tautan = document.createElement('a')
  tautan.href = URL.createObjectURL(new Blob([isi], { type: 'text/csv;charset=utf-8;' }))
  tautan.download = 'arsip-tugas-akhir.csv'
  tautan.click()
  URL.revokeObjectURL(tautan.href)

  toast.add({
    severity: 'success',
    summary: 'Ekspor selesai',
    detail: daftarTugasAkhir.length + ' baris diunduh sebagai CSV.',
    life: 3000,
  })
}
</script>

<style scoped>
.alat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.alat-kiri {
  display: flex;
  align-items: center;
  gap: .5rem;
  flex-wrap: wrap;
}

.alat-kanan {
  display: flex;
  align-items: center;
  gap: .5rem;
}

.pencarian {
  width: 306px;
}

.saring {
  min-width: 168px;
}

.kode {
  font-size: .75rem;
  font-weight: 600;
  color: var(--simta-teks-lembut);
  white-space: nowrap;
}

.sel-mhs {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}

.sel-mhs strong {
  font-weight: 600;
}

.sel-mhs small {
  color: var(--simta-teks-lembut);
  font-size: .6875rem;
}

.judul {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  max-width: 34ch;
}

.bidang {
  font-size: .75rem;
  color: var(--simta-teks-lembut);
}

.semester {
  font-size: .75rem;
  white-space: nowrap;
}

.progres {
  display: flex;
  align-items: center;
  gap: .5rem;
}

.progres> :deep(.p-progressbar) {
  flex: 1;
  min-width: 56px;
}

.progres span {
  font-size: .6875rem;
  font-weight: 600;
  color: var(--simta-teks-lembut);
  width: 30px;
  text-align: right;
}

.nilai {
  font-weight: 700;
  display: flex;
  align-items: baseline;
  gap: .3125rem;
}

.nilai small {
  font-weight: 500;
  font-size: .6875rem;
  color: var(--simta-teks-lembut);
}

.kosong-sel {
  color: var(--simta-teks-lembut);
  font-size: .8125rem;
}

.kosong {
  text-align: center;
  padding: 2.5rem 1rem;
  color: var(--simta-teks-lembut);
}

.kosong i {
  font-size: 2rem;
  opacity: .45;
  display: block;
  margin-bottom: .625rem;
}

/* ============ BARIS RINCIAN ============ */
.rincian {
  display: grid;
  grid-template-columns: 1fr 1fr 1.5fr;
  gap: 2rem;
  padding: 1.25rem 1rem 1.25rem 3rem;
  background: var(--p-surface-50);
}

html.app-dark .rincian {
  background: rgba(255, 255, 255, .02);
}

.rincian-kolom h4 {
  font-size: .6875rem;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: var(--simta-teks-lembut);
  font-weight: 700;
  margin-bottom: .875rem;
}

.daftar-pembimbing {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: .75rem;
}

.daftar-pembimbing li {
  display: flex;
  align-items: center;
  gap: .625rem;
}

.daftar-pembimbing strong {
  display: block;
  font-size: .8125rem;
  font-weight: 600;
}

.daftar-pembimbing small {
  font-size: .6875rem;
  color: var(--simta-teks-lembut);
}

.avatar-dosen {
  background: var(--p-primary-100);
  color: var(--p-primary-700);
  font-size: .6875rem;
  font-weight: 700;
  flex-shrink: 0;
}

html.app-dark .avatar-dosen {
  background: rgba(99, 102, 241, .2);
  color: var(--p-primary-200);
}

.ringkas-data {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: .5rem;
}

.ringkas-data>div {
  display: flex;
  gap: .75rem;
}

.ringkas-data dt {
  font-size: .75rem;
  color: var(--simta-teks-lembut);
  width: 106px;
  flex-shrink: 0;
}

.ringkas-data dd {
  margin: 0;
  font-size: .8125rem;
  font-weight: 500;
}

.linimasa-tanggal {
  color: var(--simta-teks-lembut);
  font-size: .6875rem;
}

.linimasa-topik {
  font-size: .8125rem;
  font-weight: 600;
}

.linimasa-catatan {
  font-size: .75rem;
  color: var(--simta-teks-lembut);
  margin-top: .125rem;
  line-height: 1.5;
}

@media (max-width: 1024px) {
  .pencarian {
    width: 100%;
  }

  .rincian {
    grid-template-columns: 1fr;
    padding-left: 1rem;
    gap: 1.5rem;
  }
}
</style>

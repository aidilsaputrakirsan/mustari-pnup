<template>
  <div class="seminar">
    <Tabs value="jadwal">
      <TabList>
        <Tab value="jadwal">
          <i class="pi pi-calendar"></i> Agenda mendatang
          <Badge :value="agendaMendatang.length" severity="danger" class="tab-lencana" />
        </Tab>
        <Tab value="arsip">
          <i class="pi pi-history"></i> Arsip pelaksanaan
          <Badge :value="arsipSeminar.length" severity="secondary" class="tab-lencana" />
        </Tab>
      </TabList>

      <TabPanels>
        <!-- ============ AGENDA MENDATANG ============ -->
        <TabPanel value="jadwal">
          <div v-if="agendaMendatang.length" class="kisi-agenda">
            <article v-for="s in agendaMendatang" :key="s.id" class="kartu-agenda panel">
              <div class="agenda-tanggal">
                <strong class="angka-tabular">{{ hari(s.tanggal) }}</strong>
                <span>{{ bulan(s.tanggal) }}</span>
              </div>

              <div class="agenda-isi">
                <div class="agenda-atas">
                  <Tag :value="s.jenis" :severity="s.jenis === 'Sidang Akhir' ? 'contrast' : 'info'" />
                  <Tag :value="s.status" :severity="severityStatus[s.status]" />
                </div>

                <h3 class="agenda-judul">{{ s.judul }}</h3>

                <p class="agenda-mhs">
                  <i class="pi pi-user"></i>
                  {{ s.namaMahasiswa }}
                  <span class="angka-tabular pemisah">{{ s.nim }}</span>
                </p>

                <div class="agenda-meta">
                  <span><i class="pi pi-clock"></i> {{ s.waktu }} WITA</span>
                  <span><i class="pi pi-map-marker"></i> {{ s.ruangan }}</span>
                </div>

                <div class="agenda-penguji">
                  <span class="penguji-label">Penguji</span>
                  <AvatarGroup>
                    <Avatar
                      v-for="(p, i) in s.penguji"
                      :key="i"
                      :label="inisial(p)"
                      shape="circle"
                      size="normal"
                      class="avatar-penguji"
                      v-tooltip.top="p"
                    />
                  </AvatarGroup>
                </div>
              </div>
            </article>
          </div>

          <div v-else class="kosong panel">
            <i class="pi pi-calendar-times"></i>
            <p>Tidak ada agenda yang belum terlaksana.</p>
          </div>
        </TabPanel>

        <!-- ============ ARSIP ============ -->
        <TabPanel value="arsip">
          <div class="panel">
            <DataTable
              v-model:filters="filter"
              :value="arsipSeminar"
              data-key="id"
              paginator
              :rows="15"
              :rows-per-page-options="[15, 30, 60]"
              :global-filter-fields="['namaMahasiswa', 'nim', 'judul', 'ruangan']"
              sort-field="tanggal"
              :sort-order="-1"
              removable-sort
              size="small"
              striped-rows
              current-page-report-template="{first}–{last} dari {totalRecords} pelaksanaan"
              paginator-template="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink RowsPerPageDropdown"
            >
              <template #header>
                <div class="alat">
                  <IconField>
                    <InputIcon class="pi pi-search" />
                    <InputText v-model="filter.global.value" placeholder="Cari mahasiswa atau judul…" class="pencarian" />
                  </IconField>
                  <Select
                    v-model="filter.semesterLabel.value"
                    :options="opsiSemester"
                    placeholder="Semua semester"
                    show-clear
                    class="saring"
                  />
                  <Select
                    v-model="filter.jenis.value"
                    :options="['Seminar Proposal', 'Sidang Akhir']"
                    placeholder="Semua jenis"
                    show-clear
                    class="saring"
                  />
                </div>
              </template>

              <Column field="tanggal" header="Tanggal" sortable style="width: 116px">
                <template #body="{ data }">
                  <span class="angka-tabular">{{ data.tanggal }}</span>
                </template>
              </Column>

              <Column field="jenis" header="Jenis" sortable style="width: 156px">
                <template #body="{ data }">
                  <Tag :value="data.jenis" :severity="data.jenis === 'Sidang Akhir' ? 'contrast' : 'info'" />
                </template>
              </Column>

              <Column field="namaMahasiswa" header="Mahasiswa" sortable style="min-width: 186px">
                <template #body="{ data }">
                  <div class="sel-mhs">
                    <strong>{{ data.namaMahasiswa }}</strong>
                    <small class="angka-tabular">{{ data.nim }}</small>
                  </div>
                </template>
              </Column>

              <Column field="judul" header="Judul" style="min-width: 320px">
                <template #body="{ data }">
                  <span class="judul">{{ data.judul }}</span>
                </template>
              </Column>

              <Column field="ruangan" header="Ruang" sortable style="min-width: 150px" />

              <Column field="semesterLabel" header="Semester" sortable style="min-width: 148px" />

              <Column field="nilai" header="Nilai" sortable style="width: 92px">
                <template #body="{ data }">
                  <span v-if="data.nilai" class="angka-tabular nilai">{{ data.nilai }}</span>
                  <span v-else class="kosong-sel">—</span>
                </template>
              </Column>
            </DataTable>
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import Avatar from 'primevue/avatar'
import AvatarGroup from 'primevue/avatargroup'
import Badge from 'primevue/badge'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import TabPanel from 'primevue/tabpanel'
import TabPanels from 'primevue/tabpanels'
import Tabs from 'primevue/tabs'
import Tag from 'primevue/tag'

import { daftarSeminar, daftarSemester, severityStatus } from '../data/seed.js'

const opsiSemester = daftarSemester.map((s) => s.label)

const filter = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  semesterLabel: { value: null, matchMode: FilterMatchMode.EQUALS },
  jenis: { value: null, matchMode: FilterMatchMode.EQUALS },
})

const agendaMendatang = computed(() =>
  daftarSeminar
    .filter((s) => s.status !== 'Selesai')
    .sort((a, b) => a.tanggal.localeCompare(b.tanggal))
)

const arsipSeminar = computed(() => daftarSeminar.filter((s) => s.status === 'Selesai'))

const namaBulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
const hari = (iso) => iso.split('-')[2]
const bulan = (iso) => namaBulan[Number(iso.split('-')[1]) - 1] + ' ' + iso.split('-')[0].slice(2)

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
</script>

<style scoped>
.tab-lencana {
  margin-left: .5rem;
}

.kisi-agenda {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(376px, 1fr));
  gap: 1rem;
  padding-top: 1.25rem;
}

.kartu-agenda {
  display: flex;
  gap: 1rem;
  padding: 1.125rem;
  transition: box-shadow .18s ease, transform .18s ease;
}

.kartu-agenda:hover {
  box-shadow: var(--simta-bayang-naik);
  transform: translateY(-1px);
}

.agenda-tanggal {
  width: 58px;
  height: 62px;
  flex-shrink: 0;
  border-radius: 10px;
  background: var(--p-primary-50);
  color: var(--p-primary-700);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

html.app-dark .agenda-tanggal {
  background: rgba(99, 102, 241, .16);
  color: var(--p-primary-200);
}

.agenda-tanggal strong {
  font-size: 1.375rem;
  font-weight: 700;
  line-height: 1;
}

.agenda-tanggal span {
  font-size: .6875rem;
  margin-top: 2px;
}

.agenda-isi {
  min-width: 0;
  flex: 1;
}

.agenda-atas {
  display: flex;
  gap: .375rem;
  flex-wrap: wrap;
}

.agenda-judul {
  font-size: .875rem;
  font-weight: 600;
  line-height: 1.45;
  margin-top: .625rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.agenda-mhs {
  font-size: .8125rem;
  color: var(--simta-teks-lembut);
  margin-top: .5rem;
  display: flex;
  align-items: center;
  gap: .375rem;
}

.agenda-mhs i {
  font-size: .75rem;
}

.pemisah::before {
  content: '·';
  margin-right: .375rem;
}

.agenda-meta {
  display: flex;
  gap: 1rem;
  margin-top: .5rem;
  font-size: .75rem;
  color: var(--simta-teks-lembut);
  flex-wrap: wrap;
}

.agenda-meta i {
  font-size: .6875rem;
  margin-right: .25rem;
}

.agenda-penguji {
  display: flex;
  align-items: center;
  gap: .625rem;
  margin-top: .875rem;
  padding-top: .875rem;
  border-top: 1px solid var(--simta-garis);
}

.penguji-label {
  font-size: .6875rem;
  text-transform: uppercase;
  letter-spacing: .05em;
  font-weight: 600;
  color: var(--simta-teks-lembut);
}

.avatar-penguji {
  background: var(--p-primary-100);
  color: var(--p-primary-700);
  font-size: .625rem;
  font-weight: 700;
}

html.app-dark .avatar-penguji {
  background: rgba(99, 102, 241, .22);
  color: var(--p-primary-200);
}

.alat {
  display: flex;
  align-items: center;
  gap: .5rem;
  flex-wrap: wrap;
}

.pencarian {
  width: 300px;
}

.saring {
  min-width: 176px;
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
  max-width: 44ch;
}

.nilai {
  font-weight: 700;
}

.kosong-sel {
  color: var(--simta-teks-lembut);
}

.kosong {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--simta-teks-lembut);
  margin-top: 1.25rem;
}

.kosong i {
  font-size: 2rem;
  opacity: .45;
  display: block;
  margin-bottom: .625rem;
}

@media (max-width: 1024px) {
  .kisi-agenda {
    grid-template-columns: 1fr;
  }

  .pencarian {
    width: 100%;
  }
}
</style>

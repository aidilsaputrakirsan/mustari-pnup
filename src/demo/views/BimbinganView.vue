<template>
  <div class="bimbingan">
    <section class="baris-kpi">
      <KartuKpi
        label="Total pertemuan"
        :nilai="ringkasan.totalBimbingan"
        ikon="pi pi-comments"
        nada="primer"
        keterangan="tercatat sepanjang arsip"
      />
      <KartuKpi
        label="Menunggu persetujuan"
        :nilai="ringkasan.bimbinganBelumDisetujui"
        ikon="pi pi-clock"
        nada="bahaya"
        keterangan="catatan belum diverifikasi pembimbing"
      />
      <KartuKpi
        label="Rata-rata per judul"
        :nilai="rerataPertemuan"
        ikon="pi pi-chart-bar"
        nada="ingat"
        keterangan="pertemuan per Tugas Akhir"
      />
      <KartuKpi
        label="Pertemuan semester ini"
        :nilai="jumlahSemesterAktif"
        ikon="pi pi-calendar-plus"
        nada="sukses"
        :keterangan="semesterAktif.label"
      />
    </section>

    <div class="panel">
      <DataTable
        v-model:filters="filter"
        :value="daftarBimbingan"
        data-key="id"
        paginator
        :rows="20"
        :rows-per-page-options="[20, 50, 100]"
        :global-filter-fields="['namaMahasiswa', 'nim', 'topik', 'pembimbing', 'kodeTa']"
        sort-field="tanggal"
        :sort-order="-1"
        removable-sort
        size="small"
        striped-rows
        scrollable
        scroll-height="calc(100vh - 460px)"
        current-page-report-template="{first}–{last} dari {totalRecords} catatan"
        paginator-template="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink RowsPerPageDropdown"
      >
        <template #header>
          <div class="alat">
            <IconField>
              <InputIcon class="pi pi-search" />
              <InputText v-model="filter.global.value" placeholder="Cari mahasiswa, topik, atau pembimbing…" class="pencarian" />
            </IconField>
            <Select
              v-model="filter.semesterLabel.value"
              :options="opsiSemester"
              placeholder="Semua semester"
              show-clear
              class="saring"
            />
            <div class="alat-sisa">
              <ToggleButton
                v-model="hanyaTertunda"
                on-label="Hanya tertunda"
                off-label="Hanya tertunda"
                on-icon="pi pi-filter-fill"
                off-icon="pi pi-filter"
                size="small"
                @change="terapkanTertunda"
              />
            </div>
          </div>
        </template>

        <template #empty>
          <div class="kosong">
            <i class="pi pi-inbox"></i>
            <p>Tidak ada catatan bimbingan yang cocok.</p>
          </div>
        </template>

        <Column field="tanggal" header="Tanggal" sortable style="width: 102px">
          <template #body="{ data }">
            <span class="angka-tabular">{{ data.tanggal }}</span>
          </template>
        </Column>

        <Column field="pertemuanKe" header="Ke-" sortable style="width: 58px">
          <template #body="{ data }">
            <span class="angka-tabular pertemuan">{{ data.pertemuanKe }}</span>
          </template>
        </Column>

        <Column field="namaMahasiswa" header="Mahasiswa" sortable style="min-width: 158px">
          <template #body="{ data }">
            <div class="sel-mhs">
              <strong>{{ data.namaMahasiswa }}</strong>
              <small class="angka-tabular">{{ data.nim }}</small>
            </div>
          </template>
        </Column>

        <Column field="topik" header="Topik pertemuan" sortable style="min-width: 196px" />

        <Column field="catatan" header="Catatan pembimbing" style="min-width: 268px">
          <template #body="{ data }">
            <span class="catatan">{{ data.catatan }}</span>
          </template>
        </Column>

        <Column field="pembimbing" header="Pembimbing" sortable style="min-width: 178px">
          <template #body="{ data }">
            <span class="pembimbing">{{ data.pembimbing }}</span>
          </template>
        </Column>

        <Column field="disetujui" header="Status" sortable style="width: 116px">
          <template #body="{ data }">
            <Tag
              :value="data.disetujui ? 'Disetujui' : 'Menunggu'"
              :severity="data.disetujui ? 'success' : 'warn'"
              :icon="data.disetujui ? 'pi pi-check' : 'pi pi-clock'"
            />
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import ToggleButton from 'primevue/togglebutton'

import KartuKpi from '../components/KartuKpi.vue'
import {
  daftarBimbingan,
  daftarSemester,
  daftarTugasAkhir,
  ringkasan,
  semesterAktif,
} from '../data/seed.js'

const opsiSemester = daftarSemester.map((s) => s.label)
const hanyaTertunda = ref(false)

const filter = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  semesterLabel: { value: null, matchMode: FilterMatchMode.EQUALS },
  disetujui: { value: null, matchMode: FilterMatchMode.EQUALS },
})

function terapkanTertunda() {
  filter.value.disetujui.value = hanyaTertunda.value ? false : null
}

const rerataPertemuan = computed(() =>
  Math.round(daftarBimbingan.length / daftarTugasAkhir.length)
)

const jumlahSemesterAktif = computed(() =>
  daftarBimbingan.filter((b) => b.semester === semesterAktif.kode).length
)
</script>

<style scoped>
.bimbingan {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.baris-kpi {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.alat {
  display: flex;
  align-items: center;
  gap: .5rem;
  flex-wrap: wrap;
}

.alat-sisa {
  margin-left: auto;
}

.pencarian {
  width: 320px;
}

.saring {
  min-width: 176px;
}

.p-datatable-tbody td:first-child {
  white-space: nowrap;
}

.pertemuan {
  font-weight: 700;
  color: var(--simta-teks-lembut);
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

.catatan {
  color: var(--simta-teks-lembut);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pembimbing {
  font-size: .75rem;
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

@media (max-width: 1280px) {
  .baris-kpi {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .pencarian {
    width: 100%;
  }

  .alat-sisa {
    margin-left: 0;
  }
}

@media (max-width: 640px) {
  .baris-kpi {
    grid-template-columns: 1fr;
  }
}
</style>

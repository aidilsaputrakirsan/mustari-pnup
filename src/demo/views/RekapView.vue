<template>
  <div class="rekap">
    <section class="baris-grafik">
      <div class="panel">
        <div class="panel-judul">
          <div>
            <h3>Persentase kelulusan antar semester</h3>
            <p>Judul yang tuntas dibanding total terdaftar pada semester bersangkutan</p>
          </div>
        </div>
        <div class="panel-isi">
          <Chart type="line" :data="dataKelulusan" :options="opsiKelulusan" class="grafik" />
        </div>
      </div>

      <div class="panel">
        <div class="panel-judul">
          <div>
            <h3>Rerata nilai akhir</h3>
            <p>Rata-rata nilai sidang per semester</p>
          </div>
        </div>
        <div class="panel-isi">
          <Chart type="bar" :data="dataNilai" :options="opsiNilai" class="grafik" />
        </div>
      </div>
    </section>

    <div class="panel">
      <DataTable :value="rekapSemester" data-key="kode" size="small" striped-rows>
        <template #header>
          <div class="panel-judul-dalam">
            <div>
              <h3>Tabel rekapitulasi</h3>
              <p>Semester berjalan ditandai dan belum memiliki angka kelulusan</p>
            </div>
          </div>
        </template>

        <Column field="label" header="Semester" style="min-width: 176px">
          <template #body="{ data }">
            <div class="sel-semester">
              <strong>{{ data.label }}</strong>
              <Tag v-if="data.aktif" value="Berjalan" severity="info" />
            </div>
          </template>
        </Column>

        <Column field="total" header="Terdaftar" sortable style="width: 116px">
          <template #body="{ data }">
            <span class="angka-tabular tebal">{{ data.total }}</span>
          </template>
        </Column>

        <Column field="lulus" header="Lulus" sortable style="width: 100px">
          <template #body="{ data }">
            <span class="angka-tabular tebal">{{ data.lulus }}</span>
          </template>
        </Column>

        <Column field="berjalan" header="Berjalan" sortable style="width: 110px">
          <template #body="{ data }">
            <span class="angka-tabular">{{ data.berjalan }}</span>
          </template>
        </Column>

        <Column field="mundur" header="Mengundurkan diri" sortable style="width: 170px">
          <template #body="{ data }">
            <span class="angka-tabular" :class="{ merah: data.mundur > 0 }">{{ data.mundur }}</span>
          </template>
        </Column>

        <Column field="persenLulus" header="Kelulusan" sortable style="min-width: 200px">
          <template #body="{ data }">
            <div v-if="!data.aktif" class="kuota">
              <ProgressBar :value="data.persenLulus" :show-value="false" style="height: 7px" />
              <span class="angka-tabular kuota-teks">{{ data.persenLulus }}%</span>
            </div>
            <span v-else class="lembut">Belum tuntas</span>
          </template>
        </Column>

        <Column field="nilaiRerata" header="Rerata nilai" sortable style="width: 130px">
          <template #body="{ data }">
            <Tag
              v-if="data.nilaiRerata"
              :value="String(data.nilaiRerata)"
              :severity="data.nilaiRerata >= 88 ? 'success' : 'info'"
            />
            <span v-else class="lembut">—</span>
          </template>
        </Column>

        <template #footer>
          <div class="kaki">
            <span>Total sepanjang arsip</span>
            <div class="kaki-angka">
              <span><strong class="angka-tabular">{{ totalSemua }}</strong> terdaftar</span>
              <span><strong class="angka-tabular">{{ totalLulus }}</strong> lulus</span>
              <span><strong class="angka-tabular">{{ persenTotal }}%</strong> rerata kelulusan</span>
            </div>
          </div>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Chart from 'primevue/chart'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import ProgressBar from 'primevue/progressbar'
import Tag from 'primevue/tag'

import { useTema } from '../composables/useTema.js'
import { rekapSemester } from '../data/seed.js'

const { gelap } = useTema()

const warnaTeks = computed(() => (gelap.value ? '#94a3b8' : '#64748b'))
const warnaGaris = computed(() => (gelap.value ? '#1e293b' : '#e2e8f0'))

/** Semester berjalan dikecualikan: kelulusannya belum final. */
const semesterTuntas = rekapSemester.filter((r) => !r.aktif)

const totalSemua = rekapSemester.reduce((a, r) => a + r.total, 0)
const totalLulus = rekapSemester.reduce((a, r) => a + r.lulus, 0)
const persenTotal = computed(() => {
  const tuntas = semesterTuntas.reduce((a, r) => a + r.total, 0)
  const lulus = semesterTuntas.reduce((a, r) => a + r.lulus, 0)
  return ((lulus / tuntas) * 100).toFixed(1)
})

const label = semesterTuntas.map((r) => r.label.replace('20', ''))

const dataKelulusan = computed(() => ({
  labels: label,
  datasets: [
    {
      label: 'Kelulusan (%)',
      data: semesterTuntas.map((r) => r.persenLulus),
      borderColor: '#4f46e5',
      backgroundColor: 'rgba(79,70,229,.12)',
      fill: true,
      tension: .35,
      pointRadius: 4,
      pointBackgroundColor: '#4f46e5',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
    },
  ],
}))

const opsiKelulusan = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { ticks: { color: warnaTeks.value, font: { size: 11 } }, grid: { display: false } },
    y: {
      min: 75,
      max: 100,
      ticks: { color: warnaTeks.value, font: { size: 11 }, callback: (v) => v + '%' },
      grid: { color: warnaGaris.value },
      border: { display: false },
    },
  },
}))

const dataNilai = computed(() => ({
  labels: label,
  datasets: [
    {
      label: 'Rerata nilai',
      data: semesterTuntas.map((r) => r.nilaiRerata),
      backgroundColor: '#0ea5e9',
      borderRadius: 5,
      maxBarThickness: 42,
    },
  ],
}))

const opsiNilai = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { ticks: { color: warnaTeks.value, font: { size: 11 } }, grid: { display: false } },
    y: {
      min: 80,
      max: 95,
      ticks: { color: warnaTeks.value, font: { size: 11 } },
      grid: { color: warnaGaris.value },
      border: { display: false },
    },
  },
}))
</script>

<style scoped>
.rekap {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.baris-grafik {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.panel-isi {
  padding: 1.25rem;
}

.grafik {
  height: 272px;
}

.panel-judul-dalam h3 {
  font-size: .9375rem;
  font-weight: 600;
}

.panel-judul-dalam p {
  font-size: .75rem;
  color: var(--simta-teks-lembut);
  margin-top: 2px;
}

.sel-semester {
  display: flex;
  align-items: center;
  gap: .5rem;
}

.sel-semester strong {
  font-weight: 600;
}

.tebal {
  font-weight: 700;
}

.merah {
  color: #dc2626;
  font-weight: 600;
}

html.app-dark .merah {
  color: #fca5a5;
}

.lembut {
  color: var(--simta-teks-lembut);
  font-size: .75rem;
}

.kuota {
  display: flex;
  align-items: center;
  gap: .625rem;
}

.kuota> :deep(.p-progressbar) {
  flex: 1;
  min-width: 64px;
}

.kuota-teks {
  font-size: .75rem;
  font-weight: 600;
  color: var(--simta-teks-lembut);
  width: 42px;
  text-align: right;
}

.kaki {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  font-size: .8125rem;
  flex-wrap: wrap;
}

.kaki-angka {
  display: flex;
  gap: 1.5rem;
  color: var(--simta-teks-lembut);
}

.kaki-angka strong {
  color: var(--simta-teks);
  font-size: .9375rem;
}

@media (max-width: 1100px) {
  .baris-grafik {
    grid-template-columns: 1fr;
  }
}
</style>

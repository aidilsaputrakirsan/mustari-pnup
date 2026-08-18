<template>
  <div class="dasbor">
    <!-- ============ KPI ============ -->
    <section class="baris-kpi">
      <KartuKpi
        label="TA berjalan"
        :nilai="ringkasan.taAktif"
        ikon="pi pi-book"
        nada="primer"
        :delta="deltaAktif"
        satuan-delta=" judul"
        :keterangan="'dibanding ' + semesterSebelumnya.label"
      />
      <KartuKpi
        label="Perlu tindakan"
        :nilai="ringkasan.perluTindakan"
        ikon="pi pi-exclamation-circle"
        nada="bahaya"
        keterangan="judul menunggu verifikasi koordinator"
      />
      <KartuKpi
        label="Progres rata-rata"
        :nilai="ringkasan.progresRerata + '%'"
        ikon="pi pi-chart-line"
        nada="ingat"
        keterangan="seluruh TA semester berjalan"
      />
      <KartuKpi
        label="Lulus sepanjang arsip"
        :nilai="ringkasan.lulusSepanjangMasa"
        ikon="pi pi-verified"
        nada="sukses"
        :keterangan="'dari ' + ringkasan.totalArsip + ' judul terarsip'"
      />
    </section>

    <!-- ============ GRAFIK ============ -->
    <section class="baris-grafik">
      <div class="panel">
        <div class="panel-judul">
          <div>
            <h3>Tren penyelesaian per semester</h3>
            <p>Jumlah judul terdaftar dibanding yang dinyatakan lulus</p>
          </div>
          <Tag :value="semesterAktif.label" severity="secondary" />
        </div>
        <div class="panel-isi">
          <Chart type="bar" :data="dataTren" :options="opsiTren" class="grafik-tinggi" />
        </div>
      </div>

      <div class="panel">
        <div class="panel-judul">
          <div>
            <h3>Sebaran bidang</h3>
            <p>Seluruh arsip</p>
          </div>
        </div>
        <div class="panel-isi">
          <Chart type="doughnut" :data="dataBidang" :options="opsiBidang" class="grafik-tinggi" />
        </div>
      </div>
    </section>

    <!-- ============ TAHAPAN + SEMINAR ============ -->
    <section class="baris-bawah">
      <div class="panel">
        <div class="panel-judul">
          <div>
            <h3>Tahapan TA semester berjalan</h3>
            <p>{{ ringkasan.taAktif }} judul aktif</p>
          </div>
          <Button label="Lihat arsip" icon="pi pi-arrow-right" icon-pos="right" text size="small"
            @click="$router.push('/tugas-akhir')" />
        </div>
        <div class="panel-isi tahapan">
          <div v-for="t in sebaranStatusAktif" :key="t.status" class="tahap">
            <div class="tahap-atas">
              <span class="tahap-nama">{{ t.status }}</span>
              <span class="tahap-angka angka-tabular">{{ t.jumlah }}</span>
            </div>
            <ProgressBar :value="persen(t.jumlah)" :show-value="false" style="height: 7px" />
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-judul">
          <div>
            <h3>Agenda terdekat</h3>
            <p>Seminar & sidang yang belum terlaksana</p>
          </div>
          <Button label="Semua jadwal" icon="pi pi-arrow-right" icon-pos="right" text size="small"
            @click="$router.push('/seminar')" />
        </div>
        <DataTable :value="agendaTerdekat" size="small" :rows="6" scrollable scroll-height="292px">
          <Column field="tanggal" header="Tanggal" style="width: 108px">
            <template #body="{ data }">
              <span class="angka-tabular">{{ tanggalPendek(data.tanggal) }}</span>
            </template>
          </Column>
          <Column field="namaMahasiswa" header="Mahasiswa">
            <template #body="{ data }">
              <div class="sel-mhs">
                <strong>{{ data.namaMahasiswa }}</strong>
                <small class="angka-tabular">{{ data.nim }}</small>
              </div>
            </template>
          </Column>
          <Column field="jenis" header="Agenda" style="width: 168px">
            <template #body="{ data }">
              <Tag :value="data.jenis" :severity="data.jenis === 'Sidang Akhir' ? 'contrast' : 'info'" />
            </template>
          </Column>
          <Column field="ruangan" header="Ruang" style="width: 140px" />
        </DataTable>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from 'primevue/button'
import Chart from 'primevue/chart'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import ProgressBar from 'primevue/progressbar'
import Tag from 'primevue/tag'

import KartuKpi from '../components/KartuKpi.vue'
import { useTema } from '../composables/useTema.js'
import {
  ringkasan,
  rekapSemester,
  sebaranBidang,
  sebaranStatusAktif,
  daftarSeminar,
  semesterAktif,
} from '../data/seed.js'

const { gelap } = useTema()

const warnaTeks = computed(() => (gelap.value ? '#94a3b8' : '#64748b'))
const warnaGaris = computed(() => (gelap.value ? '#1e293b' : '#e2e8f0'))

const semesterSebelumnya = rekapSemester[rekapSemester.length - 2]
const semesterKini = rekapSemester[rekapSemester.length - 1]
const deltaAktif = semesterKini.total - semesterSebelumnya.total

const maksTahap = Math.max(...sebaranStatusAktif.map((t) => t.jumlah))
const persen = (n) => Math.round((n / maksTahap) * 100)

/** Agenda yang belum terlaksana, diurutkan dari yang paling dekat. */
const agendaTerdekat = computed(() =>
  daftarSeminar
    .filter((s) => s.status === 'Terjadwal' || s.status === 'Menunggu Konfirmasi')
    .sort((a, b) => a.tanggal.localeCompare(b.tanggal))
)

function tanggalPendek(iso) {
  const [tahun, bulan, hari] = iso.split('-')
  const namaBulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
  return hari + ' ' + namaBulan[Number(bulan) - 1] + ' ' + tahun.slice(2)
}

/* ============ GRAFIK ============ */
const dataTren = computed(() => ({
  labels: rekapSemester.map((r) => r.label.replace('20', '').replace('/', '/')),
  datasets: [
    {
      label: 'Terdaftar',
      data: rekapSemester.map((r) => r.total),
      backgroundColor: gelap.value ? 'rgba(99,102,241,.35)' : 'rgba(99,102,241,.25)',
      borderColor: '#6366f1',
      borderWidth: 1,
      borderRadius: 5,
    },
    {
      label: 'Lulus',
      data: rekapSemester.map((r) => r.lulus),
      backgroundColor: '#4f46e5',
      borderRadius: 5,
    },
  ],
}))

const opsiTren = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: warnaTeks.value, usePointStyle: true, pointStyle: 'circle', boxWidth: 7, padding: 16 },
    },
  },
  scales: {
    x: { ticks: { color: warnaTeks.value, font: { size: 11 } }, grid: { display: false } },
    y: {
      beginAtZero: true,
      ticks: { color: warnaTeks.value, font: { size: 11 }, precision: 0 },
      grid: { color: warnaGaris.value },
      border: { display: false },
    },
  },
}))

const dataBidang = computed(() => ({
  labels: sebaranBidang.map((b) => b.bidang),
  datasets: [
    {
      data: sebaranBidang.map((b) => b.jumlah),
      backgroundColor: ['#4f46e5', '#0ea5e9', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'],
      borderWidth: 0,
      hoverOffset: 6,
    },
  ],
}))

const opsiBidang = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '62%',
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: warnaTeks.value,
        usePointStyle: true,
        pointStyle: 'circle',
        boxWidth: 7,
        padding: 10,
        font: { size: 11 },
      },
    },
  },
}))
</script>

<style scoped>
.dasbor {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.baris-kpi {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.baris-grafik {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.25rem;
}

.baris-bawah {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 1.25rem;
}

.panel-isi {
  padding: 1.25rem;
}

.grafik-tinggi {
  height: 280px;
}

.tahapan {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tahap-atas {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: .375rem;
}

.tahap-nama {
  font-size: .8125rem;
  font-weight: 500;
}

.tahap-angka {
  font-size: .875rem;
  font-weight: 700;
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

@media (max-width: 1280px) {
  .baris-kpi {
    grid-template-columns: repeat(2, 1fr);
  }

  .baris-grafik,
  .baris-bawah {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .baris-kpi {
    grid-template-columns: 1fr;
  }
}
</style>

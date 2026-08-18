<template>
  <div class="dosen">
    <Message v-if="kelebihanBeban.length" severity="warn" class="peringatan">
      <strong>{{ kelebihanBeban.length }} dosen melampaui kuota bimbingan</strong>
      pada {{ semesterAktif.label }} —
      {{ kelebihanBeban.map((d) => ringkasNama(d.nama)).join(', ') }}.
      Distribusi perlu ditinjau sebelum penetapan pembimbing berikutnya.
    </Message>

    <div class="panel">
      <DataTable
        :value="bebanDosen"
        data-key="id"
        sort-field="totalAktif"
        :sort-order="-1"
        removable-sort
        size="small"
        striped-rows
      >
        <template #header>
          <div class="panel-judul-dalam">
            <div>
              <h3>Distribusi beban pembimbing</h3>
              <p>Bimbingan aktif pada {{ semesterAktif.label }} dibanding kuota masing-masing dosen</p>
            </div>
          </div>
        </template>

        <Column field="nama" header="Dosen" sortable style="min-width: 232px">
          <template #body="{ data }">
            <div class="sel-dosen">
              <Avatar :label="inisial(data.nama)" shape="circle" class="avatar-dosen" />
              <div>
                <strong>{{ data.nama }}</strong>
                <small class="angka-tabular">NIDN {{ data.nidn }}</small>
              </div>
            </div>
          </template>
        </Column>

        <Column field="jabatan" header="Jabatan" sortable style="min-width: 124px">
          <template #body="{ data }">
            <span class="lembut">{{ data.jabatan }}</span>
          </template>
        </Column>

        <Column field="bidang" header="Bidang keahlian" sortable style="min-width: 158px">
          <template #body="{ data }">
            <span class="lembut">{{ data.bidang }}</span>
          </template>
        </Column>

        <Column field="bimbinganUtama" header="Utama" sortable style="width: 76px">
          <template #body="{ data }">
            <span class="angka-tabular tebal">{{ data.bimbinganUtama }}</span>
          </template>
        </Column>

        <Column field="bimbinganPendamping" header="Pendamping" sortable style="width: 102px">
          <template #body="{ data }">
            <span class="angka-tabular tebal">{{ data.bimbinganPendamping }}</span>
          </template>
        </Column>

        <Column field="persenKuota" header="Pemakaian kuota" sortable style="min-width: 168px">
          <template #body="{ data }">
            <div class="kuota">
              <ProgressBar
                :value="Math.min(data.persenKuota, 100)"
                :show-value="false"
                :class="{ 'bar-lebih': data.persenKuota > 100, 'bar-penuh': data.persenKuota === 100 }"
                style="height: 7px"
              />
              <span class="angka-tabular kuota-teks" :class="{ lebih: data.persenKuota > 100 }">
                {{ data.totalAktif }}/{{ data.kuota }}
              </span>
            </div>
          </template>
        </Column>

        <Column field="diluluskan" header="Diluluskan" sortable style="width: 102px">
          <template #body="{ data }">
            <span class="angka-tabular">{{ data.diluluskan }}</span>
            <small class="lembut"> / {{ data.totalSepanjangMasa }}</small>
          </template>
        </Column>

        <Column field="rerataNilai" header="Rerata nilai" sortable style="width: 106px">
          <template #body="{ data }">
            <Tag
              v-if="data.rerataNilai"
              :value="String(data.rerataNilai)"
              :severity="data.rerataNilai >= 88 ? 'success' : data.rerataNilai >= 84 ? 'info' : 'warn'"
            />
            <span v-else class="lembut">—</span>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Avatar from 'primevue/avatar'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Message from 'primevue/message'
import ProgressBar from 'primevue/progressbar'
import Tag from 'primevue/tag'

import { bebanDosen, semesterAktif } from '../data/seed.js'

const kelebihanBeban = computed(() => bebanDosen.filter((d) => d.persenKuota > 100))

function ringkasNama(nama = '') {
  return nama.split(',')[0]
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
</script>

<style scoped>
.dosen {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.peringatan {
  font-size: .8125rem;
  line-height: 1.6;
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

.sel-dosen {
  display: flex;
  align-items: center;
  gap: .625rem;
}

.sel-dosen strong {
  display: block;
  font-size: .8125rem;
  font-weight: 600;
}

.sel-dosen small {
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

.lembut {
  color: var(--simta-teks-lembut);
  font-size: .75rem;
}

.tebal {
  font-weight: 700;
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
  width: 40px;
  text-align: right;
}

.kuota-teks.lebih {
  color: #dc2626;
}

html.app-dark .kuota-teks.lebih {
  color: #fca5a5;
}

.bar-lebih :deep(.p-progressbar-value) {
  background: #dc2626;
}

.bar-penuh :deep(.p-progressbar-value) {
  background: #f59e0b;
}
</style>

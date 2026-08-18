<template>
  <article class="kpi panel">
    <div class="kpi-atas">
      <span class="kpi-label">{{ label }}</span>
      <span class="kpi-ikon" :class="'nada-' + nada">
        <i :class="ikon"></i>
      </span>
    </div>

    <strong class="kpi-nilai angka-tabular">{{ nilaiTampil }}</strong>

    <p v-if="keterangan" class="kpi-ket">
      <span v-if="delta !== null" class="kpi-delta" :class="delta >= 0 ? 'naik' : 'turun'">
        <i :class="delta >= 0 ? 'pi pi-arrow-up-right' : 'pi pi-arrow-down-right'"></i>
        {{ Math.abs(delta) }}{{ satuanDelta }}
      </span>
      {{ keterangan }}
    </p>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  nilai: { type: [Number, String], required: true },
  ikon: { type: String, default: 'pi pi-chart-line' },
  nada: { type: String, default: 'primer' }, // primer | sukses | ingat | bahaya
  keterangan: { type: String, default: '' },
  delta: { type: Number, default: null },
  satuanDelta: { type: String, default: '' },
})

const nilaiTampil = computed(() =>
  typeof props.nilai === 'number' ? props.nilai.toLocaleString('id-ID') : props.nilai
)
</script>

<style scoped>
.kpi {
  padding: 1.125rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: .5rem;
  transition: box-shadow .18s ease, transform .18s ease;
}

.kpi:hover {
  box-shadow: var(--simta-bayang-naik);
  transform: translateY(-1px);
}

.kpi-atas {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: .75rem;
}

.kpi-label {
  font-size: .75rem;
  font-weight: 600;
  color: var(--simta-teks-lembut);
  text-transform: uppercase;
  letter-spacing: .04em;
}

.kpi-ikon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  display: grid;
  place-items: center;
  font-size: .875rem;
  flex-shrink: 0;
}

.nada-primer {
  background: var(--p-primary-50);
  color: var(--p-primary-700);
}

.nada-sukses {
  background: #dcfce7;
  color: #15803d;
}

.nada-ingat {
  background: #fef3c7;
  color: #b45309;
}

.nada-bahaya {
  background: #fee2e2;
  color: #b91c1c;
}

html.app-dark .nada-primer {
  background: rgba(99, 102, 241, .16);
  color: #a5b4fc;
}

html.app-dark .nada-sukses {
  background: rgba(34, 197, 94, .16);
  color: #86efac;
}

html.app-dark .nada-ingat {
  background: rgba(245, 158, 11, .16);
  color: #fcd34d;
}

html.app-dark .nada-bahaya {
  background: rgba(239, 68, 68, .16);
  color: #fca5a5;
}

.kpi-nilai {
  font-size: 1.875rem;
  font-weight: 700;
  letter-spacing: -.03em;
  line-height: 1.1;
}

.kpi-ket {
  font-size: .75rem;
  color: var(--simta-teks-lembut);
  display: flex;
  align-items: center;
  gap: .375rem;
  flex-wrap: wrap;
}

.kpi-delta {
  display: inline-flex;
  align-items: center;
  gap: .1875rem;
  font-weight: 700;
  padding: .0625rem .375rem;
  border-radius: 999px;
  font-size: .6875rem;
}

.kpi-delta.naik {
  background: #dcfce7;
  color: #15803d;
}

.kpi-delta.turun {
  background: #fee2e2;
  color: #b91c1c;
}

html.app-dark .kpi-delta.naik {
  background: rgba(34, 197, 94, .16);
  color: #86efac;
}

html.app-dark .kpi-delta.turun {
  background: rgba(239, 68, 68, .16);
  color: #fca5a5;
}

.kpi-delta i {
  font-size: .625rem;
}
</style>

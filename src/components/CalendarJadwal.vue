<template>
  <!-- Komponen Kalender Jadwal Seminar -->
  <div class="calendar-container">
    <!-- Header Kalender -->
    <div class="calendar-header">
      <button class="cal-nav-btn" @click="prevMonth">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
      </button>
      <h3 class="cal-month-title">{{ namaBlnThn }}</h3>
      <button class="cal-nav-btn" @click="nextMonth">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>
    </div>

    <!-- Grid Hari -->
    <div class="calendar-days-header">
      <span v-for="day in namaHari" :key="day" class="day-label">{{ day }}</span>
    </div>

    <!-- Grid Tanggal -->
    <div class="calendar-grid">
      <div
        v-for="(cell, idx) in calendarCells"
        :key="idx"
        class="calendar-cell"
        :class="{
          'other-month': !cell.currentMonth,
          'has-event': cell.events.length > 0,
          'today': cell.isToday,
        }"
      >
        <span class="cell-date">{{ cell.day }}</span>
        <div v-for="event in cell.events.slice(0, 2)" :key="event.id" class="calendar-event" :class="eventClass(event)">
          <span class="event-time">{{ event.waktu }}</span>
          <span class="event-type">{{ event.jenis === 'Seminar Proposal' ? 'SP' : 'SA' }}</span>
        </div>
        <span v-if="cell.events.length > 2" class="more-events">+{{ cell.events.length - 2 }} lagi</span>
      </div>
    </div>

    <!-- Legenda -->
    <div class="calendar-legend">
      <div class="legend-item">
        <span class="legend-dot sempro"></span>
        <span>Seminar Proposal</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot sidang"></span>
        <span>Sidang Akhir</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot today-dot"></span>
        <span>Hari Ini</span>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * CalendarJadwal.vue
 * Komponen kalender kustom untuk menampilkan jadwal seminar.
 * Komponen ini dimaksudkan sebagai komponen "berat" kedua.
 */
import { ref, computed } from 'vue'

const props = defineProps({
  jadwalList: {
    type: Array,
    default: () => [],
  },
})

const namaHari = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']
const namaBulan = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember',
]

// State bulan/tahun yang ditampilkan
const currentMonth = ref(new Date().getMonth()) // 0-11
const currentYear = ref(new Date().getFullYear())

const namaBlnThn = computed(() =>
  `${namaBulan[currentMonth.value]} ${currentYear.value}`
)

function prevMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

// Generate cell kalender
const calendarCells = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const daysInPrevMonth = new Date(year, month, 0).getDate()
  const today = new Date()

  const cells = []

  // Hari dari bulan sebelumnya
  for (let i = firstDay - 1; i >= 0; i--) {
    cells.push({
      day: daysInPrevMonth - i,
      currentMonth: false,
      isToday: false,
      events: [],
    })
  }

  // Hari bulan ini
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`
    const isToday = today.getFullYear() === year && today.getMonth() === month && today.getDate() === d
    const events = props.jadwalList.filter(j => j.tanggal === dateStr)
    cells.push({
      day: d,
      currentMonth: true,
      isToday,
      events,
    })
  }

  // Hari bulan berikutnya (isi sampai 42 cell = 6 baris)
  const remaining = 42 - cells.length
  for (let i = 1; i <= remaining; i++) {
    cells.push({
      day: i,
      currentMonth: false,
      isToday: false,
      events: [],
    })
  }

  return cells
})

function eventClass(event) {
  return event.jenis === 'Seminar Proposal' ? 'event-sempro' : 'event-sidang'
}
</script>

<style scoped>
.calendar-container {
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.5rem;
}
.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}
.cal-month-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #f1f5f9;
}
.cal-nav-btn {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 6px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s;
}
.cal-nav-btn:hover {
  border-color: #3b82f6;
  color: #60a5fa;
}
.calendar-days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  margin-bottom: 4px;
}
.day-label {
  text-align: center;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  padding: 0.5rem 0;
  text-transform: uppercase;
}
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}
.calendar-cell {
  min-height: 80px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid #1e293b;
  border-radius: 8px;
  padding: 0.375rem;
  display: flex;
  flex-direction: column;
  transition: border-color 0.2s;
}
.calendar-cell:hover {
  border-color: #334155;
}
.calendar-cell.other-month {
  opacity: 0.3;
}
.calendar-cell.today {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}
.calendar-cell.has-event {
  border-color: #475569;
}
.cell-date {
  font-size: 0.75rem;
  font-weight: 500;
  color: #94a3b8;
  margin-bottom: 4px;
}
.today .cell-date {
  color: #60a5fa;
  font-weight: 700;
}
.calendar-event {
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.625rem;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  gap: 3px;
}
.event-sempro {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}
.event-sidang {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}
.event-time {
  font-weight: 600;
}
.more-events {
  font-size: 0.625rem;
  color: #64748b;
}
.calendar-legend {
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #1e293b;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #94a3b8;
}
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}
.legend-dot.sempro {
  background: rgba(59, 130, 246, 0.8);
}
.legend-dot.sidang {
  background: rgba(139, 92, 246, 0.8);
}
.legend-dot.today-dot {
  background: transparent;
  border: 2px solid #3b82f6;
}
</style>

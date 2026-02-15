<template>
  <!-- Komponen Berat: Chart Statistik menggunakan Chart.js -->
  <div class="chart-container">
    <div class="chart-grid">
      <!-- Doughnut Chart: Status Judul -->
      <div class="chart-card">
        <h3 class="chart-title">
          <span class="chart-icon">📊</span>
          Distribusi Status Judul
        </h3>
        <div class="chart-wrapper">
          <Doughnut :data="doughnutData" :options="doughnutOptions" />
        </div>
      </div>

      <!-- Bar Chart: Bimbingan per Bulan -->
      <div class="chart-card">
        <h3 class="chart-title">
          <span class="chart-icon">📈</span>
          Aktivitas Bimbingan per Bulan
        </h3>
        <div class="chart-wrapper">
          <Bar :data="barData" :options="barOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * ChartStatistik.vue
 * Komponen "berat" yang mengimport Chart.js secara penuh.
 * Digunakan untuk membandingkan eager vs lazy loading.
 */
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'

// Registrasi semua komponen Chart.js yang dibutuhkan
ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend, Filler)

// Data Doughnut Chart
const doughnutData = {
  labels: ['Disetujui', 'Sedang Berjalan', 'Revisi', 'Diajukan', 'Ditolak', 'Selesai'],
  datasets: [
    {
      data: [12, 15, 8, 6, 2, 7],
      backgroundColor: [
        'rgba(34, 197, 94, 0.8)',   // Hijau
        'rgba(59, 130, 246, 0.8)',   // Biru
        'rgba(234, 179, 8, 0.8)',    // Kuning
        'rgba(139, 92, 246, 0.8)',   // Ungu
        'rgba(239, 68, 68, 0.8)',    // Merah
        'rgba(6, 182, 212, 0.8)',    // Cyan
      ],
      borderColor: '#0f172a',
      borderWidth: 3,
      hoverOffset: 8,
    },
  ],
}

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#94a3b8',
        padding: 16,
        usePointStyle: true,
        pointStyleWidth: 10,
        font: { size: 11, family: 'Inter' },
      },
    },
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#f1f5f9',
      bodyColor: '#94a3b8',
      borderColor: '#334155',
      borderWidth: 1,
      cornerRadius: 8,
      padding: 12,
    },
  },
}

// Data Bar Chart
const barData = {
  labels: ['Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
  datasets: [
    {
      label: 'Bimbingan',
      data: [4, 6, 8, 5, 7, 3],
      backgroundColor: 'rgba(59, 130, 246, 0.6)',
      borderColor: 'rgba(59, 130, 246, 1)',
      borderWidth: 1,
      borderRadius: 6,
      borderSkipped: false,
    },
    {
      label: 'Revisi',
      data: [2, 3, 4, 6, 3, 1],
      backgroundColor: 'rgba(139, 92, 246, 0.6)',
      borderColor: 'rgba(139, 92, 246, 1)',
      borderWidth: 1,
      borderRadius: 6,
      borderSkipped: false,
    },
  ],
}

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      align: 'end',
      labels: {
        color: '#94a3b8',
        usePointStyle: true,
        pointStyleWidth: 10,
        font: { size: 11, family: 'Inter' },
      },
    },
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#f1f5f9',
      bodyColor: '#94a3b8',
      borderColor: '#334155',
      borderWidth: 1,
      cornerRadius: 8,
      padding: 12,
    },
  },
  scales: {
    x: {
      grid: { color: 'rgba(51, 65, 85, 0.3)' },
      ticks: { color: '#64748b', font: { size: 11 } },
    },
    y: {
      grid: { color: 'rgba(51, 65, 85, 0.3)' },
      ticks: { color: '#64748b', font: { size: 11 } },
      beginAtZero: true,
    },
  },
}
</script>

<style scoped>
.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}
.chart-card {
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.5rem;
}
.chart-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.chart-icon {
  font-size: 1.125rem;
}
.chart-wrapper {
  height: 280px;
  position: relative;
}
</style>

# -*- coding: utf-8 -*-
"""Membangkitkan tiga gambar pendukung pembahasan prefetching pada BAB III.

1. chart_prefetch_network.png    - timeline permintaan berkas (DATA nyata dari
                                   prefetch_network_log.json, tanpa interaksi klik)
2. diagram_strategi_pemuatan.png - perbandingan konseptual eager, lazy, dan
                                   lazy + prefetching (ilustrasi mekanisme)
3. diagram_arsitektur_chunk.png  - peta chunk hasil build beserta ukuran aslinya

Jalankan:  python buat_visual_prefetch.py
"""
import json
import os
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'laporan_tesis', 'data_pengukuran')
IMG = os.path.join(BASE, 'laporan_tesis', 'chapters', 'images')
os.makedirs(IMG, exist_ok=True)

# Palet konsisten untuk ketiga gambar
C_AWAL = '#E8743B'      # dimuat di awal
C_PREF = '#19A979'      # di-prefetch saat idle
C_KLIK = '#BBBBBB'      # menunggu diklik
C_GRID = '#DDDDDD'
C_TEKS = '#333333'

plt.rcParams.update({
    'font.size': 11,
    'axes.edgecolor': '#999999',
    'text.color': C_TEKS,
    'axes.labelcolor': C_TEKS,
    'xtick.color': C_TEKS,
    'ytick.color': C_TEKS,
})


# =====================================================================
# 1. TIMELINE PERMINTAAN BERKAS  (data nyata)
# =====================================================================
def gambar_network():
    path = os.path.join(DATA, 'prefetch_network_log.json')
    runs = json.load(open(path, encoding='utf-8'))

    # rata-ratakan waktu tiap berkas across runs
    agg = {}
    for run in runs:
        for item in run:
            agg.setdefault(item['file'], []).append(item['waktu_ms'])
    rata = {k: sum(v) / len(v) for k, v in agg.items()}

    def rapikan(nama):
        # buang hash build 8 karakter di akhir: vendor-chart-BMD3DpH8.js -> vendor-chart.js
        return re.sub(r'-[A-Za-z0-9_-]{8}\.js$', '.js', nama)

    PREFETCH = {'DaftarJudulView', 'DetailBimbinganView'}
    baris = sorted(rata.items(), key=lambda kv: kv[1])

    label, waktu, warna = [], [], []
    for f, t in baris:
        inti = f.split('-')[0]
        label.append(rapikan(f))
        waktu.append(t)
        warna.append(C_PREF if inti in PREFETCH else C_AWAL)

    # dua chunk yang TIDAK pernah diminta
    for nama in ['JadwalSeminarView.js', 'PengaturanView.js']:
        label.append(nama)
        waktu.append(None)
        warna.append(C_KLIK)

    fig, ax = plt.subplots(figsize=(11, 6))
    y = range(len(label))

    for i, (t, c) in enumerate(zip(waktu, warna)):
        if t is None:
            ax.barh(i, 480, left=0, height=0.55, color=c, alpha=0.18,
                    hatch='//', edgecolor=c)
            ax.text(240, i, 'tidak diunduh — menunggu diklik',
                    va='center', ha='center', fontsize=9.5, color='#777777', style='italic')
        else:
            ax.barh(i, 26, left=t, height=0.55, color=c, edgecolor='white')
            ax.text(t + 34, i, f'{t:.0f} ms', va='center', fontsize=10, color=C_TEKS)

    ax.set_yticks(list(y))
    ax.set_yticklabels(label, fontsize=10.5)
    ax.invert_yaxis()
    ax.set_xlabel('Waktu sejak permintaan berkas pertama (ms)')
    ax.set_xlim(-15, 520)
    ax.set_title('Rekaman Permintaan Berkas JavaScript pada Versi Optimized\n'
                 '(rata-rata 5 repetisi, tanpa satu pun interaksi klik dari pengguna)',
                 fontsize=12.5, pad=14)
    ax.grid(axis='x', color=C_GRID, linestyle='--', linewidth=0.7)
    ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)

    tanda = [
        Rectangle((0, 0), 1, 1, color=C_AWAL, label='Dimuat saat pemuatan awal'),
        Rectangle((0, 0), 1, 1, color=C_PREF, label='Di-prefetch otomatis saat main thread senggang'),
        Rectangle((0, 0), 1, 1, color=C_KLIK, alpha=0.3, hatch='//',
                  label='Belum dibutuhkan, menunggu navigasi pengguna'),
    ]
    ax.legend(handles=tanda, loc='upper right', frameon=True, fontsize=9.5,
              framealpha=0.95, borderpad=0.7)

    fig.tight_layout()
    keluar = os.path.join(IMG, 'chart_prefetch_network.png')
    fig.savefig(keluar, dpi=200)
    plt.close(fig)
    print('[1] chart_prefetch_network.png  (data nyata,', len(runs), 'repetisi)')


# =====================================================================
# 2. DIAGRAM KONSEPTUAL TIGA STRATEGI
# =====================================================================
def gambar_strategi():
    fig, ax = plt.subplots(figsize=(12.5, 7.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 11.9)
    ax.axis('off')

    def kotak(x, y, w, teks, warna, fs=9.5, tw='white'):
        ax.add_patch(FancyBboxPatch((x, y - 0.48), w, 0.96,
                                    boxstyle='round,pad=0.14,rounding_size=0.22',
                                    facecolor=warna, edgecolor='white', linewidth=1))
        ax.text(x + w / 2, y, teks, ha='center', va='center',
                fontsize=fs, color=tw, weight='bold')

    def judul_baris(y, nomor, teks, sub):
        ax.text(0, y + 1.85, f'{nomor}  {teks}', fontsize=11.5, weight='bold', color=C_TEKS)
        ax.text(0, y + 1.34, sub, fontsize=9.3, color='#666666', style='italic')

    # ---- sumbu waktu ----
    ax.annotate('', xy=(99, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='#999999', lw=1.2))
    ax.text(99, -0.42, 'waktu', ha='right', fontsize=10, color='#666666', style='italic')
    for x, t in [(8, 'buka aplikasi'), (54, 'klik menu A'), (79, 'klik menu B')]:
        ax.plot([x, x], [-0.16, 0.16], color='#999999', lw=1.2)
        ax.text(x, -0.42, t, ha='center', fontsize=9, color='#666666')

    # ---- 1. eager ----
    y1 = 9.0
    judul_baris(y1, '1.', 'Eager loading (baseline)',
                'Semua kode digabung dan diunduh sekaligus di awal')
    kotak(8, y1, 32, 'satu bundle besar - semua halaman sekaligus', '#B0392B')
    kotak(54, y1, 9, 'instan', '#7FB069', tw='#1c3d0f')
    kotak(79, y1, 9, 'instan', '#7FB069', tw='#1c3d0f')

    # ---- 2. lazy murni ----
    y2 = 5.2
    judul_baris(y2, '2.', 'Lazy loading murni',
                'Bundle awal kecil, tetapi tiap perpindahan halaman memicu unduhan baru')
    kotak(8, y2, 12, 'bundle awal kecil', C_AWAL)
    kotak(54, y2, 13, 'unduh chunk A', '#C8553D', fs=9)
    kotak(79, y2, 13, 'unduh chunk B', '#C8553D', fs=9)
    for x in (54, 79):
        ax.annotate('', xy=(x + 13, y2 + 0.78), xytext=(x, y2 + 0.78),
                    arrowprops=dict(arrowstyle='<->', color='#B0392B', lw=1.4))
        ax.text(x + 6.5, y2 + 0.96, 'JEDA', ha='center', va='bottom',
                fontsize=9.5, weight='bold', color='#B0392B')

    # ---- 3. lazy + prefetch ----
    y3 = 1.4
    judul_baris(y3, '3.', 'Lazy loading + prefetching (yang diterapkan)',
                'Bundle awal tetap kecil, chunk berikutnya diunduh lebih dulu saat peramban senggang')
    kotak(8, y3, 12, 'bundle awal kecil', C_AWAL)
    kotak(22, y3, 25, 'prefetch chunk A dan B saat idle', C_PREF, fs=9)
    kotak(54, y3, 9, 'instan', '#7FB069', tw='#1c3d0f')
    kotak(79, y3, 9, 'instan', '#7FB069', tw='#1c3d0f')
    ax.annotate('', xy=(54, y3 + 0.78), xytext=(47, y3 + 0.78),
                arrowprops=dict(arrowstyle='->', color=C_PREF, lw=1.5))
    ax.text(50.5, y3 + 0.96, 'sudah siap di cache', ha='center', va='bottom',
            fontsize=9, color=C_PREF, weight='bold')

    ax.set_title('Perbandingan Konseptual Tiga Strategi Pemuatan Modul',
                 fontsize=13, weight='bold', pad=18)
    ax.text(50, 11.5, 'Ilustrasi mekanisme berdasarkan kode, bukan hasil pengukuran waktu',
            ha='center', fontsize=9.5, color='#777777', style='italic')

    fig.tight_layout()
    keluar = os.path.join(IMG, 'diagram_strategi_pemuatan.png')
    fig.savefig(keluar, dpi=200)
    plt.close(fig)
    print('[2] diagram_strategi_pemuatan.png  (ilustrasi konseptual)')


# =====================================================================
# 3. PETA ARSITEKTUR CHUNK  (ukuran nyata dari hasil build)
# =====================================================================
def gambar_arsitektur():
    # nama, ukuran mentah KB, ukuran gzip KB
    AWAL = [
        ('index.optimized.js', 11.67, 4.41),
        ('vendor-vue.js', 103.40, 39.89),
        ('vendor-chart.js', 199.59, 68.18),
        ('DashboardView.js', 7.99, 2.63),
        ('supabase.js', 17.19, 4.97),
    ]
    PREF = [
        ('DaftarJudulView.js', 5.59, 2.40),
        ('DetailBimbinganView.js', 7.75, 3.03),
    ]
    KLIK = [
        ('JadwalSeminarView.js', 6.34, 2.52),
        ('PengaturanView.js', 5.05, 1.95),
    ]

    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(1.6, 10)
    ax.axis('off')

    def kelompok(x, judul, sub, isi, warna, alpha=1.0):
        bawah = 7.75 - len(isi) * 0.85 - 0.75
        ax.add_patch(FancyBboxPatch((x, bawah), 3.0, 8.8 - bawah,
                                    boxstyle='round,pad=0.1,rounding_size=0.15',
                                    facecolor='none', edgecolor=warna,
                                    linewidth=1.6, linestyle='--'))
        ax.text(x + 1.5, 8.45, judul, ha='center', fontsize=11.5,
                weight='bold', color=warna)
        ax.text(x + 1.5, 8.05, sub, ha='center', fontsize=8.8,
                color='#666666', style='italic')
        y = 7.4
        total = 0
        for nama, mentah, gz in isi:
            tinggi = 0.62
            ax.add_patch(FancyBboxPatch((x + 0.15, y - tinggi / 2), 2.7, tinggi,
                                        boxstyle='round,pad=0.05,rounding_size=0.1',
                                        facecolor=warna, edgecolor='white',
                                        alpha=alpha, linewidth=1))
            ax.text(x + 0.3, y + 0.09, nama, va='center', fontsize=8.8,
                    color='white' if alpha > 0.5 else '#555555', weight='bold')
            ax.text(x + 0.3, y - 0.16, f'{mentah:.1f} KB  →  {gz:.1f} KB (gzip)',
                    va='center', fontsize=7.8,
                    color='white' if alpha > 0.5 else '#666666')
            y -= 0.85
            total += gz
        ax.text(x + 1.5, bawah + 0.38, f'total terkompresi: {total:.1f} KB',
                ha='center', fontsize=9.5, weight='bold', color=warna)

    kelompok(0.3, 'Dimuat saat pembukaan', 'dibutuhkan halaman pertama', AWAL, C_AWAL)
    kelompok(3.5, 'Di-prefetch saat idle', 'tanpa menunggu klik pengguna', PREF, C_PREF)
    kelompok(6.7, 'Menunggu navigasi', 'baru diunduh bila diakses', KLIK, C_KLIK, alpha=0.45)

    for x in (3.32, 6.52):
        ax.annotate('', xy=(x + 0.16, 6.6), xytext=(x - 0.02, 6.6),
                    arrowprops=dict(arrowstyle='->', color='#999999', lw=1.6))

    ax.set_title('Peta Chunk Hasil Build SIMTA Versi Optimized dan Waktu Pemuatannya',
                 fontsize=13, weight='bold', pad=14)
    ax.text(5, 9.45, 'Ukuran diambil dari keluaran npm run build:optimized',
            ha='center', fontsize=9.5, color='#777777', style='italic')

    fig.tight_layout()
    keluar = os.path.join(IMG, 'diagram_arsitektur_chunk.png')
    fig.savefig(keluar, dpi=200)
    plt.close(fig)
    print('[3] diagram_arsitektur_chunk.png  (ukuran nyata dari build)')


if __name__ == '__main__':
    gambar_network()
    gambar_strategi()
    gambar_arsitektur()
    print('\nSelesai. Tiga gambar tersimpan di laporan_tesis/chapters/images/')

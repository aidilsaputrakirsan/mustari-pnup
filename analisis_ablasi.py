"""
Rekap statistik dan grafik studi ablasi (revisi penguji).
Membaca laporan_tesis/data_pengukuran/ablasi/*.json hasil ukur_ablasi.cjs,
menulis ringkasan_ablasi.json dan grafik ke laporan_tesis/chapters/images/.
"""
import json
import os
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "laporan_tesis")
DATA = os.path.join(BASE, "data_pengukuran", "ablasi")
IMG = os.path.join(BASE, "chapters", "images")

VARIAN = ["A0-kontrol", "A1-splitting", "A2-lazy", "A3-prefetch", "A4-gzip", "A5-gabungan", "R-baseline", "R-optimized"]
LABEL = {
    "A0-kontrol": "A0 Kontrol",
    "A1-splitting": "A1 Splitting",
    "A2-lazy": "A2 Lazy",
    "A3-prefetch": "A3 Lazy+Prefetch",
    "A4-gzip": "A4 Gzip",
    "A5-gabungan": "A5 Gabungan",
}
SKENARIO = ["ideal", "cpu_lambat", "jaringan_lambat"]
METRIK_PO = ["FCP_ms", "LCP_ms", "TBT_ms", "LoadTime_ms", "Navigasi_ms", "jumlah_js", "transfer_js_KB"]
METRIK_LH = ["PerformanceScore", "FCP_ms", "LCP_ms", "TTI_ms", "TBT_ms", "SpeedIndex"]


def ringkas(nilai):
    nilai = [float(v) for v in nilai if v is not None]
    if not nilai:
        return None
    return {
        "mean": round(st.mean(nilai), 1),
        "sd": round(st.stdev(nilai), 1) if len(nilai) > 1 else 0.0,
        "median": round(st.median(nilai), 1),
        "n": len(nilai),
    }


def baca(nama):
    path = os.path.join(DATA, nama)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    hasil = {"po": {}, "lh": {}}
    for v in VARIAN:
        hasil["po"][v] = {}
        for s in SKENARIO:
            runs = baca(f"po_{v}_{s}.json")
            hasil["po"][v][s] = {m: ringkas([r.get(m) for r in runs]) for m in METRIK_PO}
        runs = baca(f"lh_{v}.json")
        hasil["lh"][v] = {m: ringkas([r.get(m) for r in runs]) for m in METRIK_LH}

    with open(os.path.join(DATA, "ukuran_bundle.json"), encoding="utf-8") as f:
        hasil["ukuran"] = {k: {kk: vv for kk, vv in v.items() if kk != "berkas"} for k, v in json.load(f).items()}

    with open(os.path.join(DATA, "ringkasan_ablasi.json"), "w", encoding="utf-8") as f:
        json.dump(hasil, f, indent=2, ensure_ascii=False)

    buat_grafik(hasil)
    print(json.dumps(hasil, indent=1, ensure_ascii=False))


def grafik_batang(ax, judul, ylabel, nilai, sd, warna):
    label = [LABEL[v] for v in LABEL]
    bars = ax.bar(label, nilai, yerr=sd, capsize=3, color=warna, edgecolor="#333", linewidth=0.5)
    ax.set_title(judul, fontsize=11)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=25, labelsize=8)
    ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=8)
    ax.axhline(nilai[0], color="#999", linestyle="--", linewidth=0.8)
    ax.grid(axis="y", alpha=0.3)


def buat_grafik(h):
    warna = ["#95a5a6", "#3498db", "#e67e22", "#9b59b6", "#16a085", "#c0392b"]
    keys = list(LABEL)

    def ambil(skenario, metrik):
        nilai = [h["po"][v][skenario][metrik]["mean"] for v in keys]
        sd = [h["po"][v][skenario][metrik]["sd"] for v in keys]
        return nilai, sd

    # Gambar A: metrik muatan awal pada CPU 4x dan jaringan lambat
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))
    grafik_batang(axes[0][0], "TBT — CPU 4x", "ms", *ambil("cpu_lambat", "TBT_ms"), warna)
    grafik_batang(axes[0][1], "FCP — CPU 4x + jaringan lambat", "ms", *ambil("jaringan_lambat", "FCP_ms"), warna)
    grafik_batang(axes[1][0], "Load Time — CPU 4x + jaringan lambat", "ms", *ambil("jaringan_lambat", "LoadTime_ms"), warna)
    grafik_batang(axes[1][1], "Navigasi Dashboard → Daftar Judul — jaringan lambat", "ms", *ambil("jaringan_lambat", "Navigasi_ms"), warna)
    fig.suptitle("Studi Ablasi SIMTA: Kontribusi Tiap Teknik (rata-rata ± SD, garis putus = kontrol A0)", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "chart_ablasi_metrik.png"), dpi=200)
    plt.close(fig)

    # Gambar B: Lighthouse score & transfer JS awal
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    grafik_batang(axes[0], "Lighthouse Performance Score", "skor",
                  [h["lh"][v]["PerformanceScore"]["mean"] for v in keys],
                  [h["lh"][v]["PerformanceScore"]["sd"] for v in keys], warna)
    grafik_batang(axes[1], "Ukuran transfer JS saat muatan awal", "KB", *ambil("ideal", "transfer_js_KB"), warna)
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "chart_ablasi_lighthouse_transfer.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()

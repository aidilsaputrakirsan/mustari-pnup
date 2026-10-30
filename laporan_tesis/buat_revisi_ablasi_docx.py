"""
Membangkitkan dokumen revisi penguji: perbandingan kontribusi teknik
code splitting, lazy loading, prefetching, dan gzip (studi ablasi).

Gaya (font, heading, margin) diambil dari Revisi-Tesis-Mustari.docx agar
naskah sisipan langsung serasi. Angka hasil dibaca dari
data_pengukuran/ablasi/ringkasan_ablasi.json (keluaran analisis_ablasi.py).

Keluaran: Revisi-Penguji-Perbandingan-Teknik.docx
"""
import json
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "Revisi-Tesis-Mustari.docx")
# Mode pratinjau: ABLASI_DUMMY=1 memakai data dummy dan memberi tanda di setiap halaman
DUMMY = os.environ.get("ABLASI_DUMMY") == "1"
OUT = os.path.join(HERE, "Revisi-Penguji-Perbandingan-Teknik" + ("-PRATINJAU-DATA-DUMMY" if DUMMY else "") + ".docx")
DATA = os.path.join(HERE, "data_pengukuran", "ablasi", "ringkasan_ablasi_DUMMY.json" if DUMMY else "ringkasan_ablasi.json")
IMG = os.path.join(HERE, "chapters", "images", "dummy") if DUMMY else os.path.join(HERE, "chapters", "images")
LABEL_DUMMY = ""

VARIAN = ["A0-kontrol", "A1-splitting", "A2-lazy", "A3-prefetch", "A4-gzip", "A5-gabungan"]
NAMA = {
    "A0-kontrol": "A0 Kontrol",
    "A1-splitting": "A1 Code Splitting",
    "A2-lazy": "A2 Lazy Loading",
    "A3-prefetch": "A3 Lazy + Prefetching",
    "A4-gzip": "A4 Gzip",
    "A5-gabungan": "A5 Gabungan",
}

H = json.load(open(DATA, encoding="utf-8")) if os.path.exists(DATA) else None


# ---------------------------------------------------------------- data helpers
def po(v, s, m):
    if not H or not H["po"][v][s][m]:
        return None
    return H["po"][v][s][m]


def lh(v, m):
    if not H or not H["lh"][v][m]:
        return None
    return H["lh"][v][m]


def angka(x, d=1):
    if x is None:
        return "…"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ms(stat, d=1):
    return "…" if stat is None else f"{angka(stat['mean'], d)} ± {angka(stat['sd'], d)}"


def pct(baru, lama):
    """Perubahan relatif terhadap kontrol; negatif = lebih kecil/lebih cepat."""
    if baru is None or lama is None or lama == 0:
        return "…"
    p = (baru - lama) / lama * 100
    return ("+" if p > 0 else "") + angka(p) + "%"


def pct_po(v, s, m):
    a, b = po(v, s, m), po("A0-kontrol", s, m)
    return pct(a and a["mean"], b and b["mean"])


def pct_lh(v, m):
    a, b = lh(v, m), lh("A0-kontrol", m)
    return pct(a and a["mean"], b and b["mean"])


# ---------------------------------------------------------- document helpers
def dokumen_kosong():
    doc = Document(TEMPLATE)
    body = doc.element.body
    for el in list(body):
        if el.tag != qn("w:sectPr"):
            body.remove(el)
    return doc


def tambah_teks(p, teks):
    """Teks dengan penanda sederhana: **tebal**, _miring_, `kode`."""
    import re
    for bagian in re.split(r"(\*\*[^*]+\*\*|_[^_]+_|`[^`]+`)", teks):
        if not bagian:
            continue
        if bagian.startswith("**"):
            r = p.add_run(bagian[2:-2]); r.bold = True
        elif bagian.startswith("_") and bagian.endswith("_") and len(bagian) > 2:
            r = p.add_run(bagian[1:-1]); r.italic = True
        elif bagian.startswith("`"):
            r = p.add_run(bagian[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(10)
        else:
            p.add_run(bagian)
    return p


def para(doc, teks, indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    *awal, teks = teks.split("\n")
    for t in awal:
        para(doc, t, indent, align)
    p = doc.add_paragraph(style="Normal")
    p.alignment = align
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    return tambah_teks(p, teks)


def butir(doc, teks, nomor=None):
    p = doc.add_paragraph(style="Normal")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    tambah_teks(p, (f"{nomor}. " if nomor else "– ") + teks)
    return p


def judul(doc, teks, level):
    return doc.add_heading(teks, level=level)


def caption(doc, teks):
    p = doc.add_paragraph(style="Normal")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    label, _, sisa = teks.partition(" ", )
    no, _, isi = sisa.partition(" ")
    r = p.add_run(f"{label} {no} "); r.bold = True
    r = p.add_run(isi); r.italic = True
    if LABEL_DUMMY:
        r = p.add_run(LABEL_DUMMY); r.bold = True; r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    return p


def kotak_catatan(doc, teks):
    """Paragraf berlatar abu-abu untuk instruksi penempatan (bukan isi tesis)."""
    p = doc.add_paragraph(style="Normal")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "FFF4D6")
    pPr.append(shd)
    r = p.add_run("Penempatan: "); r.bold = True; r.font.color.rgb = RGBColor(0x8A, 0x5A, 0x00)
    r = p.add_run(teks); r.font.color.rgb = RGBColor(0x5A, 0x40, 0x00); r.font.size = Pt(10)
    return p


def set_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for sisi in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{sisi}")
        b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "4"); b.set(qn("w:color"), "000000")
        borders.append(b)
    tcPr.append(borders)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def tabel(doc, header, baris, lebar, tebal_baris=None, ukuran=9):
    t = doc.add_table(rows=1 + len(baris), cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, isi in enumerate([header] + baris):
        for j, teks in enumerate(isi):
            c = t.cell(i, j)
            c.width = Inches(lebar[j])
            set_border(c)
            p = c.paragraphs[0]
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            tambah_teks(p, str(teks))
            for r in p.runs:
                r.font.size = Pt(ukuran)
                if i == 0 or (tebal_baris is not None and i - 1 in tebal_baris):
                    r.bold = True
            if i == 0:
                shade(c, "D9E2F3")
    doc.add_paragraph(style="Normal")
    return t


def gambar(doc, file, lebar, teks):
    path = os.path.join(IMG, file)
    if os.path.exists(path):
        p = doc.add_paragraph(style="Normal"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Inches(lebar))
    else:
        para(doc, f"[Gambar {file} belum dibangkitkan — jalankan analisis_ablasi.py]", indent=False,
             align=WD_ALIGN_PARAGRAPH.CENTER)
    caption(doc, teks)


def tandai_dummy(doc):
    pesan = "PRATINJAU — DATA DUMMY, BUKAN HASIL PENGUKURAN. JANGAN DISERAHKAN."
    p = doc.add_paragraph(style="Normal"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(pesan + " Seluruh angka pada dokumen ini adalah data dummy untuk melihat tata letak. "
                  "Versi final memakai data pengukuran riil dari ukur_ablasi.cjs.")
    r.bold = True; r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)


def halaman_baru(doc):
    doc.add_paragraph(style="Normal").add_run().add_break(WD_BREAK.PAGE)


# ---------------------------------------------------------------- isi
def bagian_pengantar(doc):
    p = doc.add_paragraph(style="Title") if "Title" in [s.name for s in doc.styles] else doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.text = ""
    r = p.add_run("NASKAH REVISI PENGUJI\nPerbandingan Teknik Code Splitting, Lazy Loading, Prefetching, dan Gzip (Studi Ablasi)")
    r.bold = True; r.font.size = Pt(14)

    para(doc, "Tesis: _Optimasi Performa Single Page Application Menggunakan Hybrid Lazy Loading dan Code Splitting "
              "Berdasarkan Tingkat Kompleksitas Sistem_ — Mustari Muhiddin", indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    judul(doc, "A. Catatan Penguji dan Tindak Lanjut", 1)
    para(doc, "**Catatan penguji:** “Buat perbandingan antara splitting, lazy loading, prefetching, dan gzip — teknik mana "
              "yang digunakan yang membuatnya lebih optimal.”", indent=False)
    para(doc, "**Status pada naskah sebelumnya:** belum terjawab. Seluruh pengujian pada Bab III membandingkan dua versi saja, "
              "yaitu _baseline_ dan _optimized_, padahal versi _optimized_ menerapkan keempat teknik sekaligus. Akibatnya perbaikan "
              "yang terukur (misalnya Lighthouse Score naik 32,0%) tidak dapat diatribusikan ke teknik tertentu.", indent=False)
    para(doc, "**Tindak lanjut:** dilakukan _studi ablasi_ (ablation study) pada SIMTA, yaitu membangun varian aplikasi yang masing-"
              "masing hanya mengaktifkan satu teknik, lalu mengukurnya dengan instrumen dan prosedur yang sama dengan Bab III. "
              "Dengan begitu kontribusi tiap teknik dapat dibandingkan secara langsung terhadap satu varian kontrol.", indent=False)

    judul(doc, "B. Peta Penempatan pada Naskah Tesis", 1)
    tabel(doc, ["Lokasi di naskah", "Jenis perubahan", "Isi"], [
        ["Bab II — Sub-bab 2.1.10 (baru)", "Sisipan baru setelah 2.1.9", "Landasan teori prefetching dan kompresi Gzip (bagian C.1)"],
        ["Bab II — Sub-bab 2.8.1 (baru)", "Sisipan baru di akhir 2.8", "Desain studi ablasi: varian, skenario, metrik (bagian C.2)"],
        ["Bab III — Sub-bab 3.10 (baru)", "Sisipan baru setelah 3.9", "Hasil dan pembahasan perbandingan tiap teknik (bagian C.3)"],
        ["Bab IV — Sub-bab 4.1", "Tambahan butir kesimpulan ke-6", "Jawaban teknik mana yang paling berkontribusi (bagian C.4)"],
        ["Bab IV — Sub-bab 4.2", "Tambahan butir saran", "Ablasi pada Company Profile dan kondisi jaringan nyata (bagian C.4)"],
        ["Daftar Pustaka", "Tambahan 1 entri", "Deutsch (1996), RFC 1952 — spesifikasi format Gzip (bagian C.5)"],
        ["Lampiran 1", "Tambahan rincian berkas", "Skrip dan data mentah studi ablasi (bagian C.5)"],
    ], [1.8, 1.6, 2.6])
    para(doc, "Teks pada bagian C ditulis dengan gaya dan penomoran yang mengikuti naskah, sehingga dapat disalin langsung ke "
              "posisi yang ditunjukkan kotak “Penempatan”. Kotak tersebut adalah petunjuk dan tidak perlu ikut disalin.", indent=False)
    halaman_baru(doc)


def bagian_teori(doc):
    judul(doc, "C. Naskah Sisipan", 1)
    kotak_catatan(doc, "BAB II, setelah Sub-bab 2.1.9 Kompleksitas Aplikasi Web (sebelum 2.2).")
    judul(doc, "2.1.10 Prefetching dan Kompresi Gzip", 3)
    para(doc, "Dua teknik lain yang diterapkan pada versi _optimized_ bekerja pada lapisan yang berbeda dari _code splitting_ dan "
              "_lazy loading_. Keempat teknik tersebut dapat dikelompokkan berdasarkan masalah yang diselesaikannya:")
    butir(doc, "**Code splitting** — memecah satu _bundle_ menjadi beberapa _chunk_ (pada penelitian ini melalui `manualChunks` "
               "untuk `vendor-vue` dan `vendor-chart`). Teknik ini mengatur _bagaimana_ kode dikemas, tetapi tidak dengan sendirinya "
               "mengubah _kapan_ kode dimuat (Vite Team, 2024).", 1)
    butir(doc, "**Lazy loading** — menunda pengunduhan dan eksekusi modul halaman sampai rutenya diakses melalui _dynamic import_ "
               "`() => import(...)` (Bara, Boiangiu & Tudose, 2024). Teknik ini mengatur _kapan_ kode dimuat.", 2)
    butir(doc, "**Prefetching** — mengunduh lebih awal _chunk_ yang kemungkinan besar dibutuhkan berikutnya pada saat peramban "
               "senggang (`requestIdleCallback`), sehingga biaya pengunduhan dipindahkan dari saat navigasi ke waktu idle "
               "(Google Chrome Developers, 2023). Teknik ini hanya bermakna jika _lazy loading_ diterapkan lebih dulu.", 3)
    butir(doc, "**Kompresi Gzip** — memampatkan berkas teks (JavaScript, CSS, HTML) dengan algoritma DEFLATE sebelum dikirim, lalu "
               "didekompresi oleh peramban berdasarkan _header_ `Content-Encoding: gzip` (Deutsch, 1996). Teknik ini mengurangi "
               "_ukuran transfer_ tetapi tidak mengurangi jumlah kode yang harus di-_parse_ dan dieksekusi oleh mesin V8.", 4)
    para(doc, "Perbedaan lapisan inilah yang menjadi dasar hipotesis studi ablasi pada Sub-bab 2.8.1: teknik yang mengurangi kode yang "
              "dieksekusi di awal (_lazy loading_) diperkirakan paling berdampak pada TBT dan beban CPU, teknik yang mengurangi ukuran "
              "transfer (Gzip) diperkirakan paling berdampak saat jaringan lambat, sedangkan _prefetching_ diperkirakan tidak mengubah "
              "metrik muatan awal tetapi mempercepat navigasi antarhalaman.")


def bagian_metode(doc):
    kotak_catatan(doc, "BAB II, di akhir Sub-bab 2.8 Skenario Pengujian (setelah paragraf “Setiap skenario dijalankan 5 kali…”).")
    judul(doc, "2.8.1 Desain Studi Ablasi Kontribusi Tiap Teknik", 3)
    para(doc, "Perbandingan _baseline_ dan _optimized_ pada Sub-bab 3.4–3.6 menunjukkan bahwa kombinasi teknik efektif, tetapi tidak "
              "menunjukkan teknik mana yang paling berkontribusi karena keempatnya diterapkan bersamaan. Untuk menjawabnya digunakan "
              "desain _studi ablasi_: dibangun satu varian kontrol tanpa optimasi, lalu beberapa varian yang masing-masing hanya "
              "menambahkan satu teknik. Seluruh varian memakai _entry point_ yang sama (`src/ablasi/main.js`), komponen halaman "
              "yang sama, dan konfigurasi _build_ yang sama (`vite.config.ablasi.js`), sehingga satu-satunya perbedaan antarvarian "
              "adalah teknik yang diuji. Studi ablasi difokuskan pada SIMTA karena pada _Company Profile_ efek gabungan keempat "
              "teknik sudah terbukti sangat kecil (Sub-bab 3.8), sehingga pemecahan per teknik tidak akan menghasilkan perbedaan "
              "yang dapat dibedakan dari variasi pengukuran.")
    caption(doc, "Tabel 2.1 Varian aplikasi pada studi ablasi SIMTA")
    tabel(doc, ["Varian", "Code Splitting", "Lazy Loading", "Prefetching", "Gzip", "Jumlah berkas JS"], [
        [NAMA[v], *m, str(H["ukuran"][v]["jumlah_berkas_js"]) if H else "…"]
        for v, m in [
            ("A0-kontrol", ["–", "–", "–", "–"]),
            ("A1-splitting", ["√", "–", "–", "–"]),
            ("A2-lazy", ["–", "√", "–", "–"]),
            ("A3-prefetch", ["–", "√", "√", "–"]),
            ("A4-gzip", ["–", "–", "–", "√"]),
            ("A5-gabungan", ["√", "√", "√", "√"]),
        ]
    ], [1.7, 0.95, 0.95, 0.95, 0.7, 0.95], tebal_baris=[5])
    para(doc, "_Prefetching_ tidak diuji berdiri sendiri karena secara teknis hanya dapat bekerja di atas _lazy loading_; tanpa "
              "_dynamic import_ seluruh halaman sudah ada di _bundle_ awal sehingga tidak ada yang perlu di-_prefetch_. Oleh karena itu "
              "kontribusi _prefetching_ dibaca dari selisih A3 terhadap A2. Varian A5 menggabungkan keempat teknik dan menghasilkan "
              "struktur _chunk_ yang identik dengan versi _optimized_ pada Bab III (`vendor-vue`, `vendor-chart`, lima _chunk_ "
              "halaman, dan `supabase`), dengan satu perbedaan: kompresi dibatasi pada Gzip saja (tanpa Brotli) agar sesuai dengan "
              "teknik yang dibandingkan.")
    para(doc, "Selain dua kondisi pada Bab III (normal dan CPU 4x), ditambahkan kondisi ketiga, yaitu **CPU 4x + jaringan lambat** "
              "(RTT 150 ms, unduh 1,6 Mbps, unggah 750 Kbps; setara profil _Slow 4G_ Lighthouse) melalui "
              "`Network.emulateNetworkConditions` Chrome DevTools Protocol. Kondisi ini diperlukan karena dua teknik yang diuji — "
              "Gzip dan _prefetching_ — bekerja pada lapisan jaringan, sehingga manfaatnya tidak akan terlihat pada pengujian "
              "_localhost_ tanpa pembatasan jaringan.")
    para(doc, "Metrik yang diukur sama dengan Bab III (FCP, LCP, TBT, _Load Time_ melalui _PerformanceObserver_, serta Lighthouse "
              "Performance Score), ditambah dua metrik pendukung: (1) **ukuran transfer JavaScript pada muatan awal**, diambil dari "
              "_Resource Timing API_ (`transferSize`); dan (2) **latensi navigasi**, yaitu waktu sejak rute diganti dari Dashboard ke "
              "Daftar Judul sampai komponen halaman tersebut muncul di DOM, diukur 2 detik setelah halaman selesai dimuat agar "
              "_prefetching_ sempat berjalan. Setiap kombinasi varian dan kondisi diulang **10 kali** untuk _PerformanceObserver_ "
              "dan **5 kali** untuk Lighthouse. Jumlah repetisi _PerformanceObserver_ dinaikkan dari 5 menjadi 10 karena selisih "
              "antarvarian tunggal lebih kecil daripada selisih _baseline_–_optimized_, sehingga dibutuhkan sampel lebih besar "
              "untuk membedakannya dari variasi pengukuran.")


def bagian_hasil(doc):
    halaman_baru(doc)
    kotak_catatan(doc, "BAB III, sub-bab baru setelah 3.9 Verifikasi Mekanisme Prefetching (sebelum BAB IV).")
    judul(doc, "3.10 Perbandingan Kontribusi Tiap Teknik (Studi Ablasi)", 2)
    para(doc, NARASI["pembuka"])

    judul(doc, "3.10.1 Ukuran Berkas dan Transfer pada Muatan Awal", 3)
    caption(doc, "Tabel 3.9 Ukuran berkas JavaScript dan transfer muatan awal tiap varian")
    tabel(doc, ["Varian", "Berkas JS (build)", "Total JS mentah (KB)", "Berkas JS dimuat awal*", "Transfer JS awal (KB)"], [
        [NAMA[v],
         str(H["ukuran"][v]["jumlah_berkas_js"]) if H else "…",
         angka(H["ukuran"][v]["total_mentah_KB"]) if H else "…",
         angka(po(v, "ideal", "jumlah_js")["mean"], 0) if po(v, "ideal", "jumlah_js") else "…",
         angka(po(v, "ideal", "transfer_js_KB")["mean"]) if po(v, "ideal", "transfer_js_KB") else "…"]
        for v in VARIAN
    ], [1.7, 1.0, 1.15, 1.15, 1.15])
    para(doc, "* Termasuk _chunk_ yang di-_prefetch_ saat idle (diukur 2 detik setelah _load_, tanpa interaksi).", indent=False)
    para(doc, NARASI["ukuran"])

    judul(doc, "3.10.2 Metrik Muatan Awal pada Tiga Kondisi Pengujian", 3)
    for s, label, no in [("ideal", "Kondisi Normal", "3.10"), ("cpu_lambat", "CPU Diperlambat 4x", "3.11"),
                         ("jaringan_lambat", "CPU 4x + Jaringan Lambat", "3.12")]:
        caption(doc, f"Tabel {no} Metrik PerformanceObserver tiap varian — {label} (rata-rata ± SD, 10 repetisi; "
                     f"persentase terhadap A0)")
        tabel(doc, ["Varian", "FCP (ms)", "TBT (ms)", "Load Time (ms)", "Δ FCP", "Δ TBT", "Δ Load"], [
            [NAMA[v], ms(po(v, s, "FCP_ms")), ms(po(v, s, "TBT_ms")), ms(po(v, s, "LoadTime_ms")),
             "–" if v == "A0-kontrol" else pct_po(v, s, "FCP_ms"),
             "–" if v == "A0-kontrol" else pct_po(v, s, "TBT_ms"),
             "–" if v == "A0-kontrol" else pct_po(v, s, "LoadTime_ms")]
            for v in VARIAN
        ], [1.55, 1.05, 1.05, 1.05, 0.6, 0.6, 0.6], ukuran=8.5)
    gambar(doc, "chart_ablasi_metrik.png", 6.2, "Gambar 3.13 Perbandingan metrik muatan awal dan navigasi tiap varian ablasi")
    para(doc, NARASI["muatan_awal"])
    para(doc, NARASI["anomali"])

    judul(doc, "3.10.3 Latensi Navigasi Antarhalaman", 3)
    caption(doc, "Tabel 3.13 Latensi navigasi Dashboard → Daftar Judul (ms, rata-rata ± SD, 10 repetisi)")
    tabel(doc, ["Varian", "Normal", "CPU 4x", "CPU 4x + jaringan lambat"], [
        [NAMA[v], ms(po(v, "ideal", "Navigasi_ms")), ms(po(v, "cpu_lambat", "Navigasi_ms")),
         ms(po(v, "jaringan_lambat", "Navigasi_ms"))]
        for v in VARIAN
    ], [1.8, 1.4, 1.4, 1.8])
    para(doc, NARASI["navigasi"])

    judul(doc, "3.10.4 Hasil Lighthouse", 3)
    caption(doc, "Tabel 3.14 Hasil Lighthouse tiap varian ablasi (rata-rata ± SD, 5 repetisi)")
    tabel(doc, ["Varian", "Score", "FCP (ms)", "LCP (ms)", "TBT (ms)", "Δ Score"], [
        [NAMA[v], ms(lh(v, "PerformanceScore")), ms(lh(v, "FCP_ms"), 0), ms(lh(v, "LCP_ms"), 0), ms(lh(v, "TBT_ms"), 0),
         "–" if v == "A0-kontrol" else pct_lh(v, "PerformanceScore")]
        for v in VARIAN
    ], [1.6, 0.95, 1.15, 1.15, 1.0, 0.7], ukuran=8.5)
    gambar(doc, "chart_ablasi_lighthouse_transfer.png", 6.2,
           "Gambar 3.14 Lighthouse Performance Score dan ukuran transfer JavaScript muatan awal tiap varian")
    para(doc, NARASI["lighthouse"])

    judul(doc, "3.10.5 Teknik Mana yang Paling Membuat Optimal", 3)
    para(doc, NARASI["sintesis_pembuka"])
    caption(doc, "Tabel 3.15 Rangkuman kontribusi tiap teknik pada SIMTA")
    tabel(doc, ["Teknik", "Lapisan yang dipengaruhi", "Dampak terbesar pada", "Dampak berdiri sendiri", "Peringkat"],
          NARASI["tabel_rangkuman"], [1.2, 1.3, 1.45, 1.55, 0.7], ukuran=8.5)
    for i, t in enumerate(NARASI["sintesis_poin"], 1):
        butir(doc, t, i)
    para(doc, NARASI["sintesis_penutup"])


def bagian_penutup(doc):
    halaman_baru(doc)
    kotak_catatan(doc, "BAB IV, Sub-bab 4.1 Kesimpulan — tambahkan sebagai butir ke-6 setelah butir 5.")
    butir(doc, NARASI["kesimpulan"], 6)
    kotak_catatan(doc, "BAB IV, Sub-bab 4.2 Saran — tambahkan sebagai butir ke-6.")
    butir(doc, NARASI["saran"], 6)

    kotak_catatan(doc, "DAFTAR PUSTAKA — sisipkan sesuai urutan alfabet (setelah entri Bogner & Merkel, sebelum Donvir dkk.).")
    p = para(doc, "Deutsch, P. (1996). _GZIP File Format Specification Version 4.3_ (RFC 1952). Internet Engineering Task Force. "
                  "https://doi.org/10.17487/RFC1952", indent=False)
    p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.5)

    kotak_catatan(doc, "LAMPIRAN 1 — tambahkan pada rincian isi berkas arsip.")
    tabel(doc, ["Berkas", "Fungsi"], [
        ["`vite.config.ablasi.js`", "Konfigurasi build enam varian ablasi (pilih lewat variabel lingkungan VARIAN)"],
        ["`src/ablasi/`", "Entry point bersama dan tiga varian router (eager, lazy, lazy + prefetch)"],
        ["`build_ablasi.cjs`", "Membangun seluruh varian dan mencatat ukuran bundle"],
        ["`ukur_ablasi.cjs`", "Pengukuran PerformanceObserver (3 kondisi), latensi navigasi, dan Lighthouse"],
        ["`analisis_ablasi.py`", "Rekap statistik dan pembangkit Gambar 3.13–3.14"],
        ["`data_pengukuran/ablasi/`", "Data mentah (po_*.json, lh_*.json) dan ringkasan_ablasi.json"],
    ], [2.2, 3.8])
    para(doc, "Cara menjalankan ulang: `node build_ablasi.cjs` → `node ukur_ablasi.cjs` → `python analisis_ablasi.py`.", indent=False)


# Narasi pembahasan diisi setelah data pengukuran tersedia (lihat narasi_ablasi.py).
try:
    from narasi_ablasi import buat_narasi
    NARASI = buat_narasi(H, po, lh, angka, pct_po, pct_lh, NAMA)
except ImportError:
    TBD = "[Pembahasan diisi setelah pengukuran selesai.]"
    NARASI = {k: TBD for k in ["pembuka", "ukuran", "muatan_awal", "navigasi", "lighthouse", "sintesis_pembuka",
                               "sintesis_penutup", "kesimpulan", "anomali", "saran"]}
    NARASI["tabel_rangkuman"] = [["…"] * 5]
    NARASI["sintesis_poin"] = [TBD]


def main():
    doc = dokumen_kosong()
    if DUMMY:
        tandai_dummy(doc)
    bagian_pengantar(doc)
    bagian_teori(doc)
    bagian_metode(doc)
    bagian_hasil(doc)
    bagian_penutup(doc)
    doc.save(OUT)
    print("Tersimpan:", OUT)


if __name__ == "__main__":
    main()

import os

base_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis"
chapters_dir = os.path.join(base_dir, "chapters")
output_file = os.path.join(base_dir, "LAPORAN_LENGKAP_TESIS.md")

title = """<h1 align="center">Optimasi Performa Single Page Application Menggunakan Hybrid Lazy Loading dan Code Splitting Berdasarkan Tingkat Kompleksitas Sistem</h1>

---

"""

files_to_merge = [
    "BAB_1_PENDAHULUAN.md",
    "BAB_2_METODE_PENELITIAN.md",
    "BAB_3_HASIL_DAN_PEMBAHASAN.md",
    "BAB_4_PENUTUP.md",
    "DAFTAR_PUSTAKA.md"
]

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write(title)
    for filename in files_to_merge:
        filepath = os.path.join(chapters_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read()
                # Betulkan relative path image karena file LENGKAP ada di parent folder (laporan_tesis)
                # Di bab 2 dan bab 3 menggunakan "./images/...", kita ganti jadi "./chapters/images/..."
                content = content.replace("./images/", "./chapters/images/")
                outfile.write(content)
                outfile.write("\n\n---\n\n")

print(f"Berhasil menggabungkan file ke {output_file}")

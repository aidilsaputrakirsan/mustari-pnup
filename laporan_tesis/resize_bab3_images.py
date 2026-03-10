import os

filepath = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\chapters\BAB_3_HASIL_DAN_PEMBAHASAN.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Kembalikan semua width="380" menjadi width="550" khusus untuk BAB 3
new_content = content.replace('width="380"', 'width="550"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Berhasil mengembalikan ukuran gambar di Bab 3 menjadi 550px.")

# Lakukan penggabungan ulang
os.system("python merge_laporan.py")
print("Merge laporan lengkap beres.")

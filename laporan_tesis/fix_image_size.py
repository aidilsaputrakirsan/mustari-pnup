import os
import re

chapters_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\chapters"

def fix_images(filename):
    filepath = os.path.join(chapters_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def repl(m):
        alt = m.group(1)
        src = m.group(2)
        caption = m.group(3)
        # Menambahkan tag HTML agar gambar dapat diperkecil ukurannya dengan parameter `width`
        # width 550px cukup ideal agar tidak pecah/kebesaran di PDF A4
        return f'<div align="center">\n  <img src="{src}" alt="{alt}" width="550" />\n  <br>\n  <i>{caption}</i>\n</div>'
    
    # Mencari pola ![alt](src) newline *caption*
    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)\n\*(.*?)\*', repl, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_images("BAB_2_METODE_PENELITIAN.md")
fix_images("BAB_3_HASIL_DAN_PEMBAHASAN.md")

print("Gambar berhasil diubah format ukurannya ke HTML tag!")

# Jalankan ulang penggabungan ke LAPORAN_LENGKAP
os.system("python merge_laporan.py")
print("Merge laporan lengkap beres.")

import os

chapters_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\chapters"

def resize_images_in_md():
    for filename in os.listdir(chapters_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(chapters_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Ubah proporsi ukuran render di PDF/Markdown Preview menjadi lebih mungil
            # Asalnya width="550", kita ciutkan secara drastis
            new_content = content.replace('width="550"', 'width="380"')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Berhasil mengubah ukuran gambar di file: {filename}")

resize_images_in_md()

print("Kustomisasi margin ukuran gambar beres. Mengeksekusi penggabungan file...")
os.system("python merge_laporan.py")

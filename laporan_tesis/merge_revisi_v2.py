import os

base = r'D:\Github-ADL\mustari-pnup\laporan_tesis'
src = os.path.join(base, 'revisi_v2')
out = os.path.join(base, 'Revisi-v2-LaporanTesis.md')

title = '<h1 align="center">Optimasi Performa Single Page Application Menggunakan Hybrid Lazy Loading dan Code Splitting Berdasarkan Tingkat Kompleksitas Sistem</h1>\n\n---\n\n'

files = [
    'BAB_1_PENDAHULUAN.md',
    'BAB_2_METODE_DAN_TEORI.md',
    'BAB_3_HASIL_PEMBAHASAN.md',
    'BAB_4_PENUTUP_DAN_PUSTAKA.md',
    'LAMPIRAN.md',
]

with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write(title)
    for name in files:
        with open(os.path.join(src, name), encoding='utf-8') as g:
            f.write(g.read().rstrip() + '\n\n---\n\n')

print('OK', os.path.getsize(out))

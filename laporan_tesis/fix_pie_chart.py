import matplotlib.pyplot as plt
import os

base_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis"
img_dir = os.path.join(base_dir, "chapters", "images")
os.makedirs(img_dir, exist_ok=True)

labels = ['File Modul Chart.js Berbobot Berat', 'File Sistem Inti Vue/Pinia', 'Kode Murni Aplikasi Basis']
sizes = [199, 103, 43]
colors = ['#ff9999','#66b3ff','#99ff99']

fig, ax = plt.subplots(figsize=(8, 5))
# explode effect for the chart.js module to emphasize it
explode = (0.1, 0, 0)  

ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=140, colors=colors, textprops={'fontsize': 10})
ax.axis('equal')  

plt.title('Proporsi Ukuran Modul Eksternal vs Skrip Aplikasi', pad=20, fontsize=14, fontweight='bold')
plt.tight_layout()

output_path = os.path.join(img_dir, 'mermaid_5.png')
plt.savefig(output_path, dpi=300)
print("Pie chart berhasil dibuat ulang di:", output_path)

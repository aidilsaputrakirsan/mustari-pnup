import matplotlib.pyplot as plt
import os

base_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis"
img_dir = os.path.join(base_dir, "chapters", "images")
os.makedirs(img_dir, exist_ok=True)

labels = ['Chart.js Heavy Module File', 'Vue/Pinia Core System Files', 'Pure Application Code']
sizes = [199, 103, 43]
colors = ['#ff9999','#66b3ff','#99ff99']

fig, ax = plt.subplots(figsize=(8, 5))
explode = (0.1, 0, 0)

ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=140, colors=colors, textprops={'fontsize': 10})
ax.axis('equal')

plt.title('Proportion of External Modules vs Application Scripts', pad=20, fontsize=14, fontweight='bold')
plt.tight_layout()

output_path = os.path.join(img_dir, 'mermaid_5_en.png')
plt.savefig(output_path, dpi=300)
print("English pie chart saved to:", output_path)

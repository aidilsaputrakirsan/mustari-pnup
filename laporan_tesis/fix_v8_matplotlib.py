import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

base_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis"
img_dir = os.path.join(base_dir, "chapters", "images")
os.makedirs(img_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(7, 9))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Kumpulan node / kotak
nodes = [
    {"label": "1. Source Code JS", "x": 50, "y": 92, "w": 40, "h": 6, "color": "#f5f5f5"},
    {"label": "2. Lexical Parser\n(Tokenisasi)", "x": 50, "y": 79, "w": 40, "h": 7, "color": "#fff9c4"},
    {"label": "3. Abstract Syntax Tree\n(AST)", "x": 50, "y": 66, "w": 45, "h": 7, "color": "#e1f5fe"},
    {"label": "4. Ignition Interpreter", "x": 50, "y": 53, "w": 45, "h": 6, "color": "#e8f5e9"},
    {"label": "5. Bytecode\n(Abstraksi Mesin)", "x": 25, "y": 38, "w": 38, "h": 8, "color": "#ffe0b2"},
    {"label": "6. TurboFan Compiler\n(Kompilasi JIT)", "x": 75, "y": 38, "w": 38, "h": 8, "color": "#fce4ec"},
    {"label": "7. Optimized\nMachine Code", "x": 75, "y": 20, "w": 38, "h": 8, "color": "#f3e5f5"},
    {"label": "8. Eksekusi CPU\n(Hardware Processor)", "x": 50, "y": 5, "w": 50, "h": 7, "color": "#eceff1"}
]

for node in nodes:
    box = patches.FancyBboxPatch(
        (node["x"] - node["w"]/2, node["y"] - node["h"]/2),
        node["w"], node["h"],
        boxstyle="round,pad=0.3,rounding_size=1",
        ec="#424242", fc=node["color"], lw=1.5
    )
    ax.add_patch(box)
    ax.text(node["x"], node["y"], node["label"], ha='center', va='center', fontsize=10, fontweight='bold', color="#212121")

# Arrow helper
def draw_arrow(ax, x1, y1, x2, y2, label=None, label_x=None, label_y=None, style="->", rad=0, ls="-"):
    if rad != 0:
        connectionstyle = f"arc3,rad={rad}"
    else:
        connectionstyle = "arc3"
    
    ax.annotate("",
                xy=(x2, y2), xycoords='data',
                xytext=(x1, y1), textcoords='data',
                arrowprops=dict(arrowstyle=style, color="#424242", lw=2, 
                                ls=ls, connectionstyle=connectionstyle))
    if label:
        ax.text(label_x, label_y, label, ha='center', va='center', fontsize=9, 
                bbox=dict(facecolor='white', edgecolor='#e0e0e0', alpha=0.9, boxstyle="round,pad=0.3"))

# Draw arrows Vertikal Lurus
draw_arrow(ax, 50, 89, 50, 82.5)  # 1 to 2
draw_arrow(ax, 50, 75.5, 50, 69.5)  # 2 to 3
draw_arrow(ax, 50, 62.5, 50, 56)  # 3 to 4

# Ignition to Bytecode
draw_arrow(ax, 40, 50, 25, 42) 
# Bytecode to TurboFan (Hot code)
draw_arrow(ax, 44, 38, 56, 38, label="Profiling\n(Hot Code)", label_x=50, label_y=41.5)
# TurboFan to Optimized Code
draw_arrow(ax, 75, 34, 75, 24)

# Bytecode to CPU
draw_arrow(ax, 25, 34, 40, 8.5, ls="--", label="Eksekusi\nReguler", label_x=22, label_y=20.5)
# Optimized Code to CPU
draw_arrow(ax, 75, 16, 60, 8.5, ls="-", label="Eksekusi\nKecepatan Penuh", label_x=78, label_y=11.5)

# Deoptimize (Optimized -> Bytecode)
draw_arrow(ax, 65, 24, 35, 34, label="Deoptimize", label_x=50, label_y=26, rad=-0.2, ls=":")

plt.title('Arsitektur Eksekusi JIT Kompilasi V8 Engine', pad=15, fontsize=14, fontweight='bold')
plt.tight_layout()

output_path = os.path.join(img_dir, 'diagram_v8.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Berhasil merender ulang diagram V8 ke {output_path}")

# Kita edit Lebar/Width Gambar V8 dari 380px -> 480px agar cukup lega dibaca (tapi sisanya tetap 380px)
def edit_width(filename):
    path = os.path.join(chapters_dir, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Spesifik replace untuk diagram v8:
        content = content.replace('src="./chapters/images/diagram_v8.png" alt="Siklus Eksekusi V8 Engine" width="380"',
                                  'src="./chapters/images/diagram_v8.png" alt="Siklus Eksekusi V8 Engine" width="480"')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

edit_width("BAB_2_METODE_PENELITIAN.md")

# Lakukan Merge Laporan
os.system("python merge_laporan.py")
print("Merge laporan dan ganti width sukses.")

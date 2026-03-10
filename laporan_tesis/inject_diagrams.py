import base64
import json
import urllib.request
import os

base_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis"
img_dir = os.path.join(base_dir, "chapters", "images")
os.makedirs(img_dir, exist_ok=True)

# Helper function to download mermaid using mermaid.ink
def generate_mermaid_image(code, filename):
    # Untuk mermaid.ink, format base64 dari JSON object
    state = {
        "code": code,
        "mermaid": {"theme": "default"}
    }
    jstring = json.dumps(state)
    b64 = base64.b64encode(jstring.encode('utf-8')).decode('utf-8')
    url = f"https://mermaid.ink/img/{b64}"
    
    out_path = os.path.join(img_dir, filename)
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(out_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Sukses menyimpan {out_path}")
    except Exception as e:
        print(f"Gagal mengunduh {filename}: {e}")

# Diagram 6: MPA vs SPA
diag_mpa_spa = """sequenceDiagram
    participant U as Pengguna
    participant B as Browser
    participant S as Web Server
    
    Note over U,S: Arsitektur Multi-Page Application (MPA)
    U->>B: Klik Link Laman Baru
    B->>S: HTTP Request Dokumen Penuh
    S-->>B: Kirim HTML, CSS, JS Utuh
    B->>U: Reload & Render Total (Layar Berkedip Putih)
    
    Note over U,S: Arsitektur Single Page Application (SPA)
    U->>B: Klik Menu / Opsi
    B->>S: Fetch API / AJAX Request (Berupa data)
    S-->>B: Respon Data JSON Skala Kecil
    B->>B: Eksekusi JS Update Virtual DOM
    B->>U: Render Sebagian Tampilan Tanpa Reload
"""

# Diagram 7: Virtual DOM
diag_vdom = """graph TD
    A[State / Data Aplikasi Berubah] -->|Memicu Reaktivitas| B[Construct Virtual DOM Baru]
    B --> C{Diffing Algorithm}
    D[Virtual DOM Versi Lama] --> C
    C -->|Mencari Selisih/Pembeda| E[Menyusun Antrean Patch]
    E --> F[Memodifikasi Real DOM Terpilih Saja]
    F --> G[Browser Melakukan Repaint/Reflow Parsial]
"""

# Diagram 8: V8 Engine
diag_v8 = """graph LR
    A[Source Code JS] --> B[Lexical Parser]
    B --> C[Abstract Syntax Tree / AST]
    C --> D[Ignition Interpreter]
    D --> E[Bytecode]
    E --> F[TurboFan JIT Compiler]
    F --> G[Optimized Machine Code]
    E -.->|Eksekusi Reguler| H[Eksekusi di CPU]
    G -->|Eksekusi Kecepatan Penuh| H
"""

# Diagram 9: Event Loop
diag_event_loop = """graph TD
    A[Call Stack / Main Thread] -->|Deteksi Operasi Laten/Asinkron| B[Web APIs / Background]
    B -->|Operasi Selesai / File Terunduh| C[Callback / Task Queue]
    D((Event Loop)) -->|Monitor secara Konstan| A
    D -->|Instruksi Pemindahan| C
    C -.->|Memasukkan Titipan Tugas Saat Call Stack Kosong| A
"""

generate_mermaid_image(diag_mpa_spa, "diagram_mpa_spa.png")
generate_mermaid_image(diag_vdom, "diagram_vdom.png")
generate_mermaid_image(diag_v8, "diagram_v8.png")
generate_mermaid_image(diag_event_loop, "diagram_event_loop.png")

# MENYISIPKAN GAMBAR KE DALAM BAB 1
bab1_path = os.path.join(base_dir, "chapters", "BAB_1_PENDAHULUAN.md")
with open(bab1_path, 'r', encoding='utf-8') as f:
    bab1 = f.read()

sisipan_bab1 = """
<div align="center">
  <img src="./chapters/images/diagram_mpa_spa.png" alt="Perbandingan Alur MPA dan SPA" width="550" />
  <br>
  <i>Gambar 1.1 Komparasi Transmisi Data antara Arsitektur MPA Klasik dan SPA Modern.</i>
</div>
"""
bab1 = bab1.replace("Lompatan rekayasa transisi halus ini seketika menyuguhkan ilusi", sisipan_bab1 + "\nLompatan rekayasa transisi halus ini seketika menyuguhkan ilusi")
with open(bab1_path, 'w', encoding='utf-8') as f:
    f.write(bab1)

# MENYISIPKAN GAMBAR KE DALAM BAB 2
bab2_path = os.path.join(base_dir, "chapters", "BAB_2_METODE_PENELITIAN.md")
with open(bab2_path, 'r', encoding='utf-8') as f:
    bab2 = f.read()

sisipan_vdom = """
<div align="center">
  <img src="./chapters/images/diagram_vdom.png" alt="Proses Render Virtual DOM" width="550" />
  <br>
  <i>Gambar 2.1 Mekanika Pembaruan Antarmuka Melalui Algoritma Diffing Virtual-DOM.</i>
</div>
"""
bab2 = bab2.replace("Sayangnya, mekanisme cerdas dan reaktif ini membutuhkan harga mahal", sisipan_vdom + "\nSayangnya, mekanisme cerdas dan reaktif ini membutuhkan harga mahal")

sisipan_v8 = """
<div align="center">
  <img src="./chapters/images/diagram_v8.png" alt="Siklus Eksekusi V8 Engine" width="550" />
  <br>
  <i>Gambar 2.2 Alur Pemrosesan Kompilasi JIT pada Mesin Penyelaras Google V8.</i>
</div>
"""
bab2 = bab2.replace("Fenomena ini dikenal dengan sumbatan benang penyula", sisipan_v8 + "\nFenomena ini dikenal dengan sumbatan benang penyula")

sisipan_eventloop = """
<div align="center">
  <img src="./chapters/images/diagram_event_loop.png" alt="Arsitektur Event Loop" width="550" />
  <br>
  <i>Gambar 2.3 Simpul Aliran Event Loop dalam Menangani Tugas Asinkron JavaScript.</i>
</div>
"""
bab2 = bab2.replace("Segera usai layar antarmuka dasar selesai tergambar di monitor", sisipan_eventloop + "\nSegera usai layar antarmuka dasar selesai tergambar di monitor")

# Perbaiki penomoran gambar yang lama di Bab 2 agar sinkron (mulai dari Gambar 2.4 ke atas)
bab2 = bab2.replace("Gambar 2.1 Entity Relationship Diagram", "Gambar 2.4 Entity Relationship Diagram")
bab2 = bab2.replace("Gambar 2.2 Arus Transmisi Data", "Gambar 2.5 Arus Transmisi Data")
bab2 = bab2.replace("Gambar 2.3 Struktur Penangkapan Algoritma", "Gambar 2.6 Struktur Penangkapan Algoritma")
bab2 = bab2.replace("Gambar 2.4 Alur Diagram Eksekusi Puppeteer", "Gambar 2.7 Alur Diagram Eksekusi Puppeteer")

with open(bab2_path, 'w', encoding='utf-8') as f:
    f.write(bab2)

print("Semua gambar ilustrasi teori berhasil diunduh dan di-inject ke pelaporan!")

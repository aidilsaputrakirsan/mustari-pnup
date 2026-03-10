import json
import os
import re
import base64
import requests
import matplotlib.pyplot as plt
import numpy as np

base_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis"
data_dir = os.path.join(base_dir, "data_pengukuran")
img_dir = os.path.join(base_dir, "chapters", "images")
os.makedirs(img_dir, exist_ok=True)

# 1. Generate Charts
def load_json(filename):
    path = os.path.join(data_dir, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None

data = {
    'simta': {
        'baseline_ideal': load_json("baseline_ideal.json"),
        'baseline_slow': load_json("baseline_cpu_lambat.json"),
        'optimized_ideal': load_json("optimized_ideal.json"),
        'optimized_slow': load_json("optimized_cpu_lambat.json")
    },
    'cp': {
        'baseline_ideal': load_json("cp_baseline_ideal.json"),
        'baseline_slow': load_json("cp_baseline_cpu_lambat.json"),
        'optimized_ideal': load_json("cp_optimized_ideal.json"),
        'optimized_slow': load_json("cp_optimized_cpu_lambat.json")
    }
}

def plot_grouped_bar(title, ylabel, labels, baseline_data, optimized_data, filename, colors=None):
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    if colors:
        rects1 = ax.bar(x - width/2, baseline_data, width, label='Baseline', color=colors[0])
        rects2 = ax.bar(x + width/2, optimized_data, width, label='Optimized', color=colors[1])
    else:
        rects1 = ax.bar(x - width/2, baseline_data, width, label='Baseline')
        rects2 = ax.bar(x + width/2, optimized_data, width, label='Optimized')

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig(os.path.join(img_dir, filename))
    plt.close()

# TBT Chart
labels = ['SIMTA (Ideal)', 'SIMTA (Slow CPU)', 'Company Profile (Ideal)', 'Company Profile (Slow CPU)']
tbt_baseline = [
    data['simta']['baseline_ideal']['TBT_ms'],
    data['simta']['baseline_slow']['TBT_ms'],
    data['cp']['baseline_ideal']['TBT_ms'],
    data['cp']['baseline_slow']['TBT_ms']
]
tbt_optimized = [
    data['simta']['optimized_ideal']['TBT_ms'],
    data['simta']['optimized_slow']['TBT_ms'],
    data['cp']['optimized_ideal']['TBT_ms'],
    data['cp']['optimized_slow']['TBT_ms']
]
plot_grouped_bar('Perbandingan Total Blocking Time (TBT) - Baseline vs Optimized', 'TBT (ms)', labels, tbt_baseline, tbt_optimized, 'chart_tbt_comparison.png', colors=['#e74c3c', '#2ecc71'])

# FCP Chart
fcp_baseline = [
    data['simta']['baseline_ideal']['FCP_ms'],
    data['simta']['baseline_slow']['FCP_ms'],
    data['cp']['baseline_ideal']['FCP_ms'],
    data['cp']['baseline_slow']['FCP_ms']
]
fcp_optimized = [
    data['simta']['optimized_ideal']['FCP_ms'],
    data['simta']['optimized_slow']['FCP_ms'],
    data['cp']['optimized_ideal']['FCP_ms'],
    data['cp']['optimized_slow']['FCP_ms']
]
plot_grouped_bar('Perbandingan First Contentful Paint (FCP) - Baseline vs Optimized', 'FCP (ms)', labels, fcp_baseline, fcp_optimized, 'chart_fcp_comparison.png', colors=['#3498db', '#f1c40f'])

# LoadTime Chart
load_baseline = [
    data['simta']['baseline_ideal']['LoadTime_ms'],
    data['simta']['baseline_slow']['LoadTime_ms'],
    data['cp']['baseline_ideal']['LoadTime_ms'],
    data['cp']['baseline_slow']['LoadTime_ms']
]
load_optimized = [
    data['simta']['optimized_ideal']['LoadTime_ms'],
    data['simta']['optimized_slow']['LoadTime_ms'],
    data['cp']['optimized_ideal']['LoadTime_ms'],
    data['cp']['optimized_slow']['LoadTime_ms']
]
plot_grouped_bar('Perbandingan Waktu Muat Total Laman (Load Time)', 'Waktu Muat (ms)', labels, load_baseline, load_optimized, 'chart_loadtime_comparison.png', colors=['#9b59b6', '#1abc9c'])

# Memory Chart
mem_baseline = [
    float(data['simta']['baseline_ideal']['MemoryUsed_MB']),
    float(data['simta']['baseline_slow']['MemoryUsed_MB']),
    float(data['cp']['baseline_ideal']['MemoryUsed_MB']),
    float(data['cp']['baseline_slow']['MemoryUsed_MB'])
]
mem_optimized = [
    float(data['simta']['optimized_ideal']['MemoryUsed_MB']),
    float(data['simta']['optimized_slow']['MemoryUsed_MB']),
    float(data['cp']['optimized_ideal']['MemoryUsed_MB']),
    float(data['cp']['optimized_slow']['MemoryUsed_MB'])
]
plot_grouped_bar('Perbandingan Konsumsi Memori Peramban (JS Heap)', 'Memori (MB)', labels, mem_baseline, mem_optimized, 'chart_memory_comparison.png', colors=['#e67e22', '#34495e'])


# 2. Extract and Download Mermaid
chapters_dir = os.path.join(base_dir, "chapters")

def encode_mermaid(code):
    try:
        from urllib.parse import quote
        js_code = json.dumps({"code": code, "mermaid": {"theme": "default"}})
        b64 = base64.b64encode(js_code.encode('utf-8')).decode('utf-8')
        return b64
    except Exception as e:
        print("Error base64 encoding", e)
        return ""

mermaid_counter = 1
for filename in ["BAB_2_METODE_PENELITIAN.md", "BAB_3_HASIL_DAN_PEMBAHASAN.md"]:
    filepath = os.path.join(chapters_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find all mermaid blocks
    blocks = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
    for block in blocks:
        b64 = encode_mermaid(block.strip())
        url = f"https://mermaid.ink/img/{b64}"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                img_name = f"mermaid_{mermaid_counter}.png"
                img_path = os.path.join(img_dir, img_name)
                with open(img_path, 'wb') as img_f:
                    img_f.write(resp.content)
                print(f"Downloaded: {img_name} for block in {filename}")
            else:
                print(f"Failed to download mermaid: HTTP {resp.status_code}")
                print(resp.text)
        except Exception as e:
            print(f"Request failed: {e}")
        mermaid_counter += 1

print("DONE_PROCESSING")

import json
import os
import matplotlib.pyplot as plt
import numpy as np

base_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis"
data_dir = os.path.join(base_dir, "data_pengukuran")
img_dir = os.path.join(base_dir, "chapters", "images")
os.makedirs(img_dir, exist_ok=True)

# Load the aggregated stats
summary_file = os.path.join(data_dir, "summary_stats.json")

def load_summary():
    with open(summary_file, 'r') as f:
        return json.load(f)

def plot_grouped_bar(title, ylabel, labels, baseline_vals, optimized_vals, filename, colors=['#e74c3c', '#2ecc71']):
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, baseline_vals, width, label='Baseline', color=colors[0])
    rects2 = ax.bar(x + width/2, optimized_vals, width, label='Optimized', color=colors[1])

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15)
    ax.legend()

    # Add text labels on bars
    ax.bar_label(rects1, padding=3, fmt='%.1f')
    ax.bar_label(rects2, padding=3, fmt='%.1f')

    fig.tight_layout()
    plt.savefig(os.path.join(img_dir, filename), dpi=300)
    plt.close()

def generate_charts():
    s = load_summary()
    perf = s['performance']
    lh = s['lighthouse']
    
    labels = ['SIMTA (Ideal)', 'SIMTA (Slow)', 'CP (Ideal)', 'CP (Slow)']
    
    # 1. TBT Chart (PerformanceObserver)
    tbt_b = [perf['baseline_ideal']['TBT_ms']['mean'], perf['baseline_cpu_lambat']['TBT_ms']['mean'], 
             perf['cp_baseline_ideal']['TBT_ms']['mean'], perf['cp_baseline_cpu_lambat']['TBT_ms']['mean']]
    tbt_o = [perf['optimized_ideal']['TBT_ms']['mean'], perf['optimized_cpu_lambat']['TBT_ms']['mean'], 
             perf['cp_optimized_ideal']['TBT_ms']['mean'], perf['cp_optimized_cpu_lambat']['TBT_ms']['mean']]
    plot_grouped_bar('Total Blocking Time (TBT) - PerformanceObserver (Mean ms)', 'TBT (ms)', labels, tbt_b, tbt_o, 'chart_tbt_comparison.png')

    # 2. FCP Chart (PerformanceObserver)
    fcp_b = [perf['baseline_ideal']['FCP_ms']['mean'], perf['baseline_cpu_lambat']['FCP_ms']['mean'], 
             perf['cp_baseline_ideal']['FCP_ms']['mean'], perf['cp_baseline_cpu_lambat']['FCP_ms']['mean']]
    fcp_o = [perf['optimized_ideal']['FCP_ms']['mean'], perf['optimized_cpu_lambat']['FCP_ms']['mean'], 
             perf['cp_optimized_ideal']['FCP_ms']['mean'], perf['cp_optimized_cpu_lambat']['FCP_ms']['mean']]
    plot_grouped_bar('First Contentful Paint (FCP) - PerformanceObserver (Mean ms)', 'FCP (ms)', labels, fcp_b, fcp_o, 'chart_fcp_comparison.png', colors=['#3498db', '#f1c40f'])

    # 3. Memory Chart (PerformanceObserver)
    mem_b = [perf['baseline_ideal']['MemoryUsed_MB']['mean'], perf['baseline_cpu_lambat']['MemoryUsed_MB']['mean'], 
             perf['cp_baseline_ideal']['MemoryUsed_MB']['mean'], perf['cp_baseline_cpu_lambat']['MemoryUsed_MB']['mean']]
    mem_o = [perf['optimized_ideal']['MemoryUsed_MB']['mean'], perf['optimized_cpu_lambat']['MemoryUsed_MB']['mean'], 
             perf['cp_optimized_ideal']['MemoryUsed_MB']['mean'], perf['cp_optimized_cpu_lambat']['MemoryUsed_MB']['mean']]
    plot_grouped_bar('JS Heap Memory Usage (Mean MB)', 'Memory (MB)', labels, mem_b, mem_o, 'chart_memory_comparison.png', colors=['#e67e22', '#34495e'])

    # 4. LoadTime Chart (PerformanceObserver)
    lt_b = [perf['baseline_ideal']['LoadTime_ms']['mean'], perf['baseline_cpu_lambat']['LoadTime_ms']['mean'], 
            perf['cp_baseline_ideal']['LoadTime_ms']['mean'], perf['cp_baseline_cpu_lambat']['LoadTime_ms']['mean']]
    lt_o = [perf['optimized_ideal']['LoadTime_ms']['mean'], perf['optimized_cpu_lambat']['LoadTime_ms']['mean'], 
            perf['cp_optimized_ideal']['LoadTime_ms']['mean'], perf['cp_optimized_cpu_lambat']['LoadTime_ms']['mean']]
    plot_grouped_bar('Total Page Load Time (Mean ms)', 'Load Time (ms)', labels, lt_b, lt_o, 'chart_loadtime_comparison.png', colors=['#9b59b6', '#1abc9c'])

    # 5. Lighthouse Score Chart
    lh_labels = ['SIMTA', 'Company Profile']
    score_b = [lh['lighthouse_baseline']['PerformanceScore']['mean'], lh['lighthouse_cp_baseline']['PerformanceScore']['mean']]
    score_o = [lh['lighthouse_optimized']['PerformanceScore']['mean'], lh['lighthouse_cp_optimized']['PerformanceScore']['mean']]
    plot_grouped_bar('Lighthouse Performance Score (0-100)', 'Score', lh_labels, score_b, score_o, 'chart_lighthouse_score.png', colors=['#FF5722', '#4CAF50'])

    # 6. Lighthouse TTI Chart
    tti_b = [lh['lighthouse_baseline']['TTI_ms']['mean'], lh['lighthouse_cp_baseline']['TTI_ms']['mean']]
    tti_o = [lh['lighthouse_optimized']['TTI_ms']['mean'], lh['lighthouse_cp_optimized']['TTI_ms']['mean']]
    plot_grouped_bar('Lighthouse Time to Interactive (TTI)', 'TTI (ms)', lh_labels, tti_b, tti_o, 'chart_lighthouse_tti.png', colors=['#795548', '#009688'])

if __name__ == "__main__":
    if os.path.exists(summary_file):
        generate_charts()
        print("Charts generated successfully.")
    else:
        print("Summary stats file not found. Run analisis_statistik.py first.")

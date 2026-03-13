import json
import os
import numpy as np
from glob import glob

data_dir = r"c:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\data_pengukuran"

def calculate_stats(data_list, keys):
    stats = {}
    for key in keys:
        values = []
        for d in data_list:
            v = d.get(key)
            if v is not None:
                # Convert string memory to float
                if key == 'MemoryUsed_MB':
                    values.append(float(v))
                else:
                    values.append(float(v))
        
        if values:
            mean = np.mean(values)
            std = np.std(values)
            stats[key] = {"mean": round(mean, 2), "std": round(std, 2)}
    return stats

def process_files():
    # 1. Process PerformanceObserver Multi-run
    perf_files = glob(os.path.join(data_dir, "multirun_*.json"))
    perf_results = {}
    
    for f in perf_files:
        name = os.path.basename(f).replace("multirun_", "").replace(".json", "")
        with open(f, 'r') as jf:
            data = json.load(jf)
            perf_results[name] = calculate_stats(data, ['FCP_ms', 'LCP_ms', 'TBT_ms', 'LoadTime_ms', 'MemoryUsed_MB'])

    # 2. Process Lighthouse Multi-run
    lh_files = glob(os.path.join(data_dir, "lighthouse_*.json"))
    lh_results = {}
    
    for f in lh_files:
        name = os.path.basename(f).replace(".json", "") # keeps "lighthouse_baseline" etc
        with open(f, 'r') as jf:
            data = json.load(jf)
            lh_results[name] = calculate_stats(data, ['PerformanceScore', 'FCP_ms', 'LCP_ms', 'TTI_ms', 'TBT_ms', 'SpeedIndex'])

    return perf_results, lh_results

def print_summary(perf, lh):
    print("# === STATISTICAL ANALYSIS SUMMARY === #\n")
    
    # Save results to JSON
    summary = {"performance": perf, "lighthouse": lh}
    with open(os.path.join(data_dir, "summary_stats.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✅ Summary saved to summary_stats.json\n")

    print("## 1. PerformanceObserver Metrics (5 Runs Mean ± SD)")
    for target, stats in perf.items():
        print(f"### {target}")
        for metric, val in stats.items():
            print(f"- {metric}: {val['mean']} ± {val['std']}")
        print()

    print("## 2. Lighthouse Metrics (5 Runs Mean ± SD)")
    for target, stats in lh.items():
        print(f"### {target}")
        for metric, val in stats.items():
            print(f"- {metric}: {val['mean']} ± {val['std']}")
        print()

    # Calculate Improvements for SIMTA Ideal
    print("## 3. Key Improvements (SIMTA Ideal Scenario)")
    try:
        b = perf['baseline_ideal']
        o = perf['optimized_ideal']
        for m in ['FCP_ms', 'TBT_ms', 'LoadTime_ms']:
            imp = ((b[m]['mean'] - o[m]['mean']) / b[m]['mean']) * 100
            print(f"- {m} Improvement: {round(imp, 2)}%")
    except:
        pass

if __name__ == "__main__":
    p, l = process_files()
    print_summary(p, l)

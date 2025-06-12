import requests
import time
import json
from datetime import datetime

def benchmark_rpc(url):
    stats = {
        "url": url,
        "latencies": [],
        "success": 0,
        "fail": 0
    }

    for _ in range(5):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }
        start = time.time()
        try:
            r = requests.post(url, json=payload, timeout=5)
            latency = round((time.time() - start) * 1000, 2)
            if r.status_code == 200 and "result" in r.json():
                stats["latencies"].append(latency)
                stats["success"] += 1
            else:
                stats["fail"] += 1
        except:
            stats["fail"] += 1

    return stats

def main():
    with open("endpoints.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    results = []
    for url in urls:
        print(f"Benchmarking: {url}")
        stats = benchmark_rpc(url)
        results.append(stats)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Done. Results saved to results.json.")

if __name__ == "__main__":
    main()

from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def run_masscan_chunk(target, ports, rate):
    cmd = ["masscan", target, "-p", ports, "--rate", str(rate), "-oJ", "-"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def parallel_masscan(targets, port_chunks, rate=10000, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for target in targets:
            for port_chunk in port_chunks:
                futures.append(executor.submit(run_masscan_chunk, target, port_chunk, rate))
        for future in as_completed(futures):
            results.append(future.result())
    return results

def run_nmap_chunk(target, ports):
    cmd = ["nmap", "-sS", "-sV", "-O", "-p", ports, "--open", "-oX", "-", target]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def parallel_nmap(hosts_ports, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_nmap_chunk, host, ports) for host, ports in hosts_ports]
        for future in as_completed(futures):
            results.append(future.result())
    return results

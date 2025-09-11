import json

def generate_report(masscan_results, nmap_results):
    report = {
        "summary": {
            "hosts_scanned": len(set(list(masscan_results.keys()) + list(nmap_results.keys()))),
            "total_open_ports": sum(len(v) for v in nmap_results.values()),
        },
        "details": []
    }
    for ip, ports in nmap_results.items():
        report['details'].append({
            "ip": ip,
            "open_ports": ports
        })
    return report

def print_human_readable(report):
    print("=== Port Discovery Report ===")
    print(f"Hosts scanned: {report['summary']['hosts_scanned']}")
    print(f"Total open ports: {report['summary']['total_open_ports']}\n")
    for host in report['details']:
        print(f"Host: {host['ip']}")
        for port in host['open_ports']:
            print(f"  Port: {port['port']}  Service: {port['service']}")
        print()

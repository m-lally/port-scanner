from scanner import parallel_masscan, parallel_nmap
from parse import parse_masscan_json, parse_nmap_xml
from reporter import generate_report, print_human_readable
from inventory import get_targets_from_netbox, get_targets_from_nornir
from utils import chunk_ports

# Fetch targets from NetBox or Nornir
# api_url = "https://your-netbox-instance/api/"  # Replace with your NetBox API URL
# token = "your-netbox-api-token"  # Replace with your NetBox API token
targets = get_targets_from_netbox(api_url, token)  # or get_targets_from_nornir(config_file)

# Split port range for parallel scanning
port_chunks = chunk_ports("1-65535", chunk_size=1000)

# Parallel Masscan
masscan_outputs = parallel_masscan(targets, port_chunks, rate=10000, max_workers=10)
masscan_results = [parse_masscan_json(out) for out in masscan_outputs]

# Prepare Nmap input: list of (host, ports)
hosts_ports = []
for result in masscan_results:
    for host, ports in result.items():
        hosts_ports.append((host, ",".join(str(p) for p in ports)))

# Parallel Nmap
nmap_outputs = parallel_nmap(hosts_ports, max_workers=10)
nmap_results = [parse_nmap_xml(out) for out in nmap_outputs]

# Reporting
report = generate_report(masscan_results, nmap_results)
print_human_readable(report)

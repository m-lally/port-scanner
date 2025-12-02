# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based parallel port scanning tool that orchestrates masscan and nmap to efficiently discover open ports and services across network targets. It integrates with Nornir and NetBox for inventory management.

## Development Setup

### Prerequisites
- Python 3.13+
- `masscan` and `nmap` installed and available in PATH
- `uv` package manager (used for dependency management)

### Installation
```bash
uv sync
```

### Running the Scanner
```bash
uv run python main.py
```

Note: Before running, you must configure the NetBox API URL and token in `main.py`, or switch to Nornir inventory by uncommenting the appropriate line.

## Architecture

### Two-Stage Scanning Pipeline
The scanner uses a two-phase approach to balance speed and detail:

1. **Fast Discovery (masscan)**: Quickly identifies open ports across large port ranges using masscan's high-speed SYN scanning. Port ranges are chunked and scanned in parallel.

2. **Detailed Enumeration (nmap)**: Takes the discovered ports from masscan and performs service detection (-sV) and OS fingerprinting (-O) with nmap for detailed information.

### Module Structure

- **scanner.py**: Core scanning logic with parallel execution using ThreadPoolExecutor
  - `parallel_masscan()`: Distributes masscan jobs across targets and port chunks
  - `parallel_nmap()`: Runs nmap service detection on discovered ports
  
- **inventory.py**: Target acquisition from different sources
  - `get_targets_from_netbox()`: Fetches IP addresses from NetBox IPAM
  - `get_targets_from_nornir()`: Loads targets from Nornir inventory

- **parse.py**: Output parsers for scanning tools
  - `parse_masscan_json()`: Extracts open ports from masscan JSON output
  - `parse_nmap_xml()`: Extracts service details from nmap XML output

- **reporter.py**: Results formatting and output generation
  - `generate_report()`: Aggregates scan results into structured format
  - `print_human_readable()`: Console-friendly output

- **utils.py**: Helper functions
  - `chunk_ports()`: Splits port ranges for parallel scanning (default 1000 ports per chunk)
  - `resolve_target()`: DNS resolution for hostnames

- **main.py**: Orchestrates the entire scanning workflow

### Data Flow
```
NetBox/Nornir → Targets → Masscan (parallel) → JSON parsing → 
Nmap (parallel, targeted) → XML parsing → Report generation → Output
```

### Parallelization Strategy
- Both masscan and nmap use ThreadPoolExecutor for concurrent execution
- Default max_workers=10 for masscan, 5 for nmap (configurable)
- Port ranges are chunked (default 1000 ports) to enable parallel masscan jobs
- Each target+port_chunk combination becomes a separate masscan task

## Security & Permissions

### Required Privileges
- **masscan**: Requires root/sudo for raw socket access
- **nmap**: Requires root/sudo for SYN scan (-sS) and OS detection (-O)

Run with elevated privileges:
```bash
sudo uv run python main.py
```

### Network Considerations
- Masscan default rate is 10000 packets/sec (adjust in main.py to avoid overwhelming networks)
- Only scans for open ports (--open flag for nmap)
- Be mindful of scanning authorized networks only

## Configuration

Edit `main.py` to customize:
- NetBox API URL and token (lines 8-10)
- Port range to scan (line 13, default "1-65535")
- Chunk size for port splitting (line 13, default 1000)
- Masscan rate (line 16, default 10000 pps)
- Max parallel workers (lines 16, 26)

## Dependencies

Python packages managed via pyproject.toml and uv.lock:
- **nornir**: Network automation framework for inventory management
- **requests**: HTTP client for NetBox API calls
- **ruamel.yaml**: YAML parsing for Nornir configs

External system tools (install separately):
- **masscan**: Fast port scanner
- **nmap**: Network exploration and service detection

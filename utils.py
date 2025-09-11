import socket

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        return target  # Already an IP or range

def chunk_ports(port_range, chunk_size=1000):
    start, end = map(int, port_range.split('-'))
    return [f"{i}-{min(i+chunk_size-1, end)}" for i in range(start, end+1, chunk_size)]

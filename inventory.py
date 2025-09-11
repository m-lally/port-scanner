import requests

def get_targets_from_netbox(api_url, token, filter_params=None):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{api_url}/api/ipam/ip-addresses/", headers=headers, params=filter_params)
    response.raise_for_status()
    data = response.json()
    return [item['address'].split('/')[0] for item in data['results']]

# Nornir integration (example)
from nornir import InitNornir

def get_targets_from_nornir(config_file):
    nr = InitNornir(config_file=config_file)
    return [host.hostname for host in nr.inventory.hosts.values()]

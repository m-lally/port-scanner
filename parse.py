import json
import xml.etree.ElementTree as ET

def parse_masscan_json(json_output):
    try:
        data = json.loads(json_output)
        results = {}
        for entry in data:
            ip = entry['ip']
            if ip not in results:
                results[ip] = []
            results[ip].append(entry['ports'][0]['port'])
        return results
    except Exception as e:
        raise RuntimeError(f"Failed to parse Masscan output: {e}")

def parse_nmap_xml(xml_output):
    results = {}
    try:
        root = ET.fromstring(xml_output)
        for host in root.findall('host'):
            addr = host.find('address').attrib['addr']
            results[addr] = []
            for port in host.findall('.//port'):
                port_id = port.attrib['portid']
                state = port.find('state').attrib['state']
                service = port.find('service').attrib.get('name', '')
                if state == 'open':
                    results[addr].append({'port': port_id, 'service': service})
        return results
    except Exception as e:
        raise RuntimeError(f"Failed to parse Nmap output: {e}")

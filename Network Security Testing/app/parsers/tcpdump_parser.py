import json

def parse_tcpdump(tcpdump_json):
    results = []
    for entry in tcpdump_json['entries']:
        results.append({
            "id": entry['id'],
            "name": entry['name'],
            "description": entry['description'],
            "severity": entry.get('severity', 'Unknown'),
            "affected_component": entry.get('component', 'Unknown'),
            "remediation": entry.get('remediation', 'None provided'),
            "references": [entry.get('references', 'No references provided')]
        })
    return results

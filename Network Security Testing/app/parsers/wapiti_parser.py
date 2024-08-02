import json

def parse_wapiti(wapiti_json):
    results = []
    for vuln in wapiti_json['vulnerabilities']:
        results.append({
            "id": vuln['id'],
            "name": vuln['name'],
            "description": vuln['description'],
            "severity": vuln.get('severity', 'Unknown'),
            "affected_component": vuln.get('component', 'Unknown'),
            "remediation": vuln.get('remediation', 'None provided'),
            "references": [vuln.get('references', 'No references provided')]
        })
    return results

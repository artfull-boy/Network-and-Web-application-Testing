import json

def parse_ssl(ssl_json):
    results = []
    for vuln in ssl_json['vulnerabilities']:
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

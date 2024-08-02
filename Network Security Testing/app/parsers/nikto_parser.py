import json

def parse_nikto(nikto_json):
    results = []
    for vuln in nikto_json['vulnerabilities']:
        results.append({
            "id": vuln['id'],
            "name": "Unknown",  # Nikto doesn't provide a name
            "description": vuln['msg'],
            "severity": "Unknown",  # Nikto doesn't provide severity
            "affected_component": vuln['url'],
            "remediation": "None provided",  # Nikto doesn't provide remediation
            "references": [vuln.get('references', 'No references provided')]
        })
    return results

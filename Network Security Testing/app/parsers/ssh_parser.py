import json

def parse_ssh(ssh_json):
    results = []
    for vuln in ssh_json['vulnerabilities']:
        results.append({
            "id": vuln['id'],
            "name": "Unknown",  # SSH doesn't provide a name
            "description": vuln['description'],
            "severity": vuln.get('severity', 'Unknown'),
            "affected_component": vuln.get('component', 'Unknown'),
            "remediation": vuln.get('remediation', 'None provided'),
            "references": [vuln.get('references', 'No references provided')]
        })
    return results

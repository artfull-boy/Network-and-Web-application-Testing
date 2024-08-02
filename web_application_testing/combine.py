import json
from datetime import datetime

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

def parse_zap(zap_json):
    results = []
    for alert in zap_json['alerts']:
        results.append({
            "id": "Unknown",  # ZAP doesn't provide an ID
            "name": alert['alert'],
            "description": alert['description'],
            "severity": alert['risk'],
            "affected_component": alert['url'],
            "remediation": alert['solution'],
            "references": [alert.get('reference', 'No reference provided')]
        })
    return results

def parse_wapiti(wapiti_json):
    results = []
    for vuln_type, vulns in wapiti_json['vulnerabilities'].items():
        for vuln in vulns:
            results.append({
                "id": "Unknown",
                "name": vuln_type,
                "description": vuln.get('info', 'No description provided'),
                "severity": vuln.get('level', 'Unknown'),
                "affected_component": vuln.get('path', 'Unknown'),
                "remediation": "No remediation provided",
                "references": []  # Wapiti does not provide references in this format
            })
    return results


def parse_curl(curl_json):
    results = []
    
    results.append({
        "id": "N/A",
        "name": "Performance Metrics",
        "description": f"HTTP code: {curl_json['results']['http_code']}, Content type: {curl_json['results']['content_type']}, Redirect URL: {curl_json['results']['redirect_url']}",
        "severity": "N/A",
        "affected_component": curl_json['url'],
        "remediation": "N/A",
        "references": []
    })
    return results

def combine_results(tools_data):
    combined_results = []
    for tool_name, data in tools_data.items():
        parsed_data = data['parser'](data['json'])
        combined_results.append({
            "tool_name": tool_name,
            "scan_date": data['scan_date'],
            "vulnerabilities": parsed_data
        })
    return combined_results

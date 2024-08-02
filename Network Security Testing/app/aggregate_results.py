import json

def aggregate_results(tools_data):
    combined_results = []
    for tool_name, data in tools_data.items():
        parsed_data = data['parser'](data['json'])
        combined_results.append({
            "tool_name": tool_name,
            "scan_date": data['scan_date'],
            "vulnerabilities": parsed_data
        })
    return combined_results

import subprocess
import json

def run_nikto(url, output_file):
    # Define the Nikto command
    command = [
        "nikto",
        "-h", url,  # Target URL
        "-o", output_file,  # Output file
        "-Format", "json"  # Output format
    ]

    # Run the Nikto command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check if the command was successful
    if result.returncode != 0:
        print(f"Error running Nikto: {result.stderr}")
        return {"url": url, "tool": "nikto", "error": result.stderr}

    # Read the JSON output from the output file
    try:
        with open(output_file, "r") as file:
            nikto_results = json.load(file)
    except FileNotFoundError:
        print(f"Output file not found: {output_file}")
        return {"url": url, "tool": "nikto", "error": "Output file not found"}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        return {"url": url, "tool": "nikto", "error": "Error decoding JSON"}

    # Organize vulnerabilities and alerts
    vulnerabilities = []
    alerts = []
    
    if "vulnerabilities" in nikto_results:
        for vuln in nikto_results["vulnerabilities"]:
            vulnerability = {
                "id": vuln.get("id"),
                "references": vuln.get("references", ""),
                "method": vuln.get("method"),
                "message": vuln.get("msg")
            }
            vulnerabilities.append(vulnerability)

    if "errors" in nikto_results:
        for alert in nikto_results["errors"]:
            alert_info = {
                "method": alert.get("method"),
                "message": alert.get("msg")
            }
            alerts.append(alert_info)

    # Organize the results into a structured format
    organized_results = {
        "url": url,
        "tool": "nikto",
        "results": {
            "vulnerabilities": vulnerabilities,
            "alerts": alerts
        }
    }

    return organized_results



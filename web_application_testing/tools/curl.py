import subprocess
import json

def run_curl(url, output_file):
    # Enhanced cURL command to include various useful details
    command = [
        "curl",
        "-sS",  # Silent mode and show errors
        "-I",  # Fetch headers only
        "-o", "/dev/null",  # Discard output
        "-w",  # Custom output format
        """
        {
            "http_code": "%{http_code}",
            "content_type": "%{content_type}",
            "redirect_url": "%{redirect_url}",
            "time_namelookup": "%{time_namelookup}",
            "time_connect": "%{time_connect}",
            "time_appconnect": "%{time_appconnect}",
            "time_pretransfer": "%{time_pretransfer}",
            "time_redirect": "%{time_redirect}",
            "time_starttransfer": "%{time_starttransfer}",
            "time_total": "%{time_total}",
            "size_download": "%{size_download}",
            "speed_download": "%{speed_download}",
            "num_connects": "%{num_connects}",
            "local_ip": "%{local_ip}",
            "local_port": "%{local_port}",
            "remote_ip": "%{remote_ip}",
            "remote_port": "%{remote_port}",
            "ssl_verify_result": "%{ssl_verify_result}"
        }
        """,
        url
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    
    # Parse the JSON output
    try:
        curl_results = json.loads(output)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        return {"url": url, "tool": "curl", "error": "Error decoding JSON"}

    # Organize the results into a structured format
    organized_results = {
        "url": url,
        "tool": "curl",
        "results": curl_results
    }

    # Write the organized output to a file
    with open(output_file, "w") as file:
        json.dump(organized_results, file, indent=2)

    return organized_results


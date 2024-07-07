import subprocess
import json

def run_wapiti(url, output_file):
    # Define the Wapiti command
    command = [
        "wapiti",
        "-u", url,  # Target URL
        "-f", "json",  # Output format
        "-o", output_file  # Output file
    ]

    # Run the Wapiti command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check if the command was successful
    if result.returncode != 0:
        print(f"Error running Wapiti: {result.stderr}")
        return None

    # Read the output file
    with open(output_file, "r") as file:
        wapiti_results = json.load(file)

    return wapiti_results


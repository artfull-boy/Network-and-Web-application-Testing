import subprocess
import json

def run_sqlmap(url, crawl_depth=3, level=5, risk=3):
    # Define the sqlmap command
    command = [
        "sqlmap",
        "-u", url,          # Target URL
        "--batch",          # Run in non-interactive mode
        "--crawl", str(crawl_depth), # Enable crawling with specified depth
        "--level", str(level),        # Set level of tests to perform
        "--risk", str(risk),          # Set risk of tests to perform
        "--dbs"                       # Enumerate DBMS databases
    ]

    # Run the sqlmap command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check if the command was successful
    if result.returncode != 0:
        print(f"Error running sqlmap: {result.stderr}")
        return {"url": url, "tool": "sqlmap", "error": result.stderr}

    # Organize the output
    organized_results = {
        "url": url,
        "tool": "sqlmap",
        "results": result.stdout.splitlines()
    }

    return organized_results

# Example usage
url = "http://192.168.56.101/bWAPP/login.php"
output_file = "/results/sqlmap_results.json"
sqlmap_results = run_sqlmap(url)
with open(output_file, "w") as file:
    json.dump(sqlmap_results, file, indent=2)
print(json.dumps(sqlmap_results, indent=2))

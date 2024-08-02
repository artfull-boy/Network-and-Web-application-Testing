import os
from tools.zap import run_owasp_zap
from tools.curl import run_curl
from tools.nikto import run_nikto
from tools.wapiti import run_wapiti
import openai
from combine import parse_curl, parse_nikto, parse_wapiti, parse_zap, combine_results
import json
import datetime
from full_report import load_json_file, write_to_markdown, chunk_list, get_gpt4_analysis
from pdf import generate_pdf
api_key = os.getenv("OPEN_AI_API_KEY")

url = input("Welcome to your web application scanner, please enter the web application url you want to scan: ")

zap_api_key = os.getenv("ZAP_API_KEY")  

json_file_zap = "./results/zap_results.json"
zap_results = run_owasp_zap(url, zap_api_key, json_file_zap)

json_file_curl = "./results/curl_results.json"
curl_results = run_curl(url, json_file_curl)

json_file_nikto = "./results/nikto_results.json"
nikto_results = run_nikto(url, json_file_nikto)

json_file_wapiti = "./results/wapiti_results.json"
wapiti_results = run_wapiti(url, json_file_wapiti)

# Check if the files have been created
required_files = [json_file_nikto, json_file_zap, json_file_wapiti, json_file_curl]
for file in required_files:
    if not os.path.exists(file):
        raise FileNotFoundError(f"Required file not found: {file}")

# Load JSON data from files
with open(json_file_nikto, 'r') as file:
    nikto_data = json.load(file)
with open(json_file_zap, 'r') as file:
    zap_data = json.load(file)
with open(json_file_wapiti, 'r') as file:
    wapiti_data = json.load(file)
with open(json_file_curl, 'r') as file:
    curl_data = json.load(file)

# Prepare data with parsers
tools_data = {
    "Nikto": {
        "json": nikto_data,
        "parser": parse_nikto,
        "scan_date": str(datetime.datetime.now())
    },
    "ZAP": {
        "json": zap_data,
        "parser": parse_zap,
        "scan_date": str(datetime.datetime.now())
    },
    "Wapiti": {
        "json": wapiti_data,
        "parser": parse_wapiti,
        "scan_date": str(datetime.datetime.now())
    },
    "cURL": {
        "json": curl_data,
        "parser": parse_curl,
        "scan_date": str(datetime.datetime.now())
    }
}

# Combine results
combined_results = combine_results(tools_data)

# Save combined results to a JSON file
with open('combined.json', 'w') as file:
    json.dump(combined_results, file, indent=4)

json_file_path = 'combined.json'
output_file_path = 'output_report.md'


# Write the title to the markdown file
with open(output_file_path, 'w') as f:
    f.write("# Cybersecurity Report\n\n")

data = load_json_file(json_file_path)

for entry in data:
    tool_name = entry.get('tool_name', 'Unknown Tool')
    vulnerabilities = entry.get('vulnerabilities', [])
    for chunk in chunk_list(vulnerabilities, 5):
        analysis = get_gpt4_analysis(tool_name, chunk, api_key)
        write_to_markdown(output_file_path, analysis)

# Convert the markdown report to PDF
md_file = "output_report.md"  
pdf_file = "output_report.pdf" 
generate_pdf(md_file, pdf_file)
print(f"PDF generated: {pdf_file}")

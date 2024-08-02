import os
import json
from datetime import datetime
from dotenv import load_dotenv

from app.parsers.ssh_parser import parse_ssh
from app.parsers.ssl_parser import parse_ssl
from app.parsers.tcpdump_parser import parse_tcpdump
from app.parsers.wapiti_parser import parse_wapiti
from app.parsers.nmap_parser import parse_nmap
from app.utils.aggregate_results import aggregate_results
from app.utils.combine_results import combine_results
from app.utils.report_generator import generate_markdown_report

# Load environment variables
load_dotenv()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    # Load JSON results from files
    ssh_results = load_json('./results/ssh_results.json')
    ssl_results = load_json('./results/ssl_results.json')
    tcpdump_results = load_json('./results/tcpdump_results.json')
    wapiti_results = load_json('./results/wapiti_results.json')
    nmap_results = load_json('./results/nmap_results.json')

    # Prepare data with parsers
    tools_data = {
        "SSH": {
            "json": ssh_results,
            "parser": parse_ssh,
            "scan_date": str(datetime.now())
        },
        "SSL": {
            "json": ssl_results,
            "parser": parse_ssl,
            "scan_date": str(datetime.now())
        },
        "TCPDump": {
            "json": tcpdump_results,
            "parser": parse_tcpdump,
            "scan_date": str(datetime.now())
        },
        "Wapiti": {
            "json": wapiti_results,
            "parser": parse_wapiti,
            "scan_date": str(datetime.now())
        },
        "Nmap": {
            "json": nmap_results,
            "parser": parse_nmap,
            "scan_date": str(datetime.now())
        }
    }

    # Combine and aggregate results
    combined_results = combine_results(tools_data)
    aggregated_results = aggregate_results(combined_results)

    # Generate Markdown report
    markdown_report = generate_markdown_report(aggregated_results)
    
    # Save Markdown report to file
    with open('./results/output_report.md', 'w') as file:
        file.write(markdown_report)

if __name__ == "__main__":
    main()

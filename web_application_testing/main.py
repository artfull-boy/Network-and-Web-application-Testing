
from tools.zap import run_owasp_zap
from tools.curl import run_curl
from tools.nikto import run_nikto
from tools.wapiti import run_wapiti
import openai
from tool_report import generate_report, save_report, load_json
from full_report import read_markdown_file, generate_report_section, merge_report_sections, create_markdown_report, convert_markdown_to_pdf


url = input("Welcome to your web application scanner, please enter the web application url you want to scan: ")


zap_api_key = ''   # Replace with your actual ZAP API key
json_file_zap = "./results/zap_results.json"
zap_results = run_owasp_zap(url, zap_api_key, json_file_zap)

json_file_curl = "./results/curl_results.json"
curl_results = run_curl(url, json_file_curl)

json_file_nikto = "./results/nikto_results.json"
nikto_results = run_nikto(url, json_file_nikto)

json_file_wapiti = "./results/wapiti_results.json"
wapiti_results = run_wapiti(url, json_file_wapiti)


# Set up OpenAI API key
openai.api_key = '' #Replace with your own open ai api key

# Function to analyze results and generate markdown report
def analyze_results(json_file, tool_name, output_file_path):
    data = load_json(json_file)
    report = generate_report(data, tool_name)
    save_report(report, output_file_path)
    print(f"{tool_name} report generated and saved to {output_file_path}")


# Analyze ZAP results
analyze_results(json_file_zap, "ZAP", './results/zap_report.md')

# Analyze cURL results
analyze_results(json_file_curl, "cURL", './results/curl_report.md')

# Analyze Wapiti results
analyze_results(json_file_wapiti, "Wapiti", './results/wapiti_report.md')

# Analyze Nikto results
analyze_results(json_file_nikto, "Nikto", './results/nikto_report.md')


# Read the generated markdown files
zap_report = read_markdown_file('./results/zap_report.md')
curl_report = read_markdown_file('./results/curl_report.md')
wapiti_report = read_markdown_file('./results/wapiti_report.md')
nikto_report = read_markdown_file('./results/nikto_report.md')

# Generate detailed report sections using OpenAI
zap_section = generate_report_section(zap_report, "ZAP")
curl_section = generate_report_section(curl_report, "cURL")
wapiti_section = generate_report_section(wapiti_report, "Wapiti")
nikto_section = generate_report_section(nikto_report, "Nikto")

# Merge the sections into a final report
final_report = merge_report_sections([zap_section, curl_section, wapiti_section, nikto_section])

# Create a markdown file for the final report
create_markdown_report(final_report)

# Convert the markdown report to PDF
convert_markdown_to_pdf('web_application_security_report.md', 'web_application_security_report.pdf')

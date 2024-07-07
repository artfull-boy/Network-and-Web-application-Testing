import subprocess
import json
import openai
import markdown
import weasyprint

# Set your OpenAI API key
openai.api_key = ""

# Function to run a command and capture its output
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return str(e)

# Run Tcpdump
def run_tcpdump(interface):
    command = f"sudo tcpdump -c 10 -i {interface}"
    return run_command(command)

# Run Nmap
def run_nmap(target):
    command = f"nmap -sV {target}"
    return run_command(command)

# Run Nikto
def run_nikto(target):
    command = f"sudo nikto -h {target}"
    return run_command(command)

# Run ssh
def run_ssh(target):
    command = f"sudo ssh-audit {target}"
    return run_command(command)

# Run ssl
def run_ssl(target):
    command = f"sudo sslscan {target}"
    return run_command(command)

# Aggregating results
def aggregate_results(interface, target):
    results = {}
    results['tcpdump'] = run_tcpdump(interface)
    results['nmap'] = run_nmap(target)
    results['nikto'] = run_nikto(target)
    results['ssh'] = run_ssh(target)
    results['ssl'] = run_ssl(target)
    return results

# Function to generate report sections using OpenAI API
def generate_report_section(results, tool_name):
    prompt = f"""Please act like an expert at cybersecurity analysis and generate a detailed and professional vulnerability report section based on the following {tool_name} findings. The section should include the following:

1. **Vulnerability Name**: Provide a concise description of the network security issue (e.g., Open Port, Weak Encryption).
2. **Affected System/Component**: Specify the network device or service where the vulnerability is found (e.g., Firewall, Web Server).
3. **Description**: Give a detailed explanation of the vulnerability, including potential risks.
4. **Severity**: Assess the vulnerability's severity using a standard like CVSS v3.
5. **Recommendations**: Provide clear and actionable steps to mitigate or fix the vulnerability.

Additionally, ensure each vulnerability section includes the following details for better understanding:

- **Impact**: Describe the potential consequences if the vulnerability is exploited.
- **Exploitation Methods (Optional)**: Outline potential methods attackers might use to exploit the vulnerability.
- **References (Optional)**: Include links to relevant resources for further information.

Here are the results of the {tool_name} test: {results}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a network security expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=2048,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response['choices'][0]['message']['content']

# Function to merge sections into a final report
def merge_report_sections(sections):
    prompt = """Please act like an expert at cybersecurity analysis and run vulnerability tests on the {target} and merge your results with the following sections into a single cohesive and professional vulnerability report. Ensure that the report flows well, has consistent formatting, and combines all sections logically. seperate between vulnerabilities with horizontal line please

Here are the sections:
"""
    prompt += "\n\n".join(sections)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a network security expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=2048,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response['choices'][0]['message']['content']

# Function to create a single Markdown report from all parts
def create_markdown_report(report):
    with open('network_security_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

# Function to convert Markdown to HTML and then to PDF using WeasyPrint
def convert_markdown_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    # Add CSS for styling
    css = """
    @page {
        size: A4;
        margin: 1in;
    }

    body {
        background: white;
        font-family: Arial, sans-serif;
        color: black;
    }

    h1, h2, h3, h4, h5, h6 {
        color: black;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
    }

    p, li {
        color: black;
        font-family: Arial, sans-serif;
        line-height: 1.6;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1em;
    }

    table, th, td {
        border: 1px solid black;
    }

    th, td {
        padding: 0.5em;
        text-align: left;
    }
    """

    # Convert HTML to PDF with WeasyPrint
    pdf = weasyprint.HTML(string=html_content).write_pdf(stylesheets=[weasyprint.CSS(string=css)])

    # Save the PDF to a file
    with open(pdf_file, 'wb') as f:
        f.write(pdf)

    print(f"PDF generated and saved to {pdf_file}")

if __name__ == "__main__":
    # Example network interface: eth0
    interface = "eth0"
    # Example target that is legal to test on: scanme.nmap.org
    target = "scanme.nmap.org"
    results = aggregate_results(interface, target)

    # Generate individual sections for each tool
    sections = []
    for tool_name, tool_results in results.items():
        section = generate_report_section(tool_results, tool_name)
        sections.append(section)

    # Merge all sections into a final report
    final_report = merge_report_sections(sections)

    # Create Markdown report
    create_markdown_report(final_report)
    
    # Convert Markdown to PDF
    convert_markdown_to_pdf('network_security_report.md', 'Network_Security_Report3.pdf')

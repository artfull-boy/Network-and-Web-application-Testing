import openai
import markdown
import weasyprint


def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to generate report sections using OpenAI API
def generate_report_section(results, tool_name):
    prompt = f"""Please act like an expert at web application security analysis and generate a detailed and professional vulnerability report section based on the following {tool_name} findings. The section should include the following:

1. *Vulnerability Name*: Provide a concise description of the web application security issue (e.g., SQL Injection, Cross-Site Scripting).
2. *Affected System/Component*: Specify the web application component where the vulnerability is found (e.g., Web Server, Application Code).
3. *Description*: Give a detailed explanation of the vulnerability, including potential risks.
4. *Severity*: Assess the vulnerability's severity using a standard like CVSS v3.
5. *Recommendations*: Provide clear and actionable steps to mitigate or fix the vulnerability.

Additionally, ensure each vulnerability section includes the following details for better understanding:

- *Impact*: Describe the potential consequences if the vulnerability is exploited.
- *Exploitation Methods (Optional)*: Outline potential methods attackers might use to exploit the vulnerability.
- *References (Optional)*: Include links to relevant resources for further information.

Here are the results of the {tool_name} test:
{results}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a web application security expert."},
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
    prompt = """Please act like an expert at web application security analysis and merge the following sections into a single cohesive and professional vulnerability report. Ensure that the report flows well, has consistent formatting, and combines all sections logically.

Here are the sections:
"""
    prompt += "\n\n".join(sections)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a web application security expert."},
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
    with open('a_web_application_security_report.md', 'w', encoding='utf-8') as f:
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

def main():
    file_paths = [
        './results/zap_report.md',
        './results/curl_report.md',
        './results/wapiti_report.md',
        './results/nikto_report.md'
    ]
    tool_names = ["ZAP", "cURL", "Wapiti", "Nikto"]

    sections = []
    for file_path, tool_name in zip(file_paths, tool_names):
        results = read_markdown_file(file_path)
        section = generate_report_section(results, tool_name)
        sections.append(section)

    # Merge all sections into a final report
    final_report = merge_report_sections(sections)

    # Create Markdown report
    create_markdown_report(final_report)

    # Convert Markdown to PDF
    convert_markdown_to_pdf('a3_web_application_security_report.md', 'a3_web_application_security_report.pdf')

if __name__ == "__main__":
    main()

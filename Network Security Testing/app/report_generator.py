import openai
import json
import os

def generate_report_section(vulnerabilities, tool_name):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a cybersecurity expert specializing in web application security. Below is a list of vulnerabilities identified during a recent web application scan. For each vulnerability, please provide:\n\n"
                "1. Vulnerability Name: Provide a concise description of the web application security issue (e.g., SQL Injection, Cross-Site Scripting).\n"
                "2. Affected System/Component: Specify the web application component where the vulnerability is found (e.g., Web Server, Application Code).\n"
                "3. Description: Give a detailed explanation of the vulnerability, including potential risks.\n"
                "4. Severity: Assess the vulnerability's severity using a standard like CVSS v3.\n"
                "5. Recommendations: Provide clear and actionable steps to mitigate or fix the vulnerability.\n"
                "6. Remediations: Suggest comprehensive and actionable remediation steps to address the vulnerability.\n\n"
                "Additionally, ensure each vulnerability section includes the following details for better understanding:\n\n"
                "- Impact: Describe the potential consequences if the vulnerability is exploited.\n"
                "- Exploitation Methods (Optional): Outline potential methods attackers might use to exploit the vulnerability.\n"
                "- References (Optional): Include links to relevant resources for further information.\n\n"
                "Ensure that your response is in a well-structured Markdown format. Use headings and subheadings where appropriate, "
                "and insert a horizontal line (---) to separate the details of each vulnerability."
            )
        },
        {
            "role": "user",
            "content": f"Here is the list of vulnerabilities from {tool_name}:\n\n{json.dumps(vulnerabilities, indent=2)}"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5
    )

    return response.choices[0].message['content'].strip()

def merge_report_sections(sections):
    return "\n\n".join(sections)

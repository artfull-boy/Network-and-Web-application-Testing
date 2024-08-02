import openai
import json

# Function to load the JSON file
def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Function to divide the list into chunks of 5
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i+chunk_size]

# Function to send the chunk to GPT-4 API and get the response
def get_gpt4_analysis(tool_name, vulnerabilities_chunk, api_key):
    openai.api_key = api_key
    messages = [
        {
            "role": "system",
            "content": (
                "You are a cybersecurity expert specializing in web application security. Below is a list of vulnerabilities identified during a recent web application scan. For each vulnerability, please provide the following details in the specified markdown format:\n\n"
                "### Vulnerability Name:  Provide a concise description of the web application security issue (e.g., SQL Injection, Cross-Site Scripting).\n\n"
                "#### Affected System/Component\n"
                "Specify the web application component where the vulnerability is found (e.g., Web Server, Application Code).\n\n"
                "#### Description\n"
                " Give a detailed explanation of the vulnerability, including potential risks.\n\n"
                "#### Severity\n"
                " Assess the vulnerability's severity using a standard like CVSS v3.\n\n"
                "#### Recommendations\n"
                " Provide clear and actionable steps to mitigate or fix the vulnerability.\n\n"
                "#### Remediations\n"
                "Suggest comprehensive and actionable remediation steps to address the vulnerability.\n\n"
                "#### Impact\n"
                "Describe the potential consequences if the vulnerability is exploited.\n\n"
                "#### Exploitation Methods (Optional)\n"
                "Outline potential methods attackers might use to exploit the vulnerability.\n\n"
                "#### References (Optional)\n"
                "Include links to relevant resources for further information.\n\n"
                "Ensure each section header is followed by a detailed explanation, and use a horizontal line (`---`) to separate the details of each vulnerability. Every vulnerability provided must be individually addressed in full, with no omissions and no continuation instructions such as 'Continue in the same manner for the remaining vulnerabilities'."
            )
        },
        {
            "role": "user",
            "content": f"Here is the list of vulnerabilities from {tool_name}:\n\n{json.dumps(vulnerabilities_chunk, indent=2)}"
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

# Function to write the response to a markdown file
def write_to_markdown(file_path, content):
    with open(file_path, 'a') as f:
        f.write(content + '\n\n---\n\n')




import openai
import json
import os
import time





def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def analyze_chunk(chunk, tool_name):
    prompt = f"""
    You are a cybersecurity expert. Analyze the following JSON output from {tool_name} scan and generate a detailed report. The report should include:

    1. A summary of all the vulnerabilities at the beginning.
    2. Detailed descriptions of each vulnerability.
    3. Recommendations for remediation.

    JSON Data:
    {json.dumps(chunk, indent=2)}

    Generate the report in well-styled Markdown format.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response['choices'][0]['message']['content'].strip()

def generate_report(data, tool_name):
    report_parts = []
    items = list(data.items())
    chunk_size = 100  # Adjust this based on the token limits and data size
    num_chunks = len(items) // chunk_size + (1 if len(items) % chunk_size != 0 else 0)

    for i in range(num_chunks):
        chunk = dict(items[i * chunk_size: (i + 1) * chunk_size])
        report_part = analyze_chunk(chunk, tool_name)
        report_parts.append(report_part)
        time.sleep(1)  # Avoid hitting rate limits

    return "\n\n".join(report_parts)

def save_report(report, file_path):
    with open(file_path, 'w') as file:
        file.write(report)

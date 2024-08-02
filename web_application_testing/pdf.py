import markdown2
from weasyprint import HTML, CSS

# Function to convert Markdown to HTML
def markdown_to_html(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()
        html_content = markdown2.markdown(md_text)
        return html_content

# CSS style for the PDF
def generate_css():
    css = """
    @font-face {
        font-family: 'Lato', sans-serif;
        src: url('https://fonts.googleapis.com/css2?family=Lato&display=swap');
    }
    body {
        font-family: 'Lato', sans-serif;
        background-color: #fff; /* white background */
        color: #333; /* dark text */
        padding: 30px; /* increased padding */
        line-height: 1.6;
    }
    h1, h2, h3 {
        color: #555; /* dark grey headings */
        border-bottom: 1px solid #ddd; /* light grey border */
        padding-bottom: 5px;
    }
    p {
        font-size: 14pt;
        margin-bottom: 15px; /* increased margin */
    }
    code {
        background-color: #f0f0f0; /* light grey background for code blocks */
        color: #555; /* dark grey code text */
        padding: 2px 4px;
        border-radius: 4px;
        font-family: 'Courier New', monospace; /* monospace font for code */
    }
    """
    return css

# Function to generate PDF
def generate_pdf(md_file, pdf_file):
    html_content = markdown_to_html(md_file)
    css = generate_css()

    # Generate PDF using WeasyPrint
    HTML(string=html_content).write_pdf(pdf_file, stylesheets=[CSS(string=css)])

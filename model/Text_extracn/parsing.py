import os
from llama_parse import LlamaParse
from dotenv import load_dotenv

load_dotenv()

LLAMA_PARSE_API_KEY = os.getenv('LLAMA_PARSE_API_KEY')

if not LLAMA_PARSE_API_KEY:
    raise ValueError("Missing LLAMA_PARSE_API_KEY. Please set it in your .env file")

# Initialize LlamaParse
parser = LlamaParse(
    api_key=LLAMA_PARSE_API_KEY,
    fast_mode=True,
    max_pages=1
)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using LlamaParse."""
    try:
        documents = parser.load_data(pdf_path)
        extracted_text = documents[0].text  # Extracted text as a string
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


pdf_file_path = "Resume3rd.pdf" 
resume_text = extract_text_from_pdf(pdf_file_path)
print(resume_text)
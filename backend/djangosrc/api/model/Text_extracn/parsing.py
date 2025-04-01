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
        # print("inside extract text from pdf, file path: ", pdf_path)
        documents = parser.load_data(pdf_path)
        extracted_text = documents[0].text  # Extracted text as a string
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# rel_path = os.path.dirname(os.path.abspath(__file__))
# pdf_file_path = rel_path + "\Resume3rd.pdf"
# print(pdf_file_path)
# resume_text = extract_text_from_pdf(pdf_file_path)
# print("\n\n\n\nExtracted Text: ",resume_text, "\n\n\n\n")
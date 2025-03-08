import uuid
from datetime import datetime
import io
from fastapi import UploadFile
import fitz  
from docx import Document
import json
import re


def generate_unique_filename(filename: str) -> str:
    """"
    "Generate a unique filename using the current timestamp and a UUID."
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:12]
    file_extension = filename.split(".")[-1]

    unique_filename = f"{timestamp}_{unique_id}.{file_extension}"

    return unique_filename


async def save_file_in_memory(upload_file: UploadFile):
    file_content = await upload_file.read()  
    file_name = upload_file.filename  
    return io.BytesIO(file_content), file_name


# Extract text from pdf
def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    """
    pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
    text = "\n".join(page.get_text("text") for page in pdf_document)
    pdf_document.close()
    return text.strip()

# Extract text from docx using python-docx
def extract_text_from_docx(docx_file: io.BytesIO) -> str:
    """
    Extract text from a DOCX file using python-docx.
    """

    document = Document(docx_file)
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    return text.strip()


# Extract json from text
def extract_json_from_text(text: str) -> dict:
    """
    Extract JSON from a given text and return it as a dictionary.
    """
    try:
        # Remove ``` json and ``` from the text
        text = re.sub(r"```json|```", "", text).strip()

        # Find the first '{' and last '}'
        start = text.find('{')
        end = text.rfind('}')

        # Extract the substring that should be JSON
        json_str = text[start:end+1]

        # Load and return the parsed JSON
        return json.loads(json_str)
    
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError("Invalid JSON format") from e
    

# Extract personal information from json
def extract_personal_information(data):
    personal_information = [
        data.get("name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("location", ""),
    ]
    
    return personal_information

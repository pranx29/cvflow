import uuid
from datetime import datetime, timedelta
import io
from fastapi import UploadFile
import fitz  
from docx import Document
import json
import re
import pytz

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
    

# Convert to UTC datetime
def convert_to_utc(datetime: datetime) -> datetime:
    """
    Convert a datetime string to UTC using the specified timezone.
    """
    return datetime.astimezone(pytz.UTC)

# Format datetime to ISO 8601
def format_datetime_to_iso(datetime_obj: datetime) -> str:
    """
    Format a datetime object to ISO 8601 format (%Y-%m-%dT%H:%M:%S).
    """
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S")

# Add hours to datetime
def add_hours_to_datetime(datetime_obj: datetime, hours: int) -> datetime:
    """
    Add hours to a datetime object.
    """
    return datetime_obj + timedelta(hours=hours)

# Add seconds to datetime
def add_seconds_to_datetime(datetime_obj: datetime, seconds: int) -> datetime:
    """
    Add seconds to a datetime object.
    """
    return datetime_obj + timedelta(seconds=seconds)


# generate unique name
def generate_unique_name(name: str) -> str:
    """
    Generate a unique name using the current timestamp and a UUID.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:12]
    return f"{name}_{timestamp}_{unique_id}"
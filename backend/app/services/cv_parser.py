import fitz  
import logging
from fastapi import HTTPException, UploadFile
from openai import OpenAI
import json 
from typing import Dict
from core.config import settings
import io
from utils.helper import extract_text_from_pdf, extract_text_from_docx, extract_json_from_text
from fastapi import HTTPException
from utils.exceptions import CVParseException

# Initialize OpenAI client
client = OpenAI(
    base_url=settings.OPENROUTER_API_URL,
    api_key=settings.OPENROUTER_API_KEY,  
)

prompt = f"""
            Act as a data extraction assistant. Extract structured data from the given text and return a JSON object with only these sections:  

            - **personal_information**: Name, contact details, and any identifiers.  
            - **education**: Degrees, institutions, and dates.  
            - **qualifications**: Certifications, licenses, and credentials.  
            - **skills**: Technical and soft skills.  
            - **work_experience**: Job titles, companies, durations, and responsibilities. 
            - **projects**: Titles, descriptions 

            Include synonyms and related terms where applicable. Ensure proper JSON formatting.  
        """

async def parse_cv(file_content: io.BytesIO, file_name: str) -> Dict:
    """
    Parse the CV file and extract structured data using OpenAI API.
    """
    try:
        # Extract text from PDF or DOCX
        if file_name.endswith(".pdf"):
            text = extract_text_from_pdf(file_content)
        elif file_name.endswith(".docx"):
            text = extract_text_from_docx(file_content)
        else:
            raise CVParseException(message="Unsupported file format")

        # Call OpenAI API to extract structured data
        response = client.chat.completions.create(
            model=settings.OPENROUTER_LLM_API_MODEL,
            messages=[
                {"role": "user", "content": prompt + text}
            ],
            temperature=0,
        )

        # Parse the response
        parsed_data = extract_json_from_text(response.choices[0].message.content)
        return parsed_data

    except Exception as e:
        logging.error(f"Error parsing CV: {e}")
        raise CVParseException(message="Error parsing CV file.")

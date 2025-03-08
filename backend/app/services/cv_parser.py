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
from schemas.cv import CV

# Initialize OpenAI client
client = OpenAI(
    base_url=settings.OPENROUTER_API_URL,
    api_key=settings.OPENROUTER_API_KEY,  
)

prompt = """
        Act as a data extraction assistant. Extract structured data from the given text and return a JSON object with only these sections and exact keys:  

        {
        "personal_information": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
        },
        "education": [
            {
            "degree": "",
            "institution": "",
            "start_date": "",
            "end_date": ""
            }
        ],
        "qualifications": [
            {
            "certification": "",
            "issuer": "",
            "date": ""
            }
        ],
        "skills": {
            "technical": [],
            "soft": []
        },
        "work_experience": [
            {
            "job_title": "",
            "company": "",
            "start_date": "",
            "end_date": "",
            "responsibilities": []
            }
        ],
        "projects": [
            {
            "title": "",
            "description": [],
            "technologies": []
            }
        ]
        }
        """

async def parse_cv(file_content: io.BytesIO, file_name: str) -> CV:
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
        print(response.choices[0].message.content)
        parsed_data = extract_json_from_text(response.choices[0].message.content)

        return CV(**parsed_data)
    
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from OpenAI response.")
        raise CVParseException(message="Failed to decode JSON from OpenAI response.")

        # return parsed_data
    except Exception as e:
        logging.error(f"Error parsing CV: {e}")
        raise CVParseException(message="Error parsing CV file.")

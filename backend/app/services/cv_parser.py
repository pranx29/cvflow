import io
import json
import logging
from typing import Dict
from fastapi import HTTPException, UploadFile
from openai import OpenAI
from app.core.config import settings
from app.schemas.cv import CV
from app.utils.exceptions import CVParseException
from app.utils.helper import extract_text_from_pdf, extract_text_from_docx, extract_json_from_text

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

        Please ensure that the JSON object is well-formed and does not contain any additional text or formatting.
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
        parsed_data = extract_json_from_text(response.choices[0].message.content)
        return CV(**parsed_data)
    
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON from OpenAI response. Retrying...")
        try:
            # Retry the OpenAI API call
            response = client.chat.completions.create(
                model=settings.OPENROUTER_LLM_API_MODEL,
                messages=[
                    {"role": "user", "content": prompt + text + e.msg}
                ],
                temperature=0,
            )
            # Parse the response again
            parsed_data = extract_json_from_text(response.choices[0].message.content)
            return CV(**parsed_data)
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON from OpenAI response on retry.")
    except Exception as e:
        logging.error(f"Unexpected eror in cv parsing: {e}")
        raise CVParseException(message="Error parsing CV file.")

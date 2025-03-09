from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
from core.config import settings
from typing import Annotated
from schemas.applicant import Applicant
from utils.validator import validate_file
from utils.exceptions import InvalidFileException
from pydantic import ValidationError
import asyncio
from services.storage import upload_file_to_s3
from io import BytesIO
from utils.helper import save_file_in_memory, generate_unique_name, format_datetime_to_iso, convert_to_utc
from services.cv_parser import parse_cv
from services.sheets import store_in_google_sheets
from services.webhook import send_webhook
from services.email_scheduler import schedule_follow_up_email
from datetime import datetime, timedelta
import pytz


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/job-application", tags=["Job Application"])

@router.post("/submit")
async def submit_application(
    first_name: Annotated[str, Form(...)],
    last_name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    phone: Annotated[str, Form(...)],
    timezone: Annotated[str, Form(...)],
    cv: Annotated[UploadFile, File(...)],
    background_tasks: BackgroundTasks,
):
    """
    Submit a job application with CV and personal details.
    """

    try:
        # Validate applicant details
        applicant = Applicant(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            timezone=timezone,)
        
        # Validate CV file
        validate_file(cv)
        
        logger.info(f"Received job application from {applicant.email}")


        # # Save CV file in memory
        # file_content, file_name = await save_file_in_memory(cv)

        # background_tasks.add_task(
        #     process_application,
        #     applicant=applicant,
        #     file_content=file_content,
        #     file_name=file_name,
        # )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Your application has been submitted successfully."},
        )
    
    except ValidationError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except InvalidFileException as ife:
        logger.error(f"Validation error: {str(ife)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except Exception as e:
        logger.error(f"Error processing job application: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your application.",
        )

async def process_application(
    applicant: Applicant,
    file_content: BytesIO,
    file_name: str,
):
    """
    Process the job application.
    """
    # Upload CV file and parse CV concurrently
    file_copy = BytesIO(file_content.getvalue())
    upload_task = upload_file_to_s3(
        bucket_name=settings.S3_BUCKET_NAME,
        bucket_path=settings.S3_BUCKET_PATH,
        file_name=file_name,
        file_content=file_content,
    )
    parse_task = parse_cv(
        file_content=file_copy,
        file_name=file_name,
    )

    # Run both tasks concurrently
    cv_url, parsed_data = await asyncio.gather(upload_task, parse_task)

    # Store the extracted information in google sheets
    sheet_data = [f"{applicant.first_name} {applicant.last_name}"] + parsed_data.to_google_sheet_format() + [cv_url]

    # Run tasks concurrently
    await asyncio.gather(
        store_in_google_sheets(
            data=sheet_data,
            sheet_id=settings.GOOGLE_SHEET_ID,
        ),
        send_webhook(
            headers={
                "Content-Type": "application/json",
                "X-Candidate-Email": settings.CANDIDATE_EMAIL,
            },
            payload=create_webhook_payload(applicant, cv_url, parsed_data),
            url=settings.WEBHOOK_URL,
        ),
        schedule_follow_up_email_task(applicant=applicant),
    )

    logger.info(f"Job application processed for {applicant.email}")

def create_webhook_payload(applicant: Applicant, cv_url: str, parsed_data): 
    """
    Create the payload for the webhook.
    """
    return {
        "cv_data": {**parsed_data.toJson(), "cv_url": cv_url},
        "metadata": {
            "applicant_name": f"{applicant.first_name} {applicant.last_name}",
            "email": applicant.email,
            "phone": applicant.phone,
            "status": "testing",
            "cv_processed": True,
            "processed_timestamp": datetime.now().isoformat(),
        },
    }

async def schedule_follow_up_email_task(applicant: Applicant):
    """
    Schedule a follow-up email to the candidate.
    """
    tz = pytz.timezone(applicant.timezone)
    schedule_name = generate_unique_name(f"follow_up_email_{applicant.email}").replace("@", "_")
    send_time = convert_to_utc(
        datetime.now(tz) + timedelta(hours=settings.EMAIL_DELAY_HOURS),
    )

    schedule_follow_up_email(
        email=settings.VERIFIED_RECIEVER_EMAIL,
        applicant_name=f"{applicant.first_name} {applicant.last_name}",
        schedule_name=schedule_name,
        send_time=format_datetime_to_iso(send_time),
    )


from pydantic import BaseModel, EmailStr, Field

PHONE_REGEX = r"^\d{6,15}$"

class Applicant(BaseModel):
    """
    Schema for validating applicant data submitted via the job application form.
    """
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(...)
    phone: str = Field(..., pattern=PHONE_REGEX)
    timezone: str = Field(...)
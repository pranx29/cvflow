from fastapi import UploadFile
from utils.exceptions import InvalidFileException

ALLOWED_FILE_TYPES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_file(file: UploadFile):
    """Validates CV file type and size."""
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise InvalidFileException("Invalid file type. Only PDF and DOCX allowed.")
    
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)  
    
    if file_size > MAX_FILE_SIZE:
        raise InvalidFileException("File size must be less than 5MB.")
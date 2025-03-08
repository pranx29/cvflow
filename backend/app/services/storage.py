import boto3
from botocore.exceptions import NoCredentialsError
from core.config import settings
from utils.helper import generate_unique_filename
import logging
from utils.exceptions import S3UploadException
import io

# Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def upload_file_to_s3(bucket_name: str, bucket_path: str, file_name: str, file_content: io.BytesIO):
    """Uploads a file to AWS S3 and returns the public URL."""
    try:
        # Generate a unique file name
        unique_file_name = generate_unique_filename(file_name)
        
        # Upload file to S3 
        s3_client.upload_fileobj(file_content, bucket_name, f"{bucket_path}{unique_file_name}", ExtraArgs={"ACL": "public-read"})
        # Generate public URL
        s3_url = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{bucket_path}{unique_file_name}"

        return s3_url
                
    except NoCredentialsError:
        logging.error("AWS credentials not found.")
        raise S3UploadException("AWS credentials missing. Please check environment variables.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise S3UploadException("Failed to upload file to S3.")

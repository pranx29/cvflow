from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Application Configuration
    APP_ENV: str = Field("development", env="APP_ENV")
    APP_HOST: str = Field("127.0.0.1", env="APP_HOST")
    APP_PORT: int = Field(8000, env="APP_PORT")
    DEBUG: bool = Field(True, env="DEBUG")
    SECRET_KEY: str = Field("change_this_to_a_secure_random_string", env="SECRET_KEY")

    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(..., env="AWS_REGION")

    # S3 Configuration
    S3_BUCKET_NAME: str = Field(..., env="S3_BUCKET_NAME")
    S3_BUCKET_PATH: str = Field(..., env="S3_BUCKET_PATH")
    S3_PRESIGNED_URL_EXPIRY: int = Field(3600, env="S3_PRESIGNED_URL_EXPIRY")

    # AWS Lambda Configuration
    LAMBDA_FUNCTION_ARN: str = Field(..., env="LAMBDA_FUNCTION_ARN")
    EVENTBRIDGE_SCHEDULER_ROLE_ARN: str = Field(..., env="EVENTBRIDGE_SCHEDULER_ROLE_ARN")
    VERIFIED_RECIEVER_EMAIL: str = Field(..., env="VERIFIED_RECIEVER_EMAIL")

    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_FILE: str = Field(..., env="GOOGLE_SHEETS_CREDENTIALS_FILE")
    GOOGLE_SHEET_ID: str = Field(..., env="GOOGLE_SHEET_ID")

    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = Field(..., env="OPENROUTER_API_KEY")
    OPENROUTER_LLM_API_MODEL: str = Field(..., env="OPENROUTER_LLM_API_MODEL")
    OPENROUTER_API_URL: str = Field(..., env="OPENROUTER_API_URL")

    # Webhook Configuration
    WEBHOOK_URL: str = Field(..., env="WEBHOOK_URL")
    CANDIDATE_EMAIL: str = Field(..., env="CANDIDATE_EMAIL")

    # Email Scheduling Configuration
    EMAIL_DELAY_HOURS: int = Field(24, env="EMAIL_DELAY_HOURS")

    # CORS Configuration
    CORS_ALLOWED_ORIGINS: str = Field("http://localhost:3000", env="CORS_ALLOWED_ORIGINS")

settings = Settings()
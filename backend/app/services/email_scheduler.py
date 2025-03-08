import boto3
import botocore.exceptions
from datetime import datetime, timedelta
import pytz
import json
from core.config import settings
import logging
from utils.exceptions import EmailSchedulerException


# Initialize EventBridge Scheduler client
scheduler_client = boto3.client("scheduler", region_name=settings.AWS_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

def schedule_follow_up_email(applicant_name, email, schedule_name, send_time):
    try:
        # Create the schedule
        scheduler_client.create_schedule(
            Name=schedule_name,
            ScheduleExpression=f"at({send_time})", 
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": settings.LAMBDA_FUNCTION_ARN,  
                "RoleArn": settings.EVENTBRIDGE_SCHEDULER_ROLE_ARN, 
                "Input": json.dumps({"email": email, "applicant_name": applicant_name}),
            },
            ActionAfterCompletion="DELETE",
        )
    except botocore.exceptions.ClientError as e:
        logging.error(f"Failed to create schedule: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in email scheduler: {e}")
        raise EmailSchedulerException(f"Failed to schedule email: {str(e)}")


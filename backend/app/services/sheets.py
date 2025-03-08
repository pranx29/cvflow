from google.oauth2.service_account import Credentials
import gspread
from googleapiclient.errors import HttpError
from utils.exceptions import GoogleSheetsException
from core.config import settings
import logging

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

async def store_in_google_sheets(data, sheet_id):
    """ Stores the provided data in a specified Google Sheets document. """
    try:
        # Authenticate and open Google Sheets
        credentials = Credentials.from_service_account_file(settings.GOOGLE_SHEETS_CREDENTIALS_FILE, scopes=SCOPES)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id).sheet1 

        # Append new row with additional values
        sheet.append_row(data)
        
    except HttpError as error:
        logging.error(f"An error google http occurred: {error}")
    except Exception as e:
        logging.error(f"An unexpected error in storing data in google sheets: {e}")
        raise GoogleSheetsException("Failed to store data in Google Sheets.")
        
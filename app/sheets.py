from google.oauth2.service_account import Credentials
import gspread_asyncio
import logging
from app.settings import settings

def get_creds():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    try:
        return Credentials.from_service_account_file(
            settings.creds_path,
            scopes=scopes
        )
    except FileNotFoundError:
        logging.error(f"Credentials file not found: {settings.creds_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading credentials: {e}")
        raise

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

async def get_sheet():
    try:
        agc = await agcm.authorize()
        ss = await agc.open_by_key(settings.spreadsheet_id)
        ws = await ss.get_worksheet(0)
        return ws
    except PermissionError:
        logging.error(f"No permission to access spreadsheet {settings.spreadsheet_id}")
        logging.error("Make sure the service account email is added to the spreadsheet with Editor permissions")
        raise
    except Exception as e:
        logging.error(f"Error accessing Google Sheets: {e}")
        raise

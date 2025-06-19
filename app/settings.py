from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()  # подхватывает .env

class Settings(BaseModel):
    bot_token: str        = os.getenv("BOT_TOKEN")
    creds_path: str       = os.getenv("GSHEETS_CREDENTIALS")
    spreadsheet_id: str   = os.getenv("GSHEETS_SPREADSHEET_ID")

settings = Settings()

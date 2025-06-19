import gspread_asyncio
from app.settings import settings

def get_creds():
    import json
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    return json.load(open(settings.creds_path))

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

async def get_sheet():
    agc = await agcm.authorize()
    ss = await agc.open_by_key(settings.spreadsheet_id)
    ws = await ss.get_worksheet(0)
    return ws

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet_data(sheet_name):
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
    CLIENT = gspread.authorize(CREDS)
    SHEET = CLIENT.open("RespostasForm")
    worksheet = SHEET.worksheet(sheet_name)
    return worksheet.get_all_records()
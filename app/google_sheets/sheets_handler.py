import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_sheet_data(sheet_name):
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Carregar credenciais do Google Sheets a partir das variáveis de ambiente
    credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    if credentials_json is None:
        raise ValueError("As credenciais do Google Sheets não foram encontradas nas variáveis de ambiente.")
    
    credentials_dict = json.loads(credentials_json)
    CREDS = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)
    CLIENT = gspread.authorize(CREDS)
    SHEET = CLIENT.open("RespostasForm")
    worksheet = SHEET.worksheet(sheet_name)
    return worksheet.get_all_records()
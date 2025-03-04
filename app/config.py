# app/config.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Definir o escopo correto para acessar o Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Carregar credenciais do Google Sheets a partir das variáveis de ambiente
credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
if credentials_json is None:
    raise ValueError("As credenciais do Google Sheets não foram encontradas nas variáveis de ambiente.")

credentials_dict = json.loads(credentials_json)
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("RespostasForm")

FORM_SHEETS = {
    "Recanto das Emas": SHEET.worksheet("Recanto das Emas"),
    "Gama": SHEET.worksheet("Gama"),
    "Santa Maria": SHEET.worksheet("Santa Maria"),
    "Guará": SHEET.worksheet("Guará"),  # Corrigido o nome da planilha
    "Planaltina": SHEET.worksheet("Planaltina"),
    "Samambaia": SHEET.worksheet("Samambaia")
}
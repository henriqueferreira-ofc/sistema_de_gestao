# app/config.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Definir o escopo correto para acessar o Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Ajustando o caminho para a estrutura correta
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "google_sheets", "credentials.json")

CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("RespostasForm")

FORM_SHEETS = {
    "Recanto das Emas": SHEET.worksheet("Recanto das Emas"),
    "Gama": SHEET.worksheet("Gama"),
    "Santa Maria": SHEET.worksheet("Santa Maria"),
    "Guará": SHEET.worksheet("Guara"),
    "Planaltina": SHEET.worksheet("Planaltina"),
    "Samambaia": SHEET.worksheet("Samambaia")
}
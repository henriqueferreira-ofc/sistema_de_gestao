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

# Caminho padrão para as credenciais
DEFAULT_CREDENTIALS_PATH = r"C:\Users\henri\OneDrive\Documentos\SEPD DOCUMENTOS\credenciais\sistemadegestaopolitica-abc123.json"

# Tenta carregar o caminho das credenciais de uma variável de ambiente, se não usa o padrão
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", DEFAULT_CREDENTIALS_PATH)

# Verifica se o arquivo existe
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"Arquivo de credenciais não encontrado em: {CREDENTIALS_PATH}. Configure a variável de ambiente GOOGLE_CREDENTIALS_PATH ou coloque o arquivo no caminho padrão.")

# Carrega as credenciais
CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("RespostasForm")

FORM_SHEETS = {
    "Recanto das Emas": SHEET.worksheet("Recanto das Emas"),
    "Gama": SHEET.worksheet("Gama"),
    "Santa Maria": SHEET.worksheet("Santa Maria"),
    "Guará": SHEET.worksheet("Guará"),
    "Planaltina": SHEET.worksheet("Planaltina"),
    "Samambaia": SHEET.worksheet("Samambaia")
}
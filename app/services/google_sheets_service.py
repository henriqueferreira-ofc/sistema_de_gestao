import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Defina o escopo (SCOPE) para acessar o Google Sheets e Google Drive
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Caminho para o arquivo credentials.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Diretório raiz do projeto
CREDS_PATH = os.path.join(BASE_DIR, "google_sheets", "credentials.json")

# Verifique se o arquivo credentials.json existe
if not os.path.exists(CREDS_PATH):
    raise FileNotFoundError(f"Arquivo {CREDS_PATH} não encontrado!")

# Autentique com o Google Sheets usando as credenciais
CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
CLIENT = gspread.authorize(CREDS)

# Função para obter dados do Google Sheets
def obter_dados_do_sheets(nome_planilha, nome_aba):
    try:
        planilha = CLIENT.open(nome_planilha)
        aba = planilha.worksheet(nome_aba)
        dados = aba.get_all_records()
        return dados
    except Exception as e:
        print(f"Erro ao acessar o Google Sheets: {e}")
        print("Caminho do credentials.json:", CREDS_PATH)
        return None

def diagnosticar_planilhas():
    """
    Função para diagnosticar o acesso às planilhas do Google Sheets
    """
    try:
        # Tenta abrir a planilha para verificar se está funcionando
        sheet = CLIENT.open("RespostasForm")  # Substitua pelo nome da sua planilha
        worksheet = sheet.sheet1
        
        # Tenta ler alguns dados para confirmar o acesso
        dados = worksheet.get_all_records()
        
        return {
            "status": "OK",
            "mensagem": f"Planilhas acessadas com sucesso! {len(dados)} registros encontrados.",
            "dados": dados[:5]  # Retorna os primeiros 5 registros como exemplo
        }
    except Exception as e:
        return {
            "status": "Erro",
            "mensagem": f"Erro ao acessar planilhas: {str(e)}",
            "dados": None
        }

# Exportar a função
__all__ = ['diagnosticar_planilhas']
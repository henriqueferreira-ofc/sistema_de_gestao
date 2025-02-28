import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para o arquivo credentials.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Diretório raiz do projeto
CREDS_PATH = os.path.join(BASE_DIR, "google_sheets", "credentials.json")

# Verifique se o arquivo credentials.json existe
if not os.path.exists(CREDS_PATH):
    raise FileNotFoundError(f"Arquivo {CREDS_PATH} não encontrado!")

# Defina o escopo (SCOPE) para acessar o Google Sheets e Google Drive
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def diagnosticar_planilhas():
    """
    Função para diagnosticar e coletar dados de planilhas do Google Sheets.
    Retorna uma lista de registros coletados das abas especificadas.
    """
    try:
        # Autenticação com o Google Sheets
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
        client = gspread.authorize(creds)
        
        # Abre a planilha
        sheet = client.open("RespostasForm")  # Nome da planilha no Google Sheets
        
        # Lista de abas esperadas
        planilhas = ["Recanto das Emas", "Gama", "Santa Maria", "Guará", "Planaltina", "Samambaia"]
        dados = []
        
        # Obtém todas as abas disponíveis para logging
        abas_disponiveis = [ws.title for ws in sheet.worksheets()]
        logger.info(f"Abas disponíveis no Google Sheet 'RespostasForm': {abas_disponiveis}")

        # Itera sobre as planilhas esperadas
        for planilha in planilhas:
            if planilha not in abas_disponiveis:
                logger.warning(f"A aba '{planilha}' não foi encontrada. Pulando...")
                continue
            
            try:
                worksheet = sheet.worksheet(planilha)
                registros = worksheet.get_all_records()
                dados.extend(registros)
                logger.info(f"Dados carregados da aba '{planilha}' com sucesso. Total de registros: {len(registros)}")
            except gspread.exceptions.WorksheetNotFound as e:
                logger.error(f"Erro ao acessar a aba '{planilha}': {e}")
                continue
            except Exception as e:
                logger.error(f"Erro inesperado ao processar a aba '{planilha}': {e}")
                continue

        if not dados:
            logger.warning("Nenhum dado foi carregado das planilhas.")
            return []  # Retorna lista vazia se não houver dados

        logger.info(f"Total de registros carregados: {len(dados)}")
        return dados

    except gspread.exceptions.SpreadsheetNotFound as e:
        logger.error(f"Planilha 'RespostasForm' não encontrada: {e}")
        return []
    except Exception as e:
        logger.error(f"Erro geral em diagnosticar_planilhas: {e}")
        return []

# Exportar a função
__all__ = ['diagnosticar_planilhas']

# Função auxiliar (opcional, caso queira reutilizá-la em outro contexto)
def obter_dados_do_sheets(nome_planilha, nome_aba):
    """
    Função auxiliar para obter dados de uma aba específica em uma planilha do Google Sheets.
    """
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
        client = gspread.authorize(creds)
        planilha = client.open(nome_planilha)
        aba = planilha.worksheet(nome_aba)
        dados = aba.get_all_records()
        logger.info(f"Dados obtidos da aba '{nome_aba}' na planilha '{nome_planilha}' com sucesso.")
        return dados
    except Exception as e:
        logger.error(f"Erro ao acessar o Google Sheets - Planilha: {nome_planilha}, Aba: {nome_aba}: {e}")
        return None
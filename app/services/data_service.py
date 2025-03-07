import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Definir o escopo correto para acessar o Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Ajustando o caminho para a estrutura correta
CREDENTIALS_PATH = 'C:\\Users\\henri\\OneDrive\\Documentos\\SEPD DOCUMENTOS\\credenciais\\sistemadegestaopolitica-def0b2c64083.json'

CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPE)

CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("RespostasForm")

def obter_dados_do_sheets():
    planilha = SHEET.sheet1
    return planilha.get_all_records()

def diagnosticar_planilhas():
    try:
        return {"status": "OK", "mensagem": "Planilhas acessadas com sucesso!"}
    except Exception as e:
        return {"status": "Erro", "mensagem": str(e)}

def gerar_graficos():
    """
    Função para gerar os gráficos com as análises solicitadas
    """
    try:
        dados = obter_dados_planilha()
        if 'erro' in dados:
            return {'erro': dados['erro']}

        registros = dados['registros']
        
        # 1. Interesse em Política (Gráfico de Pizza)
        interesse_politica = {}
        for registro in registros:
            resposta = registro.get('Interesse em Política', 'Não respondeu').strip()
            interesse_politica[resposta] = interesse_politica.get(resposta, 0) + 1
        
        grafico_interesse = {
            'data': [{
                'values': list(interesse_politica.values()),
                'labels': list(interesse_politica.keys()),
                'type': 'pie',
                'hole': 0.4,
                'name': 'Interesse em Política'
            }],
            'layout': {
                'title': 'Interesse em Política',
                'showlegend': True,
                'height': 400
            }
        }

        # 2. Serviços por Cidade (Gráfico de Barras)
        servicos_cidade = {}
        for registro in registros:
            cidade = registro.get('Cidade de Origem', 'Não especificada')
            servicos_cidade[cidade] = servicos_cidade.get(cidade, 0) + 1
        
        grafico_servicos = {
            'data': [{
                'x': list(servicos_cidade.keys()),
                'y': list(servicos_cidade.values()),
                'type': 'bar',
                'name': 'Serviços por Cidade'
            }],
            'layout': {
                'title': 'Quantidade de Serviços por Cidade',
                'xaxis': {'title': 'Cidade'},
                'yaxis': {'title': 'Quantidade'},
                'height': 400
            }
        }

        # 3. Interesse em Política por Cidade (Gráfico de Barras Empilhadas)
        politica_cidade = {}
        for registro in registros:
            cidade = registro.get('Cidade de Origem', 'Não especificada')
            interesse = registro.get('Interesse em Política', 'Não respondeu').strip()
            if cidade not in politica_cidade:
                politica_cidade[cidade] = {'Sim': 0, 'Não': 0, 'Não respondeu': 0}
            politica_cidade[cidade][interesse] = politica_cidade[cidade].get(interesse, 0) + 1

        grafico_politica_cidade = {
            'data': [
                {
                    'x': list(politica_cidade.keys()),
                    'y': [dados['Sim'] for dados in politica_cidade.values()],
                    'name': 'Sim',
                    'type': 'bar'
                },
                {
                    'x': list(politica_cidade.keys()),
                    'y': [dados['Não'] for dados in politica_cidade.values()],
                    'name': 'Não',
                    'type': 'bar'
                }
            ],
            'layout': {
                'title': 'Interesse em Política por Cidade',
                'barmode': 'stack',
                'xaxis': {'title': 'Cidade'},
                'yaxis': {'title': 'Quantidade'},
                'height': 400
            }
        }

        # 4. Tipos de Serviços de Interesse (Gráfico de Barras Horizontais)
        servicos_interesse = {}
        for registro in registros:
            servico = registro.get('Qual benefício você precisa', 'Não especificado').strip()
            servicos_interesse[servico] = servicos_interesse.get(servico, 0) + 1
        
        # Ordenar por quantidade
        servicos_ordenados = dict(sorted(servicos_interesse.items(), key=lambda x: x[1], reverse=True))
        
        grafico_servicos_interesse = {
            'data': [{
                'y': list(servicos_ordenados.keys()),
                'x': list(servicos_ordenados.values()),
                'type': 'bar',
                'orientation': 'h',
                'name': 'Serviços de Interesse'
            }],
            'layout': {
                'title': 'Serviços Mais Procurados',
                'xaxis': {'title': 'Quantidade'},
                'yaxis': {'title': 'Serviço'},
                'height': 400
            }
        }

        return {
            'interesse_politica': grafico_interesse,
            'servicos_cidade': grafico_servicos,
            'politica_cidade': grafico_politica_cidade,
            'servicos_interesse': grafico_servicos_interesse
        }

    except Exception as e:
        print(f"Erro ao gerar gráficos: {str(e)}")
        return {'erro': str(e)}

def obter_dados_planilha():
    try:
        # Obter todos os registros da planilha
        registros = obter_dados_do_sheets()
        
        # Extrair cabeçalho
        cabecalho = registros[0].keys() if registros else []

        # Calcular estatísticas por cidade
        estatisticas_cidades = {}
        for registro in registros:
            cidade = registro.get('Cidade de Origem', 'Não especificada')
            estatisticas_cidades[cidade] = estatisticas_cidades.get(cidade, 0) + 1

        # Calcular total de registros
        total_registros = len(registros)

        return {
            'cabecalho': cabecalho,
            'registros': registros,
            'estatisticas_cidades': estatisticas_cidades,
            'total_registros': total_registros
        }
    except Exception as e:
        print(f"Erro ao obter dados da planilha: {str(e)}")
        return {'erro': str(e)}

# Exportar a função
__all__ = ['gerar_graficos']

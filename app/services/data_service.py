import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Definir o escopo correto para acessar o Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Ajustando o caminho para a estrutura correta
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "google_sheets", "credentials.json")

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
    """
    Função para obter dados de todas as abas (cidades) da planilha
    """
    try:
        # Abrir a planilha
        planilha = CLIENT.open("RespostasForm")
        
        # Definir o cabeçalho na ordem desejada
        cabecalho_desejado = [
            'Cidade de Origem',
            'Nome',
            'Telefone',
            'Qual Deficiência',
            'Conhece os Atendimentos',
            'Benefício que você Precisa',
            'Ficou sabendo da Carreta',
            'Por Quem',
            'Política',
            'Carimbo de Data/Hora'
        ]
        
        # Mapeamento para padronizar os nomes das colunas
        mapeamento_colunas = {
            # Mapeamento para campos de telefone
            'Telefone': 'Telefone',
            'Qual seu telefone?': 'Telefone',
            'Número de telefone': 'Telefone',
            
            # Mapeamento para campos de deficiência
            'Qual o tipo de deficiência?': 'Qual Deficiência',
            'Qual tipo de deficiência': 'Qual Deficiência',
            'Tipo de deficiência': 'Qual Deficiência',
            
            # Mapeamento para conhecimento dos atendimentos
            'Você conhece todos os atendimentos e serviços oferecidos pela SEPD (Secretaria da Pessoa com Deficiência)?': 'Conhece os Atendimentos',
            'Conhece os Atendimentos': 'Conhece os Atendimentos',
            'Você conhece os atendimentos?': 'Conhece os Atendimentos',
            
            # Mapeamento para benefícios
            'Qual benefício você precisa': 'Benefício que você Precisa',
            'Benefício que você Precisa': 'Benefício que você Precisa',
            'Qual benefício precisa?': 'Benefício que você Precisa',
            
            # Mapeamento para informação sobre a carreta
            'Ficou sabendo da Carreta': 'Ficou sabendo da Carreta',
            'Como ficou sabendo da carreta?': 'Ficou sabendo da Carreta',
            
            # Mapeamento para fonte da informação
            'Por quem': 'Por Quem',
            'Porque Quem': 'Porque Quem',
            'Por qual meio?': 'Porque Quem',
            
            # Mapeamento para interesse em política
            'Interesse em Política': 'Política',
            'Política': 'Política',
            'Tem interesse em política?': 'Política',
            
            # Outros mapeamentos existentes
            'Carimbo de data/hora': 'Carimbo de Data/Hora'
        }
        
        # Mapeamento das abas por cidade
        abas_cidades = {
            "Recanto das Emas": planilha.worksheet("Recanto das Emas"),
            "Gama": planilha.worksheet("Gama"),
            "Santa Maria": planilha.worksheet("Santa Maria"),
            "Guará": planilha.worksheet("Guara"),
            "Planaltina": planilha.worksheet("Planaltina"),
            "Samambaia": planilha.worksheet("Samambaia")
        }
        
        # Coletar dados de todas as abas
        todos_registros = []
        estatisticas_cidades = {}
        
        for cidade, worksheet in abas_cidades.items():
            try:
                print(f"Processando dados de {cidade}...")
                dados_aba = worksheet.get_all_records()
                
                # Debug: mostrar as colunas da planilha
                if dados_aba:
                    print(f"Colunas em {cidade}:", list(dados_aba[0].keys()))
                
                for registro in dados_aba:
                    registro_processado = {'Cidade de Origem': cidade}
                    
                    # Processar nome
                    nome = None
                    for chave in registro:
                        if 'Qual seu nome?' in chave or 'Nome' in chave:
                            valor = registro[chave]
                            if isinstance(valor, str) and valor.strip():
                                nome = valor.strip()
                                break
                    registro_processado['Nome'] = nome if nome else 'Não informado'
                    
                    # Processar deficiência - usando o nome exato da coluna
                    tipo_deficiencia = None
                    for chave in registro:
                        if 'Qual o tipo de deficiência?' in chave:
                            valor = registro[chave]
                            if isinstance(valor, str):
                                tipo_deficiencia = valor.strip()
                                break
                    registro_processado['Qual Deficiência'] = tipo_deficiencia if tipo_deficiencia else 'Não informado'
                    
                    # Processar todos os outros campos usando o mapeamento
                    for chave_original, valor in registro.items():
                        for padrao, padronizado in mapeamento_colunas.items():
                            if padrao.lower() in chave_original.lower():
                                if isinstance(valor, str):
                                    valor = valor.strip()
                                registro_processado[padronizado] = valor if valor != '' else 'Não informado'
                                break
                    
                    todos_registros.append(registro_processado)
                
                estatisticas_cidades[cidade] = len(dados_aba)
                print(f"Encontrados {len(dados_aba)} registros em {cidade}")
                
            except Exception as e:
                print(f"Erro ao processar aba {cidade}: {str(e)}")
                continue
        
        if not todos_registros:
            return {'cabecalho': [], 'registros': [], 'erro': 'Nenhum dado encontrado'}
        
        # Padronizar todos os registros
        registros_padronizados = []
        for registro in todos_registros:
            registro_padrao = {}
            for coluna in cabecalho_desejado:
                registro_padrao[coluna] = registro.get(coluna, 'Não informado')
            registros_padronizados.append(registro_padrao)
        
        print(f"Total de registros processados: {len(registros_padronizados)}")
        
        # Debug: mostrar exemplo de registro processado
        if registros_padronizados:
            print("\nExemplo de registro processado:")
            print(f"Deficiência: {registros_padronizados[0].get('Qual Deficiência', 'Não informado')}")
        
        return {
            'cabecalho': cabecalho_desejado,
            'registros': registros_padronizados,
            'total_registros': len(registros_padronizados),
            'estatisticas_cidades': estatisticas_cidades
        }
        
    except Exception as e:
        print(f"Erro ao obter dados das planilhas: {str(e)}")
        return {'cabecalho': [], 'registros': [], 'erro': str(e)}

# Exportar a função
__all__ = ['gerar_graficos']

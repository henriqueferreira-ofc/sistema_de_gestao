import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app.config import FORM_SHEETS  # importando as configurações existentes

def init_dashboard(server):
    dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=['/static/css/dashboard.css'])

    # Função para obter dados
    def get_data():
        dados_consolidados = []
        for form_name, worksheet in FORM_SHEETS.items():
            registros = worksheet.get_all_records()
            for registro in registros:
                dados_registro = {
                    'Cidade de Origem': form_name,
                    'deficiencia': None,
                    'interesse_politica': None,
                    'conhece_servicos': None
                }

                for coluna in registro.keys():
                    if "deficiência" in coluna.lower():
                        dados_registro['deficiencia'] = registro[coluna]
                    elif any(termo in coluna.lower() for termo in ["política", "politica"]):
                        dados_registro['interesse_politica'] = registro[coluna]
                    elif "conhece" in coluna.lower() and "serviços" in coluna.lower():
                        dados_registro['conhece_servicos'] = registro[coluna]

                dados_consolidados.append(dados_registro)

        df = pd.DataFrame(dados_consolidados)
        print("DataFrame coletado:", df.head())  # Adiciona log para verificar o conteúdo do DataFrame
        return df

    # Verifica se FORM_SHEETS não está vazio
    if FORM_SHEETS:
        default_city = list(FORM_SHEETS.keys())[0]
        city_options = [{'label': cidade, 'value': cidade} for cidade in FORM_SHEETS.keys()]
    else:
        default_city = None
        city_options = []

    # Adiciona logs para verificar o conteúdo de FORM_SHEETS e city_options
    print("FORM_SHEETS:", FORM_SHEETS)
    print("city_options:", city_options)

    # Layout do dashboard
    dash_app.layout = html.Div([
        html.H1('Dashboard Analítico', style={'textAlign': 'center'}),

        # Filtros
        html.Div([
            html.Label('Selecione a Cidade:'),
            dcc.Dropdown(
                id='cidade-filter',
                options=city_options,
                value=default_city,  # Seleciona a primeira cidade por padrão, se disponível
                multi=False
            )
        ], style={'width': '50%', 'margin': '20px auto'}),

        # KPIs
        html.Div([
            html.Div([
                html.H3('Total de Atendimentos'),
                html.H4(id='total-atendimentos')
            ], className='kpi-box'),
            html.Div([
                html.H3('Interesse em Política'),
                html.H4(id='total-interesse')
            ], className='kpi-box'),
            html.Div([
                html.H3('Conhecem os Serviços'),
                html.H4(id='total-conhece')
            ], className='kpi-box')
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px 0'}),

        # Gráficos
        html.Div([
            html.Div([
                dcc.Graph(id='interesse-politica-graph')
            ], style={'width': '48%'}),
            html.Div([
                dcc.Graph(id='deficiencia-graph')
            ], style={'width': '48%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),

        # Tabela detalhada
        html.Div([
            html.H3('Detalhamento por Cidade'),
            dcc.Graph(id='cidade-table')
        ])
    ])

    # Callbacks para atualizar os gráficos
    @dash_app.callback(
        [Output('total-atendimentos', 'children'),
         Output('total-interesse', 'children'),
         Output('total-conhece', 'children'),
         Output('interesse-politica-graph', 'figure'),
         Output('deficiencia-graph', 'figure'),
         Output('cidade-table', 'figure')],
        [Input('cidade-filter', 'value')]
    )
    def update_graphs(selected_cidade):
        df = get_data()
        print("DataFrame filtrado:", df.head())  # Adiciona log para verificar o conteúdo do DataFrame filtrado

        if 'Cidade de Origem' not in df.columns:
            print("Erro: A coluna 'Cidade de Origem' não está presente no DataFrame.")
            return (
                "N/A",
                "N/A",
                "N/A",
                go.Figure(),
                go.Figure(),
                go.Figure()
            )

        df_filtered = df[df['Cidade de Origem'] == selected_cidade]

        # KPIs
        total_atendimentos = len(df_filtered)
        total_interesse = len(df_filtered[df_filtered['interesse_politica'] == 'Sim'])
        total_conhece = len(df_filtered[df_filtered['conhece_servicos'] == 'Sim'])

        # Gráfico de Interesse em Política
        fig_interesse = px.bar(
            df_filtered.groupby('Cidade de Origem')['interesse_politica'].value_counts().unstack(),
            barmode='group',
            title='Interesse em Política por Cidade',
            labels={'value': 'Quantidade', 'Cidade de Origem': 'Cidade'}
        )

        # Gráfico de Tipos de Deficiência
        fig_deficiencia = px.pie(
            df_filtered,
            names='deficiencia',
            title='Distribuição por Tipo de Deficiência'
        )

        # Tabela detalhada
        table_data = df_filtered.groupby('Cidade de Origem').agg({
            'interesse_politica': lambda x: (x == 'Sim').sum(),
            'conhece_servicos': lambda x: (x == 'Sim').sum(),
        }).reset_index()

        fig_table = go.Figure(data=[go.Table(
            header=dict(values=['Cidade de Origem', 'Interesse em Política', 'Conhece Serviços'],
                       fill_color='paleturquoise',
                       align='left'),
            cells=dict(values=[table_data['Cidade de Origem'],
                              table_data['interesse_politica'],
                              table_data['conhece_servicos']],
                       fill_color='lavender',
                       align='left'))
        ])

        return (
            f"{total_atendimentos:,}",
            f"{total_interesse:,}",
            f"{total_conhece:,}",
            fig_interesse,
            fig_deficiencia,
            fig_table
        )

    return dash_app.server
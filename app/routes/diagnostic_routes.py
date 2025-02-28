from flask import Blueprint, render_template
from app.services.google_sheets_service import diagnosticar_planilhas
import logging

diagnostic_bp = Blueprint("diagnostic", __name__)

# Configuração de logging (opcional, para depuração)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@diagnostic_bp.route("/diagnostico", methods=["GET"])
def diagnostico():
    try:
        # Obtém os dados do serviço Google Sheets
        dados = diagnosticar_planilhas()

        # Verifica se os dados estão no formato esperado
        if dados is None or not isinstance(dados, list):
            logger.warning("Dados retornados não são uma lista válida. Usando lista vazia.")
            dados = []
        
        if not all(isinstance(registro, dict) for registro in dados):
            logger.warning("Alguns registros não são dicionários. Filtrando dados inválidos.")
            dados = [registro for registro in dados if isinstance(registro, dict)]

        # Calcula as estatísticas gerais
        total_registros = len(dados)
        cidades_unicas = len(set(registro.get('3 - Cidade', '') for registro in dados))
        
        # Calcula deficiências mais comuns
        deficiencias_comuns = {}
        for registro in dados:
            deficiencia = registro.get('4 - Qual o tipo de deficiência?', 'Não informado')
            deficiencias_comuns[deficiencia] = deficiencias_comuns.get(deficiencia, 0) + 1
        # Formata como lista de tuplas ordenadas (deficiência, contagem)
        deficiencias_comuns = sorted(deficiencias_comuns.items(), key=lambda x: x[1], reverse=True)[:3]  # Top 3

        # Calcula os pontos de atenção (case-insensitive para "Sim")
        conhece_sepd = len([
            r for r in dados 
            if r.get('5 - Você conhece todos os atendimentos e serviços oferecidos pela SEPD (Secretaria da Pessoa com Deficiência)?', '').lower() == 'sim'
        ])
        interessados_politica = len([
            r for r in dados 
            if r.get('9 - Se interessa por política?', '').lower() == 'sim'
        ])

        # Renderiza a página HTML passando os dados e estatísticas
        return render_template(
            'diagnostico.html',
            dados=dados,
            total_registros=total_registros,
            cidades_unicas=cidades_unicas,
            deficiencias_comuns=deficiencias_comuns,
            conhece_sepd=conhece_sepd,
            interessados_politica=interessados_politica
        )

    except Exception as e:
        logger.error(f"Erro ao processar a rota /diagnostico: {e}")
        # Renderiza a página com dados vazios em caso de erro
        return render_template(
            'diagnostico.html',
            dados=[],
            total_registros=0,
            cidades_unicas=0,
            deficiencias_comuns=[],
            conhece_sepd=0,
            interessados_politica=0
        )
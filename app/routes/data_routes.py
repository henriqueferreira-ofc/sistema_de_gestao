from flask import Blueprint, render_template
from app.services.data_service import obter_dados_planilha

data_bp = Blueprint('data', __name__)

@data_bp.route('/dados')
def exibir_dados():
    try:
        dados = obter_dados_planilha()
        if 'erro' in dados:
            return render_template('dados.html', erro=dados['erro'])
        print(dados)  # Adicione este print para verificar os dados no console
        return render_template('dados.html', dados=dados, erro=None)
    except Exception as e:
        return render_template('dados.html', erro=str(e))
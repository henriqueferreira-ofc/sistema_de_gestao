from flask import Blueprint, render_template
from app.services.data_service import gerar_graficos

graph_bp = Blueprint("graph", __name__)

@graph_bp.route("/visualizar", methods=["GET"])
def visualizar_graficos():
    graficos = gerar_graficos()
    return render_template("graphs.html", graficos=graficos)

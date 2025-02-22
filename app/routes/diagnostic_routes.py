from flask import Blueprint, jsonify
from app.services.google_sheets_service import diagnosticar_planilhas

diagnostic_bp = Blueprint("diagnostic", __name__)

@diagnostic_bp.route("/diagnostico", methods=["GET"])
def diagnostico():
    resultado = diagnosticar_planilhas()
    return jsonify(resultado)

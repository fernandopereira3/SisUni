from flask import render_template, Blueprint
from Data.conexao import cpppac

cpppac = cpppac()

frequencia_bp = Blueprint("frequencia", __name__, template_folder="templates")

@frequencia_bp.route("/frequencia", methods=["GET"])
def definir_frequencia():
    try:
        # Definir hoje
        hoje_inicio = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        hoje_fim = datetime.datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999
        )
        
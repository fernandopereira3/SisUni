from flask import render_template, Blueprint
from Data.conexao import cpppac

cpppac = cpppac()

simic_bp = Blueprint("simic", __name__, template_folder="templates")


@simic_bp.route("/simic", methods=["GET"])
def simic():
    """Página principal de simic"""
    return render_template("simic.html")


@simic_bp.route("/simic/novo-cadastro/<matricula>", methods=["GET"])
def novo_cadastro(matricula):
    """Página de novo cadastro"""
    return render_template("novo_cadastro.html", matricula=matricula)

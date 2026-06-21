from flask import render_template, Blueprint
import datetime
from Data.conexao import cpppac

cpppac = cpppac()

frequencia_bp = Blueprint("frequencia", __name__, template_folder="templates")


@frequencia_bp.route("/freguencia")
def definir_frequencia():
    return render_template("frequencia.html")

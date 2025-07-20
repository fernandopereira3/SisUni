from flask import render_template, flash, redirect, url_for, Blueprint
import pandas as pd
from Data.conexao import conexao

# Criar o blueprint
rotas_saida_bp = Blueprint("rotas_saida", __name__)
db = conexao()


@rotas_saida_bp.route("/saida", methods=["GET"])
def lista_saida():
    return render_template("saida.html")

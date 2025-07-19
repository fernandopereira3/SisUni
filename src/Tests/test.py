from flask import Flask, render_template, request, Blueprint
from Data.conexao import conexao
from Funcoes.funcoes import construir_tabela_trabalho

bp_test = Blueprint('test',  __name__, 
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/static')
db = conexao()

@bp_test.route('/test/trab')
def test_trab():
    return render_template('404.html')
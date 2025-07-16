from flask import render_template, Blueprint
from Funcoes.funcoes import construir_tabela_trabalho
from Data.conexao import conexao
db = conexao()

trabalho_bp = Blueprint('trabalho', __name__, template_folder='templates')

def conf_trabalho(matricula):
    """Verifica se uma matrícula existe na coleção 'trab'"""
    try:
        # Verificar diretamente no MongoDB
        resultado = db.trab.find_one({'matricula': str(matricula)})
        return resultado is not None
    except Exception as e:
        print(f'Erro ao verificar matrícula: {e}')
        return False

        
@trabalho_bp.route('/trabalho', methods=['GET'])
def trabalho():
    """Página principal de trabalho"""
    return render_template('trabalho.html')

@trabalho_bp.route('/trabalho/api', methods=['GET'])
def api_trabalho():
    """API para obter os dados em formato JSON"""
    try:
        if 'trab' in db.list_collection_names():
            documentos = list(db.trab.find({}, {'_id': 0}))
            return {
                'status': 'success',
                'data': documentos,
                'count': len(documentos),
            }
        else:
            return {
                'status': 'warning',
                'message': 'Coleção não encontrada',
                'data': [],
                'count': 0,
            }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

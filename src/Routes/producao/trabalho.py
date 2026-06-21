from flask import render_template, Blueprint
from Data.conexao import cpppac

cpppac = cpppac()

trabalho_bp = Blueprint("trabalho", __name__, template_folder="templates")


def conf_trabalho(matricula):
    try:
        # Verificar diretamente no MongoDB
        resultado = cpppac.trabalho.find_one({"matricula": str(matricula)})
        return resultado is not None
    except Exception as e:
        print(f"Erro ao verificar matrícula: {e}")
        return False


@trabalho_bp.route("/trabalho", methods=["GET"])
def trabalho():
    """Página principal de trabalho"""
    return render_template("trabalho.html")


@trabalho_bp.route("/trabalho/api", methods=["GET"])
def api_trabalho():
    """API para obter os dados em formato JSON"""
    try:
        if "trabalho" in cpppac.list_collection_names():
            documentos = list(cpppac.trabalho.find({}, {"_id": 0}))
            return {
                "status": "success",
                "data": documentos,
                "count": len(documentos),
            }
        else:
            return {
                "status": "warning",
                "message": "Coleção não encontrada",
                "data": [],
                "count": 0,
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

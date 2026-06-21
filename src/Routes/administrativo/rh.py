from flask import (
    render_template,
    request,
    Blueprint,
    session,
    redirect,
    url_for,
    jsonify,
)
import datetime
from functools import wraps
from Data.conexao import cpppac

rh_bp = Blueprint("rh", __name__)
cpppac = cpppac()


def verificar_acesso_rh():
    if "user" not in session:
        if request.is_json or "/api/" in request.path:
            return jsonify({"status": "error", "message": "Usuário não logado"})
        return redirect(url_for("rotas.login"))
    usuario = cpppac.usuarios.find_one({"username": session["user"]})
    setor = str(usuario.get("setor", "")).strip().lower() if usuario else ""
    if setor not in ("cpd", "administrativo", "rh"):
        if request.is_json or "/api/" in request.path:
            return jsonify({"status": "error", "message": "Acesso negado"})
        return render_template(
            "401.html", message="Acesso restrito ao setor administrativo"
        )
    return None


def require_rh(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        resp = verificar_acesso_rh()
        if resp is not None:
            return resp
        return f(*args, **kwargs)

    return decorated


@rh_bp.route("/funcionarios", methods=["GET"])
def funcionarios():
    username = session.get("user")
    usuario = cpppac.usuarios.find_one({"username": username})
    return render_template("funcionarios.html", usuario=usuario)


@rh_bp.route("/api/listar_funcionarios", methods=["GET"])
@require_rh
def listar_funcionarios():
    try:
        funcionarios = list(cpppac.usuarios.find({}, {"_id": 0, "password": 0}))
        for func in funcionarios:
            login_times = func.get("login_times", [])
            func["total_logins"] = (
                len(login_times) if isinstance(login_times, list) else 0
            )
            func["ultimo_login"] = login_times[-1] if login_times else "Nunca"
            func.pop("login_times", None)
            folgas = func.get("folgas", [])
            func["total_folgas"] = len(folgas) if isinstance(folgas, list) else 0
            func.pop("folgas", None)
        return jsonify(
            {"success": True, "funcionarios": funcionarios, "total": len(funcionarios)}
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"})


@rh_bp.route("/api/criar_funcionario", methods=["POST"])
@require_rh
def criar_funcionario():
    try:
        username_criador = session["user"]
        user_criador = cpppac.usuarios.find_one({"username": username_criador})
        if not user_criador or not user_criador.get("star", False):
            return jsonify({"status": "error", "message": "Acesso negado"})

        data = request.get_json()
        nome_completo = data.get("nome_completo", "").strip()
        username = data.get("username", "").strip().lower().replace(" ", "")
        turno = data.get("turno")
        lvl = data.get("lvl")

        if not nome_completo or not username or not turno:
            return jsonify(
                {
                    "status": "error",
                    "message": "Nome completo, username e turno são obrigatórios",
                }
            )

        if cpppac.usuarios.find_one({"username": username}):
            return jsonify(
                {"status": "error", "message": f"Username '{username}' já existe"}
            )

        novo_funcionario = {
            "username": username,
            "nome_completo": nome_completo,
            "turno": turno,
            "lvl": lvl,
            "login_times": [datetime.datetime.now()],
            "folgas": [],
            "data_criacao": datetime.datetime.now(),
            "criado_por": username_criador,
        }
        resultado = cpppac.usuarios.insert_one(novo_funcionario)
        if resultado.inserted_id:
            return jsonify(
                {
                    "status": "success",
                    "message": "Funcionário criado com sucesso",
                    "username": username,
                }
            )
        return jsonify({"status": "error", "message": "Erro ao criar funcionário"})
    except Exception:
        return jsonify({"status": "error", "message": "Erro interno do servidor"})


@rh_bp.route("/api/editar_funcionario/<username>", methods=["PUT"])
@require_rh
def editar_funcionario(username):
    try:
        username_editor = session.get("user")
        data = request.get_json()
        nome = data.get("nome", "").strip()
        turno = data.get("turno", "")
        lvl = data.get("lvl")

        if not nome or not turno:
            return jsonify({"message": "Nome e turno são obrigatórios"}), 400

        resultado = cpppac.usuarios.update_one(
            {"username": username},
            {
                "$set": {
                    "nome_completo": nome,
                    "turno": turno,
                    "lvl": lvl,
                    "editado_em": datetime.datetime.now(),
                    "editado_por": username_editor,
                }
            },
        )
        if resultado.modified_count > 0:
            return jsonify({"message": "Funcionário editado com sucesso"}), 200
        return jsonify({"message": "Nenhuma alteração foi feita"}), 400
    except Exception as e:
        return jsonify({"message": f"Erro interno: {str(e)}"}), 500


@rh_bp.route("/api/excluir_funcionario/<username>", methods=["DELETE"])
@require_rh
def excluir_funcionario(username):
    try:
        username_editor = session.get("user")
        if username == username_editor:
            return jsonify({"message": "Você não pode excluir sua própria conta"}), 400

        funcionario = cpppac.usuarios.find_one({"username": username})
        if not funcionario:
            return jsonify({"message": "Funcionário não encontrado"}), 404

        nome_funcionario = funcionario.get("nome_completo", username)
        resultado = cpppac.usuarios.delete_one({"username": username})
        if resultado.deleted_count > 0:
            return jsonify(
                {"message": f"Funcionário {nome_funcionario} excluído com sucesso"}
            ), 200
        return jsonify({"message": "Funcionário não encontrado para exclusão"}), 404
    except Exception as e:
        return jsonify({"message": f"Erro interno: {str(e)}"}), 500

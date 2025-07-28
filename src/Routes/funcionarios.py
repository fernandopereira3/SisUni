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
import re
from Data.conexao import conexao
from Funcoes.funcoes import PesquisaForm, construir_tabela

# Criar o blueprint
funcionarios_bp = Blueprint("funcionarios", __name__)
db = conexao()


@funcionarios_bp.route("/funcionarios", methods=["GET"])
def funcionarios():
    # Verificar se o usuário está logado
    if "user" not in session:
        return redirect(url_for("rotas.login"))

    # Buscar o usuário na coleção usuarios
    username = session["user"]
    user = db.usuarios.find_one({"username": username})

    # Verificar se o usuário existe e tem turno 1
    if not user or user.get("turno") != "1":
        return render_template(
            "acesso_negado.html", message="Acesso restrito ao turno 1"
        )

    return render_template("funcionarios.html")


@funcionarios_bp.route("/api/pesquisar_funcionarios", methods=["POST"])
def pesquisar_funcionarios():
    # Verificar se o usuário está logado e tem turno 1
    if "user" not in session:
        return jsonify({"status": "error", "message": "Usuário não logado"})

    username = session["user"]
    user = db.usuarios.find_one({"username": username})

    if not user or user.get("turno") != "1":
        return jsonify({"status": "error", "message": "Acesso negado"})

    try:
        data = request.get_json()
        nome = data.get("nome", "").strip()
        departamento = data.get("departamento", "").strip()
        status = data.get("status", "").strip()
        turno_pesquisa = data.get("turno", "").strip()

        # Construir query para pesquisa na coleção usuarios
        query = {}

        # Filtrar por nome se fornecido
        if nome:
            query["username"] = {"$regex": nome, "$options": "i"}

        # Filtrar por turno se fornecido
        if turno_pesquisa:
            query["turno"] = turno_pesquisa

        # Buscar funcionários na coleção usuarios
        funcionarios = list(db.usuarios.find(query).sort("username", 1))

        # Construir HTML da tabela de resultados
        html_tabela = construir_tabela_funcionarios(funcionarios)

        return jsonify(
            {"status": "success", "html": html_tabela, "total": len(funcionarios)}
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def construir_tabela_funcionarios(funcionarios):
    if not funcionarios:
        return '<div class="alert alert-info">Nenhum funcionário encontrado.</div>'

    html = """
    <div class="table-responsive">
        <table class="table table-striped table-hover">
            <thead class="table-dark">
                <tr>
                    <th>Nome de Usuário</th>
                    <th>Turno</th>
                    <th>Último Login</th>
                    <th>Total de Logins</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
    """

    for funcionario in funcionarios:
        username = funcionario.get("username", "N/A")
        turno = funcionario.get("turno", "N/A")
        login_times = funcionario.get("login_times", [])

        # Último login
        ultimo_login = "Nunca"
        if login_times:
            ultimo_login = (
                login_times[-1].strftime("%d/%m/%Y %H:%M")
                if isinstance(login_times[-1], datetime.datetime)
                else str(login_times[-1])
            )

        # Total de logins
        total_logins = len(login_times)

        html += f"""
            <tr>
                <td>{username}</td>
                <td><span class="badge bg-primary">Turno {turno}</span></td>
                <td>{ultimo_login}</td>
                <td>{total_logins}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="verDetalhes('{username}')">
                        <i class="fas fa-eye"></i> Ver
                    </button>
                    <button class="btn btn-sm btn-outline-warning" onclick="editarFuncionario('{username}')">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                </td>
            </tr>
        """

    html += """
            </tbody>
        </table>
    </div>
    """

    return html


@funcionarios_bp.route("/funcionarios/folgas", methods=["GET"])
def folgas():
    # Verificar se o usuário está logado
    if "user" not in session:
        return redirect(url_for("rotas.login"))

    # Buscar o usuário na coleção usuarios
    username = session["user"]
    user = db.usuarios.find_one({"username": username})

    # Verificar se o usuário existe
    if not user:
        return render_template("acesso_negado.html", message="Usuário não encontrado")

    try:
        # Buscar folgas já agendadas do usuário
        folgas_agendadas = list(db.folgas.find({"username": username}).sort("data", 1))

        # Converter ObjectId para string para evitar erro de serialização JSON
        for folga in folgas_agendadas:
            if "_id" in folga:
                folga["_id"] = str(folga["_id"])

        return render_template("folgas.html", folgas=folgas_agendadas)
    except Exception as e:
        return f"Erro ao carregar folgas: {str(e)}"


@funcionarios_bp.route("/api/agendar_folga", methods=["POST"])
def agendar_folga():
    # Verificar se o usuário está logado
    if "user" not in session:
        return jsonify({"status": "error", "message": "Usuário não logado"})

    username = session["user"]
    user = db.usuarios.find_one({"username": username})

    if not user:
        return jsonify({"status": "error", "message": "Usuário não encontrado"})

    try:
        data = request.get_json()
        data_folga = data.get("data")
        motivo = data.get("motivo", "").strip()

        if not data_folga:
            return jsonify({"status": "error", "message": "Data é obrigatória"})

        # Converter string para datetime
        data_obj = datetime.datetime.strptime(data_folga, "%Y-%m-%d")

        # Verificar se já existe folga agendada para esta data
        folga_existente = db.folgas.find_one({"username": username, "data": data_obj})

        if folga_existente:
            return jsonify(
                {
                    "status": "error",
                    "message": "Já existe folga agendada para esta data",
                }
            )

        # Criar novo agendamento de folga
        nova_folga = {
            "username": username,
            "data": data_obj,
            "motivo": motivo,
            "status": "pendente",
            "data_criacao": datetime.datetime.now(),
            "aprovado_por": None,
            "data_aprovacao": None,
        }

        # Inserir no banco
        resultado = db.folgas.insert_one(nova_folga)

        if resultado.inserted_id:
            return jsonify(
                {
                    "status": "success",
                    "message": "Folga agendada com sucesso",
                    "id": str(resultado.inserted_id),
                }
            )
        else:
            return jsonify({"status": "error", "message": "Erro ao agendar folga"})

    except ValueError:
        return jsonify({"status": "error", "message": "Formato de data inválido"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@funcionarios_bp.route("/api/cancelar_folga", methods=["POST"])
def cancelar_folga():
    # Verificar se o usuário está logado
    if "user" not in session:
        return jsonify({"status": "error", "message": "Usuário não logado"})

    username = session["user"]
    user = db.usuarios.find_one({"username": username})

    if not user:
        return jsonify({"status": "error", "message": "Usuário não encontrado"})

    try:
        data = request.get_json()
        folga_id = data.get("id")

        if not folga_id:
            return jsonify({"status": "error", "message": "ID da folga é obrigatório"})

        from bson import ObjectId

        # Verificar se a folga existe e pertence ao usuário
        folga = db.folgas.find_one({"_id": ObjectId(folga_id), "username": username})

        if not folga:
            return jsonify({"status": "error", "message": "Folga não encontrada"})

        # Verificar se a folga ainda pode ser cancelada (não aprovada)
        if folga.get("status") == "aprovada":
            return jsonify(
                {
                    "status": "error",
                    "message": "Não é possível cancelar folga já aprovada",
                }
            )

        # Remover a folga
        resultado = db.folgas.delete_one({"_id": ObjectId(folga_id)})

        if resultado.deleted_count > 0:
            return jsonify(
                {"status": "success", "message": "Folga cancelada com sucesso"}
            )
        else:
            return jsonify({"status": "error", "message": "Erro ao cancelar folga"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

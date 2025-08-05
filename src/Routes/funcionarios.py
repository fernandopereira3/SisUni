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
from bson import ObjectId
from Data.conexao import conexao

# Criar o blueprint
funcionarios_bp = Blueprint("funcionarios", __name__)
db = conexao()


# Decorador para verificar autenticação e autorização
def require_turno1(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar se o usuário está logado
        if "user" not in session:
            if request.is_json or "/api/" in request.path:
                return jsonify({"status": "error", "message": "Usuário não logado"})
            return redirect(url_for("rotas.login"))

        # Buscar o usuário na coleção usuarios
        username = session["user"]
        user = db.usuarios.find_one({"username": username})

        # Verificar se o usuário existe e tem turno 1
        if not user or user.get("turno") != "1":
            if request.is_json or "/api/" in request.path:
                return jsonify({"status": "error", "message": "Acesso negado"})
            return render_template("401.html", message="Acesso restrito ao turno 1")

        return f(*args, **kwargs)

    return decorated_function


@funcionarios_bp.route("/funcionarios", methods=["GET"])
@require_turno1
def funcionarios():
    return render_template("funcionarios.html")


@funcionarios_bp.route("/funcionarios/folgas", methods=["GET"])
@require_turno1
def folgas():
    """Página de gerenciamento de folgas"""
    username = session["user"]

    try:
        # Buscar usuário e suas folgas
        usuario = db.usuarios.find_one({"username": username})
        folgas_agendadas = []

        if usuario:
            # Garantir que o usuário tem o campo folgas inicializado
            if "folgas" not in usuario:
                db.usuarios.update_one({"username": username}, {"$set": {"folgas": []}})
                folgas_agendadas = []
            else:
                folgas_agendadas = usuario["folgas"]

                # Converter datas datetime para strings para serialização JSON
                for folga in folgas_agendadas:
                    if isinstance(folga.get("data"), datetime.datetime):
                        folga["data"] = folga["data"].strftime("%Y-%m-%d")
                    if isinstance(folga.get("data_criacao"), datetime.datetime):
                        folga["data_criacao"] = folga["data_criacao"].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    if isinstance(folga.get("data_aprovacao"), datetime.datetime):
                        folga["data_aprovacao"] = folga["data_aprovacao"].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                # Ordenar por data (agora como strings)
                folgas_agendadas.sort(key=lambda x: x.get("data", "1900-01-01"))

        return render_template("folgas.html", folgas=folgas_agendadas, usuario=usuario)
    except Exception as e:
        return f"Erro ao carregar folgas: {str(e)}"


@funcionarios_bp.route("/api/folgas_mes", methods=["GET"])
@require_turno1
def folgas_mes():
    """Buscar todas as folgas de um mês específico"""
    try:
        # Obter parâmetros de ano e mês da query string
        ano = request.args.get("ano", type=int)
        mes = request.args.get("mes", type=int)

        if not ano or not mes:
            # Se não especificado, usar mês atual
            hoje = datetime.datetime.now()
            ano = hoje.year
            mes = hoje.month

        # Calcular primeiro e último dia do mês
        primeiro_dia = datetime.datetime(ano, mes, 1)
        if mes == 12:
            ultimo_dia = datetime.datetime(ano + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            ultimo_dia = datetime.datetime(ano, mes + 1, 1) - datetime.timedelta(days=1)

        # Buscar todos os usuários que têm folgas no mês
        usuarios = list(
            db.usuarios.find(
                {
                    "folgas": {
                        "$elemMatch": {
                            "data": {"$gte": primeiro_dia, "$lte": ultimo_dia},
                            "status": {"$in": ["pendente", "aprovada"]},
                        }
                    }
                }
            )
        )

        # Extrair folgas do mês de cada usuário
        folgas_com_nomes = []
        for usuario in usuarios:
            folgas_usuario = usuario.get("folgas", [])
            for folga in folgas_usuario:
                # Verificar se a folga está no período desejado
                if (
                    folga.get("data")
                    and primeiro_dia <= folga["data"] <= ultimo_dia
                    and folga.get("status") in ["pendente", "aprovada"]
                ):
                    folga_info = {
                        "data": folga["data"].strftime("%Y-%m-%d"),
                        "username": usuario["username"],
                        "nome_completo": usuario.get(
                            "nome_completo", usuario["username"]
                        ),
                        "status": folga["status"],
                    }
                    folgas_com_nomes.append(folga_info)

        # Ordenar por data
        folgas_com_nomes.sort(key=lambda x: x["data"])

        return jsonify({"status": "success", "folgas": folgas_com_nomes})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@funcionarios_bp.route("/api/listar_funcionarios", methods=["GET"])
@require_turno1
def listar_funcionarios():
    """API para listar funcionários baseado nas permissões do usuário"""
    try:
        # Verificar se o usuário tem permissão (star = true)
        username = session.get("user")
        if not username:
            return jsonify({"success": False, "message": "Usuário não autenticado"})

        usuario_atual = db.usuarios.find_one({"username": username})
        if not usuario_atual or not usuario_atual.get("star", False):
            return jsonify(
                {
                    "success": False,
                    "message": "Acesso negado. Permissões insuficientes.",
                }
            )

        # Definir filtro baseado no usuário
        filtro = {}

        # Se o usuário é fernandopereira, pode ver todos os funcionários
        if username == "fernandopereira":
            filtro = {}  # Sem filtro, vê todos
        else:
            # Usuários com star = true veem apenas funcionários do mesmo turno
            turno_usuario = usuario_atual.get("turno")
            if turno_usuario:
                filtro = {"turno": turno_usuario}
            else:
                # Se não tem turno definido, não vê ninguém
                filtro = {"turno": "__turno_inexistente__"}

        # Buscar funcionários baseado no filtro
        funcionarios = list(db.usuarios.find(filtro, {"_id": 0}))

        # Processar dados para melhor visualização
        for funcionario in funcionarios:
            # Processar login_times
            if "login_times" in funcionario and isinstance(
                funcionario["login_times"], list
            ):
                funcionario["total_logins"] = len(funcionario["login_times"])
                if funcionario["login_times"]:
                    # Pegar o último login (mais recente)
                    funcionario["ultimo_login"] = funcionario["login_times"][-1]
                else:
                    funcionario["ultimo_login"] = "Nunca"
                # Remover o array completo para economizar dados
                del funcionario["login_times"]
            else:
                funcionario["total_logins"] = 0
                funcionario["ultimo_login"] = "Nunca"

            # Processar folgas (opcional, para não sobrecarregar)
            if "folgas" in funcionario:
                if isinstance(funcionario["folgas"], list):
                    funcionario["total_folgas"] = len(funcionario["folgas"])
                # Remover folgas detalhadas para economizar dados
                del funcionario["folgas"]
            else:
                funcionario["total_folgas"] = 0

        return jsonify(
            {"success": True, "funcionarios": funcionarios, "total": len(funcionarios)}
        )

    except Exception as e:
        print(f"Erro ao listar funcionários: {str(e)}")
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"})


@funcionarios_bp.route("/api/editar_funcionario/<username>", methods=["PUT"])
@require_turno1
def editar_funcionario(username):
    """API para editar dados de um funcionário"""
    try:
        # Verificar se o usuário tem permissão (star = true)
        username_editor = session.get("user")
        if not username_editor:
            return jsonify({"message": "Usuário não autenticado"}), 401

        usuario_editor = db.usuarios.find_one({"username": username_editor})
        if not usuario_editor or not usuario_editor.get("star", False):
            return jsonify({"message": "Acesso negado. Permissões insuficientes."}), 403

        # Buscar o funcionário a ser editado
        funcionario = db.usuarios.find_one({"username": username})
        if not funcionario:
            return jsonify({"message": "Funcionário não encontrado"}), 404

        # Verificar se o usuário pode editar este funcionário (mesmo turno, exceto fernandopereira)
        if username_editor != "fernandopereira":
            turno_editor = usuario_editor.get("turno")
            turno_funcionario = funcionario.get("turno")
            if turno_editor != turno_funcionario:
                return jsonify(
                    {"message": "Você só pode editar funcionários do seu turno"}
                ), 403

        data = request.get_json()
        nome = data.get("nome", "").strip()
        turno = data.get("turno", "")
        star = data.get("star", False)

        # Validação básica
        if not nome or not turno:
            return jsonify({"message": "Nome e turno são obrigatórios"}), 400

        # Atualizar dados do funcionário
        resultado = db.usuarios.update_one(
            {"username": username},
            {
                "$set": {
                    "nome_completo": nome,
                    "turno": turno,
                    "star": star,
                    "editado_em": datetime.datetime.now(),
                    "editado_por": username_editor,
                }
            },
        )

        if resultado.modified_count > 0:
            return jsonify({"message": "Funcionário editado com sucesso"}), 200
        else:
            return jsonify({"message": "Nenhuma alteração foi feita"}), 400

    except Exception as e:
        print(f"Erro ao editar funcionário: {str(e)}")
        return jsonify({"message": f"Erro interno: {str(e)}"}), 500


@funcionarios_bp.route("/api/excluir_funcionario/<username>", methods=["DELETE"])
@require_turno1
def excluir_funcionario(username):
    """API para excluir um funcionário"""
    try:
        # Verificar se o usuário tem permissão (star = true)
        username_editor = session.get("user")
        if not username_editor:
            return jsonify({"message": "Usuário não autenticado"}), 401

        usuario_editor = db.usuarios.find_one({"username": username_editor})
        if not usuario_editor or not usuario_editor.get("star", False):
            return jsonify({"message": "Acesso negado. Permissões insuficientes."}), 403

        # Buscar o funcionário a ser excluído
        funcionario = db.usuarios.find_one({"username": username})
        if not funcionario:
            return jsonify({"message": "Funcionário não encontrado"}), 404

        # Não permitir auto-exclusão
        if username == username_editor:
            return jsonify({"message": "Você não pode excluir sua própria conta"}), 400

        # Verificar se o usuário pode excluir este funcionário (mesmo turno, exceto fernandopereira)
        if username_editor != "fernandopereira":
            turno_editor = usuario_editor.get("turno")
            turno_funcionario = funcionario.get("turno")
            if turno_editor != turno_funcionario:
                return jsonify(
                    {"message": "Você só pode excluir funcionários do seu turno"}
                ), 403

        nome_funcionario = funcionario.get("nome_completo", username)

        # Excluir funcionário
        resultado = db.usuarios.delete_one({"username": username})

        if resultado.deleted_count > 0:
            return jsonify(
                {"message": f"Funcionário {nome_funcionario} excluído com sucesso"}
            ), 200
        else:
            return jsonify(
                {"message": "Funcionário não foi encontrado para exclusão"}
            ), 404

    except Exception as e:
        print(f"Erro ao excluir funcionário: {str(e)}")
        return jsonify({"message": f"Erro interno: {str(e)}"}), 500


@funcionarios_bp.route("/api/aprovar_folga", methods=["POST"])
@require_turno1
def aprovar_folga():
    """Aprovar uma folga"""
    try:
        # Verificar se o usuário tem permissão (star = true)
        username_aprovador = session["user"]
        user_aprovador = db.usuarios.find_one({"username": username_aprovador})

        if not user_aprovador or not user_aprovador.get("star", False):
            return jsonify({"status": "error", "message": "Acesso negado"})

        data = request.get_json()
        username = data.get("username")
        data_folga = data.get("data")

        if not username or not data_folga:
            return jsonify(
                {"status": "error", "message": "Username e data são obrigatórios"}
            )

        # Converter string para datetime
        data_obj = datetime.datetime.strptime(data_folga, "%Y-%m-%d")

        # Atualizar status da folga para aprovada
        resultado = db.usuarios.update_one(
            {
                "username": username,
                "folgas.data": data_obj,
                "folgas.status": "pendente",
            },
            {
                "$set": {
                    "folgas.$.status": "aprovada",
                    "folgas.$.aprovado_por": username_aprovador,
                    "folgas.$.data_aprovacao": datetime.datetime.now(),
                }
            },
        )

        if resultado.modified_count > 0:
            return jsonify(
                {"status": "success", "message": "Folga aprovada com sucesso"}
            )
        else:
            return jsonify(
                {"status": "error", "message": "Folga não encontrada ou já aprovada"}
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@funcionarios_bp.route("/api/criar_funcionario", methods=["POST"])
@require_turno1
def criar_funcionario():
    """Criar novo funcionário"""
    try:
        # Verificar se o usuário tem permissão (star = true)
        username_criador = session["user"]
        user_criador = db.usuarios.find_one({"username": username_criador})

        if not user_criador or not user_criador.get("star", False):
            return jsonify({"status": "error", "message": "Acesso negado"})

        data = request.get_json()
        nome_completo = data.get("nome_completo", "").strip()
        username = data.get("username", "").strip().lower().replace(" ", "")
        turno = data.get("turno")
        star = data.get("star", False)

        # Validação
        if not nome_completo or not username or not turno:
            return jsonify(
                {
                    "status": "error",
                    "message": "Nome completo, username e turno são obrigatórios",
                }
            )

        # Verificar se o username já existe
        usuario_existente = db.usuarios.find_one({"username": username})
        if usuario_existente:
            return jsonify(
                {"status": "error", "message": f"Username '{username}' já existe"}
            )

        # Criar novo funcionário
        novo_funcionario = {
            "username": username,
            "nome_completo": nome_completo,
            "turno": turno,
            "star": star,
            "login_times": [datetime.datetime.now()],
            "folgas": [],
            "data_criacao": datetime.datetime.now(),
            "criado_por": username_criador,
        }

        # Inserir no banco
        resultado = db.usuarios.insert_one(novo_funcionario)

        if resultado.inserted_id:
            return jsonify(
                {
                    "status": "success",
                    "message": "Funcionário criado com sucesso",
                    "username": username,
                    "nome_completo": nome_completo,
                    "turno": turno,
                    "star": star,
                }
            )
        else:
            return jsonify({"status": "error", "message": "Erro ao criar funcionário"})

    except Exception as e:
        print(f"Erro ao criar funcionário: {e}")
        return jsonify({"status": "error", "message": "Erro interno do servidor"})


@funcionarios_bp.route("/api/editar_folga", methods=["POST"])
@require_turno1
def editar_folgas():
    """Edita folgas de terceiros"""
    try:
        # Verificar se o usuário tem permissão (star = true)
        username_editor = session["user"]
        user_editor = db.usuarios.find_one({"username": username_editor})

        if not user_editor or not user_editor.get("star", False):
            return jsonify({"status": "error", "message": "Acesso negado"})

        data = request.get_json()
        username = data.get("username")
        data_folga_antiga = data.get("data_antiga")
        data_folga_nova = data.get("data_nova")
        novo_motivo = data.get("motivo")
        acao = data.get("acao")  # "editar" ou "apagar"

        if not username or not data_folga_antiga:
            return jsonify(
                {
                    "status": "error",
                    "message": "Username e data antiga são obrigatórios",
                }
            )

        # Converter string para datetime
        data_antiga_obj = datetime.datetime.strptime(data_folga_antiga, "%Y-%m-%d")

        if acao == "apagar":
            # Apagar a folga
            resultado = db.usuarios.update_one(
                {"username": username}, {"$pull": {"folgas": {"data": data_antiga_obj}}}
            )

            if resultado.modified_count > 0:
                return jsonify(
                    {"status": "success", "message": "Folga apagada com sucesso"}
                )
            else:
                return jsonify({"status": "error", "message": "Folga não encontrada"})

        elif acao == "editar":
            if not data_folga_nova or not novo_motivo:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Data nova e motivo são obrigatórios para edição",
                    }
                )

            data_nova_obj = datetime.datetime.strptime(data_folga_nova, "%Y-%m-%d")

            # Editar a folga existente
            resultado = db.usuarios.update_one(
                {"username": username, "folgas.data": data_antiga_obj},
                {
                    "$set": {
                        "folgas.$.data": data_nova_obj,
                        "folgas.$.motivo": novo_motivo,
                        "folgas.$.editado_por": username_editor,
                        "folgas.$.data_edicao": datetime.datetime.now(),
                    }
                },
            )

            if resultado.modified_count > 0:
                return jsonify(
                    {"status": "success", "message": "Folga editada com sucesso"}
                )
            else:
                return jsonify({"status": "error", "message": "Folga não encontrada"})

        elif acao == "criar":
            if not data_folga_nova or not novo_motivo:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Data e motivo são obrigatórios para criar nova folga",
                    }
                )

            data_nova_obj = datetime.datetime.strptime(data_folga_nova, "%Y-%m-%d")

            # Verificar se já existe folga nesta data
            usuario_existente = db.usuarios.find_one(
                {"username": username, "folgas.data": data_nova_obj}
            )

            if usuario_existente:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Já existe uma folga agendada para esta data",
                    }
                )

            # Criar nova folga
            nova_folga = {
                "data": data_nova_obj,
                "motivo": novo_motivo,
                "status": "pendente",
                "criado_por": username_editor,
                "data_criacao": datetime.datetime.now(),
            }

            resultado = db.usuarios.update_one(
                {"username": username}, {"$push": {"folgas": nova_folga}}
            )

            if resultado.modified_count > 0:
                return jsonify(
                    {"status": "success", "message": "Nova folga criada com sucesso"}
                )
            else:
                return jsonify(
                    {"status": "error", "message": "Erro ao criar nova folga"}
                )
        else:
            return jsonify(
                {
                    "status": "error",
                    "message": "Ação inválida. Use 'editar', 'apagar' ou 'criar'",
                }
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@funcionarios_bp.route("/api/folgas_pendentes", methods=["GET"])
@require_turno1
def folgas_pendentes():
    """Buscar todas as folgas pendentes de aprovação"""
    try:
        # Verificar se o usuário tem permissão (star = true)
        username = session["user"]
        print(f"DEBUG: Username da sessão: {username}")
        user = db.usuarios.find_one({"username": username})
        print(f"DEBUG: Usuário encontrado: {user}")

        if not user or not user.get("star", False):
            print(
                f"DEBUG: Acesso negado - star: {user.get('star', False) if user else 'usuário não encontrado'}"
            )
            return jsonify({"status": "error", "message": "Acesso negado"})

        # Buscar todas as folgas pendentes
        pipeline = [
            {"$unwind": "$folgas"},
            {"$match": {"folgas.status": "pendente"}},
            {
                "$project": {
                    "username": 1,
                    "nome_completo": 1,
                    "data": "$folgas.data",
                    "motivo": "$folgas.motivo",
                    "status": "$folgas.status",
                }
            },
            {"$sort": {"data": 1}},
        ]

        folgas_pendentes = list(db.usuarios.aggregate(pipeline))

        # Converter ObjectIds e datas para string
        for folga in folgas_pendentes:
            # Converter ObjectId para string
            if "_id" in folga and isinstance(folga["_id"], ObjectId):
                folga["_id"] = str(folga["_id"])

            # Converter datas para string
            if isinstance(folga["data"], datetime.datetime):
                folga["data"] = folga["data"].strftime("%Y-%m-%d")

        return jsonify({"status": "success", "folgas": folgas_pendentes})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@funcionarios_bp.route("/api/agendar_folga", methods=["POST"])
@require_turno1
def agendar_folga():
    """Agendar folga para um funcionário"""
    username = session["user"]

    try:
        data = request.get_json()
        data_folga = data.get("data")
        motivo = data.get("motivo", "").strip()

        if not data_folga:
            return jsonify({"status": "error", "message": "Data é obrigatória"})

        # Converter string para datetime
        data_obj = datetime.datetime.strptime(data_folga, "%Y-%m-%d")

        # Buscar o usuário
        usuario = db.usuarios.find_one({"username": username})
        if not usuario:
            return jsonify({"status": "error", "message": "Usuário não encontrado"})

        # Garantir que o usuário tem o campo folgas inicializado
        if "folgas" not in usuario:
            db.usuarios.update_one({"username": username}, {"$set": {"folgas": []}})
            usuario["folgas"] = []

        # Verificar se já existe folga agendada para esta data
        folgas_usuario = usuario.get("folgas", [])
        for folga in folgas_usuario:
            if folga.get("data") == data_obj:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Já existe folga agendada para esta data",
                    }
                )

        # Criar novo agendamento de folga
        nova_folga = {
            "data": data_obj,
            "motivo": motivo,
            "status": "pendente",
            "data_criacao": datetime.datetime.now(),
            "aprovado_por": None,
            "data_aprovacao": None,
        }

        # Adicionar folga ao array do usuário
        resultado = db.usuarios.update_one(
            {"username": username}, {"$push": {"folgas": nova_folga}}
        )

        if resultado.modified_count > 0:
            return jsonify(
                {
                    "status": "success",
                    "message": "Folga agendada com sucesso",
                }
            )
        else:
            return jsonify({"status": "error", "message": "Erro ao agendar folga"})

    except ValueError:
        return jsonify({"status": "error", "message": "Formato de data inválido"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@funcionarios_bp.route("/api/cancelar_folga", methods=["POST"])
@require_turno1
def cancelar_folga():
    """Cancelar folga de um funcionário"""
    username = session["user"]

    try:
        data = request.get_json()
        data_folga = data.get("data")

        if not data_folga:
            return jsonify(
                {"status": "error", "message": "Data da folga é obrigatória"}
            )

        # Converter string para datetime
        data_obj = datetime.datetime.strptime(data_folga, "%Y-%m-%d")

        # Buscar o usuário e verificar se a folga existe
        usuario = db.usuarios.find_one({"username": username})
        if not usuario:
            return jsonify({"status": "error", "message": "Usuário não encontrado"})

        folgas_usuario = usuario.get("folgas", [])
        folga_encontrada = None

        for folga in folgas_usuario:
            if folga.get("data") == data_obj:
                folga_encontrada = folga
                break

        if not folga_encontrada:
            return jsonify({"status": "error", "message": "Folga não encontrada"})

        # Verificar se a folga ainda pode ser cancelada (não aprovada)
        if folga_encontrada.get("status") == "aprovada":
            return jsonify(
                {
                    "status": "error",
                    "message": "Não é possível cancelar folga já aprovada",
                }
            )

        # Remover a folga do array
        resultado = db.usuarios.update_one(
            {"username": username}, {"$pull": {"folgas": {"data": data_obj}}}
        )

        if resultado.modified_count > 0:
            return jsonify(
                {"status": "success", "message": "Folga cancelada com sucesso"}
            )
        else:
            return jsonify({"status": "error", "message": "Erro ao cancelar folga"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

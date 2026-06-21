from flask import render_template, request, Blueprint, session, redirect, url_for, jsonify
import datetime
from bson import ObjectId
from Data.conexao import cpppac

folgas_bp = Blueprint("folgas", __name__)
cpppac = cpppac()


def verificar_acesso_folgas():
    if "user" not in session:
        return redirect(url_for("rotas.login"))
    return None


@folgas_bp.route("/funcionarios/folgas", methods=["GET"])
def folgas():
    resp = verificar_acesso_folgas()
    if resp:
        return resp
    username = session["user"]
    try:
        usuario = cpppac.usuarios.find_one({"username": username})
        folgas_agendadas = []
        if usuario:
            if "folgas" not in usuario:
                cpppac.usuarios.update_one({"username": username}, {"$set": {"folgas": []}})
            else:
                folgas_agendadas = usuario["folgas"]
                for folga in folgas_agendadas:
                    if isinstance(folga.get("data"), datetime.datetime):
                        folga["data"] = folga["data"].strftime("%Y-%m-%d")
                    if isinstance(folga.get("data_criacao"), datetime.datetime):
                        folga["data_criacao"] = folga["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")
                    if isinstance(folga.get("data_aprovacao"), datetime.datetime):
                        folga["data_aprovacao"] = folga["data_aprovacao"].strftime("%Y-%m-%d %H:%M:%S")
                folgas_agendadas.sort(key=lambda x: x.get("data", "1900-01-01"))
        return render_template("folgas.html", folgas=folgas_agendadas, usuario=usuario)
    except Exception as e:
        return f"Erro ao carregar folgas: {str(e)}"


@folgas_bp.route("/api/folgas_mes", methods=["GET"])
def folgas_mes():
    resp = verificar_acesso_folgas()
    if resp:
        return resp
    try:
        ano = request.args.get("ano", type=int)
        mes = request.args.get("mes", type=int)
        if not ano or not mes:
            hoje = datetime.datetime.now()
            ano, mes = hoje.year, hoje.month

        primeiro_dia = datetime.datetime(ano, mes, 1)
        ultimo_dia = (
            datetime.datetime(ano + 1, 1, 1) - datetime.timedelta(days=1)
            if mes == 12
            else datetime.datetime(ano, mes + 1, 1) - datetime.timedelta(days=1)
        )

        usuarios = list(cpppac.usuarios.find({
            "folgas": {"$elemMatch": {
                "data": {"$gte": primeiro_dia, "$lte": ultimo_dia},
                "status": {"$in": ["pendente", "aprovada"]},
            }}
        }))

        folgas_com_nomes = []
        for usuario in usuarios:
            for folga in usuario.get("folgas", []):
                if (folga.get("data") and primeiro_dia <= folga["data"] <= ultimo_dia
                        and folga.get("status") in ["pendente", "aprovada"]):
                    folgas_com_nomes.append({
                        "data": folga["data"].strftime("%Y-%m-%d"),
                        "username": usuario["username"],
                        "nome_completo": usuario.get("nome_completo", usuario["username"]),
                        "status": folga["status"],
                    })

        folgas_com_nomes.sort(key=lambda x: x["data"])
        return jsonify({"status": "success", "folgas": folgas_com_nomes})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@folgas_bp.route("/api/agendar_folga", methods=["POST"])
def agendar_folga():
    resp = verificar_acesso_folgas()
    if resp:
        return resp
    username = session["user"]
    try:
        data = request.get_json()
        data_folga = data.get("data")
        motivo = data.get("motivo", "").strip()

        if not data_folga:
            return jsonify({"status": "error", "message": "Data é obrigatória"})

        data_obj = datetime.datetime.strptime(data_folga, "%Y-%m-%d")
        usuario = cpppac.usuarios.find_one({"username": username})
        if not usuario:
            return jsonify({"status": "error", "message": "Usuário não encontrado"})

        if "folgas" not in usuario:
            cpppac.usuarios.update_one({"username": username}, {"$set": {"folgas": []}})
            usuario["folgas"] = []

        for folga in usuario.get("folgas", []):
            if folga.get("data") == data_obj:
                return jsonify({"status": "error", "message": "Já existe folga agendada para esta data"})

        nova_folga = {"data": data_obj, "motivo": motivo, "status": "pendente",
                      "data_criacao": datetime.datetime.now(), "aprovado_por": None, "data_aprovacao": None}
        resultado = cpppac.usuarios.update_one({"username": username}, {"$push": {"folgas": nova_folga}})

        if resultado.modified_count > 0:
            return jsonify({"status": "success", "message": "Folga agendada com sucesso"})
        return jsonify({"status": "error", "message": "Erro ao agendar folga"})
    except ValueError:
        return jsonify({"status": "error", "message": "Formato de data inválido"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@folgas_bp.route("/api/cancelar_folga", methods=["POST"])
def cancelar_folga():
    resp = verificar_acesso_folgas()
    if resp:
        return resp
    username = session["user"]
    try:
        data = request.get_json()
        data_folga = data.get("data")
        if not data_folga:
            return jsonify({"status": "error", "message": "Data da folga é obrigatória"})

        data_obj = datetime.datetime.strptime(data_folga, "%Y-%m-%d")
        usuario = cpppac.usuarios.find_one({"username": username})
        if not usuario:
            return jsonify({"status": "error", "message": "Usuário não encontrado"})

        folga_encontrada = next((f for f in usuario.get("folgas", []) if f.get("data") == data_obj), None)
        if not folga_encontrada:
            return jsonify({"status": "error", "message": "Folga não encontrada"})
        if folga_encontrada.get("status") == "aprovada":
            return jsonify({"status": "error", "message": "Não é possível cancelar folga já aprovada"})

        resultado = cpppac.usuarios.update_one({"username": username}, {"$pull": {"folgas": {"data": data_obj}}})
        if resultado.modified_count > 0:
            return jsonify({"status": "success", "message": "Folga cancelada com sucesso"})
        return jsonify({"status": "error", "message": "Erro ao cancelar folga"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@folgas_bp.route("/api/aprovar_folga", methods=["POST"])
def aprovar_folga():
    resp = verificar_acesso_folgas()
    if resp:
        return resp
    try:
        username_aprovador = session["user"]
        user_aprovador = cpppac.usuarios.find_one({"username": username_aprovador})
        if not user_aprovador or not user_aprovador.get("star", False):
            return jsonify({"status": "error", "message": "Acesso negado"})

        data = request.get_json()
        username = data.get("username")
        data_folga = data.get("data")
        if not username or not data_folga:
            return jsonify({"status": "error", "message": "Username e data são obrigatórios"})

        data_obj = datetime.datetime.strptime(data_folga, "%Y-%m-%d")
        resultado = cpppac.usuarios.update_one(
            {"username": username, "folgas.data": data_obj, "folgas.status": "pendente"},
            {"$set": {"folgas.$.status": "aprovada", "folgas.$.aprovado_por": username_aprovador,
                      "folgas.$.data_aprovacao": datetime.datetime.now()}},
        )
        if resultado.modified_count > 0:
            return jsonify({"status": "success", "message": "Folga aprovada com sucesso"})
        return jsonify({"status": "error", "message": "Folga não encontrada ou já aprovada"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@folgas_bp.route("/api/editar_folga", methods=["POST"])
def editar_folga():
    resp = verificar_acesso_folgas()
    if resp:
        return resp
    try:
        username_editor = session["user"]
        user_editor = cpppac.usuarios.find_one({"username": username_editor})
        if not user_editor or not user_editor.get("star", False):
            return jsonify({"status": "error", "message": "Acesso negado"})

        data = request.get_json()
        username = data.get("username")
        data_folga_antiga = data.get("data_antiga")
        data_folga_nova = data.get("data_nova")
        novo_motivo = data.get("motivo")
        acao = data.get("acao")

        if not username or not data_folga_antiga:
            return jsonify({"status": "error", "message": "Username e data antiga são obrigatórios"})

        data_antiga_obj = datetime.datetime.strptime(data_folga_antiga, "%Y-%m-%d")

        if acao == "apagar":
            resultado = cpppac.usuarios.update_one(
                {"username": username}, {"$pull": {"folgas": {"data": data_antiga_obj}}}
            )
            msg = "Folga apagada com sucesso" if resultado.modified_count > 0 else "Folga não encontrada"
            status = "success" if resultado.modified_count > 0 else "error"
            return jsonify({"status": status, "message": msg})

        elif acao in ("editar", "criar"):
            if not data_folga_nova or not novo_motivo:
                return jsonify({"status": "error", "message": "Data nova e motivo são obrigatórios"})
            data_nova_obj = datetime.datetime.strptime(data_folga_nova, "%Y-%m-%d")

            if acao == "editar":
                resultado = cpppac.usuarios.update_one(
                    {"username": username, "folgas.data": data_antiga_obj},
                    {"$set": {"folgas.$.data": data_nova_obj, "folgas.$.motivo": novo_motivo,
                              "folgas.$.editado_por": username_editor, "folgas.$.data_edicao": datetime.datetime.now()}},
                )
            else:
                nova_folga = {"data": data_nova_obj, "motivo": novo_motivo, "status": "pendente",
                              "criado_por": username_editor, "data_criacao": datetime.datetime.now()}
                resultado = cpppac.usuarios.update_one({"username": username}, {"$push": {"folgas": nova_folga}})

            msg = "Operação realizada com sucesso" if resultado.modified_count > 0 else "Folga não encontrada"
            status = "success" if resultado.modified_count > 0 else "error"
            return jsonify({"status": status, "message": msg})

        return jsonify({"status": "error", "message": "Ação inválida"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@folgas_bp.route("/api/folgas_pendentes", methods=["GET"])
def folgas_pendentes():
    resp = verificar_acesso_folgas()
    if resp:
        return resp
    try:
        username = session["user"]
        user = cpppac.usuarios.find_one({"username": username})
        if not user or not user.get("star", False):
            return jsonify({"status": "error", "message": "Acesso negado"})

        pipeline = [
            {"$unwind": "$folgas"},
            {"$match": {"folgas.status": "pendente"}},
            {"$project": {"username": 1, "nome_completo": 1, "data": "$folgas.data",
                          "motivo": "$folgas.motivo", "status": "$folgas.status"}},
            {"$sort": {"data": 1}},
        ]
        folgas_list = list(cpppac.usuarios.aggregate(pipeline))
        for folga in folgas_list:
            if "_id" in folga and isinstance(folga["_id"], ObjectId):
                folga["_id"] = str(folga["_id"])
            if isinstance(folga.get("data"), datetime.datetime):
                folga["data"] = folga["data"].strftime("%Y-%m-%d")

        return jsonify({"status": "success", "folgas": folgas_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

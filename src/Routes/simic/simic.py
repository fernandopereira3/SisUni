from flask import render_template, Blueprint, request, jsonify, session, abort, redirect, url_for
from Data.conexao import cpppac
import datetime

cpppac = cpppac()

simic_bp = Blueprint("simic", __name__, template_folder="templates")


def verificar_acesso_simic():
    if "user" not in session:
        abort(403)
    usuario = cpppac.usuarios.find_one({"username": session["user"]})
    if not usuario:
        abort(403)
    setor = str(usuario.get("setor", "")).strip().lower()
    if setor not in ("cpd", "simic"):
        abort(403)


@simic_bp.route("/simic", methods=["GET"])
def simic():
    if "user" not in session:
        return redirect(url_for("rotas.login"))
    verificar_acesso_simic()
    return render_template("simic.html")


@simic_bp.route("/simic/cadastrar", methods=["POST"])
def cadastrar():
    verificar_acesso_simic()

    dados = request.get_json()
    if not dados:
        return jsonify({"status": "error", "message": "Dados inválidos"}), 400

    matricula = str(dados.get("matricula", "")).strip()
    nome = str(dados.get("nome", "")).strip()

    if not matricula or not nome:
        return jsonify({"status": "error", "message": "Matrícula e Nome são obrigatórios"}), 400

    if cpppac.sentenciados.find_one({"matricula": matricula}):
        return jsonify({"status": "error", "message": f"Matrícula {matricula} já cadastrada"}), 409

    campos_int = ("anos_de_prisao", "meses_de_prisao", "dias_de_prisao", "numero_de_filhos", "hediondo")
    doc = {"matricula": matricula, "nome": nome, "cadastrado_em": datetime.datetime.now(), "cadastrado_por": session.get("user")}

    for campo, valor in dados.items():
        if campo in ("matricula", "nome"):
            continue
        if campo in campos_int:
            try:
                doc[campo] = int(valor) if valor not in (None, "") else 0
            except (ValueError, TypeError):
                doc[campo] = 0
        else:
            doc[campo] = str(valor).strip() if valor is not None else ""

    cpppac.sentenciados.insert_one(doc)

    return jsonify({"status": "success", "message": f"Sentenciado {nome} cadastrado com sucesso", "matricula": matricula})


@simic_bp.route("/simic/verificar/<matricula>", methods=["GET"])
def verificar_matricula(matricula):
    verificar_acesso_simic()
    existe = cpppac.sentenciados.find_one({"matricula": matricula}, {"_id": 0, "nome": 1}) is not None
    return jsonify({"existe": existe})

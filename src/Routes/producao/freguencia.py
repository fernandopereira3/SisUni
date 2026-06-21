from flask import render_template, Blueprint, jsonify
from Data.conexao import cpppac

cpppac = cpppac()

frequencia_bp = Blueprint("frequencia", __name__, template_folder="templates")


@frequencia_bp.route("/freguencia")
def definir_frequencia():
    return render_template("frequencia.html")


@frequencia_bp.route("/api/reeducando/<matricula>")
def api_reeducando(matricula):
    digitos = "".join(c for c in str(matricula) if c.isdigit())
    if not digitos:
        return jsonify({"erro": "Matrícula inválida"}), 400

    # aceita a matrícula com ou sem zeros à esquerda: 470709 == 00470709
    candidatos = {digitos, digitos.lstrip("0"), digitos.zfill(8)}
    candidatos.discard("")

    trabalho = cpppac.trabalho.find_one(
        {"matricula": {"$in": list(candidatos)}}, {"_id": 0}
    )
    if not trabalho:
        return jsonify({"erro": "Reeducando não encontrado no trabalho"}), 404

    # informações vêm da coleção `trabalho`
    dados = {
        "matricula": trabalho.get("matricula", ""),
        "nome": trabalho.get("nome", ""),
        "local_trabalho": trabalho.get("setor", ""),
        "localizacao_atual": trabalho.get("alojamento", ""),
    }
    return jsonify(dados)

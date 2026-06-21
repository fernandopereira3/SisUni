from flask import render_template, request, Blueprint, session, redirect, url_for
import datetime
import re
from Data.conexao import cpppac
from Funcoes.funcoes import PesquisaForm, construir_tabela

pesquisas_bp = Blueprint("pesquisas", __name__)
cpppac = cpppac()


def verificar_acesso_sentenciados():
    if "user" not in session:
        return redirect(url_for("rotas.login"))
    return None


@pesquisas_bp.route("/pesquisas/dia-de-visita", methods=["GET"])
def lista_pesquisas():
    resp = verificar_acesso_sentenciados()
    if resp:
        return resp
    data_pesquisa = request.args.get("data")

    if data_pesquisa:
        try:
            data_obj = datetime.datetime.strptime(data_pesquisa, "%Y-%m-%d")
            data_inicio = data_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            data_fim = data_obj.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

            documentos = list(
                cpppac.sentenciados.find(
                    {
                        "visitas": {
                            "$elemMatch": {"$gte": data_inicio, "$lte": data_fim}
                        }
                    },
                    {"_id": 0},
                ).sort("nome", 1)
            )

            for doc in documentos:
                visitas_data = [
                    v for v in doc.get("visitas", []) if data_inicio <= v <= data_fim
                ]
                doc["data_visita"] = (
                    visitas_data[-1].strftime("%d/%m/%Y %H:%M") if visitas_data else ""
                )
                marcadores = doc.get("marcadores", [0, 0, 0, 0])
                doc["garrafas"] = marcadores[0] if len(marcadores) > 0 else 0
                doc["homens"] = marcadores[1] if len(marcadores) > 1 else 0
                doc["mulheres"] = marcadores[2] if len(marcadores) > 2 else 0
                doc["criancas"] = marcadores[3] if len(marcadores) > 3 else 0

            resumo = {
                "data_atual": data_obj.strftime("%d/%m/%Y"),
                "matriculas": len(documentos),
                "garrafas": 0,
                "homens": 0,
                "mulheres": 0,
                "criancas": 0,
                "total_visitantes": 0,
            }
            return render_template("lista.html", documentos=documentos, resumo=resumo)

        except ValueError:
            resumo = {
                "data_atual": "Data inválida",
                "matriculas": 0,
                "garrafas": 0,
                "homens": 0,
                "mulheres": 0,
                "criancas": 0,
                "total_visitantes": 0,
            }
            return render_template("lista.html", documentos=[], resumo=resumo)

    resumo = {
        "data_atual": "Selecione uma data",
        "matriculas": 0,
        "garrafas": 0,
        "homens": 0,
        "mulheres": 0,
        "criancas": 0,
        "total_visitantes": 0,
    }
    return render_template("lista.html", documentos=[], resumo=resumo)


@pesquisas_bp.route("/pesquisas/sentenciados", methods=["GET", "POST"])
def pesquisa_sentenciados():
    resp = verificar_acesso_sentenciados()
    if resp:
        return resp
    form = PesquisaForm()
    tabela_html = ""

    if form.validate_on_submit():
        matricula = form.matricula.data.strip()
        nome = form.nome.data.strip()
        colecao = request.form.get("colecao", "sentenciados")
        query = {}
        if matricula:
            query["matricula"] = {
                "$regex": f"^\\s*{re.escape(matricula)}\\s*",
                "$options": "i",
            }
        if nome:
            query["nome"] = {"$regex": nome, "$options": "i"}
        tabela_html = construir_tabela(query=query, incluir_acoes=True, colecao=colecao)

    return render_template("pesquisa.html", form=form, tabela_html=tabela_html)

from flask import render_template, request, Blueprint
import datetime
import re
from Data.conexao import conexao
from Funcoes.funcoes import PesquisaForm, construir_tabela

# Criar o blueprint
pesquisas_bp = Blueprint("pesquisas", __name__)
db = conexao()


@pesquisas_bp.route("/pesquisas/dia-de-visita", methods=["GET"])
def lista_pesquisas():
    data_pesquisa = request.args.get("data")

    if data_pesquisa:
        # Converter string de data para datetime
        try:
            data_obj = datetime.datetime.strptime(data_pesquisa, "%Y-%m-%d")
            data_inicio = data_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            data_fim = data_obj.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

            # Buscar documentos que têm visitas na data especificada
            documentos = list(
                db.sentenciados.find(
                    {
                        "visitas": {
                            "$elemMatch": {"$gte": data_inicio, "$lte": data_fim}
                        }
                    },
                    {"_id": 0},
                ).sort("nome", 1)
            )

            # Processar documentos
            for doc in documentos:
                # Filtrar apenas as visitas da data pesquisada
                visitas_data = [
                    v for v in doc.get("visitas", []) if data_inicio <= v <= data_fim
                ]

                # Pegar a última visita da data
                if visitas_data:
                    doc["data_visita"] = visitas_data[-1].strftime("%d/%m/%Y %H:%M")
                else:
                    doc["data_visita"] = ""

                # Separar marcadores
                marcadores = doc.get("marcadores", [0, 0, 0, 0])
                doc["garrafas"] = marcadores[0] if len(marcadores) > 0 else 0
                doc["homens"] = marcadores[1] if len(marcadores) > 1 else 0
                doc["mulheres"] = marcadores[2] if len(marcadores) > 2 else 0
                doc["criancas"] = marcadores[3] if len(marcadores) > 3 else 0

            # Resumo simplificado mostrando apenas as matrículas com visitas
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
            # Data inválida, retornar lista vazia
            documentos = []
            resumo = {
                "data_atual": "Data inválida",
                "matriculas": 0,
                "garrafas": 0,
                "homens": 0,
                "mulheres": 0,
                "criancas": 0,
                "total_visitantes": 0,
            }
            return render_template("lista.html", documentos=documentos, resumo=resumo)

    # Se não há data especificada, retornar lista vazia
    documentos = []
    resumo = {
        "data_atual": "Selecione uma data",
        "matriculas": 0,
        "garrafas": 0,
        "homens": 0,
        "mulheres": 0,
        "criancas": 0,
        "total_visitantes": 0,
    }
    return render_template("lista.html", documentos=documentos, resumo=resumo)


@pesquisas_bp.route("/pesquisas/sentenciados", methods=["GET", "POST"])
def pesquisa_sentenciados():
    form = PesquisaForm()
    tabela_html = ""

    if form.validate_on_submit():
        matricula = form.matricula.data.strip()
        nome = form.nome.data.strip()
        colecao = request.form.get(
            "colecao", "sentenciados"
        )  # Default para sentenciados
        query = {}

        if matricula:
            query["matricula"] = {
                "$regex": f"^\\s*{re.escape(matricula)}\\s*",
                "$options": "i",
            }
        if nome:
            query["nome"] = {"$regex": nome, "$options": "i"}

        # Só gera tabela quando há pesquisa
        tabela_html = construir_tabela(query=query, incluir_acoes=True, colecao=colecao)

    return render_template("pesquisa.html", form=form, tabela_html=tabela_html)

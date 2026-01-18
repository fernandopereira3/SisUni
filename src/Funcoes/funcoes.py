from flask_wtf import FlaskForm
import datetime
from wtforms import StringField, SubmitField
from Data.conexao import conexao

db = conexao()


class PesquisaForm(FlaskForm):
    matricula = StringField("Matrícula")
    nome = StringField("Nome")
    garrafas = StringField("Garrafas")
    homens = StringField("Homens")
    mulheres = StringField("Mulheres")
    criancas = StringField("Crianças")
    pesquisar = SubmitField("PESQUISAR")


class PesquisaFuncionarios(FlaskForm):
    nome = StringField("Nome")
    pesquisar = SubmitField("PESQUISAR")


def construir_tabela(
    documentos=None,
    query=None,
    incluir_acoes=True,
    classe_css="table table-striped",
    colecao="sentenciados",
):
    try:
        # Se não foram passados documentos, buscar no banco
        if documentos is None:
            if query is None:
                # Query padrão - todos os documentos
                query = {}

            # Selecionar a coleção apropriada
            if colecao == "excluidos":
                documentos = list(db.excluidos.find(query, {"_id": 0}).sort("nome", 1))
            else:
                documentos = list(
                    db.sentenciados.find(query, {"_id": 0}).sort("nome", 1)
                )

        if documentos:
            # Colunas básicas
            acoes_header = "<th>Ações</th>" if incluir_acoes else ""
            table_id = f"tabela-{colecao}"

            # Definir cores e badges baseados na coleção
            if colecao == "excluidos":
                table_class = f"{classe_css} table-danger"
                badge_class = "badge bg-danger"
                badge_text = "EXCLUÍDO"
                header_class = "table-danger"
            else:
                table_class = f"{classe_css} table-success"
                badge_class = "badge bg-success"
                badge_text = "ATIVO"
                header_class = "table-success"

            html = f"""
            <div class="mb-3">
                <h5><span class="{badge_class}">{badge_text.upper()}</span></h5>
            </div>
            <table class="{table_class}" id="{table_id}">
                <thead class="{header_class}">
                    <tr>
                        <th>Matrícula</th>
                        <th>Nome</th>
                        <th>Pavilhão</th>
                        <th>Status</th>
                        {acoes_header}
                    </tr>
                </thead>
                <tbody>
            """

            # Adicionar cada documento como uma linha
            for doc in documentos:
                matricula = doc.get("matricula", "")
                nome = doc.get("nome", "")
                pavilhao = doc.get("pavilhao", "") or doc.get("pavilhao", "")

                # Badge de status baseado na coleção
                if colecao == "excluidos":
                    status_badge = '<span class="badge bg-danger">EXCLUÍDO</span>'
                    motivo_exclusao = doc.get("motivo_exclusao", "")
                    if motivo_exclusao:
                        status_badge += (
                            f'<br><small class="text-muted">{motivo_exclusao}</small>'
                        )
                else:
                    status_badge = '<span class="badge bg-success">ATIVO</span>'

                # Coluna de ações (se solicitada)
                acoes_cell = ""
                if incluir_acoes:
                    acoes_cell = """
                        <td>
                            
                        </td>
                    """

                linha = f"""
                    <tr id="row-{matricula}">
                        <td>{matricula}</td>
                        <td>{nome}</td>
                        <td>{pavilhao}</td>
                        <td>{status_badge}</td>
                        {acoes_cell}
                    </tr>
                """
                html += linha

            # Fechar a tabela
            html += """
                </tbody>
            </table>
            """
            return html
        else:
            return '<p class="alert alert-info">Nenhum resultado encontrado.</p>'

    except Exception as e:
        print(f"Erro ao construir tabela: {e}")
        return f"<p class='alert alert-danger'>Erro ao processar dados: {e}</p>"


def construir_tabela_trabalho(
    documentos=None,
    classe_css="table table-striped",
):
    try:
        if not documentos:
            return '<p class="alert alert-info">Nenhum documento para exibir.</p>'

        headers = ["Matrícula", "Nome", "Setor"]
        fields = ["matricula", "nome", "setor"]

        header_html = "".join(f"<th>{h}</th>" for h in headers)

        html = f"""
        <table class="{classe_css}" id="tabela-trabalho">
            <thead>
                <tr>
                    {header_html}
                </tr>
            </thead>
            <tbody>
        """

        for doc in documentos:
            linha = '<tr id="row-{}">\n'.format(doc.get("matricula", ""))
            for field in fields:
                value = doc.get(field, "")
                linha += f"<td>{value}</td>\n"
            linha += "</tr>\n"
            html += linha

        html += """
            </tbody>
        </table>
        """
        return html
    except Exception as e:
        print(f"Erro ao construir tabela de trabalho: {e}")
        return f"<p class='alert alert-danger'>Erro ao processar dados da tabela de trabalho: {e}</p>"


def resumo_visitas():
    try:
        # Definir o início e fim do dia de hoje
        hoje_inicio = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        hoje_fim = datetime.datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

        # Usar agregação do MongoDB para melhor performance
        pipeline = [
            {
                "$match": {
                    "visitas": {"$elemMatch": {"$gte": hoje_inicio, "$lte": hoje_fim}}
                }
            },
            {"$project": {"matricula": 1, "marcadores": 1}},
        ]

        documentos_hoje = list(db.sentenciados.aggregate(pipeline))

        # Calcular resumo
        total_matriculas = len(documentos_hoje)
        total_garrafas = 0
        total_homens = 0
        total_mulheres = 0
        total_criancas = 0

        for doc in documentos_hoje:
            marcadores = doc.get("marcadores", [0, 0, 0, 0])

            # Conversão otimizada
            if marcadores and len(marcadores) >= 4:
                try:
                    total_garrafas += int(marcadores[0] or 0)
                    total_homens += int(marcadores[1] or 0)
                    total_mulheres += int(marcadores[2] or 0)
                    total_criancas += int(marcadores[3] or 0)
                except (ValueError, TypeError):
                    continue

        return {
            "matriculas": total_matriculas,
            "garrafas": total_garrafas,
            "homens": total_homens,
            "mulheres": total_mulheres,
            "criancas": total_criancas,
            "total_visitantes": total_homens + total_mulheres + total_criancas,
            "data_atual": datetime.datetime.now().strftime("%d/%m/%Y"),
        }

    except Exception as e:
        print(f"Erro ao calcular resumo: {str(e)}")
        return {
            "matriculas": 0,
            "garrafas": 0,
            "homens": 0,
            "mulheres": 0,
            "criancas": 0,
            "total_visitantes": 0,
            "data_atual": datetime.datetime.now().strftime("%d/%m/%Y"),
        }


def export_aux():
    """
    Exports documents from the aux collection
    Returns the cursor with all documents excluding _id field
    """
    try:
        filter = {}
        project = {"_id": 0}

        result = db.aux.find(filter=filter, projection=project)
        return result

    except Exception as e:
        print(f"Error exporting aux collection: {e}")
        return None

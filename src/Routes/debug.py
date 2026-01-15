import pandas as pd
from flask import (
    jsonify,
    request,
    render_template,
    Blueprint,
    session,
    abort,
)
import json
from Data.conexao import conexao

db = conexao()

debug_bp = Blueprint("debug", __name__)


def verificar_acesso_debug():
    """Verifica se o usuário tem permissão para acessar debug"""
    if "user" not in session:
        abort(403)  # Forbidden - usuário não logado

    usuario_logado = session["user"].lower()
    if usuario_logado != "fernandopereira":
        abort(403)  # Forbidden - usuário não autorizado


## Pagina inicial de debug ###
@debug_bp.route("/debug", methods=["GET"])
def debug_trabalho():
    verificar_acesso_debug()
    return render_template("debug.html")


######### Estatistica das colecoes ############
@debug_bp.route("/debug/sentenciados/db", methods=["GET"])
def debug_sentenciados_db():
    """Debug route to view sentenciados collection data"""
    verificar_acesso_debug()
    try:
        count = db.sentenciados.count_documents({})
        documentos = list(db.sentenciados.find({}).limit(100))
        primeiro_doc = db.sentenciados.find_one({})

        df_temp = pd.DataFrame(documentos)
        if "_id" in df_temp.columns:
            df_temp = df_temp.drop(columns=["_id"])

        estrutura = (
            {k: type(v).__name__ for k, v in primeiro_doc.items() if k != "_id"}
            if primeiro_doc
            else {}
        )

        html_output = generate_collection_debug_html(
            "Sentenciados", count, estrutura, df_temp
        )
        return render_template("debug.html", debug_content=html_output)
    except Exception as e:
        return render_template("debug.html", debug_content=generate_error_html(str(e)))


@debug_bp.route("/debug/trabalho/db", methods=["GET"])
def debug_trabalho_db():
    """Debug route to view trabalho collection data"""
    verificar_acesso_debug()
    try:
        count = db.trab.count_documents({})
        documentos = list(db.trab.find({}).limit(100))
        primeiro_doc = db.trab.find_one({})

        df_temp = pd.DataFrame(documentos)
        if "_id" in df_temp.columns:
            df_temp = df_temp.drop(columns=["_id"])

        estrutura = (
            {k: type(v).__name__ for k, v in primeiro_doc.items() if k != "_id"}
            if primeiro_doc
            else {}
        )

        html_output = generate_collection_debug_html(
            "Trabalho", count, estrutura, df_temp
        )
        return render_template("debug.html", debug_content=html_output)
    except Exception as e:
        return render_template("debug.html", debug_content=generate_error_html(str(e)))


@debug_bp.route("/debug/visitas/db", methods=["GET"])
def debug_visitas_db():
    """Debug route to view visitas collection data"""
    verificar_acesso_debug()
    try:
        count = db.visitas.count_documents({})
        documentos = list(db.visitas.find({}).limit(100))
        primeiro_doc = db.visitas.find_one({})

        df_temp = pd.DataFrame(documentos)
        if "_id" in df_temp.columns:
            df_temp = df_temp.drop(columns=["_id"])

        estrutura = (
            {k: type(v).__name__ for k, v in primeiro_doc.items() if k != "_id"}
            if primeiro_doc
            else {}
        )

        html_output = generate_collection_debug_html(
            "Visitas", count, estrutura, df_temp
        )
        return render_template("debug.html", debug_content=html_output)
    except Exception as e:
        return render_template("debug.html", debug_content=generate_error_html(str(e)))


def generate_collection_debug_html(collection_name, count, estrutura, df):
    """Helper function to generate debug HTML output"""
    return f"""
    <div class="container debug-container">
        <h2>Debug MongoDB - Coleção '{collection_name}'</h2>
        
        <div class="card mb-4">
            <div class="card-body bg-primary text-white">
                Informações da Coleção
            </div>
            <div class="card-body">
                <p><strong>Total de documentos:</strong> {count}</p>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header bg-info text-white">
                Estrutura dos Documentos
            </div>
            <div class="card-body">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Campo</th>
                            <th>Tipo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f"<tr><td>{campo}</td><td>{tipo}</td></tr>" for campo, tipo in estrutura.items()])}
                    </tbody>
                </table>
            </div>
        </div>
        
        <h3>Amostra de Dados (100 primeiros registros)</h3>
        <div class="table-responsive">
            {df.to_html(classes="table table-striped table-sm", index=False) if not df.empty else "<p>Não há dados na coleção.</p>"}
        </div>
        
        <div class="mt-4">
            <h3>Estatísticas Numéricas</h3>
            {df.describe().to_html(classes="table table-bordered") if not df.empty and df.select_dtypes(include=["number"]).shape[1] > 0 else "<p>Não há dados numéricos para análise estatística.</p>"}
        </div>
    </div>
    """


def generate_error_html(error_message):
    """Helper function to generate error HTML"""
    return f"""
    <div class="alert alert-danger">
        <h4>Erro ao acessar o banco de dados</h4>
        <p>{error_message}</p>
    </div>
    """


def generate_collection_not_found_html(db_name, colecoes):
    """Helper function to generate collection not found HTML"""
    return f"""
    <div class="container debug-container">
        <div class="alert alert-warning">
            <h4>Coleção 'trabalho' não encontrada no banco de dados</h4>
            <p>Banco de dados: {db_name}</p>
            <p>Coleções disponíveis: {", ".join(colecoes) if colecoes else "Nenhuma"}</p>
        </div>
    </div>
    """


def generate_db_error_html(error):
    """Helper function to generate database error HTML"""
    return f"""
    <div class="container">
        <div class="alert alert-danger">
            <h4>Erro ao acessar o banco de dados</h4>
            <p>{str(error)}</p>
        </div>
    </div>
    """


######### Fim Estatistica das colecoes ############


@debug_bp.route("/normalizar_banco", methods=["GET", "POST"])
def normalizar_banco():
    verificar_acesso_debug()
    if request.method == "GET":
        # Retornar página simples de confirmação
        from flask_wtf.csrf import generate_csrf

        csrf_token = generate_csrf()
        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="alert alert-warning">
                <h4><i class="fas fa-exclamation-triangle"></i> Normalizar Banco de Dados</h4>
                <p>Esta ação irá converter todos os nomes para MAIÚSCULAS.</p>
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{csrf_token}"/>
                    <button type="submit" class="btn btn-warning">
                        <i class="fas fa-check"></i> Confirmar Normalização
                    </button>
                    <a href="/debug" class="btn btn-secondary">Cancelar</a>
                </form>
            </div>
        """,
        )

    try:
        total_atualizados = 0
        erros = []

        # 1. NORMALIZAR SENTENCIADOS
        print("Normalizando sentenciados...")
        for doc in db.sentenciados.find():
            try:
                updates = {}

                # Nome
                if "nome" in doc and doc["nome"]:
                    nome_novo = doc["nome"].upper().strip()
                    if doc["nome"] != nome_novo:
                        updates["nome"] = nome_novo

                # Outros campos texto
                for campo in ["procedencia", "artigo", "observacoes"]:
                    if campo in doc and doc[campo] and isinstance(doc[campo], str):
                        valor_novo = doc[campo].upper().strip()
                        if doc[campo] != valor_novo:
                            updates[campo] = valor_novo

                if updates:
                    db.sentenciados.update_one({"_id": doc["_id"]}, {"$set": updates})
                    total_atualizados += 1

            except Exception as e:
                erros.append(f"Sentenciado {doc.get('matricula', 'N/A')}: {str(e)}")

        # 2. NORMALIZAR VISITAS
        print("Normalizando visitas...")
        if "visita" in db.list_collection_names():
            for doc in db.visita.find():
                try:
                    updates = {}

                    for campo in ["nome", "visitante", "parentesco"]:
                        if campo in doc and doc[campo]:
                            valor_novo = doc[campo].upper().strip()
                            if doc[campo] != valor_novo:
                                updates[campo] = valor_novo

                    if updates:
                        db.visita.update_one({"_id": doc["_id"]}, {"$set": updates})
                        total_atualizados += 1

                except Exception as e:
                    erros.append(f"Visita {doc.get('matricula', 'N/A')}: {str(e)}")

        # 3. NORMALIZAR TRABALHO
        print("Normalizando trabalho...")
        if "trab" in db.list_collection_names():
            for doc in db.trab.find():
                try:
                    updates = {}

                    for campo in ["nome", "setor", "funcao"]:
                        if campo in doc and doc[campo] and isinstance(doc[campo], str):
                            valor_novo = doc[campo].upper().strip()
                            if doc[campo] != valor_novo:
                                updates[campo] = valor_novo

                    if updates:
                        db.trab.update_one({"_id": doc["_id"]}, {"$set": updates})
                        total_atualizados += 1

                except Exception as e:
                    erros.append(f"Trabalho {doc.get('matricula', 'N/A')}: {str(e)}")

        # RESULTADO SIMPLES
        resultado_html = f"""
        <div class="alert alert-success">
            <h4><i class="fas fa-check-circle"></i> Normalização Concluída!</h4>
            <p><strong>Total de registros atualizados:</strong> {total_atualizados}</p>
            {
            f"<p><strong>Erros encontrados:</strong> {len(erros)}</p>" if erros else ""
        }
        </div>
        
        {
            f'''
        <div class="alert alert-warning">
            <h5>Erros:</h5>
            <ul>
                {"".join([f"<li>{erro}</li>" for erro in erros[:10]])}
                {f"<li>... e mais {len(erros) - 10} erros</li>" if len(erros) > 10 else ""}
            </ul>
        </div>
        '''
            if erros
            else ""
        }
        
        <div class="mt-3">
            <a href="/debug" class="btn btn-primary">
                <i class="fas fa-arrow-left"></i> Voltar ao Debug
            </a>
            <a href="/" class="btn btn-success">
                <i class="fas fa-home"></i> Página Inicial
            </a>
        </div>
        """

        return render_template("debug.html", debug_content=resultado_html)

    except Exception as e:
        erro_html = f"""
        <div class="alert alert-danger">
            <h4><i class="fas fa-exclamation-circle"></i> Erro na Normalização</h4>
            <p><strong>Erro:</strong> {str(e)}</p>
            <div class="mt-3">
                <a href="/debug" class="btn btn-primary">Voltar ao Debug</a>
            </div>
        </div>
        """
        return render_template("debug.html", debug_content=erro_html)


@debug_bp.route("/api/normalizar_preview", methods=["GET"])
def preview_normalizacao():
    verificar_acesso_debug()
    """Preview simplificado da normalização"""
    try:
        contadores = {"sentenciados": 0, "visitas": 0, "trabalho": 0}

        # Contar sentenciados que precisam normalização
        for doc in db.sentenciados.find().limit(100):
            if (
                "nome" in doc
                and doc["nome"]
                and doc["nome"] != doc["nome"].upper().strip()
            ):
                contadores["sentenciados"] += 1

        # Contar visitas que precisam normalização
        if "visita" in db.list_collection_names():
            for doc in db.visita.find().limit(100):
                for campo in ["nome", "visitante", "parentesco"]:
                    if (
                        campo in doc
                        and doc[campo]
                        and doc[campo] != doc[campo].upper().strip()
                    ):
                        contadores["visitas"] += 1
                        break

        # Contar trabalho que precisa normalização
        if "trab" in db.list_collection_names():
            for doc in db.trab.find().limit(100):
                for campo in ["nome", "setor"]:
                    if (
                        campo in doc
                        and doc[campo]
                        and isinstance(doc[campo], str)
                        and doc[campo] != doc[campo].upper().strip()
                    ):
                        contadores["trabalho"] += 1
                        break

        return jsonify({"status": "success", "preview": contadores})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# LIMPAR MATRICULA COMPLETA SISTEMA DE ADMIN
@debug_bp.route("/clear", methods=["GET"])
def clean_matricula_complete():
    verificar_acesso_debug()
    count = 0
    for doc in db.sentenciados.find():
        if "matricula" in doc and isinstance(doc["matricula"], str):
            original = doc["matricula"]

            clean_matricula = (
                original.replace(" ", "").replace(".", "").replace("-", "")
            )

            if len(clean_matricula) > 0:
                clean_matricula = clean_matricula[:-1]

            if clean_matricula != original:
                db.sentenciados.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"matricula": clean_matricula}},
                )
                count += 1

    return render_template(
        "debug.html",
        debug_content=f"""
        <div class="alert alert-success">
            <h4>Limpeza de Matrículas Concluída</h4>
            <p>Total de matrículas atualizadas: {count}</p>
        </div>
    """,
    )


@debug_bp.route("/clear/trab", methods=["GET"])
def clean_trab():
    count = 0
    for doc in db.trab.find():
        if "matricula" in doc and isinstance(doc["matricula"], str):
            original = doc["matricula"]

            clean_matricula = (
                original.replace(" ", "").replace(".", "").replace("-", "")
            )

            if len(clean_matricula) > 0:
                clean_matricula = clean_matricula[:-1]

            if clean_matricula != original:
                db.trab.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"matricula": clean_matricula}},
                )
                count += 1

    return render_template(
        "debug.html",
        debug_content=f"""
        <div class="alert alert-success">
            <h4>Limpeza de Matrículas Concluída</h4>
            <p>Total de matrículas atualizadas: {count}</p>
        </div>
    """,
    )


@debug_bp.route("/clear/aux", methods=["GET"])
def clean_banco_aux():
    count = 0
    for doc in db.aux.find():
        if "matricula" in doc and isinstance(doc["matricula"], str):
            original = doc["matricula"]

            clean_matricula = (
                original.replace(" ", "").replace(".", "").replace("-", "")
            )

            if len(clean_matricula) > 0:
                clean_matricula = clean_matricula[:-1]

            if clean_matricula != original:
                db.aux.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"matricula": clean_matricula}},
                )
                count += 1

    return render_template(
        "debug.html",
        debug_content=f"""
        <div class="alert alert-success">
            <h4>Limpeza de Matrículas Concluída</h4>
            <p>Total de matrículas atualizadas: {count}</p>
        </div>
    """,
    )


@debug_bp.route("/clear/excluidos", methods=["GET"])
def clean_excluidos():
    count = 0
    for doc in db.excluidos.find():
        if "matricula" in doc and isinstance(doc["matricula"], str):
            original = doc["matricula"]

            clean_matricula = (
                original.replace(" ", "").replace(".", "").replace("-", "")
            )

            if len(clean_matricula) > 0:
                clean_matricula = clean_matricula[:-1]

            if clean_matricula != original:
                db.excluidos.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"matricula": clean_matricula}},
                )
                count += 1

    return render_template(
        "debug.html",
        debug_content=f"""
        <div class="alert alert-success">
            <h4>Limpeza de Matrículas Concluída</h4>
            <p>Total de matrículas atualizadas: {count}</p>
        </div>
    """,
    )


@debug_bp.route("/debug/banco/export", methods=["GET", "POST"])
def export_aux():
    import os
    from flask_wtf.csrf import CSRFError

    """Route to export aux collection to JSON file"""
    if request.method == "GET":
        from flask_wtf.csrf import generate_csrf

        csrf_token = generate_csrf()
        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="container">
                <h3>Exportar Coleção Auxiliar</h3>
                <p>Exporte a coleção auxiliar para um arquivo JSON. Depois importe para sentenciados, ele vai importar e somente os novos registros</p>
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{csrf_token}"/>
                    <div class="form-group">
                        <label>Export Directory Path:</label>
                        <input type="text" name="export_path" class="form-control" 
                               placeholder="Diretorio onde salvar" required>
                    </div>
                    <div class="form-group mt-3">
                        <label>Filename:</label>
                        <input type="text" name="filename" class="form-control" 
                               value="aux_export.json" required>
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">
                        Export Database
                    </button>
                </form>
            </div>
        """,
        )

    # Handle POST request
    try:
        # Log CSRF token information for debugging
        csrf_token_form = request.form.get("csrf_token")
        csrf_token_header = request.headers.get("X-CSRFToken")
        print(f"DEBUG CSRF - Form token: {csrf_token_form}")
        print(f"DEBUG CSRF - Header token: {csrf_token_header}")
        print(f"DEBUG CSRF - Form data: {dict(request.form)}")

        export_path = request.form.get("export_path", ".")
        filename = request.form.get("filename", "aux_export.json")
    except CSRFError as e:
        print(f"CSRF Error: {e}")
        return render_template(
            "debug.html",
            debug_content=f'<div class="alert alert-danger">CSRF Error: {str(e)}</div>',
        )
    except Exception as e:
        print(f"General Error in POST processing: {e}")
        return render_template(
            "debug.html",
            debug_content=f'<div class="alert alert-danger">Error: {str(e)}</div>',
        )

    # Export aux collection to JSON
    aux_docs = list(db.aux.find({}, {"_id": 0}))  # Exclude _id field

    if not aux_docs:
        return render_template(
            "debug.html",
            debug_content='<div class="alert alert-warning">No documents found in aux collection</div>',
        )

    try:
        full_path = os.path.join(export_path, filename)

        # Create directory if it doesn't exist
        os.makedirs(export_path, exist_ok=True)

        # Save to JSON file in specified path
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(aux_docs, f, ensure_ascii=False, indent=2)

        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="container">
                <div class="alert alert-success">
                    <h4>Export Completed</h4>
                    <p>File has been saved to: {full_path}</p>
                </div>
                <div class="mt-3">
                    <a href="/debug/banco/export" class="btn btn-primary">Export Another File</a>
                    <a href="/debug/banco/import" class="btn btn-secondary">Go to Import Page</a>
                </div>
            </div>
        """,
        )
    except Exception as e:
        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="alert alert-danger">
                <h4>Export Failed</h4>
                <p>Error: {str(e)}</p>
                <a href="/debug/banco/export" class="btn btn-primary mt-2">Try Again</a>
            </div>
        """,
        )


@debug_bp.route("/debug/banco/import", methods=["GET"])
def import_banco():
    """Main import page with options for different import operations"""
    return render_template(
        "debug.html",
        debug_content="""
        <div class="container">
            <h3>Importar / Gerenciar Banco de Dados</h3>
            <p>Escolha uma das opções abaixo para importar ou gerenciar dados do banco:</p>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5><i class="fas fa-upload"></i> Importar Sentenciados</h5>
                        </div>
                        <div class="card-body">
                            <p>Importe dados para a coleção de sentenciados a partir de um arquivo JSON.</p>
                            <a href="/debug/banco/import/sentenciados" class="btn btn-primary">
                                <i class="fas fa-file-import"></i> Importar Sentenciados
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header bg-danger text-white">
                            <h5><i class="fas fa-trash"></i> Excluir Sentenciados</h5>
                        </div>
                        <div class="card-body">
                            <p>Exclua sentenciados baseado nas matrículas da coleção excluídos.</p>
                            <a href="/debug/banco/import/excluidos" class="btn btn-danger">
                                <i class="fas fa-user-minus"></i> Excluir Sentenciados
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <a href="/debug" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Voltar ao Debug
                </a>
            </div>
        </div>
    """,
    )


@debug_bp.route("/debug/banco/import/sentenciados", methods=["GET", "POST"])
def import_sentenciados():
    """Route to import JSON file to sentenciados collection"""
    if request.method == "GET":
        from flask_wtf.csrf import generate_csrf

        csrf_token = generate_csrf()
        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="container">
                <h3>Import to Sentenciados</h3>
                <form method="POST" enctype="multipart/form-data">
                    <input type="hidden" name="csrf_token" value="{csrf_token}"/>
                    <div class="form-group">
                        <label>JSON File:</label>
                        <input type="file" name="file" class="form-control" accept=".json">
                    </div>
                    <p></p>
                    <button type="submit" class="btn btn-primary">Import to Sentenciados</button>
                </form>
                <div class="mt-3">
                    <a href="/debug/banco/import" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Voltar às Opções de Import
                    </a>
                </div>
            </div>
        """,
        )

    # Process uploaded file
    file = request.files.get("file")
    if not file or file.filename == "":
        return render_template(
            "debug.html",
            debug_content='<div class="alert alert-danger">No file selected</div>',
        )

    if not file.filename.endswith(".json"):
        return render_template(
            "debug.html",
            debug_content='<div class="alert alert-danger">Invalid format. Use JSON file.</div>',
        )

    # Read JSON file
    try:
        records = json.load(file)
    except Exception as e:
        return render_template(
            "debug.html",
            debug_content=f'<div class="alert alert-danger">Error reading JSON: {str(e)}</div>',
        )

    # Insert records into sentenciados collection
    inserted = duplicates = errors = 0
    error_msgs = []

    for record in records:
        try:
            # Check if matricula exists
            if "matricula" in record:
                existing = db.sentenciados.find_one({"matricula": record["matricula"]})
                if existing:
                    duplicates += 1
                    continue

                db.sentenciados.insert_one(record)
                inserted += 1
            else:
                errors += 1
                error_msgs.append("Record missing matricula field")
        except Exception as e:
            errors += 1
            error_msgs.append(str(e))

    return render_template(
        "debug.html",
        debug_content=f"""
        <div class="alert alert-info">
            <h4>Import Results</h4>
            <p>Records inserted: {inserted}</p>
            <p>Duplicates skipped: {duplicates}</p>
            <p>Errors: {errors}</p>
            {f"<p>Error messages:</p><ul>{''.join([f'<li>{msg}</li>' for msg in error_msgs[:5]])}</ul>" if error_msgs else ""}
        </div>
        <div class="mt-3">
            <a href="/debug/banco/import/sentenciados" class="btn btn-primary">Importar Novamente</a>
            <a href="/debug/banco/import" class="btn btn-secondary">Voltar às Opções de Import</a>
        </div>
    """,
    )


@debug_bp.route("/debug/banco/import/excluidos", methods=["GET", "POST"])
def import_excluidos():
    """Route to exclude records from sentenciados based on excluidos collection"""
    if request.method == "GET":
        from flask_wtf.csrf import generate_csrf

        csrf_token = generate_csrf()
        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="container">
                <h3>Excluir Sentenciados</h3>
                <p>Esta operação irá excluir da coleção 'sentenciados' todas as matrículas que constam na coleção 'excluidos'.</p>
                <div class="alert alert-warning">
                    <strong>Atenção:</strong> Esta operação não pode ser desfeita. Certifique-se de que deseja prosseguir.
                </div>
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{csrf_token}"/>
                    <button type="submit" class="btn btn-danger">
                        <i class="fas fa-trash"></i> Excluir Sentenciados
                    </button>
                    <a href="/debug" class="btn btn-secondary">Cancelar</a>
                </form>
            </div>
        """,
        )

    # Handle POST request - perform exclusion
    try:
        # Get all matriculas from excluidos collection
        excluidos_docs = list(db.excluidos.find({}, {"matricula": 1, "_id": 0}))

        if not excluidos_docs:
            return render_template(
                "debug.html",
                debug_content='<div class="alert alert-warning">Nenhuma matrícula encontrada na coleção excluidos</div>',
            )

        # Extract matriculas from excluidos collection
        matriculas_excluir = [
            doc.get("matricula") for doc in excluidos_docs if doc.get("matricula")
        ]

        if not matriculas_excluir:
            return render_template(
                "debug.html",
                debug_content='<div class="alert alert-warning">Nenhuma matrícula válida encontrada na coleção excluidos</div>',
            )

        # Delete records from sentenciados collection
        result = db.sentenciados.delete_many({"matricula": {"$in": matriculas_excluir}})

        deleted_count = result.deleted_count
        total_matriculas = len(matriculas_excluir)

        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="alert alert-success">
                <h4>Exclusão Concluída</h4>
                <p>Total de matrículas na coleção excluidos: {total_matriculas}</p>
                <p>Registros excluídos da coleção sentenciados: {deleted_count}</p>
                <p>Registros não encontrados: {total_matriculas - deleted_count}</p>
            </div>
            <div class="mt-3">
                <a href="/debug/banco/import/excluidos" class="btn btn-primary">Executar Novamente</a>
                <a href="/debug/banco/import" class="btn btn-secondary">Voltar às Opções de Import</a>
            </div>
        """,
        )

    except Exception as e:
        return render_template(
            "debug.html",
            debug_content=f"""
            <div class="alert alert-danger">
                <h4>Erro na Exclusão</h4>
                <p>Erro: {str(e)}</p>
                <a href="/debug/banco/import/excluidos" class="btn btn-primary mt-2">Tentar Novamente</a>
                <a href="/debug/banco/import" class="btn btn-secondary mt-2">Voltar às Opções de Import</a>
            </div>
        """,
        )

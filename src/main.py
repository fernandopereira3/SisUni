import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from Routes.jumbo import jumbo_bp as BPjumbo
from Routes.rotas import rotas_bp as BProtas
from Routes.debug import debug_bp as BPdebug
from Routes.trabalho import trabalho_bp as BPtrabalho
from Routes.pesquisas import pesquisas_bp as BPpesquisas
from Routes.funcionarios import funcionarios_bp as BPfuncionarios
from Tests.test import bp_test
from Data.conexao import conexao

db = conexao()

# Configurar Flask para servir arquivos estáticos
app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder="Routes/static",
    static_url_path="/static",
    template_folder="Routes/templates",
)
# Use a fixed secret key for development to avoid CSRF token invalidation
app.config["SECRET_KEY"] = "dev-secret-key-for-csrf-tokens"

# Configurar proteção CSRF com configurações específicas
app.config["WTF_CSRF_TIME_LIMIT"] = None  # Remove timeout do token CSRF
app.config["WTF_CSRF_SSL_STRICT"] = False  # Permite CSRF em HTTP
csrf = CSRFProtect(app)

# Registrar apenas os blueprints necessários
app.register_blueprint(BPjumbo)
app.register_blueprint(BProtas)
app.register_blueprint(BPdebug)
app.register_blueprint(BPtrabalho)
app.register_blueprint(BPpesquisas)
app.register_blueprint(BPfuncionarios)
app.register_blueprint(bp_test)


# Error handlers para páginas personalizadas
@app.errorhandler(401)
def unauthorized(error):
    return render_template("401.html"), 401


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

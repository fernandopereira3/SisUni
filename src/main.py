import os
from flask import Flask
from Routes.jumbo import jumbo_bp as BPjumbo
from Routes.rotas import rotas_bp as BProtas
from Routes.debug import debug_bp as BPdebug
from Routes.trabalho import trabalho_bp as BPtrabalho
from Routes.rotas_saida import rotas_saida_bp as BProtas_saida
from Tests.test import bp_test
from Data.conexao import conexao

db = conexao()

# Configurar Flask para servir arquivos estáticos
app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder="Routes/static",
    static_url_path="/static",
)
secret_key = os.urandom(24)
app.config["SECRET_KEY"] = secret_key

# Registrar apenas os blueprints necessários
app.register_blueprint(BPjumbo)
app.register_blueprint(BProtas)
app.register_blueprint(BPdebug)
app.register_blueprint(BPtrabalho)
app.register_blueprint(BProtas_saida)
app.register_blueprint(bp_test)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

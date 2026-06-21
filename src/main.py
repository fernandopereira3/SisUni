from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from Routes.rotas import rotas_bp as BProtas
from Routes.debug import debug_bp as BPdebug
from Routes.administrativo.rh import rh_bp as BPrh
from Routes.seguranca.folgas import folgas_bp as BPfolgas
from Routes.sentenciados.pesquisas import pesquisas_bp as BPpesquisas
from Routes.sentenciados.visitas import visitas_bp as BPvisitas
from Routes.producao.trabalho import trabalho_bp as BPtrabalho
from Routes.producao.freguencia import frequencia_bp as BPfrequencia
from Routes.simic.simic import simic_bp as BPsimic
from Tests.test import bp_test
from Data.conexao import conexao_mongo as conexao
from apscheduler.schedulers.background import BackgroundScheduler
from Funcoes.exportar_banco import sincronizar


db = conexao()

# Índices da coleção logs: TTL 60 dias + índice de tipo para filtros rápidos
db.logs.create_index("timestamp", expireAfterSeconds=5_184_000)
db.logs.create_index("tipo")


app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder="Routes/static",
    static_url_path="/static",
    template_folder="Routes/templates",
)
app.config["SECRET_KEY"] = "dev-secret-key-for-csrf-tokens"
app.config["WTF_CSRF_TIME_LIMIT"] = None
app.config["WTF_CSRF_SSL_STRICT"] = False
csrf = CSRFProtect(app)

csrf.exempt(BPdebug)

app.register_blueprint(BProtas)
app.register_blueprint(BPdebug)
app.register_blueprint(BPrh)
app.register_blueprint(BPfolgas)
app.register_blueprint(BPpesquisas)
app.register_blueprint(BPvisitas)
app.register_blueprint(BPtrabalho)
app.register_blueprint(BPfrequencia)
app.register_blueprint(BPsimic)
app.register_blueprint(bp_test)


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
    scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")
    scheduler.add_job(sincronizar, "cron", hour=6, minute=0)
    scheduler.add_job(sincronizar, "cron", hour=12, minute=0)
    scheduler.add_job(sincronizar, "cron", hour=18, minute=0)
    scheduler.start()
    print("Scheduler iniciado: sincronização às 06:00, 12:00 e 18:00.")

    app.run(host="0.0.0.0", port=5000, debug=True)

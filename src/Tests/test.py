from flask import render_template, Blueprint
from Data.conexao import conexao

bp_test = Blueprint(
    "test",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)
db = conexao()


@bp_test.route("/test/trab")
def test_trab():
    return render_template("404.html")

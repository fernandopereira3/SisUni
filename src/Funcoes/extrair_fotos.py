import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from Data.conexao import conexao_sql
import sqlalchemy as sa

PASTA_SAIDA = os.path.join(os.path.dirname(__file__), "..", "..", "fotos")


def limpar_matricula(raw: str) -> str:
    s = raw.replace(" ", "").replace(".", "").replace("-", "")
    return s[:-1] if len(s) > 0 else s


def extrair():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    engine = conexao_sql()
    with engine.connect() as conn:
        result = conn.execute(
            sa.text(
                "SELECT matricula, foto FROM sen WHERE excluido = 0 AND foto IS NOT NULL"
            )
        )
        rows = result.fetchall()

    print(f"{len(rows)} fotos encontradas. Extraindo...")

    ok = 0
    erros = 0
    for matricula_raw, foto_bytes in rows:
        if not foto_bytes:
            continue
        try:
            matricula = limpar_matricula(str(matricula_raw))
            caminho = os.path.join(PASTA_SAIDA, f"{matricula}.jpg")
            with open(caminho, "wb") as f:
                f.write(foto_bytes)
            ok += 1
        except Exception as e:
            print(f"  Erro em {matricula_raw!r}: {e}")
            erros += 1

    pasta = os.path.abspath(PASTA_SAIDA)
    print(f"Concluído: {ok} salvas, {erros} erros → {pasta}")
    return ok, erros, pasta


if __name__ == "__main__":
    extrair()

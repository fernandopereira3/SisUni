import pandas as pd
from datetime import datetime
from Data.conexao import conexao_mongo, conexao_sql


def sincronizar():
    print(
        f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Iniciando sincronização SQL → MongoDB..."
    )

    try:
        engine = conexao_sql()

        query = """
        SELECT
            s.matricula,
            s.nome,
            s.vulgo,
            s.codigo_pavilhao,
            p.pavilhao,
            s.cela,
            s.regime,
            s.artigo,
            s.deecrim,
            s.anos_de_prisao,
            s.meses_de_prisao,
            s.dias_de_prisao,
            s.prisao,
            s.inclusao,
            s.procedencia,
            s.reincidente,
            s.hediondo,
            s.situacao_criminal,
            s.rg,
            s.cpf,
            s.nascimento,
            s.naturalidade,
            s.uf,
            s.nacionalidade,
            s.sexo,
            s.estado_civil,
            s.numero_de_filhos,
            s.pai,
            s.mae,
            s.esposa,
            s.profissao,
            s.grau_escolaridade,
            s.cutis,
            s.cabelos,
            s.olhos,
            s.estatura,
            s.peso,
            s.sinais_tatuagens,
            s.sinais_cicatrizes,
            s.endereco_familiar,
            s.bairro_familiar,
            s.cidade_familiar,
            s.uf_familiar,
            s.cep_familiar,
            s.contato,
            s.controle_interno,
            s.observacoes
        FROM sen s
        LEFT JOIN pav p ON s.codigo_pavilhao = p.codigo_pavilhao
        WHERE s.excluido = 0
        AND s.codigo_pavilhao BETWEEN 10 AND 19
        ORDER BY s.nome;
        """

        df = pd.read_sql(query, con=engine)
        df = df.where(pd.notnull(df), None)

        for col in df.columns:
            if hasattr(df[col], "dt"):
                df[col] = df[col].astype(str).where(df[col].notna(), None)

        documentos = df.to_dict(orient="records")

        db = conexao_mongo()
        db["sentenciados"].drop()
        db["sentenciados"].insert_many(documentos)

        print(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ✓ {len(documentos)} registros sincronizados."
        )

    except Exception as e:
        print(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ✗ Erro na sincronização: {e}"
        )


if __name__ == "__main__":
    sincronizar()

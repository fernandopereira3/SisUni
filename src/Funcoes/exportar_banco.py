import pandas as pd
import datetime as dt
from Data.conexao import conexao_mongo, conexao_sql
from Funcoes.foto import foto_para_base64


def sincronizar():
    print(
        f"[{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Iniciando sincronização SQL → MongoDB..."
    )

    try:
        engine = conexao_sql()

        query = """
        SELECT *
        FROM sen s
        LEFT JOIN pav p ON s.codigo_pavilhao = p.codigo_pavilhao
        WHERE s.excluido = 0;
        """

        df = pd.read_sql(query, con=engine)
        df = df.where(pd.notnull(df), None)

        # converter datetime.date e datetime64 para string
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].apply(
                    lambda x: (
                        x.strftime("%d/%m/%Y")
                        if isinstance(x, (dt.date, dt.datetime))
                        else x
                    )
                )
            elif hasattr(df[col], "dt"):
                df[col] = df[col].dt.strftime("%d/%m/%Y").where(df[col].notna(), None)

        documentos = df.to_dict(orient="records")

        for doc in documentos:
            doc["foto"] = foto_para_base64(doc.get("foto"))
            doc.pop("tamanho_foto", None)

        db = conexao_mongo()
        collection = db["sentenciados"]
        collection.drop()
        collection.insert_many(documentos)

        # limpar matrículas: remove espaços, pontos, hífens e o último dígito
        count = 0
        for doc in collection.find():
            if "matricula" in doc and isinstance(doc["matricula"], str):
                original = doc["matricula"]
                limpa = original.replace(" ", "").replace(".", "").replace("-", "")
                if len(limpa) > 0:
                    limpa = limpa[:-1]
                if limpa != original:
                    collection.update_one(
                        {"_id": doc["_id"]}, {"$set": {"matricula": limpa}}
                    )
                    count += 1

        print(
            f"[{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ✓ {len(documentos)} registros sincronizados, {count} matrículas limpas."
        )

    except Exception as e:
        print(
            f"[{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ✗ Erro na sincronização: {e}"
        )


if __name__ == "__main__":
    sincronizar()

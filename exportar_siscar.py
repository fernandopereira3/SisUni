import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine


def conexao():
    client = MongoClient("mongodb://localhost:27017/")  # CONETAR COM O MONGO DB
    db = client["cpppac"]
    return db


def exportar_para_csv():
    nome_arquivo_csv = "banco.csv"

    try:
        print("Conectando ao banco de dados MySQL 5.5...")
        engine = create_engine(
            "mysql+mysqlconnector://root:futuro07@10.0.0.2:3309/siscar"
        )  # CONECTAR COM O BANCO DE DADOS MYSQL 5.5

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

        print("Conexão SQL bem-sucedida!")
        df = pd.read_sql(query, con=engine)

        df.to_csv(nome_arquivo_csv, sep=";", index=False, encoding="utf-8-sig")
        print("🎉 Arquivo CSV gerado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")


def importar_mongo():
    from pymongo import MongoClient

    try:
        print("Conectando ao MongoDB...")
        client = MongoClient("mongodb://localhost:27017/")  # CONETAR COM O MONGO DB
        db = client["cpppac"]
        collection = db["sentenciados"]

        collection.drop()  # Limpa a coleção antes de inserir novos dados

        df = pd.read_csv("banco.csv", sep=";", encoding="utf-8-sig")
        documentos = df.to_dict(orient="records")
        resultado = collection.insert_many(documentos)
        print(f"{len(resultado.inserted_ids)} documentos inseridos no MongoDB.")

    except Exception as e:
        print(f"❌ Erro ao conectar ou inserir no MongoDB: {e}")
    finally:
        client.close()


def clean_matricula_complete():
    db = conexao()
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


if __name__ == "__main__":
    exportar_para_csv()
    importar_mongo()
    clean_matricula_complete()
    print("Processo concluído!")

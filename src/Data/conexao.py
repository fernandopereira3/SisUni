import os
from pymongo import MongoClient
from sqlalchemy import create_engine

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = "cpppac"
MYSQL_URI = os.getenv(
    "MYSQL_URI", "mysql+mysqlconnector://root:futuro07@10.0.0.2:3309/siscar"
)

# Cliente único — todos os módulos compartilham o mesmo pool de conexões
_client = MongoClient(MONGO_URI)
_db = _client[MONGO_DB]


def conexao_mongo():
    return _db


cpppac = conexao_mongo


def conexao_sql():
    return create_engine(MYSQL_URI)

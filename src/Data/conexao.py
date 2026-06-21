import os
from pymongo import MongoClient
from sqlalchemy import create_engine

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = "cpppac"
MYSQL_URI = os.getenv(
    "MYSQL_URI", "mysql+mysqlconnector://root:futuro07@10.0.0.2:3309/siscar"
)


def conexao_mongo():
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB]


def conexao_sql():
    return create_engine(MYSQL_URI)

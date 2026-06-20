from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/cpppac")


def conexao_mongo():
    mongo = PyMongo(app)
    db = mongo.db
    mongo.db.command("ping")
    print("Conexão bem-sucedida ao MongoDB!")
    return db


def conexao_sql():
    from sqlalchemy import create_engine

    engine = create_engine("mysql+mysqlconnector://root:futuro07@10.0.0.2:3309/siscar")
    return engine

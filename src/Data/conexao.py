from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/cpppac")

def conexao():
    mongo = PyMongo(app)
    db = mongo.db
    mongo.db.command("ping")
    print("Conexão bem-sucedida ao MongoDB!")
    return db

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
# MongoDB connection via Docker: Flask container talks to MongoDB container named 'mongo'
app.config["MONGO_URI"] = "mongodb://mongo:27017/cpppac"


class MockResult:
    def __init__(self):
        self.inserted_id = None
        self.modified_count = 0
        self.matched_count = 0
        self.deleted_count = 0
        self.acknowledged = True


class MockCursor:
    def __init__(self, data=None):
        self.data = data or []

    def sort(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def skip(self, *args, **kwargs):
        return self

    def __iter__(self):
        return iter(self.data)


class MockCollection:
    def find(self, *args, **kwargs):
        return MockCursor()

    def find_one(self, *args, **kwargs):
        return None

    def count_documents(self, *args, **kwargs):
        return 0

    def insert_one(self, *args, **kwargs):
        return MockResult()

    def update_one(self, *args, **kwargs):
        return MockResult()

    def delete_one(self, *args, **kwargs):
        return MockResult()

    def delete_many(self, *args, **kwargs):
        return MockResult()

    def aggregate(self, *args, **kwargs):
        return MockCursor()


class MockDB:
    def __getattr__(self, name):
        return MockCollection()

    def list_collection_names(self):
        return []

    def command(self, *args, **kwargs):
        pass


def conexao():
    try:
        mongo = PyMongo(app)
        db = mongo.db
        mongo.db.command("ping")
        print("Conexão bem-sucedida ao MongoDB!")
        return db

    except Exception as e:
        print("Usando MockDB para execução sem banco de dados.")
        return MockDB()

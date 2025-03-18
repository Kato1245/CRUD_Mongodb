from pymongo import MongoClient
# import certifi

MONGO_URI = 'mongodb://localhost:27017/'
# ca = certifi.where() -  tlsCAFile = ca

def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client["db_crud"]
    except ConnectionError:
        print('Error de conexión con la db')
    return db



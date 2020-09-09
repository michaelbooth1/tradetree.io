import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('tradetree-d9eb6-ee8e440b5851.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_database():
    return db



import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def uploadFile(filename):
    cred = credentials.Certificate('serviceAccount.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()






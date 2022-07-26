import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid

def uploadFile(df):
    cred = credentials.Certificate('serviceAccount.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    doc_ref = db.collection(u'Data').document(str(uuid.uuid4()))
    doc_ref.set({
    df
})










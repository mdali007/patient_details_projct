from pymongo import MongoClient
from django.conf import settings

def get_db():
    client = MongoClient(settings.MONGO_URI)
    return client[settings.MONGO_DB_NAME]

def init_db():
    db = get_db()
    if "patients" not in db.list_collection_names():
        db.create_collection("patients")
        db.patients.create_index("patient_id", unique=True)
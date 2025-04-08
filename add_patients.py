# from pymongo import MongoClient
# client = MongoClient("mongodb+srv://dbUser:DBpassword123@cluster0.aqkwkpd.mongodb.net/?retryWrites=true&w=majority")
# db = client["patient_db"]
# print("Collections:", db.list_collection_names())

from pymongo import MongoClient
import random
from datetime import datetime, timedelta
import faker

fake = faker.Faker()

#  MongoDB Atlas config
MONGO_URI = "mongodb+srv://dbUser:DBpassword123@cluster0.aqkwkpd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB_NAME = "patient_db"

#  Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db['patients']

#  Config values
blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
genders = ['Male', 'Female', 'Other']
diseases = ['Cold', 'Fever', 'Diabetes', 'Covid', 'Flu', 'Injury']

#  Insert 100 fake patients
for i in range(100):
    dob = fake.date_of_birth(minimum_age=20, maximum_age=60)
    patient = {
        'patient_id': f"P-{1000+i}",
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_birth': dob.strftime('%Y-%m-%d'),
        'gender': random.choice(genders),
        'blood_type': random.choice(blood_types),
        'disease': random.choice(diseases)
    }
    collection.insert_one(patient)

print(" Successfully inserted 100 patients into MongoDB Atlas ")

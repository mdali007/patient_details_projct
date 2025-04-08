from django.http import JsonResponse
from django.shortcuts import render
from .mongo_ut import get_db
from bson import ObjectId
import json

# Serialization function
def serialize_patient(p):
    return {
        "id": str(p["_id"]),
        "patient_id": p.get("patient_id", ""),
        "first_name": p.get("first_name", ""),
        "last_name": p.get("last_name", ""),
        "date_of_birth": p.get("date_of_birth", ""),
        "gender": p.get("gender", ""),
        "blood_type": p.get("blood_type", ""),
        "disease": p.get("disease", ""),
    }

def index(request):
    return render(request, 'list.html')

def get_patients(request):
    db = get_db()
    collection = db.patients

    page = int(request.GET.get('page', 1))
    per_page = 20
    skip = (page - 1) * per_page

    query = {}
    
    # Handle all search parameters
    if request.GET.get('patient_id'):
        query['patient_id'] = {'$regex': request.GET['patient_id'], '$options': 'i'}
    
    if request.GET.get('first_name'):
        query['first_name'] = {'$regex': request.GET['first_name'], '$options': 'i'}
    
    if request.GET.get('last_name'):
        query['last_name'] = {'$regex': request.GET['last_name'], '$options': 'i'}
    
    if request.GET.get('date_of_birth'):
        query['date_of_birth'] = request.GET['date_of_birth']
    
    if request.GET.get('gender'):
        query['gender'] = request.GET['gender']
    
    if request.GET.get('blood_type'):
        query['blood_type'] = {'$regex': request.GET['blood_type'], '$options': 'i'}
    
    if request.GET.get('disease'):
        query['disease'] = {'$regex': request.GET['disease'], '$options': 'i'}

    total = collection.count_documents(query)
    raw_patients = collection.find(query).skip(skip).limit(per_page)

    patients = [serialize_patient(p) for p in raw_patients]

    return JsonResponse({
        'patients': patients,
        'pages': (total + per_page - 1) // per_page,
        'total': total
    })



def add_patients(request):
    if request.method == 'POST':
        db = get_db()
        collection = db.patients

        data = json.loads(request.body)
        new_patient = {
            "patient_id":data.get('patient_id','').strip(),
            "first_name":data.get('first_name',''),
            "last_name":data.get('last_name',''),
            "date_of_birth":data.get('date_of_birth',''),
            "gender":data.get('gender',''),
            "blood_type":data.get('blood_type',''),
            "disease":data.get('disease','')
        }
        result = collection.insert_one(new_patient)

        return JsonResponse({
                'status': 'success',
                'message': 'Patient added successfully!',
                'patient_id': str(result.inserted_id)
            })
    

def pat_details(request, patient_id):
     db = get_db()
     collection = db.patients

     patient = collection.find_one({"patient_id": patient_id})
     return render(request, 'pat_detail.html', {'patient': patient})


def delete_patient(request, patient_id):
    db = get_db()
    collection = db.patients
    
    collection.delete_one({'patient_id': patient_id})
    return redirect(request.META.get('HTTP_REFERER', '/'))
    

from django.urls import path
from core import views

urlpatterns = [
    path('', views.index),
    path('api/patients/', views.get_patients),
    path('api/addpatients/', views.add_patients),
    path('patient-details/<str:patient_id>/', views.pat_details),
    path('deletepatient/<str:patient_id>/', views.delete_patient),
]

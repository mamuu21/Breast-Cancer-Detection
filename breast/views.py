from django.db.models.query import QuerySet
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import Patient
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.shortcuts import render

import logging
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .tflite_model import TFLiteModel as TFLModel

import numpy as np
from PIL import Image

import io
import requests


# @method_decorator(csrf_exempt, name='dispatch')
# class PredictView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body.decode('utf-8')).get('input_data')
#             if data is None:
#                 return JsonResponse({'error': 'No input data provided'}, status=400)
            
#             prediction_result = tflite_model.predict(data)
#             return JsonResponse({'prediction': prediction_result})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

# Configure logging


logger = logging.getLogger(__name__)        
        
class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = "login"
    
    
    def get_context_data(self, **kwargs):
        # Filter patients with breast cancer
        cancer_patients = Patient.objects.filter(status=True)

        # Filter patients with no breast cancer
        normal_patients = Patient.objects.filter(status=False)

        # Count the number of patients with breast cancer and no breast cancer
        cancer_count = cancer_patients.count()
        normal_count = normal_patients.count()

        return {
            "cancer_count": cancer_count,
            "normal_count": normal_count
        }
        
    
class PatientListView(ListView):
    template_name = "patient_list.html"
    model = Patient
    
    
class ReportView(TemplateView):
    template_name = "report.html"
   

class PatientDetailsView(TemplateView):
    template_name = "patient_details.html"
    
    def post(self, request,*args):
        
        print('start point 2')
        if request.method=='POST':
            patient_id = request.POST.get('data')
            print(patient_id)
        else:
            print('failed')
    
    
class ImageView(ListView):
    template_name = "images.html" 
    model = Patient
    
    
    def get_queryset(self):
        return Patient.objects.all()
       
    
class AddPatientView(CreateView):
    template_name = "add_patient.html"
    model = Patient
    fields = ["patient_id", "name", "age", "gender", "image"]
    success_url = reverse_lazy("analysis_page")
    

    def form_valid(self, form):
        form.instance.status = True  # Assuming True represents "normal"
        form.save()
        return super().form_valid(form)
   
    # TODO : adding model to investigate uploaded image for cancer detection
      
      
class AnalysisPageView(TemplateView):
    template_name = "analysis_page.html"
    
    
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, RadiologistComment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .tflite_model import TFLiteModel as TFLModel
      
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
      

    def form_valid(self, form):
        form.instance.status = True  # Assuming True represents "normal"
        form.save()
        return super().form_valid(form)
    
    # take patient id from the form and redirect to the analysis page
    def get_success_url(self):
        return reverse_lazy("analysis_page", kwargs={"patient_id": self.object.patient_id})
        
        
        
      
      
class AnalysisPageView(DetailView):
    template_name = "analysis_page.html"
    model = Patient
    context_object_name = "patient"
    slug_url_kwarg = 'patient_id'
    
    
    def get_object(self, queryset=None):
        return self.model.objects.get(patient_id=self.kwargs.get('patient_id'))
    
    def post(self, request, *args, **kwargs):
        patient_id = self.kwargs.get('patient_id')
        comment = request.POST.get('comment')
        
        patient = Patient.objects.get(patient_id=patient_id)
        radiologist = request.user
        
        RadiologistComment.objects.create(
            patient=patient,
            radiologist=radiologist,
            comment=comment
        )
        
        return super().get(request, *args, **kwargs)
    
    
    # use LTModel to perform cancer detection from the image
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        patient = context['patient']
        image_path = patient.image.path
        print(image_path)
        
        model = TFLModel(image_path=image_path)
        prediction = model.predict()
        
        print(prediction)
        
        if prediction == 0:
            result = 'Normal'  
        else:
            result = 'Cancerous'
            
        print(result)
        
        context['result'] = result
        
        return context
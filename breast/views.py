from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import Patient
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


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

class PatientDetailsView(TemplateView):
    template_name = "patient_details.html"
    
    def post(self, request,*args):
        
        print('start point 2')
        if request.method=='POST':
            patient_id = request.POST.get('data')
            print(patient_id)
        else:
            print('failed')
    
class AnalysisPageView(TemplateView):
    template_name = "analysis_page.html"
    
class ImageView(ListView):
    template_name = "images.html" 
       
    
class AddPatientView(CreateView):
    template_name = "add_patient.html"
    model = Patient
    fields = ["patient_id", "name", "age", "gender", "image"]
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self, form):
        # Set status to "normal" before saving the form
        form.instance.status = True  # Assuming True represents "normal"
        return super().form_valid(form)
    
    # TODO : adding model to investigate uploaded image for cancer detection
      
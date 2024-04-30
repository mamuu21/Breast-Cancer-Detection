from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import Patient
from django.urls import reverse_lazy
from django.http import JsonResponse


class DashBoardView(TemplateView):
    template_name = "dashboard.html"
    
    
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
       
    
class LoginView(LoginView):
    template_name = "login.html"
    

    
class LogoutView(LogoutView):
    template_name = "login.html"
    # success_url = reverse_lazy('login')
    
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        form.save()  # Save the user
        return super().form_valid(form) 
    
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
    
def getUserDetails(request):
    print('helolo')
    if request.method=='POST':
        request_getdata = request.POST.get('patient_id')
        print(request_getdata)
        
    else:
        print('No data')    
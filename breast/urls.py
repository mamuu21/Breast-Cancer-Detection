from django.urls import path
from .views import DashBoardView, AddPatientView, PatientListView, ImageView, LoginView, RegisterView, LogoutView, PatientDetailsView, AnalysisPageView

urlpatterns = [
    path("", DashBoardView.as_view(), name="dashboard"),
    path("add_patient/", AddPatientView.as_view(), name="add_patient"),
    path("patient_list/", PatientListView.as_view(), name="patient_list"),
    path("images/", ImageView.as_view(), name="images"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("patient_details/", PatientDetailsView.as_view(), name="patient_details"),
    path("analysis_page/", AnalysisPageView.as_view(), name="analysis_page"),
    
    
    
  
] 
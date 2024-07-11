from django.urls import path
from .views import DashBoardView, AddPatientView, PatientListView, ImageView, PatientDetailsView, AnalysisPageView, ReportView
from django.contrib.auth.views import LoginView, LogoutView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html", next_page="dashboard"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", DashBoardView.as_view(), name="dashboard"),
    path("add_patient/", AddPatientView.as_view(), name="add_patient"),
    path("patient_list/", PatientListView.as_view(), name="patient_list"),
    path("images/", ImageView.as_view(), name="images"),
    path("patient_details/", PatientDetailsView.as_view(), name="patient_details"),
    path("analysis/<str:patient_id>/", AnalysisPageView.as_view(), name="analysis_page"),
    path("report/", ReportView.as_view(), name="report"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

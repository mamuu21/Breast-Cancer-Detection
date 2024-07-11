from django.contrib import admin
from .models import Patient, CustomUser, RadiologistComment
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "name", "gender", "status")
    search_fields = ("patient_id", "name", "status")
    list_filter = ("status",)
    ordering = ("name", "status")
    list_per_page = 10
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter patients based on the admin class
        if self.__class__.__name__ == 'AdminCancerPatient':
            return qs.filter(status=True)
        elif self.__class__.__name__ == 'AdminNormalPatient':
            return qs.filter(status=False)
        else:
            return qs


class AdminRadiologistComment(admin.ModelAdmin):
    list_display = ("patient", "radiologist", "date")
    search_fields = ("patient", "radiologist")
    list_filter = ("date",)
    ordering = ("date",)
    list_per_page = 10
    
    
class AdminCancerPatient(PatientAdmin):
    pass
    
class AdminNormalPatient(PatientAdmin):
    pass
    
class AdminUser(admin.ModelAdmin):
    list_display = ("username", "first_name", "middle_name", "last_name", "email", "is_radiologist")
    search_fields = ("username", "first_name", "last_name")
    list_filter = ("last_name",)

admin.site.register(Patient, PatientAdmin)  # Register the base class
admin.site.register(CustomUser, AdminUser)
admin.site.register(RadiologistComment, AdminRadiologistComment)

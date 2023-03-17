from django.urls import path
from .views import OnboardingAPI, DashboardAPI, PatientUserInfo, DoctorAPI, PatientUserInfoByID, DoctorAlerts, UserHomePage, AddFileAPI

urlpatterns = [
    
    # Main API
    path('onboarding', OnboardingAPI.as_view(), name='onboarding'),
    
    path('dashboard/<user_id>', DashboardAPI.as_view(), name='dashboard'),
    
    path('patient-user-info',PatientUserInfo.as_view(), name='patient-user-info'),
    path('patient/<user_id>',PatientUserInfoByID.as_view() ,name='patient-user'),
    
    path('doctor-user-info',DoctorAPI.as_view(), name='doctor-user-info'),
    path('docter-alerts', DoctorAlerts.as_view(), name='doctor-user-info'),
    
    path('user-dashboard/<user_id>',UserHomePage.as_view(), name='user-homepage'),
    path('add-files', AddFileAPI.as_view(), name='add-files'),
    
    
    #Open API's
    
    
    
    #Socket API urls
    
    
    
    
    ]
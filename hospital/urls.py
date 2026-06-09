from django.urls import path    
from . import views
urlpatterns = [
   path('',views.home,name='home'),
   path('register/', views.patient_register, name='patient_register'),
   path('login/',views.signin,name='signin'),
   path('patient-dashboard/',views.patient_dashboard,name='patient_dashboard'),
   path('book-appointment/',views.book_appointment,name='book_appointment'),
   path('appointment-status/',views.appointment_status,name='appointment_status'),
   path('prescription/',views.prescription,name='prescription'),
   path('doctor-details/',views.doctor_details,name='doctor_details'),
   path('signout/',views.signout,name='signout'),
   path('doctor-dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
   path('doctor-appointments/',views.doctor_appointments,name='doctor_appointments'),
   path('patient-details/',views.patient_details,name='patient_details'),  
]
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
   path('update-notes/<int:appointment_id>/',views.update_notes,name='update_notes'),
   path('add-prescription/<int:appointment_id>/',views.add_prescription,name='add_prescription'),
   path('manage-availability/',views.manage_availability,name='manage_availability'),
   path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
   path('add-department/',views.add_department,name='add_department'),
   path('view-departments/',views.view_departments,name='view_departments'),
   path('add-doctor/',views.add_doctor,name='add_doctor'),
   path('view-doctors/',views.view_doctors,name='view_doctors'),
   path('view-patients/',views.view_patients,name='view_patients'),
   path('view-appointments/',views.view_appointments,name='view_appointments'),
   path('generate-report/',views.generate_report,name='generate_report'),
   path(
    'doctor-dates/<int:doctor_id>/',
    views.doctor_available_dates,
    name='doctor_available_dates'
),
path(
    'download-report/',
    views.download_report,
    name='download_report'
),
]
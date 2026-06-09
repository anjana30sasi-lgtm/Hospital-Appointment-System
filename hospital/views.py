
from django.shortcuts import render,redirect    
from django.contrib.auth import authenticate, login, logout
from .forms import Doctor, patientRegisterForm,LoginForm,AppointmentForm
from .models import Appointment    
# Create your views here.
def home(request):
    return render(request,'home.html')

def patient_register(request):
    form = patientRegisterForm()
    if request.method == "POST":
        form = patientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'home.html')
    return render(request,'patient_register.html',{"form":form})
def signin(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:
                login(request, user)

                return redirect('patient_dashboard')  # HERE

    else:
        form = LoginForm()

    return render(request,'signin.html',{'form':form})
def patient_dashboard(request):
    return render(request,'patient_dashboard.html')
def book_appointment(request):
    form = AppointmentForm()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data["department"]
            doctor = form.cleaned_data["doctor"]
            appointment_date = form.cleaned_data["appointment_date"]
            appointment_time = form.cleaned_data["appointment_time"]

            # Save the appointment to the database
            appointment = Appointment(
                patient=request.user.patient,  # Assuming you have a Patient model linked to the User model
                doctor=doctor,
                department=department,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            appointment.save()

            return redirect('patient_dashboard')  # Redirect to the dashboard after booking

    return render(request, 'book_appointment.html', {'form': form})
def appointment_status(request):
    appointments=Appointment.objects.all()
    return render(request,'appointment_status.html',{'appointments':appointments})
def prescription(request):
    appointments=Appointment.objects.all()
    return render(request,'prescription.html',{'appointments':appointments})
def doctor_details(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_details.html', {'doctors': doctors})
def signout(request):
    logout(request)
    return redirect('home')
def doctor_dashboard(request):
    return render(request,'doctor_dashboard.html')
def doctor_appointments(request):
    appointments=Appointment.objects.all() 
    return render(request, 'doctor_appointments.html', {'appointments': appointments}   )
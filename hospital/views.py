
from django.shortcuts import render,redirect    
from django.contrib.auth import authenticate, login, logout
from .forms import Doctor, patientRegisterForm,LoginForm,AppointmentForm
from .models import Appointment, Availability, Department, Patient
from django.contrib.auth.models import User    
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

                if user.is_superuser:
                    return redirect('admin_dashboard')

                elif user.is_staff:
                    return redirect('doctor_dashboard')

                else:
                    return redirect('patient_dashboard')

            else:
                form.add_error(
                    None,
                    "Invalid Email or Password"
                )

    else:
        form = LoginForm()

    return render(
        request,
        'signin.html',
        {'form': form}
    )
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
def patient_details(request):
    patients = Patient.objects.all()
    return render(request,'patient_details.html')
def update_notes(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        notes = request.POST.get('notes')
        appointment.notes = notes
        appointment.save()
        return redirect('doctor_appointments')
    return render(request, 'update_notes.html', {'appointment': appointment})
def add_prescription(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        prescription = request.POST.get('prescription')
        appointment.prescription = prescription
        appointment.save()
        return redirect('doctor_appointments')
    return render(request, 'add_prescription.html', {'appointment': appointment})
def manage_availability(request):
    # Logic to manage doctor availability
    if request.method == "POST":
        doctor=Doctor.objects.get(id=request.POST.get('doctor_id'))
        Availability.objects.create(
            doctor=doctor,
            date=request.POST.get('date'),
            status=request.POST.get('status')
        )
        return redirect('doctor_dashboard')
    doctors = Doctor.objects.all()
    return render(request, 'manage_availability.html', {'doctors': doctors})
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def add_department(request):
   if request.method == "POST":
           name = request.POST.get('name')
           department = department.objects.create(name=name)
           return redirect('view_departments')  # Redirect to the department list page after adding a new department
    # Logic to add a new department
   return render(request, 'add_department.html')

def view_departments(request):
    departments = Department.objects.all()
    return render(request, 'view_departments.html', {'departments': departments})

def add_department(request):

    if request.method == "POST":

        name = request.POST.get('name')

        Department.objects.create(
            name=name
        )

        return redirect('view_departments')

    return render(request, 'add_department.html')
def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'view_doctors.html', {'doctors': doctors})
def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'view_patients.html', {'patients': patients})  
def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'view_appointments.html', {'appointments': appointments})      
def add_doctor(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization')
        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)
        doctor = Doctor.objects.create(
            name=name,
            email=email,
            phone=phone,
            specialization=specialization,
            department=department
        )
        User.objects.create_user(
    username=email,
    email=email,
    password=password,
    is_staff=True
)
        return redirect('view_doctors')  # Redirect to the doctor list page after adding a new doctor
    departments = Department.objects.all()
    return render(request, 'add_doctor.html', {'departments': departments})
def generate_report(request):
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    appointments = Appointment.objects.all()
    context = {
        'total_patients': total_patients,   

        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'appointments': appointments
    }
    return render(request, 'generate_report.html', context)

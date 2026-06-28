
from django.shortcuts import render,redirect    
from django.contrib.auth import authenticate, login, logout
from .forms import  patientRegisterForm,LoginForm,AppointmentForm
from .models import Appointment, Availability, Department, Patient, Doctor
from django.contrib.auth.models import User    
from django.http import JsonResponse
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# Create your views here.
def home(request):
    return render(request,'home.html')

def patient_register(request):
    form = patientRegisterForm()
    if request.method == "POST":
        form = patientRegisterForm(request.POST)
        if form.is_valid():

            patient = form.save()

            User.objects.create_user(
        username=patient.email,
        email=patient.email,
        password=form.cleaned_data['password']
    )

            return redirect('home')
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
    return render(request,'patient_dashboard.html',{'patient_name': request.user.username})

def book_appointment(request):

    form = AppointmentForm(request.POST or None)

    if request.method == "POST":

        print("POST DATA:", request.POST)

        if form.is_valid():

            doctor = form.cleaned_data["doctor"]
            appointment_date = form.cleaned_data["appointment_date"]
            appointment_time = form.cleaned_data["appointment_time"]

            patient = Patient.objects.get(
                email=request.user.email
            )

            availability = Availability.objects.filter(
                doctor=doctor,
                date=appointment_date,
                status="Available"
            ).exists()

            print("Availability:", availability)

            if not availability:

                form.add_error(
                    None,
                    "Doctor is not available on this date"
                )

            else:

                already_booked = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time
                ).exists()

                print("Already Booked:", already_booked)

                if already_booked:

                    form.add_error(
                        None,
                        "This time slot is already booked"
                    )

                else:

                    Appointment.objects.create(
                        patient=patient,
                        doctor=doctor,
                        appointment_date=appointment_date,
                        appointment_time=appointment_time
                    )

                    print("Appointment Saved Successfully")

                    return redirect('patient_dashboard')

        else:

            print("Form Errors:", form.errors)

    return render(
        request,
        'book_appointment.html',
        {'form': form}
    )

def prescription(request):

    patient = Patient.objects.get(
        email=request.user.email
    )

    appointments = Appointment.objects.filter(
        patient=patient
    )

    return render(
        request,
        'prescription.html',
        {'appointments': appointments}
    )
def doctor_details(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_details.html', {'doctors': doctors})

def signout(request):
    logout(request)
    return redirect('home')

def doctor_dashboard(request):
    return render(request,'doctor_dashboard.html')

def doctor_appointments(request):

    doctor = Doctor.objects.get(
        email=request.user.email
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    )

    return render(
        request,
        'doctor_appointments.html',
        {'appointments': appointments}
    )
def view_patients(request):

    patients = Patient.objects.all()

    return render(
        request,
        'view_patients.html',
        {
            'patients': patients
        }
    )
def patient_details(request):

    doctor = Doctor.objects.get(
        email=request.user.email
    )

    patients = Patient.objects.filter(
        appointment__doctor=doctor
    ).distinct()

    return render(
        request,
        'patient_details.html',
        {
            'patients': patients
        }
    )

def update_notes(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        notes = request.POST.get('notes')
        appointment.notes = notes
        appointment.save()
        return redirect('doctor_appointments')
    return render(request, 'update_notes.html', {'appointment': appointment})

def add_prescription(request, appointment_id):

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    if request.method == "POST":

        appointment.prescription = request.POST.get(
            'prescription'
        )

        appointment.status = "Completed"

        appointment.save()

        return redirect(
            'doctor_appointments'
        )

    return render(
        request,
        'add_prescription.html',
        {'appointment': appointment}
    )

def manage_availability(request):

    doctor = Doctor.objects.get(
        email=request.user.email
    )

    if request.method == "POST":

        Availability.objects.create(
            doctor=doctor,
            date=request.POST.get('date'),
            status=request.POST.get('status')
        )

        return redirect('doctor_dashboard')

    return render(
        request,
        'manage_availability.html',
        {'doctor': doctor}
    )

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
def appointment_status(request):

    patient = Patient.objects.get(
        email=request.user.email
    )

    appointments = Appointment.objects.filter(
        patient=patient
    )

    return render(
        request,
        'appointment_status.html',
        {'appointments': appointments}
    )
def doctor_available_dates(request, doctor_id):

    dates = Availability.objects.filter(
        doctor_id=doctor_id,
        status="Available"
    )

    available_dates = []

    for d in dates:

        available_dates.append(
            d.date.strftime("%Y-%m-%d")
        )

    return JsonResponse(
        available_dates,
        safe=False
    )
def download_report(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hospital_report.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>Hospital Appointment System Report</b>", styles["Title"]))

    data = [["Patient", "Doctor", "Date", "Time", "Status"]]

    appointments = Appointment.objects.all()

    for a in appointments:
        data.append([
            a.patient.name,
            a.doctor.name,
            str(a.appointment_date),
            str(a.appointment_time),
            a.status
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.blue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    elements.append(table)

    doc.build(elements)

    return response
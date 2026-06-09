from django import forms
from .models import Doctor, Patient,Department,Appointment

class patientRegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"Password"}),
        label="Password",
    )

    class Meta:
        model= Patient
        fields = ["name","email","age","password"]
        widgets = {
            "name":forms.TextInput(attrs={"placeholder": "Name"}),
            "age": forms.NumberInput(attrs={"placeholder": "Age"}),

        }
        labels = {
            "name": "Name",
            "email": "Email",
            "age": "Age",
            "password":"Password",
        }


class LoginForm(forms.Form):
    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )
class AppointmentForm(forms.Form):
     department = forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Select Department")

     doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),empty_label="Select Doctor")
     appointment_date = forms.DateField(widget=forms.SelectDateWidget())
     appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
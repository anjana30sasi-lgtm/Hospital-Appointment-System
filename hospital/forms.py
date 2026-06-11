from django import forms
from .models import Doctor, Patient,Department,Appointment

class patientRegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder":"Password"}
        )
    )

    class Meta:
        model = Patient

        fields = [
            "name",
            "email",
            "age",
            "phone",
            "address"
        ]
class LoginForm(forms.Form):
    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )
class AppointmentForm(forms.Form):

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department"
    )

    doctor = forms.ModelChoiceField(
    queryset=Doctor.objects.none(),
    empty_label="Choose Doctor"
)

    appointment_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'})
)

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'department' in self.data:
            department_id = self.data.get('department')

            self.fields['doctor'].queryset = Doctor.objects.filter(
                department_id=department_id
            )
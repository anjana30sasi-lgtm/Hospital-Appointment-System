from django import forms
from .models import Book, Register

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title","author","price","published_date"]
        widgets= {
            "published_date":forms.DateInput(attrs={"type":"date"}),
            
        }
class RegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"Password"}),
        label="Password",
    )

    class Meta:
        model= Register
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
    email=forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"Password"}),
        label="Password",
    )
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import Book, Register
from .forms import BookForm,RegisterForm,LoginForm

# Create your views here.
def home(request):
    return render(request,'home.html')

def customer_list(request):
    return render(request, 'customer_list.html')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=BookForm()
    return render(request,'add_books.html',{"form":form})
def viewBooks(request):
    books=Book.objects.all()
    return render(request, 'view_books.html', {'books': books})
def signup(request):
    if request.method == 'POST':
       ''' name=request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        password =  request.POST.get('password')

        Register.objects.create_user(username=email,email=email,password=password,name=name,age=age)

        return redirect('home')
    return render(request,'signup.html')'''
       
       form = RegisterForm(request.POST)
       if form.is_valid():
           user=form.save(commit=False)
           user.username = form.cleaned_data.get("email","")
           user.set_password(form.cleaned_data["password"])
           user.save()
           print("Saved Successfully")
           return redirect('home')
    else:
           form = RegisterForm()
    return render(request, 'signup.html',{"form":form})   

def viewUser(request):
    users=Register.objects.all()
    return render(request, 'users.html',{'data':users})
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user = authenticate(request,username=email,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None,"Invalid email or password")
        else:
            form=LoginForm()
    else:
        form=LoginForm()
    return render(request, 'signin.html',{"form":form})
def signout(request):
    logout(request)
    return redirect('home')
def view_users(request):
    users=Register.objects.filter(is_superuser=False)
    return render(request, 'view_users.html',{"users":users})
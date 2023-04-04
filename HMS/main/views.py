from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Student, Person
from .forms import StudentAdmissionForm
# Create your views here.
@login_required(login_url = "main-login")
def index(request):
    role = request.user.role
    if role == "admission":
        return redirect("admission-index")
    return render(request, "index-student.html")

@login_required(login_url = "main-login")
def admissionIndex(request):
    if request.user.role != "admission":
        return redirect("index")
    return render(request, 'index-admission.html')

@login_required(login_url = "main-login")
def newAdmission(request):
    if request.user.role != "admission":
        return redirect("index")
    if request.method == 'POST':
        form = StudentAdmissionForm(request.POST)
        if form.is_valid():
            person = Person.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                address = form.cleaned_data['address'],
                telephoneNumber = form.cleaned_data['telephoneNumber'],
            )
            # create a new Student object associated with the Person object
            student = Student.objects.create(
                person = person,
                rollNumber = "sad",
            )
            return HttpResponse("Hemlo")
        else:
            return HttpResponse("SadLyf")
    else:
        form = StudentAdmissionForm()
    return render(request, 'student_admission.html', {'form': form})
    

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.success(request, "Skill Issue")
            return redirect("main-login")
    else:
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form})
        
def logoutUser(request):
    logout(request)
    messages.success(request, "You need some milk")
    return redirect("main-login")
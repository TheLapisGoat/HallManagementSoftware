from django.shortcuts import render, redirect
from datetime import date
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from .models import Student, Person, Hall, MessAccount, MessAccountHistory, Complaint, Warden
from .forms import StudentAdmissionForm, MessAccountFormSet, ComplaintForm, WardenCreationForm, WardenAdmissionForm

def getFreeRoom():
    halls = Hall.objects.all()
    for hall in halls:
        if hall.getCurrentOccupancy() < hall.getMaxOccupancy():
            rooms = hall.boarderRooms.all()
            for room in rooms:
                if room.currentOccupancy < room.maxOccupancy:
                    return room
    return None

@login_required(login_url = "main-login")
def index(request):
    role = request.user.role
    if role == "admission":
        return redirect("admission-index")
    elif role == "student":
        name = request.user.first_name + " " + request.user.last_name
        hall = request.user.student.hall.name
        roomNumber = request.user.student.room.roomNumber
        rent = request.user.student.room.rent
        sum_amenity = request.user.student.hall.amenityRooms.aggregate(Sum('rent'))['rent__sum']
        context = {'name': name, 'room': roomNumber, 'hall': hall, 'rent': rent, 'sum_amenity': sum_amenity,}
        return render(request, "index-student.html",context )
    elif role == "mess_manager":
        return redirect("messmanager-index")
    else:
        return HttpResponse("Damn Boi")

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
            
            room = getFreeRoom()
            if room is None:
                form.add_error(field = None, error = "Error! There is no space left in the institute")
                return render(request, 'student_admission.html', {'form': form})
            
            person = Person.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                address = form.cleaned_data['address'],
                telephoneNumber = form.cleaned_data['telephoneNumber'],
            )
            
            student = Student.objects.create(
                person = person,
                rollNumber = form.cleaned_data['rollNumber'],
                hall = room.hall,
                room = room
            )
            
            return redirect("admission-index")
        else:
            return render(request, 'student_admission.html', {'form': form})
    else:
        form = StudentAdmissionForm()
        return render(request, 'student_admission.html', {'form': form})

@login_required(login_url = "main-login")
def messManagerIndex(request):
    if request.user.role != "mess_manager":
        return redirect("index")
    return render(request, 'index-messmanager.html')

@login_required(login_url = "main-login")
def manageMessAccounts(request):
    if request.user.role != "mess_manager":
        return redirect("index")
    
    hall = request.user.mess_manager.hall
    students = Student.objects.filter(hall = hall)
    current_date = date.today()
    
    for student in students:
        mess_account = student.messAccount
        if current_date.month != mess_account.last_update.month or current_date.year != mess_account.last_update.year:
            MessAccountHistory.objects.create(mess_account = mess_account, last_update = mess_account.last_update, due = mess_account.due)
            mess_account.last_update = current_date
            mess_account.due = 0
            mess_account.save()
    
    if request.method == "POST":
        formset = MessAccountFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Mess accounts updated successfully')
            return redirect("manage-mess-accounts")
        else:
            return render(request, 'update-mess-accounts.html', {'formset': formset})
    else:
        mess_accounts = MessAccount.objects.filter(student__in=students).distinct()
        formset = MessAccountFormSet(queryset=mess_accounts)
        
    return render(request, 'update-mess-accounts.html', {"formset": formset})
        
@login_required(login_url = "main-login")
def dues(request):
    if request.user.role != "student":
        return redirect("index")
    student = request.user.student
    room_dues=student.room.rent
    amenity_rooms = request.user.student.hall.amenityRooms.annotate(total_rent=Sum('rent')).values('name', 'total_rent')
    return render(request, 'dues-student.html', {'student': student, 'room_dues': room_dues, 'amenity_rooms': amenity_rooms})

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
        
@login_required(login_url = "main-login")
def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("main-login")

@login_required(login_url = "main-login")
def complaints(request):
    complaints = request.user.student.s_complaints.all()
    return render(request, "complaints.html", {'complaints': complaints})

@login_required(login_url = "main-login")    
def newComplaints(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = Complaint.objects.create(
                student = request.user.student,
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                date = form.cleaned_data['date'],
                nameagainst = form.cleaned_data['nameagainst'],
                complaintregister = request.user.student.hall.complaint_register
            )
            request.user.student.s_complaints.add(complaint)
            return redirect("complaints-student")
        else:
            return render(request, "new-complaints.html", {'form': form})
    else:
        form = ComplaintForm()
        return render(request, 'new-complaints.html', {'form': form})
    
@login_required(login_url = "main-login")
def newWarden(request):
    
    if request.user.role != "admission":
        return redirect("index")
    
    if request.method == 'POST':
        form = WardenAdmissionForm(request.POST)
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
            
            warden = Warden.objects.create(
                person = person,
                hall = form.cleaned_data['hall'],
            )
            
            return redirect("admission-index")
        else:
            return render(request, 'new_warden.html', {'form': form})
    else:
        form = WardenAdmissionForm()
        return render(request, 'new_warden.html', {'form': form})
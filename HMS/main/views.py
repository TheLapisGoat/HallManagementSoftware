from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from .models import Student, Person, Hall, MessAccount, Due, Complaint, Warden, HallClerk, HallEmployee, HallEmployeeLeave, UserPayment, Payment, AmenityRoom
from .forms import StudentAdmissionForm, MessAccountFormSet, PaymentForm, ComplaintForm, WardenCreationForm, WardenAdmissionForm, HallEmployeeForm, HallEmployeeLeaveForm, HallEmployeeEditForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
import time
from decimal import Decimal

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
        return render(request, "index-student.html",context)
    elif role == "mess_manager":
        return redirect("messmanager-index")
    elif role == "hall_clerk":
        return redirect("hallclerk-index")
    elif role == "admin":
        return redirect("admin-index")
    elif role == "warden":
        return redirect("warden-index")
    else:
        return HttpResponse("Damn Boi")
    
@login_required(login_url = "main-login")
def passbook(request):
    if request.user.role != "student":
        return redirect("index")

    student = request.user.student
    passbook = student.passbook
    dues = passbook.dues.order_by('-timestamp')
    payments = passbook.payments.order_by('-timestamp')
    total_due = dues.aggregate(total=Sum('demand'))['total']
    total_paid = payments.aggregate(total=Sum('fulfilled'))['total']

    context = {
        'dues': dues,
        'payments': payments,
        'total_due': total_due,
        'total_paid': total_paid,
    }

    return render(request, 'passbook.html', context)

@login_required(login_url = "main-login")
def pay(request):
    if request.user.role != "student":
        return redirect("index")
    dues = request.user.student.passbook.dues.all()
    payments = request.user.student.passbook.payments.all()
    total_due = dues.aggregate(total = Sum('demand'))['total']
    total_paid = payments.aggregate(total = Sum('fulfilled'))['total']
    
    if total_paid is not None and total_due is not None:
        total_due = total_due - total_paid
    
    total_due = total_due
    total_paid = total_paid
    if total_due is not None and total_due > 0:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.method == 'POST':
            form = PaymentForm(total_due, request.POST)
            if form.is_valid():
                checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(form.cleaned_data['amount']*100), # convert the price to cents
                        'product_data': {
                            'name': 'Fees',
                        },
                    },
                    'quantity': 1,
                },
                ],
                mode='payment',
                customer_creation = 'always',
                success_url=settings.REDIRECT_URL + '/passbook/pay/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.REDIRECT_URL + '/passbook/pay/cancel',
                )
                return redirect(checkout_session.url, code=303)
            else:
                return render(request, 'payment_form.html', {'form': form, 'total_due': total_due})
        else:
            form = PaymentForm(total_due=round(total_due, 2))

        return render(request, 'payment_form.html', {'form': form, 'total_due': round(total_due, 2)})
    else:
        messages.add_message(request, messages.INFO, "You have no dues left")
        return redirect("passbook")

@login_required(login_url = "main-login")
def admissionIndex(request):
    if request.user.role != "admission":
        return redirect("index")
    students = Student.objects.all()
    
    rollNumber_filter = request.GET.get('filter_rollNumber', None)
    hall_filter = request.GET.get('filter_hall', None)
    
    if rollNumber_filter:
        students = students.filter(rollNumber__icontains = rollNumber_filter)
    if hall_filter:
        students = students.filter(hall__name__icontains = hall_filter)
    
    return render(request, 'index-admission.html', {'students': students})

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
def hallClerkIndex(request):
    if request.user.role != "hall_clerk":
        return redirect("index")
    
    employees = HallEmployee.objects.filter(hall = request.user.hall_clerk.hall)
    return render(request, 'index-hallclerk.html', {'employees': employees})
    
@login_required(login_url = "main-login")
def edit_hallemployee(request, pk):
    if request.user.role != "hall_clerk":
        return redirect("index")
    employee = get_object_or_404(HallEmployee, pk = pk)
    
    if request.method == "POST":
        form = HallEmployeeEditForm(request.POST, instance = employee)
        if form.is_valid():
            form.save()
            return redirect('hallclerk-index')
        else:
            return render(request, 'edit_hallemployee.html', {'form': form, 'employee': employee})
        
    form = HallEmployeeEditForm(instance = employee)
    return render(request, 'edit_hallemployee.html', {'form': form, 'employee': employee})

@login_required(login_url = "main-login")
def leaves_hallemployee(request, pk):
    if request.user.role != "hall_clerk":
        return redirect("index")
    employee = get_object_or_404(HallEmployee, pk=pk)
    leaves = employee.leaves.all()
    return render(request, 'leaves_hallemployee.html', {'employee': employee, 'leaves': leaves})

@login_required(login_url = "main-login")
def add_hallemployee_leave(request, pk):
    if request.user.role != "hall_clerk":
        return redirect("index")
    hallemployee = HallEmployee.objects.get(pk=pk)
    form = HallEmployeeLeaveForm(hallemployee, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('leaves-hallemployees', pk=pk)
        else:
            return HttpResponse(form.errors.as_text())
    context = {'form': form, 'hallemployee': hallemployee}
    return render(request, 'add_leave_hallemployee.html', context)

@login_required(login_url="main-login")
def add_hallemployee(request):
    if request.user.role != "hall_clerk":
        return redirect("index")
    
    if request.method == 'POST':
        form = HallEmployeeForm(request.user.hall_clerk.hall, request.POST)
        if form.is_valid():
            form.save()
            return redirect('hallclerk-index')
    else:
        form = HallEmployeeForm(request.user.hall_clerk.hall)
    return render(request, 'add_hallemployee.html', {'form': form})

@login_required(login_url = "main-login")
def delete_hallemployee(request, pk):
    if request.user.role != "hall_clerk":
        return redirect("index")
    employee = get_object_or_404(HallEmployee, pk=pk)
    employee.delete()
    return redirect('hallclerk-index')

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
                nameagainst = form.cleaned_data['complainee'],
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
    
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    student = request.user.student
    Payment.objects.create(passbook = student.passbook, fulfilled = Decimal(session.amount_total)/100)
    user_payment = UserPayment.objects.create(student=student, stripe_checkout_id = checkout_session_id, payment_bool=True)
    user_payment.save()
    return render(request, 'payment_successful.html', {'customer': customer})

def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	return render(request, 'payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = event['data']['object']
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        # line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)

@login_required(login_url = "main-login")
def wardenIndex(request):
    if request.user.role != "warden":
        return redirect("index")
    
    hall = request.user.warden.hall
    currentOccupancy = hall.getCurrentOccupancy()
    maxOccupancy = hall.getMaxOccupancy()
    
    context = {'hall': hall, 'currentOccupancy': currentOccupancy, 'maxOccupancy': maxOccupancy}
    return render(request, 'index-warden.html', context)

@login_required(login_url = "main-login")
def calculate_student_fees(request):
    if request.user.role != "warden":
        return redirect("index")
    
    hall = request.user.warden.hall
    students = hall.students.all()
    amenityFees = AmenityRoom.objects.filter(hall = hall).aggregate(total = Sum('rent'))['total']
    
    totalFees = 0
    for student in students:
        totalFees += student.room.rent + amenityFees + student.messAccount.due
    
    context = {
        'hall': hall,
        'students': students,
        'amenityFees': amenityFees,
        'totalFees': totalFees,
    }
    return render(request, 'calculate_student_fees.html', context)

@login_required(login_url = "main-login")
def confirm_student_fees(request, pk):
    if request.user.role != "warden":
        return redirect("index")
    
    hall = Hall.objects.get(pk=pk)
    students = hall.students.all()
    amenityFees = AmenityRoom.objects.filter(hall = hall).aggregate(total = Sum('rent'))['total']
    
    for student in students:
        passbook = student.passbook
        
        messAccount = student.messAccount
        Due.objects.create(passbook = passbook, demand = messAccount.due, type = 'mess')
        messAccount.due = Decimal('0.00')
        messAccount.save()
        
        Due.objects.create(passbook = passbook, demand = amenityFees, type = 'amenityRooms')
        
        Due.objects.create(passbook = passbook, demand = student.room.rent, type = 'boarderRoom')
    
    return redirect('index')

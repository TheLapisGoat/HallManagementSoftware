from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def home(request):
    return render(request, 'HMS/home.html')

def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
        else:
            form = UserCreationForm()
    form = UserCreationForm()
    return render(response, "HMS/register.html", {"form": form})
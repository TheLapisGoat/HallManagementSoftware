from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person, Student

class PersonCreationForm(UserCreationForm):
    address = forms.CharField(max_length=255, required=True)
    telephoneNumber = forms.IntegerField(required=True)
    role = forms.ChoiceField(choices=Person.ROLES, required=True)

    class Meta:
        model = Person
        fields = ('username', 'email', 'password1', 'password2', 'address', 'telephoneNumber', 'role')
        
class PersonChangeForm(UserChangeForm):
    address = forms.CharField(max_length=255, required=True)
    telephoneNumber = forms.IntegerField(required=True)
    role = forms.ChoiceField(choices=Person.ROLES, required=True)

    class Meta:
        model = Person
        fields = ('username', 'email', 'address', 'telephoneNumber', 'role')
        
class StudentAdmissionForm(forms.Form):
    username = forms.CharField(max_length = 150, required = True)
    password = forms.CharField(widget=forms.PasswordInput, required = True)
    first_name = forms.CharField(max_length = 150, required = True)
    last_name = forms.CharField(max_length = 150, required = True)
    email = forms.EmailField(required = True)
    address = forms.CharField(widget = forms.Textarea, required = True)
    telephoneNumber = forms.IntegerField(required = True)
        
    

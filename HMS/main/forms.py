from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person, MessAccount
from django.core.validators import MinValueValidator

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
    confirm_password = forms.CharField(widget=forms.PasswordInput, required = True)
    rollNumber = forms.CharField(max_length = 100)
    first_name = forms.CharField(max_length = 150, required = True)
    last_name = forms.CharField(max_length = 150, required = True)
    email = forms.EmailField(required = True)
    address = forms.CharField(widget = forms.Textarea, required = True)
    telephoneNumber = forms.IntegerField(required = True)
    
    def clean(self):
        cleaned_data = super(forms.Form, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data
    
# class MessAccountForm(forms.ModelForm):
#     class Meta:
#         model = MessAccount
#         fields = ['student', 'month', 'dues', 'paid']

#     def __init__(self, *args, **kwargs):
#         super(MessAccountForm, self).__init__(*args, **kwargs)
#         self.fields['student'].disabled = True
#         self.fields['month'].widget.attrs['readonly'] = True

class MessUpdateForm(forms.ModelForm):
    
    due = forms.DecimalField(label='Due Amount',required=True, validators=[MinValueValidator(0)], decimal_places = 2, max_digits = 8)
    
    class Meta:
        model = MessAccount
        fields = ['due']
        
MessAccountFormSet = forms.modelformset_factory(model = MessAccount, form = MessUpdateForm, fields=('due',), extra = 0)
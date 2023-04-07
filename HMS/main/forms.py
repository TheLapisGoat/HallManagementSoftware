from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import Person, MessAccount, Student, Hall, BoarderRoom
from django.core.validators import MinValueValidator, MaxValueValidator

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
        
class StudentCreationForm(forms.ModelForm):
    
    username = forms.CharField(max_length = 150, required = True)
    password = forms.CharField(widget=forms.PasswordInput, required = True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required = True)
    first_name = forms.CharField(max_length = 150, required = True)
    last_name = forms.CharField(max_length = 150, required = True)
    email = forms.EmailField(required = True)
    address = forms.CharField(widget = forms.Textarea, required = True)
    telephoneNumber = forms.IntegerField(required = True)
    
    class Meta:
        model = Student
        fields = ('hall', 'rollNumber', 'room')
        
    def save(self, commit=True):
        person = Person.objects.create_user(
                username = self.cleaned_data['username'],
                password = self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email = self.cleaned_data['email'],
                address = self.cleaned_data['address'],
                telephoneNumber = self.cleaned_data['telephoneNumber'],
            )
        student = super().save(commit=False)
        student.person = person
        if commit:
            student.save()
        return student

class StudentChangeForm(forms.ModelForm):
    
    username = forms.CharField(max_length = 150)
    first_name = forms.CharField(max_length = 150)
    last_name = forms.CharField(max_length = 150)
    email = forms.EmailField()
    address = forms.CharField(widget = forms.Textarea)
    telephoneNumber = forms.IntegerField()
    
    class Meta:
        model = Student
        fields = ('hall', 'rollNumber', 'room')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            person = self.instance.person
            self.fields['username'].initial = person.username
            self.fields['first_name'].initial = person.first_name
            self.fields['last_name'].initial = person.last_name
            self.fields['email'].initial = person.email
            self.fields['address'].initial = person.address
            self.fields["telephoneNumber"].initial = person.telephoneNumber
            self.fields['room'].initial = self.instance.room
            self.fields['hall'].initial = self.instance.hall
            self.fields['rollNumber'].initial = self.instance.rollNumber
    
    def save(self, commit=True):
        student = super().save(commit=False)
        person = student.person
        person.username = self.cleaned_data['username']
        person.address = self.cleaned_data['address']
        person.first_name = self.cleaned_data['first_name']
        person.last_name = self.cleaned_data['last_name']
        person.email = self.cleaned_data['email']
        person.telephoneNumber = self.cleaned_data['telephoneNumber']
        person.save()
        student.room = self.cleaned_data['room']
        student.hall = self.cleaned_data['hall']
        student.rollNumber = self.cleaned_data['rollNumber']
        if commit:
            student.save()
        return student
        
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

class MessUpdateForm(forms.ModelForm):
    
    rollNumber = forms.CharField(max_length = 100, disabled = True, label = "Roll Number")
    currentDue = forms.DecimalField(label='Current Due', disabled = True, decimal_places = 2, max_digits = 8)
    due = forms.DecimalField(required=True, validators=[MinValueValidator(0)], decimal_places = 2, max_digits = 8, label = "New Due Amount")
    
    class Meta:
        model = MessAccount
        fields = ['due']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            student = self.instance.student
            self.fields['currentDue'].initial = self.instance.due
            self.fields['rollNumber'].initial = student.rollNumber

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=8, decimal_places=2, validators = [MinValueValidator(10)])
    
    def __init__(self, total_due, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].validators.append(MaxValueValidator(total_due))
        self.fields["amount"].initial = total_due
        
MessAccountFormSet = forms.modelformset_factory(model = MessAccount, form = MessUpdateForm, fields=('rollNumber', 'currentDue', 'due',), extra = 0)
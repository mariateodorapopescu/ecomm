from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
# if you open up the libs you can customize thiungs around there

class UserRegisterForm(UserCreationForm):
# class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Nume de utilizator"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"e-mail"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Parola..."}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirmare parola"}))
    class Meta:
        model = User
        fields = ['username', 'email']

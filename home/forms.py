from django.forms import ModelForm
from .models import Appoinment, Patient


#auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class PatientForm(ModelForm):
	class Meta:
		model = Patient
		fields = '__all__'
		exclude = ['user']


class AppoinmentForm(ModelForm):
	class Meta:
		model = Appoinment
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
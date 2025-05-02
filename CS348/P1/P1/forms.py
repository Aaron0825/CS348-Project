from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2", "groups"]

class TestForm(ModelForm):
	class Meta:
		model = Test
		fields = '__all__'
            
class TRForm(ModelForm):
	class Meta:
		model = TestResult
		fields = ["score"]

class TGradeForm(ModelForm):
	class Meta:
		model = TestResult
		fields = ["student", "score"]

class HWForm(ModelForm):
	class Meta:
		model = Homework
		fields = '__all__'

class HRForm(ModelForm):
	class Meta:
		model = HomeworkResult
		fields = ["score"]

class HGradeForm(ModelForm):
	class Meta:
		model = HomeworkResult
		fields = ["student", "score"]
from django import forms
from django.forms import ModelForm
from .models import RequestQuiz, AddStudent

class RequestForm(ModelForm):
    class Meta:
        model=RequestQuiz
        fields=['region','school', 'student_amount', 'summa', 
        'name', 'iin', 'number', 'limit_in_month', 'limit_start', 'limit_end', 'kvitancia']
        widgets = {
        'region': forms.Select(attrs={'class':'form-control'}),
        'school': forms.TextInput(attrs={'class':'form-control'}),
        'student_amount': forms.TextInput(attrs={'class':'form-control'}),
        'summa': forms.TextInput(attrs={'class':'form-control'}),
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'iin': forms.TextInput(attrs={'class':'form-control'}),
        'number': forms.TextInput(attrs={'class':'form-control'}),
        'limit_start': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
        'limit_end': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
    }

class AddStudentForm(ModelForm):
    class Meta:
        model=AddStudent
        fields=['excel_file']

        widgets = {
        'excel_file': forms.FileInput(attrs={'class':'form-control'}),
    }
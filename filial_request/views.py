from django.shortcuts import render, redirect
from .models import RequestQuiz
from .forms import RequestForm, AddStudentForm
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.
def request_page(request):
    if request.method=='POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponse("Запрос отправлен")
    else:
        form = RequestForm()
        return render(request,'login/request.html', {'form':form})


def add_students(request):
    form = AddStudentForm()
    if request.method=='POST' and request.FILES['document']:
        # form = AddStudentForm(request.POST, request.FILES)
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        return HttpResponse("Ученики добавлены")
        # if form.is_valid():
        #     form.save()
    # context={
    #         'form':form,
    #     }
    return render(request,'quizes/addstudent.html')
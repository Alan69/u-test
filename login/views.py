from django.contrib.auth import logout,authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('login') 
    else: 
        form = CustomUserCreationForm()
        if request.method=='POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'login/auth.html',context)
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
       context={}
       return render(request,'login/login.html',context)
 
def logoutPage(request):
    logout(request)
    return redirect('login')
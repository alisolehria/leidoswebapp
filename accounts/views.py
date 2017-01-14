from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import profile

def login_user(request):
    form = LoginForm(request.POST or None)
    title = "Log In"
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        query = profile.objects.get(user = user)
        if(query.designation == 'Admin'):
            return redirect('/admin/dashboard')
        elif(query.designation == 'Project Manager'):
            return redirect('/pm/profile')
        else:
            return redirect('/employee/profile')
    return render(request, 'registration/login.html',{"form":form,"title":title})




def logout_user(request):
    logout(request)
    return login_user(request)
from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required #makes sure that user needs to be logged in before logged out
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user #make sure it´s a 1-to-1 relationship between profile and user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    
    else:

        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request, "basic_app/registration.html"
                            ,{'registered':registered,
                            'user_form':user_form,
                            'profile_form':profile_form})



def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username') #gets the username of dicitionary from submitted login html
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active")
        
        else:
            print("Someone tried to login and failed")
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request,'basic_app/login.html',{})
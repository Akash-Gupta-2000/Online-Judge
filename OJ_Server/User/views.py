from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.forms.models import model_to_dict
import warnings
warnings.filterwarnings("ignore")

def home(request):
    return render(request, "homepage.html")

# @csrf_exempt
def register(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            first_name = request.POST["firstname"]
            last_name = request.POST["lastname"]
            email = request.POST["email"]
            password1 = request.POST["password1"]
            password2 = request.POST["password1"]

            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('/users/register')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exist! Please try some other email.")
                return redirect('/users/register')
            
            if password1 != password2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('/users/register')
        
            newuser = User.objects.create_user(
                username = username, email = email, password = password1, first_name = first_name, 
                last_name = last_name, is_active = True)
            print(newuser)
            messages.success(request, 'User Registered Successfully. Please Login to Continue!!')

            return redirect('/users/login')

        return render(request, "register.html")

    except Exception as e:
        messages.error(request, f"Exception Occured while User Registration: {str(e)}")
        return redirect('/users')

def login(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)
            print('User Name: ', user)
            if user:
                auth_login(request, user)
                return redirect('/problems/getAllProblems')
            
            else:
                messages.success(request, "Invalid Credentials!!")
                return redirect('/users/login')
            
        return render(request, "login.html")

    except Exception as e:
        messages.error(request, f"Exception Occured while Login: {str(e)}")
        return redirect('/users')
    
def logout(request):
    try:
        if request.user.is_authenticated:
            auth_logout(request)
            messages.success(request, "Logged Out Successfully!!")
        else:
            messages.success(request, 'User Already Logged Out. Please Login Again to Continue!!')

        return redirect('/users')

    except Exception as e:
        messages.error(request, f"Exception Occured while Logging Out: {str(e)}")
        return redirect('/users')
    
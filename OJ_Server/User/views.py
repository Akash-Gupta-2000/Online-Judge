from django.shortcuts import render
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.forms.models import model_to_dict
import warnings
warnings.filterwarnings("ignore")

@csrf_exempt
def register(request):
    try:
        if request.method != "POST":
            return JsonResponse({'status': 'Only POST Method is Allowed'}, status = 400)

        jsonData = json.loads(request.body)
        mandatory_fields = ['username', 'email','password','firstname','lastname']
        for field in mandatory_fields:
            if field not in jsonData:
                return JsonResponse({'status': 'Mandatory Fields Not Present'}, status = 400)

        newuser = User.objects.create_user(
            username = jsonData["username"], email = jsonData["email"], 
            password = jsonData["password"], first_name = jsonData["firstname"], 
            last_name = jsonData["lastname"], is_active = True)

        return JsonResponse({'message': 'User Successfully Registered'}, status = 200)

    except Exception as e:
        return JsonResponse({'status': 'Exception Occured while User Registration', 'exception': str(e)}, status = 400)

def login(request):
    try:
        if request.method != "POST":
            return JsonResponse({'status': 'Only POST Method is Allowed'}, status = 400)

        jsonData = json.loads(request.body)
        if 'username' not in jsonData or 'password' not in jsonData:
            return JsonResponse({'message': 'Required fields Username/Password Missing'}, status = 400)

        user = authenticate(request, username = jsonData["username"], password = jsonData["password"])
        print('User Name: ', user)
        if user:
            auth_login(request, user)
            return JsonResponse({'message': 'Login Successful', 'object': model_to_dict(user)})
        
        else:
            return JsonResponse({'message': 'Login Failed'}, status = 400)

    except Exception as e:
        return JsonResponse({'status': 'Exception Occured while Login', 'exception': str(e)}, status = 400)
    
def logout(request):
    try:
        if request.method != "POST":
            return JsonResponse({'status': 'Only POST Method is Allowed'}, status =  400)

        if request.user.is_authenticated:
            auth_logout(request)
            return JsonResponse({'message': 'Logout Sucessful'}, status = 200)

        else:
            return JsonResponse({'message': 'User Already Logged Out. Please Login Again to Continue'}, status = 400)

    except Exception as e:
        return JsonResponse({'status': 'Exception Occured while Logging Out', 'exception': str(e)}, status = 400)
    
def getProfile(request):
    try:
        if request.method != "GET":
            return JsonResponse({'status': 'Only GET Method is Allowed'}, status = 400)

        if request.user.is_authenticated:
            print("User Profile Fetched Successfully")
            return JsonResponse((model_to_dict(request.user)), safe = False)

        else:
            print("Please Login with a verified User Profile")
            return JsonResponse({'message': 'Please Login with a verified User Profile'}, status = 400)

    except Exception as e:
        return JsonResponse({'status': 'Exception Occured while fetching User Profile', 'exception': str(e)}, status=400)


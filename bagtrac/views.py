from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
@csrf_exempt
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            messages.success(request , "You have been Logged IN")
            return redirect('home')
        else:
            messages.success(request , "There was an Error Loggin In , Try Again . . .")
            return redirect('home')
    else:
        return render(request , 'home.html' )
    

def to_sql(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request , "You Have Been Logged Out.... ")
    return redirect('home')


    
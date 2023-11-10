from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Data
from django.utils import timezone
from django.db import IntegrityError

@csrf_exempt
def home(request):
    last_cv = Data.objects.last()  
    last_cv_value = last_cv.cv if last_cv else "" 

    if request.method == 'POST':
        cv = request.POST.get('CV', '')
        bag_seal_id = request.POST.get('Bag/Seal_ID', '')
        cage_id = request.POST.get('Cage_ID', '')
        time1 = timezone.now()

        try:
            data_instance = Data(cv=cv, bag_seal_id=bag_seal_id, cage_id=cage_id, time1=time1)
            data_instance.save()
        except IntegrityError:
            messages.error(request , "Bag Already Added")
            print("IntegrityError: Bag Already Added")

        last_cv_value = cv

    return render(request, 'home.html', {'last_cv_value': last_cv_value})


def search(request):
    return render(request , 'search.html')
from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Data
from django.utils import timezone

@csrf_exempt
def home(request):
    last_cv = Data.objects.last()  
    last_cv_value = last_cv.cv if last_cv else "" 

    if request.method == 'POST':
        cv = request.POST['CV']
        bag_seal_id = request.POST['Bag/Seal_ID']
        cage_id = request.POST['Cage_ID']
        time1 = timezone.now()

     
        data_instance = Data(cv=cv, bag_seal_id=bag_seal_id, cage_id=cage_id, time1=time1)
        data_instance.save()

        last_cv_value = cv

    return render(request, 'home.html', {'last_cv_value': last_cv_value})


        


    



       

    



    
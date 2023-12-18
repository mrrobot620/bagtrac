from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Data
from django.utils import timezone
from django.db import IntegrityError
import pytz
import csv
from pytz import timezone as pytz_timezone


IST = pytz_timezone('Asia/Kolkata') 


@login_required
def home(request):
    if request.user.is_authenticated:
        last_cv = Data.objects.last()  
        last_cv_value = last_cv.cv if last_cv else "" 
        if request.method == 'POST':
            cv = request.POST.get('CV', '')
            bag_seal_id = request.POST.get('Bag/Seal_ID', '')
            cage_id = request.POST.get('Cage_ID', '')
            time1 = timezone.now()
            try:
                current_user = request.user
                user = User.objects.get(pk=current_user.id)
                data_instance = Data(cv=cv, bag_seal_id=bag_seal_id, cage_id=cage_id, time1=time1, user=user.username)
                data_instance.save()
            except IntegrityError as E:
                messages.error(request, {f'Error': {E}})
                print(f"IntegrityError: Bag Already Added" , {E})
            last_cv_value = cv
        return render(request, 'home.html', {'last_cv_value': last_cv_value})
    else:
        return render(request, 'login.html')

@login_required
def search(request):
    bag_id = request.GET.get('bag_id')
    search_results = Data.objects.filter(bag_seal_id=bag_id)
    
    if search_results:
        for result in search_results:
            # Convert time from UTC to IST
            result.time1 = result.time1.astimezone(IST)
            result.time1_str = result.time1.strftime("%b. %d, %Y, %I:%M %p")
    if not search_results and bag_id:
        return render(request, 'search.html', {'search_results': search_results, 'bag_id': bag_id, 'not_found': True})
    return render(request, 'search.html', {'search_results': search_results , 'bag_id':bag_id})

@login_required
def cage_search(request):
    cage_id = request.GET.get('cage_id')
    search_results = Data.objects.filter(cage_id=cage_id)
    if search_results:
        ist = pytz.timezone('Asia/Kolkata')
        for result in search_results:
            result.time1 = result.time1.astimezone(IST)
            result.time1_str = result.time1.strftime("%b. %d, %Y, %I:%M %p")
    if not search_results and cage_id:
        return render(request , 'cage_search.html' , {'search_results': search_results , "cage_id": cage_id , "not_found": True})
    return render(request , 'cage_search.html' , {"search_results": search_results , 'cage_id':cage_id})

@login_required
def multi_search(request):
    if request.method == "POST":
        bag_ids_input = request.POST.get('bag_ids')
        bag_ids = bag_ids_input.split()
        search_results = Data.objects.filter(bag_seal_id__in=bag_ids)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
        writer = csv.writer(response)
        writer.writerow(['Bag ID', 'CV', 'Time', 'Cage ID', 'Username'])
        for result in search_results:
            writer.writerow([result.bag_seal_id, result.cv, result.time1, result.cage_id, result.user])
        return response
    return render(request  , 'search.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            return render(request , 'login.html' , {'error': "Invalid Username or Password"})
    return render(request , 'login.html')

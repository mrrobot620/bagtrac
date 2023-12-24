from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from reportlab.lib.pagesizes import landscape
from .models import Data , Cage
from django.utils import timezone
from django.db import IntegrityError
import pytz
import csv
from pytz import timezone as pytz_timezone
import os
from io import BytesIO
import qrcode
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Cage, Data , Bags
import uuid
from reportlab.pdfgen import canvas
from django.core.files.storage import default_storage
from django.conf import settings
import os
from io import BytesIO
import qrcode
from PIL import ImageDraw
from PIL import ImageFont
from reportlab.pdfgen import canvas


IST = pytz_timezone('Asia/Kolkata') 
@login_required
def home(request):
    if request.user.is_authenticated:
        last_cv = Data.objects.last()  
        last_cv_value = last_cv.cv if last_cv else "" 
        if request.method == 'POST':
            cv = request.POST.get('CV', '')
            bag_seal_id = request.POST.get('Bag/Seal_ID', '')
            cage_id= request.POST.get('Cage_ID', '')
            try:
                cage_instance = Cage.objects.get(cage_name = cage_id)
            except ObjectDoesNotExist as E:
                messages.error(request , {f"Cage {cage_id} does not exist"})
                return render(request, 'home.html', {'last_cv_value': last_cv_value})
            time1 = timezone.now()
            try:
                current_user = request.user
                user = User.objects.get(pk=current_user.id)
                data_instance = Data(cv=cv, bag_seal_id=bag_seal_id, cage_id=cage_instance, time1=time1, user=user.username)
                data_instance.save()
            except IntegrityError as E:
                messages.error(request, f"Bag {bag_seal_id} already exist")
                print(f"IntegrityError: Bag Already Added" , {E})
            try:
                cage_instance.is_occupied = True
                cage_instance.save()
            except Exception as e:
                messages.error(request , e)
            try:
                assign_bag_to_cage(bag_seal_id)
            except Exception as e:
                print(e)   
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
    search_results = Data.objects.filter(cage_id_id__cage_name=cage_id)
    bags_count = Data.objects.filter(cage_id_id__cage_name=cage_id).aggregate(total_bags=Count('id'))
    total_bags_in_cage = bags_count['total_bags']
    if search_results:
        ist = pytz.timezone('Asia/Kolkata')
        for result in search_results:
            # print(result.__dict__)
            result.time1 = result.time1.astimezone(IST)
            result.time1_str = result.time1.strftime("%b. %d, %Y, %I:%M %p")
    if not search_results and cage_id:
        return render(request , 'cage_search.html' , {'search_results': search_results , "cage_id": cage_id , "not_found": True , })
    return render(request , 'cage_search.html' , {"search_results": search_results , 'cage_id':cage_id , 'total_bags_in_cage': total_bags_in_cage})

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
            ist_time = result.time1.astimezone(IST).strftime("%b. %d, %Y, %I:%M %p")
            writer.writerow([result.bag_seal_id, result.cv, ist_time, result.cage_id.cage_name, result.user])
        return response
    return render(request, 'search.html')


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

@login_required
def cage_generator(request):
    active_cages = None
    if request.method == "GET":
        try:
            active_cages = Cage.objects.filter(is_occupied=True)
            print(active_cages) 
        except Exception as e:
            print(e)
    return render(request, "cage_generator.html", {'active_cages': active_cages})


def generate_cage(request):
    if request.method == 'POST':
        try:
            new_cage_id = f"T{Cage.objects.count() + 1}"
            cage_uuid = uuid.uuid4()
            new_cage = Cage(cage_name=new_cage_id, uuid=cage_uuid)
            new_cage.save() 
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr.add_data(str(cage_uuid))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            pdf_buffer = BytesIO()
            width, height = 33, 55
            p = canvas.Canvas(pdf_buffer, pagesize=(width, height))
            p.setFont("Helvetica-Bold", 9)  
            p.drawString(7, height - 12, f"{new_cage_id}") 
            img_width, img_height = 20, 20 
            p.drawInlineImage(img, (width - img_width) / 2, (height - img_height) / 2, width=img_width, height=img_height)
            p.save()
            pdf_buffer.seek(0)
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{new_cage_id}.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f'Error occurred: {str(e)}')
    return HttpResponse('Invalid request method')


def assign_bag_to_cage(bag_id):
    bag = Bags.objects.get(bag_id=bag_id)
    bag_grid_code = bag.grid_code
    cage_to_assign = None
    cages = Cage.objects.filter(is_occupied=True)  # Assuming 'is_occupied' marks an occupied cage
    for cage in cages:
        assigned_bags = Bags.objects.filter(cage_id=cage.id)[:2]
        if len(assigned_bags) == 2:
            if assigned_bags[0].grid_code == assigned_bags[1].grid_code:
                cage_to_assign = cage
                break
    if cage_to_assign:
        bag.cage_id = cage_to_assign
        bag.save()
        return True
    else:
        return False
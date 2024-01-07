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
from .models import Data , Cage , Bags , ibbags , GridArea , BNRBag
from django.utils import timezone
from django.db import IntegrityError
import pytz
import csv
from pytz import timezone as pytz_timezone
import os
from io import BytesIO
from django.shortcuts import get_object_or_404
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
import re
from .auto_put_in import hms_login , hubSystem , auto_bag_put
from rest_framework import generics
from .serializers import BagsSerializer
from django.db.models import Q
from django.utils.timezone import localtime, make_aware



IST = pytz_timezone('Asia/Kolkata') 
@login_required
def home(request):
    if request.user.is_authenticated:
        last_cv = Data.objects.filter(user=request.user).last() 
        last_cv_value = last_cv.cv if last_cv else "" 
        if request.method == 'POST':
            cv = request.POST.get('CV', '')
            bag_seal_id = request.POST.get('Bag/Seal_ID', '')
            cage_id= request.POST.get('Cage_ID', '')
            try:
                cage_instance = Cage.objects.get(cage_name=cage_id)
            except ObjectDoesNotExist as E:
                messages.error(request, f"Cage {cage_id} does not exist")
                return render(request, 'home.html', {'last_cv_value': last_cv_value})
            time1 = timezone.now()
            try:
                cage_instance.is_occupied = True
                cage_instance.save()
            except Exception as e:
                messages.error(request, e)
            try:
                assigned = assign_bag_to_cage(bag_seal_id , cage_id)
                print("Assignement Succesfull")
                if not assigned:
                    messages.error(request, f"Bag '{bag_seal_id}' cannot be assigned to Cage: {cage_id}")
                else:
                    try:
                        current_user = request.user
                        user = User.objects.get(pk=current_user.id)
                        data_instance = Data(cv=cv, bag_seal_id=bag_seal_id, cage_id=cage_instance, time1=time1, user=user.username)
                        try:
                            bag_instance = get_object_or_404(Bags, bag_id=bag_seal_id)
                            bag_instance.recieved_at_cv = True
                            bag_instance.save()
                        except Exception as e:
                            print(e)
                            messages.error(request, f"Unable to update the Bag  {e}")
                        data_instance.save()
                    except IntegrityError as E:
                        messages.error(request, f"Bag {bag_seal_id} already exists")
                        print(f"IntegrityError: Bag Already Added" , {E})
            except Exception as e:
                print(f"Error in assigning bag: {e}")
                messages.error(request, f"Error in assigning bag: {e}")
            
            last_cv_value = cv
        return render(request, 'home.html', {'last_cv_value': last_cv_value} )
    else:
        return render(request, 'login.html')

@login_required
def search(request):
    bag_id = request.GET.get('bag_id')
    search_results = Data.objects.filter(bag_seal_id=bag_id)
    bag_grid = []
    bag_status = {}
    if search_results:
        for result in search_results:
            result.time1 = result.time1.astimezone(IST)
            result.time1_str = result.time1.strftime("%b. %d, %Y, %I:%M %p")
            bag_grid_data = Bags.objects.filter(bag_id=result.bag_seal_id)
            for bag in bag_grid_data:
                if bag is not None:
                    try:
                        bag.bag_label_generated = True
                        bag.save()
                        bag_status = {
                                'Bag Created': Bags.objects.filter(bag_id=result.bag_seal_id, bag_created=True).exists(),
                                'Label Pasted': Bags.objects.filter(bag_id=result.bag_seal_id, bag_label_generated=True).exists(),
                                'Received at CV': Bags.objects.filter(bag_id=result.bag_seal_id, recieved_at_cv=True).exists(),
                                'Grid Put In': Bags.objects.filter(bag_id=result.bag_seal_id, put_in_grid=True).exists(),
                                'Grid Put Out': Bags.objects.filter(bag_id=result.bag_seal_id, put_out_grid=True).exists(),}
                        print(bag_status)
                    except Exception as e:
                        print(e)
            bag_grid.extend(bag_grid_data)
    if not search_results and bag_id:
        return render(request, 'search.html', {'search_results': search_results, 'bag_id': bag_id, 'not_found': True})
    return render(request, 'search.html', {'search_results': search_results , 'bag_id':bag_id , "bag_grid":bag_grid , "bag_status":bag_status} )

@login_required
def new_search(request):
    query = request.GET.get('search_query')
    search_results = None
    bag_grid = None
    bag_status = None
    if query:
        search_results = Bags.objects.filter(
            Q(bag_id__icontains=query) | Q(seal_id__icontains=query)
        )
        if search_results:
            for result in search_results:
                result.time1 = localtime(result.time1).strftime("%b. %d, %Y, %I:%M %p")
                bag_status = {
                    'Bag Created': result.bag_created,
                    'Label Pasted': result.bag_label_generated,
                    'Received at CV': result.recieved_at_cv,
                    'Grid Put In': result.put_in_grid,
                    'Grid Put Out': result.put_out_grid,
                }
                bag_grid = result.grid_code
            return render(
                request,
                'new_search.html',
                {
                    'search_results': search_results,
                    'bag_id': query,
                    'bag_grid': bag_grid,
                    'bag_status': bag_status,
                },
            )
    if not search_results and query:
        return render(request,'new_search.html',{'search_results': search_results, 'bag_id': query, 'not_found': True})
    return render(request, 'new_search.html', {"search_results":search_results , 'bag_id':query , 'bag_grid':bag_grid , "bag_status":bag_status })
                
                

@login_required
def cage_search(request):
    cage_id = request.GET.get('cage_id')
    search_results = Data.objects.filter(cage_id_id__cage_name=cage_id)
    bags_count = Data.objects.filter(cage_id_id__cage_name=cage_id).aggregate(total_bags=Count('id'))
    total_bags_in_cage = bags_count['total_bags']
    bag_grid = [] 
    if search_results:
        ist = pytz.timezone('Asia/Kolkata')
        for result in search_results:
            # print(result.__dict__)
            result.time1 = result.time1.astimezone(IST)
            result.time1_str = result.time1.strftime("%b. %d, %Y, %I:%M %p")
            bag_grid_data = Bags.objects.filter(bag_id=result.bag_seal_id)
            bag_grid.extend(bag_grid_data)
    if not search_results and cage_id:
        return render(request, 'cage_search.html', {'search_results': search_results, "cage_id": cage_id, "not_found": True})
    return render(request, 'cage_search.html', {"search_results": search_results, 'cage_id': cage_id, 'total_bags_in_cage': total_bags_in_cage, "bag_grid": bag_grid})

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
            return redirect('ib_bagtrac')
        else:
            return render(request , 'login.html' , {'error': "Invalid Username or Password"})
    return render(request , 'login.html')

@login_required
def cage_generator(request):
    active_cages = None
    if request.method == "GET":
        try:
            active_cages = Cage.objects.filter(is_occupied=True)
            for cages in active_cages:
                cages.last_used = cages.last_used.astimezone(IST).strftime("%b. %d, %Y, %I:%M %p")
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
            qr.add_data(str(new_cage_id))
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
            print(e)
            return HttpResponse(f'Error occurred: {str(e)}')
    return HttpResponse('Invalid request method')

def assign_bag_to_cage(bag_id , cage_id):
    try:
        bag = Bags.objects.get(bag_id=bag_id)
        bag_grid_code = bag.grid_code
        print(bag_grid_code)
        assigned_cages = Cage.objects.filter(is_occupied=True, cage_name=cage_id)
        print(assigned_cages.__dict__)
        cage1 = Cage.objects.get(cage_name = cage_id )
        print(cage1)
        for cage in assigned_cages:
            assigned_bags = Bags.objects.filter(cage=cage)
            if not assigned_bags.exists() or any(assigned_bag.grid_code == bag_grid_code for assigned_bag in assigned_bags):
                bag.cage = cage
                bag.save()
                cage1.grid_code = bag_grid_code
                cage1.save()
                print("Cage Assigned")
                return True
            else:
                print("cage_not_assigned")
                return False
    except Exception as e:
        print(e)

@login_required
def ib_bagtrac(request):
    last_cage = ibbags.objects.filter(user=request.user).last()
    last_cage_1 = last_cage.cage_id if last_cage else ""
    if request.method == 'POST':
        bag_id = request.POST.get('Bag/Seal_ID', '')
        cage_id = request.POST.get('Cage_ID', '')
        time1 = timezone.now()
        current_user = request.user
        user = User.objects.get(pk=current_user.id)
        data_instance = ibbags(bag_id=bag_id, cage_id=cage_id, time1=time1, user=user)
        identifiers = ["ZO", "B5", "B1", "B2", "B3", "B4", "B6"]
        tags = ["Success"] * len(identifiers)
        bag_in_db = BNRBag.objects.filter(bag=bag_id)
        print(bag_in_db)
        if bag_in_db.exists():
            for item in bag_in_db:
                item.recieved  = True
                item.save()
            messages.error(request, "Bag Not Received")
        
        cage_updated = False
        for index, identifier in enumerate(identifiers):
            if identifier.lower() in bag_id.lower():
                try:
                    data_instance.save()
                except IntegrityError as e:
                    messages.success(request, f"Bag Already Scanned {bag_id}")
                    break
                else:
                    messages.success(request, f"{identifier}", extra_tags=tags[index])
                    last_cage_1 = cage_id
                    cage_updated = True
                    break
        else:
            data_instance.save()
            if not cage_updated:
                last_cage_1 = cage_id

    return render(request, 'ib.html', {"last_cage": last_cage_1})


@login_required
def ib_multi_search(request):
    if request.method == "POST":
        bag_ids_input = request.POST.get('bag_ids')
        bag_ids = bag_ids_input.split()
        search_results = ibbags.objects.filter(bag_id__in=bag_ids)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
        writer = csv.writer(response)
        writer.writerow(['Bag ID', 'Time', 'Cage ID', 'Username'])
        for result in search_results:
            ist_time = result.time1.astimezone(IST).strftime("%b. %d, %Y, %I:%M %p")
            writer.writerow([result.bag_id, ist_time, result.cage_id, result.user])
        return response
    return render(request, 'search.html')

    
@login_required
def ib_search(request):
    bag_id = request.GET.get('bag_id')
    search_results = ibbags.objects.filter(bag_id=bag_id)
    if search_results:
        for result in search_results:
            # Convert time from UTC to IST
            result.time1 = result.time1.astimezone(IST)
            result.time1_str = result.time1.strftime("%b. %d, %Y, %I:%M %p")
        return render(request, 'ib_search.html', {'search_results': search_results})
    if not search_results and bag_id:
        return render(request, 'ib_search.html', {'search_results': search_results, 'bag_id': bag_id, 'not_found': True})
    return render(request , 'ib_search.html')   

@login_required
def download_all_data(request):
    # Fetch all data from your model
    all_data = ibbags.objects.all()
    
    if all_data:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Bag ID', 'Cage ID', 'Time' , "User"])  # Adjust headers as needed
        for result in all_data:
            result.time1 = result.time1.astimezone(IST)
            result.time1_str = result.time1.strftime("%b. %d, %Y, %I:%M %p")
            writer.writerow([result.bag_id, result.cage_id, result.time1 , result.user])  # Adjust fields based on your model
        return response
    messages.error(request , F'Error No Data Available')

@login_required
def assign_cage_to_grid(request, grid_code, cage_id):
    try:
        grid_area = GridArea.objects.get(grid_code=grid_code, label=cage_id)
        cage_instance = Cage.objects.get(cage_name=cage_id)
        cage_instance.grid_area = grid_area
        grid_area.is_assigned = True
        grid_area.save()
        cage_instance.save()
        messages.success(request , f"Cage {cage_id} assigned to grid {grid_code}{cage_id}")
    except GridArea.DoesNotExist:
        messages.success(request , f"Grid area {grid_code}{cage_id} does not exist")
    except Cage.DoesNotExist:
        messages.error(request , f"Cage {cage_id} does not exist")
    except Exception as e:
        messages.error(request , f"Error assigning cage to grid: {e}")


def put_in(request):
    if request.method == 'POST':
        cage_id = request.POST.get('cage')
        grid_area_id = request.POST.get('grid_area')
        try:
            cage = Cage.objects.get(cage_name=cage_id)
            grid_area = GridArea.objects.get(grid_code=grid_area_id)
            bags  = Bags.objects.filter(cage_id__cage_name=cage_id)
            grid_area.grid_code1  = re.sub(r'\D' , "" , grid_area.grid_code)
            print(grid_area.grid_code)
            if cage.grid_code == grid_area.grid_code1:
                cage.grid_area = grid_area
                grid_area.is_assigned = True
                grid_area.cage_id = cage
                hms_login()
                hubSystem()
                for bag in bags:
                    print(bag)
                    if bag is not None:
                        bag.put_in_grid = True
                        auto_bag_put(bag.bag_id , "36b93e66-2cdb-4859-8ed9-e2796bd522dd")
                        bag.save()
                    else:
                        messages.error(request , f"Empty Cage")
                cage.save()
                grid_area.save()
                messages.success(request, f"Cage {cage_id} assigned to Grid Area {grid_area_id}" , extra_tags="Success")
            else:
                messages.error(request, "Cage ID and Grid Area ID do not match!")
        except Cage.DoesNotExist:
            messages.error(request, f"Cage {cage_id} does not exist")
        except GridArea.DoesNotExist:
            messages.error(request, f"Grid Area {grid_area_id} does not exist")
    return render(request, 'put_in.html')

@login_required
def put_out(request):
    if request.method == "POST":
        grid_area = request.POST.get('grid_area')
        try:
            grid_area_instance = GridArea.objects.get(grid_code=grid_area)
            assigned_cage = grid_area_instance.cage
            if assigned_cage:
                grid_area_instance.is_assigned = False
                grid_area_instance.save()
                bags = Bags.objects.filter(cage=assigned_cage)
                for bag in bags:
                    bag.put_out_grid = True
                    bag.cage = None
                    bag.save()
                messages.success(request, "Cage successfully removed from the grid area"  , extra_tags="Success")
                datas  = Data.objects.filter(cage_id_id=assigned_cage)
                for data in datas:
                    data.cage_id= None
                    print("here")
                    data.save()
                cage = Cage.objects.get(cage_name=assigned_cage)
                cage.grid_code = "NA"
                cage.grid_area = None
                cage.is_occupied = False
                cage.save()
            else:
                messages.error(request, f"No cage assigned to grid area {grid_area}")
        except GridArea.DoesNotExist:
            messages.error(request, f"Grid area {grid_area} does not exist")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return render(request, 'put_out.html')

@login_required
def add_bnr_bags(request):
    if request.method == "POST":
        if 'addbnr' in request.POST:
            bnr_bags = request.POST.get('addbnr')
            bnrs = bnr_bags.split()
            print(bnrs)
            for bnr in bnrs:
                BNRBag.objects.create(bag=bnr)
        else:
            print("'addbnr' key not found in POST data")
    return render(request, 'bnr.html')


@login_required
def download_bnr(request):
    if request.method == 'POST':
        bag_ids = request.POST.get('download_bnr', '').split()  
        bnr_data = BNRBag.objects.filter(bag__in=bag_ids)  
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bnr_status.csv"'
        writer = csv.writer(response)
        writer.writerow(['Bag', 'Status'])
        for bag in bnr_data:
            status = 'Received' if bag.recieved else 'Not Received'
            writer.writerow([bag.bag, status])
        return response
    return HttpResponse("Invalid Request")


class BagsCreateView(generics.CreateAPIView):
    queryset = Bags.objects.all()
    serializer_class = BagsSerializer

    def create(self, request, *args, **kwargs):
        # Add 'label_generated' to request data with default value True if not provided
        if 'bag_label_generated' not in request.data:
            request.data['bag_label_generated'] = True
        
        return super().create(request, *args, **kwargs)
#Line added
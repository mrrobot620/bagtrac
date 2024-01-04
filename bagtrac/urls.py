from django.urls import path
from . import views

urlpatterns = [
    path("login" , views.login_view , name="login"),
    path("search" , views.search , name="search"),
    path("home" , views.home , name='home'),
    path('logout' , views.logout_view , name="logout"),
    path('multi_search' , views.multi_search , name="multi_search"),
    path('cage_search' , views.cage_search , name='cage_search'),
    path('cage_generator' , views.cage_generator , name="cage_generator"),
    path('generate_cage', views.generate_cage, name='generate_cage'),
    path('ib' , views.ib_bagtrac , name="ib_bagtrac" ),
    path('ib_search' , views.ib_search , name="ib_search"),
    path('ib_mult_search' , views.ib_multi_search , name="ib_multi_search"),
    path('download_all_data' , views.download_all_data , name="download_all_data"),
    path("put_in" , views.put_in , name="put_in"),
    path('put_out' , views.put_out , name="put_out" ),
    path('add_bnr' , views.add_bnr_bags , name="add_bnr"),
    path('download_bnr' , views.download_bnr , name="download_bnr")
]

# this line added second time
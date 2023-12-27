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
    path('ib' , views.ib_bagtrac , name="ib_bagtrac" )
]
from django.urls import path
from . import views

urlpatterns = [
    path("login" , views.login_view , name="login"),
    path("search" , views.search , name="search"),
    path("home" , views.home , name='home'),
    path('logout' , views.logout_view , name="logout"),
]
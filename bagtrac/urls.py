from django.urls import path
from . import views

urlpatterns = [
    path("" , views.home , name="home"),
    # path("/login" , views.login_user , name="login"),
    path("logout/" , views.logout_user , name="logout"),
    path("to_sql/" , views.to_sql , name='to_sql')

]
from django.contrib import admin 
from .models import Cvs , Data , Cage , Bags , ibbags , GridArea                    


# Register your models here.

admin.site.register(Cvs)
admin.site.register(Data)
admin.site.register(Cage)
admin.site.register(Bags)
admin.site.register(ibbags)
admin.site.register(GridArea)
from django.contrib import admin 
from .models import Cvs , Data , Cage , Bags , ibbags , GridArea , BNRBag , PTC          


# Register your models here.

admin.site.register(Cvs)
admin.site.register(Data)
admin.site.register(Cage)
admin.site.register(Bags)
admin.site.register(ibbags)
admin.site.register(GridArea)
admin.site.register(BNRBag)
admin.site.register(PTC)
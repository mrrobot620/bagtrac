from django.db import models


class Cvs(models.Model):
    cv = models.CharField(max_length=10)
    def __str__(self):
        return(self.cv)
    
class Data(models.Model):
    time1 = models.DateTimeField(auto_now_add=True)
    cv = models.CharField(max_length=20)
    bag_seal_id = models.CharField(max_length=20 , unique=True)
    cage_id = models.CharField(max_length=20)

    def __str__(self):
        return self.bag_seal_id
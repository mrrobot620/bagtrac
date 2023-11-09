from django.db import models


class Cvs(models.Model):
    cv = models.CharField(max_length=10)
    def __str__(self):
        return(self.cv)
    
class Data(models.Model):
    date_time = models.DateTimeField()
    cv = models.CharField(max_length=20)
    bag = models.CharField(max_length=20)
    cage = models.CharField(max_length=20)

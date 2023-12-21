from django.db import models
from django.contrib.auth.models import User
import uuid

class Cvs(models.Model):
    cv = models.CharField(max_length=10)
    def __str__(self):
        return(self.cv)
    
class Cage(models.Model):
    cage_name = models.CharField(max_length=10, unique=True)  # T1, T2, ...
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_occupied = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cage_id

class Data(models.Model):
    time1 = models.DateTimeField(auto_now_add=True)
    cv = models.CharField(max_length=20)
    bag_seal_id = models.CharField(max_length=255 , unique=True)
    cage_id = models.ForeignKey(Cage , on_delete=models.CASCADE)
    user = models.CharField(max_length=255)

    def __str__(self):
        return self.bag_seal_id
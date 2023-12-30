from django.db import models
from django.contrib.auth.models import User
import uuid

class Cvs(models.Model):
    cv = models.CharField(max_length=10)
    def __str__(self):
        return(self.cv)
    
class GridArea(models.Model):
    grid_code = models.CharField(max_length=10)
    label = models.CharField(max_length=10)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_assigned = models.BooleanField(default=False)
    # Other fields or metadata related to the grid area
    
    def __str__(self):
        return f"Grid {self.grid_code}"

class Cage(models.Model):
    cage_name = models.CharField(max_length=10, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_occupied = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)
    grid_code = models.CharField(max_length=10, default="NA")
    grid_area = models.OneToOneField(GridArea, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.cage_name

class Data(models.Model):
    time1 = models.DateTimeField(auto_now_add=True)
    cv = models.CharField(max_length=20)
    bag_seal_id = models.CharField(max_length=255 , unique=True)
    cage_id = models.ForeignKey(Cage , on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    def __str__(self):
        return self.bag_seal_id
    
class Bags(models.Model):
    bag_id = models.CharField(max_length=255 , unique=True)
    grid_code = models.CharField(max_length=10)
    cage = models.ForeignKey(Cage , on_delete=models.CASCADE , null=True , blank=True) 
    bag_created =  models.BooleanField(default=True)
    bag_label_generated = models.BooleanField(default=False)
    recieved_at_cv = models.BooleanField(default=False)
    put_in_grid = models.BooleanField(default=False)
    put_out_grid = models.BooleanField(default=False)
    def __str__(self):
        return self.bag_id
    
class ibbags(models.Model):
    time1 = models.DateTimeField(auto_now_add=True)
    bag_id = models.CharField(max_length=255)
    cage_id = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    def __str__(self):
        return self.bag_id
    

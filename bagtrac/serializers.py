from rest_framework import serializers
from .models import Bags

class BagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bags
        fields = ['bag_id', 'seal_id', 'grid_code' , 'bag_label_generated']

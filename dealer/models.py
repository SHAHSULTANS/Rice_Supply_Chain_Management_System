from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser
# Create your models here.



# class Location(models.Model):
#     """For tracking geographical locations of all parties"""
#     district = models.CharField(max_length=50)
#     upazila = models.CharField(max_length=50)
#     union = models.CharField(max_length=50, blank=True)
#     address = models.TextField()

class DealerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    storage_capacity = models.PositiveIntegerField()
    
    
    
     
# class MillProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     # mill_name = models.CharField(max_length=100)
#     # license_number = models.CharField(max_length=50)
    



class PaddyStock(models.Model):
    dealer = models.ForeignKey(DealerProfile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # like ton or mon or kg.
    moisture_content = models.DecimalField(max_digits=4, decimal_places=1)  # percentage
    stored_since = models.DateTimeField(auto_now_add=True)
    # current_location = models.ForeignKey(Location, on_delete=models.PROTECT)
    is_available = models.BooleanField(default=True)
    price_per_mon= models.DecimalField(max_digits=10, decimal_places=2) #kg/ton/mon
    quality_notes = models.TextField(blank=True)
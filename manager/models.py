from django.db import models
from accounts.models import CustomUser
from dealer.models import PaddyStock
# Create your models here.

class ManagerProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'manager'})
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()
    mill_name = models.CharField(max_length=100)
    mill_location = models.TextField()
    profile_image = models.ImageField(upload_to="manager_profile/",blank=True,null=True)
    experience_year = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.mill_name})"
    
    
class RicePost(models.Model):
    manager = models.ForeignKey(CustomUser,on_delete=models.CASCADE, limit_choices_to={'role':'manager'})
    rice_name = models.CharField(max_length=200, blank=True, null=True)
    quality = models.CharField(max_length=100)
    quantity_kg = models.FloatField()
    price_per_kg = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    is_sold = models.BooleanField(default=False)
    rice_image = models.ImageField(upload_to="rice_image/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

        
        
        
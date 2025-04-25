from django.db import models
from accounts.models import CustomUser
# Create your models here.
class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role':'customer'})
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    address =models.TextField()
    image = models.ImageField(upload_to="customer_profile/",blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
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
    dealer = models.ForeignKey('DealerProfile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Name or type of the paddy (e.g., BRRI Dhan 28)")
    image = models.ImageField(upload_to='paddy_images/', blank=True, null=True, help_text="Upload a photo of the paddy.")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Quantity in kg, ton, or mon.")
    moisture_content = models.DecimalField(max_digits=4, decimal_places=1, help_text="Moisture content (%)")
    stored_since = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    price_per_mon = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per mon (or other unit)")
    quality_notes = models.TextField(blank=True, help_text="Any notes about the quality.")

    class Meta:
        ordering = ['-stored_since']
        # verbose_name = _("Paddy Stock")
        # verbose_name_plural = _("Paddy Stocks")

    def __str__(self):
        return f"{self.name} - {self.quantity} units at {self.price_per_mon} per mon"
    

    
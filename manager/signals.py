from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Purchase_paddy, PaddyStockOfManager

@receiver(post_save, sender=Purchase_paddy)
def update_paddy_stock_of_manager(sender, instance, created, **kwargs):
    if instance.status == "Successful":
        manager = instance.manager
        paddy = instance.paddy
        
        stock, created = PaddyStockOfManager.objects.get_or_create(
            manager=manager,
            paddy_name = paddy.name,
            moisture_content = paddy.moisture_content,
            # rice_type = paddy.rice_type,
            defaults={
                'total_quantity' : 0,
                'total_price' : 0,
                'average_price_per_kg' : 0,
            }
        )
        
        stock.total_quantity += instance.quantity_purchased
        stock.total_price += instance.total_price
        
        if stock.total_quantity > 0:
            stock.average_price_per_kg = round(Decimal(stock.total_price)/Decimal(stock.total_quantity),2)
        
        stock.save()
        
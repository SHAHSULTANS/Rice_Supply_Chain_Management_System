from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Purchase_paddy, PaddyStockOfManager,PurchaseRice, RiceStock


@receiver(post_save, sender=Purchase_paddy)
def update_paddy_stock_of_manager(sender, instance, created, **kwargs):
    if instance.status == "Successful":
        manager = instance.manager
        paddy = instance.paddy
        
        stock, created = PaddyStockOfManager.objects.get_or_create(
            manager=manager,
            paddy_name = paddy.name,
            moisture_content = paddy.moisture_content,
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
        
        


@receiver(post_save, sender=PurchaseRice)
def add_purchased_rice_to_stock(sender, instance, created, **kwargs):
    if instance.status == 'Successful':
        manager = instance.manager
        rice_post = instance.rice

        rice_name = rice_post.rice_name
        quality = rice_post.quality
        quantity = instance.quantity_purchased
        total_price = instance.total_price

        average_price = float(total_price) / float(quantity)

        stock, created = RiceStock.objects.get_or_create(
            manager=manager,
            rice_name=rice_name,
            quality=quality,
            defaults={
                'stock_quantity': quantity,
                'total_price': total_price,
                'average_price_per_kg': average_price,
            }
        )

        if not created:
            previous_qty = stock.stock_quantity
            previous_total_price = stock.total_price

            new_total_qty = previous_qty + quantity
            new_total_price = previous_total_price + total_price
            new_avg_price = new_total_price / new_total_qty

            stock.stock_quantity = new_total_qty
            stock.total_price = new_total_price
            stock.average_price_per_kg = round(new_avg_price, 2)
            stock.save()
        
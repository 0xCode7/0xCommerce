from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime


# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.CharField(max_length=100)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=50, null=True, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_zipcode = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping Address - {self.user.username}'


def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        shipping_address = ShippingAddress(user=instance)
        shipping_address.save()


post_save.connect(create_shipping_address, sender=User)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    shipping_address = models.TextField(max_length=15000)  # Box containing all the shipping address details
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'order - {str(self.id)}'


# Auto Add Shipping Date
@receiver(pre_save, sender=Order)
def set_shipped_date(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)

        if instance.shipped and not obj.shipped:
            instance.date_shipped = now


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'

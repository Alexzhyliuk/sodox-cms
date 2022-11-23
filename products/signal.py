from django.db.models.signals import post_save

from products.models import Product, ProductCharacteristic


def add_characteristic_to_product(sender, instance, created, *args, **kwargs):
    characteristic = instance
    if created:
        pass


post_save.connect(add_characteristic_to_product, sender=ProductCharacteristic)
   
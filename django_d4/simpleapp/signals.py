from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def product_created(instance, **kwargs):
    print('Создан товар', instance)

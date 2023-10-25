from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


# Товар для витрины
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0,
                                      'Quantity should be >= 0')])
    # Поле которое будет ссылаться на модель категории
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                 related_name='products')
    # все продукты в категории будут доступны через поле products
    price = models.FloatField(
        validators=[MinValueValidator(0.0,
                                      'Price should be >= 0')])

    def __str__(self):
        return f'{self.category} : {self.name} : {self.description[:20]}'

    # Добавим absolute_urls
    def get_absolute_url(self):
        return f'/products/{self.id}'
        # return reverse('product_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


# Категория, к которой будет привязываться товар
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name.title()}'


class Subscriptions(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE,
                                 related_name='subscriptions')

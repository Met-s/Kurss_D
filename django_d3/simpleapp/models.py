from django.db import models
from django.core.validators import MinValueValidator


# Товар для витрины
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()



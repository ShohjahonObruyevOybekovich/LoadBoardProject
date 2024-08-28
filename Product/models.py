from django.contrib.auth import get_user_model
from django.db import models

from django.db import models

from account.models import CustomUser

class Product(models.Model):
    title = models.CharField(max_length=255)
    places = models.IntegerField()
    view = models.CharField(max_length=255)
    cube = models.DecimalField(max_digits=10, decimal_places=2)
    kg = models.DecimalField(max_digits=10, decimal_places=2)
    cube_kg = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=255)
    debt = models.DecimalField(max_digits=10, decimal_places=2)
    where_from = models.CharField(max_length=255)
    date = models.DateTimeField()
    transport = models.CharField(max_length=255)
    current_place = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')

from datetime import timezone, datetime

from django.contrib.auth import get_user_model
from django.db import models

from django.db import models

from account.models import CustomUser

class Product(models.Model):
    title = models.CharField(max_length=255)
    places = models.CharField(max_length=255,null=True, blank=True)
    view = models.CharField(max_length=255,null=True, blank=True)
    cube = models.CharField(max_length=255,null=True, blank=True )
    kg = models.CharField(max_length=255,null=True,blank=True)
    cube_kg = models.CharField( max_length=255,null=True,blank=True)
    price = models.CharField( max_length=255,null=True,blank=True)
    payment = models.CharField(max_length=255, null=True,blank=True)
    debt = models.CharField(max_length=255, null=True,blank=True)
    where_from = models.CharField(max_length=255, null=True,blank=True)
    date = models.DateTimeField(default=datetime.now())
    transport = models.CharField(max_length=255, null=True,blank=True)
    current_place = models.CharField(max_length=255, null=True,blank=True)
    STATUS_CHOICES = [
        ('На складе Китая', 'На складе Китая'),
        ('На складе Узбекистана', 'На складе Узбекистана'),
        ('в пути', 'в пути'),
        ('Ожидающий', 'Ожидающий'),
        ('Завершен', 'Завершен'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')

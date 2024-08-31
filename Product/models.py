from datetime import timezone, datetime

from django.contrib.auth import get_user_model
from django.db import models

from django.db import models

from account.models import CustomUser

class Product(models.Model):
    title = models.CharField(max_length=255)
    places = models.IntegerField(null=True, blank=True)
    view = models.CharField(max_length=255,null=True, blank=True)
    cube = models.DecimalField(max_digits=10,decimal_places=8,null=True, blank=True )
    kg = models.DecimalField(max_digits=10,null=True,blank=True,decimal_places=8)
    cube_kg = models.DecimalField(max_digits=10, null=True,blank=True,decimal_places=8)
    price = models.DecimalField(max_digits=10, null=True,blank=True,decimal_places=8)
    payment = models.CharField(max_length=255, null=True,blank=True)
    debt = models.DecimalField(max_digits=10, null=True,blank=True,decimal_places=8)
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')

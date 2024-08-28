from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product

@admin.register(Product)
class QuestionPartsAdmin(admin.ModelAdmin):
    list_display = ('title','kg')
    search_fields = ('title',)
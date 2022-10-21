from distutils.command.upload import upload
from turtle import mode
from unicodedata import name
from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200,default='description')
    price=models.IntegerField(default='10')
    description=models.TextField(default='description')
    image=models.ImageField(blank=True,default='images',upload_to='images')
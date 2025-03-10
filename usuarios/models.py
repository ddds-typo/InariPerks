from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    altura=models.IntegerField(blank=True, null=True)
    edad=models.IntegerField(blank=True, null=True)
    peso=models.IntegerField(blank=True, null=True)
    genero=models.CharField(max_length=5,blank=True, null=True)

from django.db import models

# Create your models here.

class user(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64,null=False,unique=True)
    password = models.CharField(max_length=64,null=False)
    email = models.CharField(max_length=64,null=True,unique=True)
    phone = models.CharField(max_length=64,null=False,unique=True)

from django.db import models

# Create your models here.

class user(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64,null=False)
    password = models.CharField(max_length=64,null=False)
    email = models.CharField(max_length=64,null=False)
    sfID = models.CharField(max_length=64,null=False)
    phone = models.CharField(max_length=64,null=False)

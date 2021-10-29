from django.db import models

# Create your models here.

class user(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    email = models.EmailField(max_length=50,null=False,blank=False,unique=True)
    password = models.CharField(max_length=50,null=False,blank=False)

class advisor(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    photo = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=False, blank=False)

class callsBooked(models.Model):
    dateTime = models.CharField(max_length=50,null=False,blank=False) 
    adv = models.ForeignKey(advisor, on_delete=models.CASCADE)
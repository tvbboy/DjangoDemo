from django.db import models

# Create your models here.
class testForTeaching(models.Model):
    logintimes = models.IntegerField(default=0)
    username = models.CharField(max_length=20)
    qq = models.CharField(max_length=20,null=True)
    email= models.EmailField()
    password = models.CharField(max_length=256)
    gender= models.CharField(max_length=10)
    birthdate= models.DateField()
    nativePlace= models.CharField(max_length=20)
    regdate= models.DateTimeField()
    is_Active = models.BooleanField(default=True,null=True)
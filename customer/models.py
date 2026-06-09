from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    published_date = models.DateField()

    def _str_(self):
        return self.title
    
class Register(AbstractUser):
    name=models.CharField(max_length=100,default="")
    age=models.IntegerField(default=0)
    
    
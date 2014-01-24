from django.db import models

# Create your models here.

class droid_model(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=50)
    md5 = models.CharField(max_length=16)
    email = models.EmailField()
    is_checked = models.BooleanField()

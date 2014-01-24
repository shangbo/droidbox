from django.db import models

# Create your models here.

class droidModel(models.Model):
    name = models.CharField(max_length=50)
    md5 = models.CharField(max_length=32)
    email = models.EmailField()
    is_checked = models.BooleanField()

    def __repr__(self):
        return self.name

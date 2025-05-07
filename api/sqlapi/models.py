from django.db import models

# Create your models here.
class post(models.Model):
    
    username = models.CharField(max_length=255)
    data = models.TextField()

class alert(models.Model):
    
    username = models.CharField(max_length=255)
    data = models.TextField()
    time = models.DateTimeField(auto_now=True)

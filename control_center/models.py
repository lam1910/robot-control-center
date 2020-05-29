from django.db import models

# Create your models here.
class Order(models.Model):
    start = models.CharField(max_length=1)
    finish = models.CharField(max_length=1)
    status = models.CharField(max_length=12, default = 'incomplete')
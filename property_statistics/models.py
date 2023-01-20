from django.db import models


class Property(models.Model):
    price = models.IntegerField()
    dept_code = models.IntegerField()
    city = models.CharField(max_length=100)
    zip_code = models.IntegerField()

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Band(models.Model):
    name = models.fields.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=155, unique=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=155, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutriscore = models.IntegerField()
    nutrigrade = models.CharField(max_length=1, default='')
    url = models.CharField(max_length=255, default="")
    image_url = models.CharField(max_length=255, default="")
    salt = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    calories = models.FloatField(default=0)
    fat = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Alternative(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

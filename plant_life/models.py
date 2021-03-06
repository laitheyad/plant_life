import random
import string

from django.db import models
from django.conf import settings
from django.db import models


class User(models.Model):
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=13)
    email = models.EmailField(blank=True, null=True)
    status_selection = [
        ('Customer', 'Customer'),
        ('Expert', 'Expert'),
        ('Seller', 'Seller')
    ]
    status = models.CharField(choices=status_selection, default='Customer', max_length=20)

    def __str__(self):
        return u'{} || status: {}'.format(self.username.username, self.status)


class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=500)
    avatar = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)

    def __str__(self):
        return '{} || {}'.format(str(self.shop.name), self.title)


class Item(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=10.0)
    avatar = models.ImageField(null=True, blank=True)
    avatar_2 = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{} || {} ||{}'.format(str(self.shop.name), str(self.category.title), self.title)


class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    bill_id = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return '{} || {} ||{}'.format(str(self.user), str(self.item.title), self.total_price)


class Slider(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

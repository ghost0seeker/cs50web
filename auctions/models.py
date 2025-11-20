from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionItem(models.Model):
    title = models.CharField(max_length=64) 
    desc = models.TextField()
    image = models.URLField(blank=True, null=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=32)
    state = models.CharField(max_length=32)

class Bid(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bit_time = models.DateField(auto_now_add=True)

class Comment(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    comment = models.TextField()

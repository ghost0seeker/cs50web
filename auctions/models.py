from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class AuctionItem(models.Model):
    title = models.CharField(max_length=64) 
    desc = models.TextField()
    image = models.URLField(blank=True, null=True)
    initial_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=32)

    def _get_highest_bid_obj(self):
        return self.bid_set.order_by('-price').first()
    
    def get_highest_bid(self):
        highest_bid = self._get_highest_bid_obj()
        if highest_bid:
            return highest_bid.price
        return self.initial_bid_price

class Bid(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateField(auto_now_add=True)

class Comment(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class State(models.Model):
    type = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.type}"

class AuctionItem(models.Model):
    title = models.CharField(max_length=64) 
    desc = models.TextField()
    image = models.URLField(blank=True, null=True)
    initial_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_DEFAULT, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def get_highest_bid_obj(self):
        return self.bid_set.order_by('-price').first()
    
    def get_highest_bid(self):
        highest_bid = self.get_highest_bid_obj()
        if highest_bid:
            return highest_bid.price
        return self.initial_bid_price

    def get_highest_bid_user(self):
        highest_bid = self.get_highest_bid_obj()
        if highest_bid:
            return highest_bid.user
        else:
            return None
    
    def change_state(self):
        if self.state.id == 1:
            self.state = State.objects.get(pk=2)
            return True
        else:
            return False
    
    def __str__(self):
        return f"{self.title} {self.get_highest_bid()} {self.state}"

class Bid(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} placed {self.price} bid on {self.item.title}"

class Comment(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

class Winner(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} won {self.item.title} at {self.bid.price}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(AuctionItem)

    def __str__(self):
        return f"Watchlist of {self.user.username}"
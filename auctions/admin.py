from django.contrib import admin
from .models import AuctionItem,Bid,Comment,Category,User,State,Winner,Watchlist
# Register your models here.
admin.site.register(AuctionItem)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(State)
admin.site.register(Winner)
admin.site.register(Watchlist)
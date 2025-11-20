from django.contrib import admin
from .models import AuctionItem,Bid,Comment,Category
# Register your models here.
admin.site.register(AuctionItem)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
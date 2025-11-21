from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

from .models import User, AuctionItem, Bid, Comment, Category
from .forms import NewItemForm, NewBidForm


def create_listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            category = Category.objects.get(pk=form.cleaned_data["category"])
            item = AuctionItem(
                    title=form.cleaned_data["title"],
                    desc=form.cleaned_data["description"],
                    image=form.cleaned_data["image"],
                    initial_bid_price=form.cleaned_data["initial_bid_price"],
                    category=category,
                )
            item.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "message" : "Invalid Data", #TODO: use form object errors instead
                "categories": categories,
            })

    return render(request, "auctions/create_listing.html", {
        "categories": categories
        })


def index(request):
    auction_items = AuctionItem.objects.all()
    for auction in auction_items:
        print(auction.get_highest_bid())
    return render(request, "auctions/index.html", {
        "auction_items" : auction_items,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def item_view(request, item_id):
    auction_item = AuctionItem.objects.get(pk=item_id)
    comments = auction_item.comment_set.all()
    return render(request, "auctions/item.html", {
        "item": auction_item,
        "comments": comments,
    })

def bid_item(request, item_id):
    # pass
    if request.method == "POST":
        auction_item = AuctionItem.objects.get(pk=item_id)
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data["bid_amount"]
            current_bid = auction_item.get_highest_bid()

            if bid_amount > current_bid:
                new_bid = Bid(
                            item=auction_item,
                            user=request.user,
                            price = bid_amount,
                        )
                new_bid.save()
                messages.success(request, "Bid Placed!")
                return redirect('item', item_id)
            else:
                messages.error(request, 'Bid amount lower than current bid')
                return redirect('item', item_id)
        else:
            messages.error(request, 'Error while bidding, please try again')
            return redirect('item', item_id)
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

from .models import User, AuctionItem, Bid, Comment, Category, Winner, State, Watchlist
from .forms import NewItemForm, NewBidForm, NewComment, NewWatchlist

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@login_required
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
    auction_items = AuctionItem.objects.filter(state=State.objects.get(pk=1))
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

@login_required
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
    current_bid = auction_item.bid_set.all().last()
    is_in_watchlist = Watchlist.objects.filter(
        user=request.user,
        items = auction_item,
    )

    context =  {
            "item": auction_item,
            "comments": comments,
            "current_bid": current_bid,
            "is_in_watchlist": is_in_watchlist,
        }
    
    if auction_item.state.type == "New Listing":
        if request.user.id == auction_item.user.id:
            context["user_is_same"] = True
            return render(request, "auctions/item.html", context)
        else:
            return render(request, "auctions/item.html", context)
    else:
        context["winner"] = Winner.objects.filter(item=auction_item).first()
        return render(request, "auctions/item.html", context)

@login_required
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

@login_required
def comment(request,item_id):
    if request.method == "POST":
        form = NewComment(request.POST)
        if form.is_valid():
            new_comment = Comment(
                    item=AuctionItem.objects.get(pk=item_id),
                    text = form.cleaned_data["comment_text"],
                    user = request.user,
            )
            new_comment.save()
            return redirect('item', item_id)
        else:
            messages.error(request, "Form Data Invalid")
            return redirect('item', item_id)

@login_required
def close_auction(request, item_id):
    if request.method == "POST":
        auction_item = AuctionItem.objects.get(pk=item_id)
        highest_bid = auction_item.get_highest_bid_obj()
        winner_user = auction_item.get_highest_bid_user()
        if winner_user:
            winner = Winner(
                    item=auction_item,
                    user=winner_user,
                    bid=highest_bid,
            )
            auction_item.change_state()
            auction_item.save()
            winner.save()
            return redirect('item', item_id)

@login_required
def watchlist(request):
    watchlist, created = request.user.watchlist_set.get_or_create()
    if request.method == "POST":
        form = NewWatchlist(request.POST)
        if form.is_valid():
            watchlist.items.add(AuctionItem.objects.get(pk=form.cleaned_data["item_id"]))
            return redirect('item', form.cleaned_data["item_id"])
        else:
            messages.error(request, "Failed to add item to watchlist")
            return redirect('item', form.cleaned_data["item_id"])
            
    context = {}
    if watchlist:
        context["watchlist"] = watchlist
    else:
        context["watchlist"] = None
    
    return render(request, "auctions/watchlist.html", context)

def categories(request):
    categories = Category.objects.exclude(pk=2)
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def category_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category_view.html", {
        "category": category,
    })
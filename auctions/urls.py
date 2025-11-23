from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("item/<int:item_id>", views.item_view, name="item"),
    path("item/<int:item_id>/bid", views.bid_item, name="bid_item"),
    path("item/<int:item_id>/comment", views.comment, name="comment"),
    path("item/<int:item_id>/close_auction", views.close_auction, name="close_auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_view, name="category_view"),
]

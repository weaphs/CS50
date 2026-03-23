from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_auction", views.create_auction , name="create_auction"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("auctions/<str:id>/", views.auction, name="auction"),
    path("make_bet/<str:id>", views.make_bet, name="make_bet"),
    path("make_comment/<str:id>", views.make_comment, name="make_comment"),
    path("watchlist/<int:id>/", views.toggle_watchlist, name="watchlist")
]

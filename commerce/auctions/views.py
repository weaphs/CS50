from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User, Auction
from .forms import BetForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    auctions = Auction.objects.all()
    context = {"auctions":auctions}
    return render(request, "auctions/index.html", context)


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


def auction(request, id):
    if request.method == "GET":
        auction = get_object_or_404(Auction, pk=id)
        context = {"auction":auction,
                   "bet_form":BetForm(),
                   "comment_form":CommentForm()}
        return render(request, "auctions/auction.html", context)

def create_auction(request):
    return render(request, "auctions/create_auction.html")

@login_required
def make_bet(request, id):
    auction = get_object_or_404(Auction, pk=id)
    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            new_amount = form.cleaned_data['current_bet']
            current_amount = auction.current_bet.current_bet if auction.current_bet else auction.init_bet
            if new_amount <= current_amount:
                messages.error(request, f"Bet must be bigger than ({current_amount} )")
            bet = form.save(commit=False)
            bet.user = request.user
            bet.auction = auction
            bet.save()
            auction.current_bet = bet
            auction.save()
            messages.success(request, f"Your bet {bet.current_bet} approved")
            return redirect('auction', id=auction.id)
    else:
        form = BetForm()
        context = {
            "auction": auction,
            "form": form,
        }
        return render(request, "auctions/auction.html", context)

@login_required
def toggle_watchlist(request, id):
    auction = get_object_or_404(Auction, pk=id)
    user = request.user

    if auction in user.watchlist.all():
        user.watchlist.remove(auction)
    else:
        user.watchlist.add(auction)

    return redirect('auction', id=id)

@login_required
def make_comment(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        user = request.user
        auction = get_object_or_404(Auction, pk=id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.auction = auction
            comment.save()
            messages.success(request, f"Comment received")
            return redirect('auction', id=auction.id)
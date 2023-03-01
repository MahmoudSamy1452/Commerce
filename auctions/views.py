from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

def index(request):
    max_bid = {}
    for listing in Listing.objects.filter(closed=False):
        max_bid[listing.id]=(Bid.objects.filter(Listing = listing).aggregate(models.Max("value")))['value__max']
    superusers = User.objects.filter(is_superuser=True)
    superuser_ids = [user.id for user in superusers]
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False),
        "highest_bid":max_bid,
        "superusers": superuser_ids
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

@login_required
def add(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new = Listing.objects.create(title=form.cleaned_data["title"], description=form.cleaned_data['description'], base_price=form.cleaned_data['starting_bid'], photo=form.cleaned_data['photo'], category=form.cleaned_data['category'], creator=request.user, closed=False)
            return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/add.html", {
        "form": ListingForm()
    })

def bid_view(request, listing_id):
    message = ''
    max_bid = Bid.objects.filter(Listing = Listing.objects.get(pk=listing_id)).aggregate(models.Max("value"))
    if request.method == "POST":
        if 'submit-form1' in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                if (max_bid['value__max'] == None or (max_bid['value__max'] != None and max_bid["value__max"] < form.cleaned_data['value'])) and Listing.objects.get(pk=listing_id).base_price <= form.cleaned_data['value']:
                    Bid.objects.create(Listing=Listing.objects.get(pk=listing_id), value=form.cleaned_data["value"], User=request.user)
                    message = 'bid added successfully'
                else:
                    message = 'Value must be greater than the last bid'
        elif 'submit-form2' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                Comment.objects.create(Listing=Listing.objects.get(pk=listing_id),content=form.cleaned_data['content'], User =request.user)
    else: 
        if 'add' in request.GET:
            Listing.objects.get(pk=listing_id).watching.add(request.user)
        elif 'remove' in request.GET:
            Listing.objects.get(pk=listing_id).watching.remove(request.user)
        elif 'close' in request.GET:
            Listing.objects.filter(pk=listing_id).update(closed=True)
    return render(request, 'auctions/view.html',{
        "BidForm": BidForm(),
        "listing": Listing.objects.get(pk=listing_id),
        "bids": Bid.objects.filter(Listing=Listing.objects.get(pk=listing_id)),
        "message": message,
        "comments": Comment.objects.filter(Listing=Listing.objects.get(pk=listing_id)),
        "CommentForm": CommentForm(),
        "status": request.user.is_authenticated and Listing.objects.get(pk=listing_id) in Listing.objects.filter(watching = request.user),
        "highest_bid":max_bid['value__max'],
        "winner": Bid.objects.filter(Listing=Listing.objects.get(pk=listing_id)).last
    })

@login_required
def watch(request):
    return render(request, 'auctions/index.html', {
        "listings": Listing.objects.filter(watching = request.user),
        "watch": True
    })

def category(request):
    category=''
    if "filtering" in request.GET:
        category=request.GET.get('category')
    return render(request, 'auctions/category.html', {
        "listings": Listing.objects.filter(category = category, closed = False),
        "form": CategoriesForm(request.GET)
    })
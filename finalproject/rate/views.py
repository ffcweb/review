from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Store, Follow, StoreProfile, UserProfile, FavoriteStore, StoreFollowers
from .models import Review, LikeReview, CommentOnReview
from django.urls import reverse
from .forms import ReviewForm
from .models import Store, Review

def index(request):
    # return render(request, "rate/index.html")
    reviews = Review.objects.all().order_by("-timestamp")

     # use pagination built-in function
    paginator = Paginator(reviews, 10)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        paginated_reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        paginated_reviews = paginator.page(paginator.num_pages)
    
    return render(request, 'rate/index.html', {'reviews': paginated_reviews})



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
            return render(request, "rate/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "rate/login.html")


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
            return render(request, "rate/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "rate/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "rate/register.html")

# =============================
# For the store's profile to post new review  
@login_required
def create_review(request):
    if request.method == "POST":
        content = request.POST["content"]
        spending = request.POST["spending"]
        store_id = request.POST["store_id"]
        user = request.user
        print(request)
        Review.objects.create(content=content, user = user, spending= spending, store_id=store_id)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'rate/create_review.html')
#   return render(request, 'rate/create_review.html', {'form': form, 'store': store})

    # ==============================================

# @login_required
def all_reviews(request):
    # First, get all the reviews in timestamp order.
    reviews = Review.objects.all().order_by('-timestamp')

    # Use pagination built-in function.
    paginator = Paginator(reviews, 10)  # Show 10 reviews per page.
    page = request.GET.get('page')
    try:
        paginated_reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        paginated_reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        paginated_reviews = paginator.page(paginator.num_pages)

    return render(request, 'rate/all_reviews.html', { 'reviews': paginated_reviews})



def store_list(request):
    stores = Store.objects.all().order_by('-Joined_date')
    return render(request, 'rate/store_list.html', {'stores': stores})

# def store_profile(request, store_id):
#     store = get_object_or_404(Store, pk=store_id)
#     reviews = Review.objects.filter(store_name=store)
#     return render(request, 'rate/store_profile.html', {'store': store, 'reviews': reviews})

def store_profile(request, store_id):
    reviews = Review.objects.all().order_by('-timestamp')
    store = get_object_or_404(Store, id =store_id)

  # Use pagination built-in function.
    paginator = Paginator(reviews, 10)  # Show 10 reviews per page.
    page = request.GET.get('page')
    try:
        paginated_reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        paginated_reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        paginated_reviews = paginator.page(paginator.num_pages)

    return render(request, 'rate/store_profile.html', {'store': store, "reviews":paginated_reviews })

    # ==============================================
def popular_stores(request):
    # Placeholder logic for popular_stores view
    return render(request, 'rate/popular_stores.html')  # Replace with your actual template
    # ==============================================
def star_stores(request):
    # Placeholder logic for star_stores view
    return render(request, 'rate/star_stores.html')  # Replace with your actual template
    # ==============================================

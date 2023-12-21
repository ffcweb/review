from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db import IntegrityError
from django.db.models import Count
from django.db.models import Q  # Import Q object for OR conditions
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from .forms import ReviewForm
from django.views.decorators.http import require_POST
from .models import User, Store, Review, UserProfile, FavoriteStore, Category
from .models import SearchBox, LikeReview, CommentOnReview, StoreFollowers


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

# def index(request):
#     reviews = Review.objects.all().order_by("-timestamp")
#     context = {'reviews': reviews}
#     return render(request, 'rate/index.html', context)


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
def category_list(request):
    categories = Category.objects.all()
    print(categories)
    context = {'categories': categories}
    return render(request, 'rate/category_list.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    print(category)
    context = {'category': category}
    return render(request, 'rate/category_detail.html', context)


# For the store's profile to post new review
@login_required
def create_review(request):
    if request.method == "POST":
        print(request.POST)  # Add this line to print the POST data

        content = request.POST["content"]
        spending = request.POST["spending"]
        store_id = request.POST["store_id"]
        rating = request.POST["star_rating"]
       
        user = request.user

        print(request)
        Review.objects.create(content=content, user=user, spending=spending, store_id=store_id, star_rating=rating)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'rate/create_review.html')

    # ==============================================

def all_reviews(request, ):
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
    # return render(request, 'rate/store_list.html', {'stores': stores})

    # Use pagination built-in function.
    paginator = Paginator(stores, 10)  # Show 10 reviews per page.
    page = request.GET.get('page')
    try:
        paginated_stores = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        paginated_stores = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        paginated_stores = paginator.page(paginator.num_pages)

    return render(request, 'rate/store_list.html', { 'stores': paginated_stores})


def store_profile(request, store_id):
    store = get_object_or_404(Store, id = store_id)
    print("=================", store)
    reviews = Review.objects.filter(store = store).order_by('-timestamp')

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

    return render(request, 'rate/store_profile.html', { "store": store, 'reviews': paginated_reviews})

# ================================================
@login_required
def user_profile(request, user_id):
  
    # First, get all the reviews in timestamp order.
    user = get_object_or_404(User, id = user_id)
    user_reviews = Review.objects.filter(user=user).order_by('-timestamp')

# Use pagination built-in function.
    paginator = Paginator(user_reviews, 10)  # Show 10 reviews per page.
    page = request.GET.get('page')
    try:
        paginated_user_reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        paginated_user_reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        paginated_user_reviews = paginator.page(paginator.num_pages)

    context = {
        'user': user,
        'user_reviews': user_reviews,
        'paginated_user_reviews':paginated_user_reviews
    }
    print(context)
    # return render(request, 'rate/user_profile.html', context)
    return render(request, 'rate/user_profile.html', context)

    # ==============================================
def popular_stores(request):
    return render(request, 'rate/popular_stores.html')  


    # ==============================================
def star_stores(request):
    return render(request, 'rate/star_stores.html')  
    # ==============================================


def search_store(request):
    query = request.GET.get('q', '')
    results = SearchBox.objects.filter(store_name__icontains=query)
    
    context = {'results': results, 'query': query}
    return render(request, 'rate/search_results.html', context)


@login_required
def toggle_follow_store(request, store_id):
    user_to_follow_store = get_object_or_404(Store, id=store_id)
    user = request.user
    
    StoreFollowers = request.store.StoreFollowers

    if request.method == 'POST':
        if user_to_follow_store in storeFollowers.follower.all():
            storeFollowers.follower.remove(user_to_follow)
        else:
            storeFollowers.follower.add(user_to_follow)
            storeFollowers.save()
            storeFollowers.followers.count()
            storeFollowers.save()
    return JsonResponse({'followers_count': StoreFollowers.followers_count})

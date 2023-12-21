from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from statistics import mean
from django.db import IntegrityError
from django.db.models import Count
from django.db.models import Q  # Import Q object for OR conditions
from django.contrib.auth.decorators import login_required

from django.views.generic.base import View
from django.http import JsonResponse
from django.urls import reverse
# from .forms import ReviewForm
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

    for review in reviews:
        likes = LikeReview.objects.filter(review=review)
        review.like_count = len(likes)


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

    for store in stores:
        reviews = Review.objects.filter(store=store)
        if len(reviews)>0:
            average_rating= mean([x.star_rating for x in reviews])
        else:
            average_rating=0

        store.average_rating=round(average_rating,1)
        store.review_count= len(reviews)


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
    reviews = Review.objects.filter(store = store).order_by('-timestamp')

    if len(reviews)>0:
        average_rating= mean([x.star_rating for x in reviews])
    else:
        average_rating=0

    store.average_rating=round(average_rating,1)
    store.review_count= len(reviews)

    for review in reviews:
        likes = LikeReview.objects.filter(review=review)
        review.like_count = len(likes)

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

def user_profile(request, user_id):
    # First, get all the reviews in timestamp order.
    user = get_object_or_404(User, id = user_id)
    user_reviews = Review.objects.filter(user=user).order_by('-timestamp')
   
    # give the number of the like_count for the user profile page
    reviews = Review.objects.filter(user=user).order_by('-timestamp')
    for review in reviews:
        likes = LikeReview.objects.filter(review=review)
        review.like_count = len(likes)

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
    return render(request, 'rate/user_profile.html', context)

    # return render(request, 'rate/store_profile.html', { "user": user, 'reviews': paginated_reviews})
    # return render(request, 'rate/user_profile.html', { 'reviews': reviews })

    # ==============================================
class UserProfileView(View):
    template_name = 'user_profile.html'

    def get(self, request, *args, **kwargs):
        user = UserProfile.objects.get(username='username') 
        return render(request, self.template_name, {'user': user})

    def post(self, request, *args, **kwargs):
        user = UserProfile.objects.get(username='username') 
        new_image_url = request.POST.get('new_image_url')

        if new_image_url:
            user.image_url = new_image_url
            user.save()

            return JsonResponse({'status': 'success', 'message': 'Profile image updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid image URL'})



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
    store_to_follow = get_object_or_404(Store, id=store_id)
    user = request.user

    follower_store_pair = StoreFollowers.objects.filter(follower=follower, store=store)
    print(follower_store_pair)

    # if request.method == 'POST':
    #     if storeToFollow in storeFollowers.follower.all():
    #         storeFollowers.follower.remove(storeToFollow)
    #     else:
    #         storeFollowers.follower.add(storeToFollow)
    #         storeFollowers.save()
    #         storeFollowers.follower.count()
    #         storeFollowers.save()
    # return JsonResponse({'follower': StoreFollowers.follower})


# Review_id :is from the urls.py 
@require_POST
@login_required
def toggle_like(request,review_id):
    user= request.user
    user_reivew_pair=LikeReview.objects.filter(
        user=user, review_id=review_id
    )

    if user_reivew_pair.exists():
        # the pair above exists then delete the data.
        user_reivew_pair.delete()
    else:
        # else add a new recored in LikeReview table.
        LikeReview.objects.create(user=user,review_id=review_id)

    # filter the new added recored 
    likes = LikeReview.objects.filter(review_id=review_id)

    #  count the number of likes fot this review ID, including the one just added.
    new_like_count = len(likes)

    # return these data to the front-end
    data ={
        'review_id':review_id,
        'new_like_count':new_like_count,
    }
    return JsonResponse(data)
       


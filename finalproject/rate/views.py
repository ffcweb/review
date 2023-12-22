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
from .models import User, Store, Review, FavoriteStore, Category
from .models import SearchBox, LikeReview, CommentOnReview, StoreFollowers
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UpdateProfileForm




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
        if content == '':
            content = "My reviews is empty"


        spending = request.POST["spending"]
        store_id = request.POST["store_id"]
        rating = request.POST["star_rating"]
        image_url = request.POST['image_url']
        if image_url == '':
            image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBp_jLbdg8HuM0rkuzxlGxfyB8cswrmAlFVUHdXckCgfEk4HH-Jj-HnTU4Mnu8T0VYMxc&usqp=CAU"
       
        user = request.user

        print(request)
        Review.objects.create(content=content, user=user, spending=spending, image_url=image_url,store_id=store_id, star_rating=rating)
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



def store_list(request,sort_by):
    stores = Store.objects.all()#.order_by('-Joined_date')
    # return render(request, 'rate/store_list.html', {'stores': stores})

    for store in stores:
        reviews = Review.objects.filter(store=store)
        if len(reviews)>0:
            average_rating= mean([x.star_rating for x in reviews])
        else:
            average_rating=0

        store.average_rating=round(average_rating,1)
        store.review_count= len(reviews)


    # for the reverse order
    if sort_by == 'rating':
        stores= sorted(stores, key = lambda x: x.average_rating, reverse = True)
    elif sort_by == 'reviews':
        stores = sorted(stores, key = lambda x: x.review_count, reverse = True)
    else:
        stores = sorted(stores, key = lambda x: x.Joined_date, reverse = True)


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

    context={
        'stores':paginated_stores,
        'sort_by': sort_by,
    }

    return render(request, 'rate/store_list.html', context)

def store_profile(request, store_id):
    store = get_object_or_404(Store, id = store_id)
    reviews = Review.objects.filter(store = store).order_by('-timestamp')

    if request.user.is_anonymous:
        # user is not logged in 
        follow_button_text="Follow"
    else:
        store_follower_pair = StoreFollowers.objects.filter(
            follower=request.user)
        if store_follower_pair.exists():
            follow_button_text="Unfollow"
        else:
            follow_button_text="Follow"

    if len(reviews)>0:
        average_rating= mean([x.star_rating for x in reviews])
    else:
        average_rating=0

    store.average_rating=round(average_rating,1)
    store.review_count= len(reviews)

    all_followers =  StoreFollowers.objects.filter(store=store)
    follower_count=len(all_followers)

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

    context = {
        "store":store,
        "follow_button_text":follow_button_text,
        "reviews":paginated_reviews,
        'follower_count':follower_count,
    }

    return render(request, 'rate/store_profile.html', context)

    # return render(request, 'rate/store_profile.html', { "store": store, 'reviews': paginated_reviews})

# ================================================

# def user_profile(request, user_id):
#     # First, get all the reviews in timestamp order.
#     user = get_object_or_404(User, id = user_id)
#     user_reviews = Review.objects.filter(user=user).order_by('-timestamp')

   
#     # give the number of the like_count for the user profile page
#     reviews = Review.objects.filter(user=user).order_by('-timestamp')
#     for review in reviews:
#         likes = LikeReview.objects.filter(review=review)
#         review.like_count = len(likes)

# # Use pagination built-in function.
#     paginator = Paginator(user_reviews, 10)  # Show 10 reviews per page.
#     page = request.GET.get('page')
#     try:
#         paginated_user_reviews = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver the first page.
#         paginated_user_reviews = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g., 9999), deliver the last page of results.
#         paginated_user_reviews = paginator.page(paginator.num_pages)

#     context = {
#         'user': user,
#         'user_reviews': user_reviews,
#         'paginated_user_reviews':paginated_user_reviews
#     }
#     print(context)
#     return render(request, 'rate/user_profile.html', context)

    # return render(request, 'rate/store_profile.html', { "user": user, 'reviews': paginated_reviews})
    # return render(request, 'rate/user_profile.html', { 'reviews': reviews })


def user_profile(request, user_id):
    user = get_object_or_404(User, id = user_id)
    user_reviews = Review.objects.filter(user=user).order_by('-timestamp')

   
    # give the number of the like_count for the user profile page
    reviews = Review.objects.filter(user=user).order_by('-timestamp')
    for review in reviews:
        likes = LikeReview.objects.filter(review=review)
        review.like_count = len(likes)


    paginator = Paginator(user_reviews, 10)
    page = request.GET.get('page')
    try:
        paginated_user_reviews = paginator.page(page)
    except PageNotAnInteger:
        paginated_user_reviews = paginator.page(1)
    except EmptyPage:
        paginated_user_reviews = paginator.page(paginator.num_pages)

    # Add the form for updating the profile image
    update_profile_form = UpdateProfileForm()

    context = {
        'user': user,
        'user_reviews': user_reviews,
        'paginated_user_reviews': paginated_user_reviews,
        'update_profile_form': update_profile_form,
    }

    return render(request, 'rate/user_profile.html', context)
    # ==============================================

@require_POST
@login_required
def update_user_image(request):
    user= request.user
    new_image_url= request.POST['newImageUrl']

    # update the database
    user.image_url = new_image_url
    user.save()

    data= {
        'status':'success',
        'new_image_url':new_image_url,
        'message':f'Updated user image url to {new_image_url}'
    }
    return JsonResponse(data)


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

@require_POST
@login_required
def toggle_follow_store(request, store_id):
    
    user = request.user

    follower_store_pair = StoreFollowers.objects.filter(follower=user, store_id=store_id)
    if follower_store_pair.exists():
        follower_store_pair.delete()
        new_status="Unfollowed"
    else:
        StoreFollowers.objects.create(follower=user,store_id=store_id)
        new_status = "Followed"

    followers= StoreFollowers.objects.filter(store_id=store_id)
    new_follower_count = len(followers)

    store = get_object_or_404(Store, id= store_id)

    data={
        'store_id': store_id,
        'store_name':store.name,
        'new_status':new_status,
        'new_followers_count':new_follower_count,
    }
    return JsonResponse(data)


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
       


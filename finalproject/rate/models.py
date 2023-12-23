from django.contrib.auth.models import AbstractUser
from django.db import models


# User Class: 
# Purpose: Represents a user in the system.
# Inheritance: Inherits from AbstractUser.
# Fields:Inherits fields from AbstractUser (provided by Django).
class User(AbstractUser):
    introduction = models.CharField(max_length=200,default='My introduction')
    image_url = models.URLField(default='https://cdn4.iconfinder.com/data/icons/music-ui-solid-24px/24/user_account_profile-2-512.png')

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    stores = models.ManyToManyField('Store', related_name='categories')
    image_url = models.URLField(max_length=200, null=True, blank=True, default="")

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=200)
    Joined_date = models.DateTimeField("date Joined")
    address = models.CharField(max_length=400)
    introduction = models.CharField(max_length=400)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='store_categories')
    image_url = models.URLField(max_length=200, null=True, blank=True, default="")
    link_url = models.URLField(max_length=200, null=True, blank=True)
    star_rating = models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], default=1)    
    
    def __str__(self):
        return self.name

#  has a follwer count and follower id , store id, 
class StoreFollowers(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    # followers_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.follower.username} follows {self.store.name}"


class FavoriteStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
  
    def __str__(self):
        return f"{self.user.username}'s favorite store: {self.store.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    spending = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    link_url = models.URLField(max_length=200, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    star_rating = models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], default=1)
    def __str__(self):
        return f"{self.user.username}'s Review for {self.store.name}"


class LikeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # count=
    
    def __str__(self):
        return f"{self.user.username} likes {self.review}"


class CommentOnReview(models.Model):
    content = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    review_content = models.TextField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)


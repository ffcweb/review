from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Store(models.Model):
    name = models.CharField(max_length=200)
    Joined_date = models.DateTimeField("date Joined")
    address = models.CharField(max_length=400)
    introduction = models.CharField(max_length=400)
    
    # closing
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    category = models.CharField(max_length=35)
    image_url = models.URLField(max_length=200, null=True, blank=True, default="")
    link_url = models.URLField(max_length=200, null=True, blank=True)
    
    star_rating = models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], default=1)    

    # avarage_rate = models.DecimalField(max_digits=10, decimal_places=2)
    def average_star_rating(self):
        # Calculate the average star rating based on associated reviews
        average_rating = self.review_set.aggregate(Avg('star_rating'))['star_rating__avg']
        
        # If there are no reviews, return a default value (e.g., 0)
        return average_rating if average_rating is not None else 0

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    spending = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    link_url = models.URLField(max_length=200, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)

    star_rating = models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], default=1)

    def __str__(self):
        return f"{self.user.username}'s Review for {self.store.name}"

class LikeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} likes {self.review}"

    def increment_count(self):
        self.count += 1
        self.save()

class CommentOnReview(models.Model):
    content = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    review_content = models.TextField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    introduction = models.CharField(max_length=400)
    joined_date = models.DateTimeField("Joined Date", auto_now_add=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    image_url = models.URLField(max_length=200, null=True, blank=True)
    link_url = models.URLField(max_length=200, null=True, blank=True)

    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

     # favorite stores
    favorite_stores = models.ManyToManyField(Store, through='FavoriteStore', related_name='favorited_by')

    def __str__(self):
        return self.user.username

class StoreProfile(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, symmetrical=False, related_name='store_followers')

     # for followers count
    followers_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.store_name.name

class StoreFollowers(models.Model):
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.follower.username} follows {self.store.store_name.name}"

    def increment_count(self):
        self.count += 1
        self.save()


class FavoriteStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    # A user_profile field that references UserProfile with a foreign key. 
    # This ensures that the FavoriteStore model has the required foreign key to UserProfile.
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite store: {self.store.name}"
from django.contrib import admin
from .models import Category, Store, Review, LikeReview, CommentOnReview
from .models import StoreFollowers,FavoriteStore

# Register your models here.
admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Review)
admin.site.register(LikeReview)
admin.site.register(CommentOnReview)
# admin.site.register(Follow)
# admin.site.register(UserProfile)
# admin.site.register(StoreProfile)
admin.site.register(StoreFollowers)
admin.site.register(FavoriteStore)

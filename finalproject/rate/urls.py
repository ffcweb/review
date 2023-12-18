
from django.urls import path
from .views import all_reviews
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:store_id>/', views.store_profile, name='store_profile'),

    path('users/<int:user_id>/', views.user_profile, name='user_profile'),

    path('all_reviews/', views.all_reviews, name='all_reviews'),
    # path('all_reviews/<int:pk>/', all_reviews, name='all_reviews'),
    # path('review/', views.review, name='review'),

    path('create_review/', views.create_review, name='create_review'),
    path('create_review/<int:user_id>/', views.create_review, name='create_review'),
     # path('submit_review/<int:store_id>/', views.submit_review, name='submit_review'),
    # path('submit_review/', views.submit_review, name='submit_review'),

    path('popular_stores/', views.popular_stores, name='popular_stores'),
    path('star_stores/', views.star_stores, name='star_stores'),

]

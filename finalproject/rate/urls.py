
from django.urls import path
from .views import all_reviews, category_list,category_detail
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    

    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:store_id>/', views.store_profile, name='store_profile'),
    path('all_reviews/', views.all_reviews, name='all_reviews'),
    path('create_review/', views.create_review, name='create_review'),

    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),


    path('popular_stores/', views.popular_stores, name='popular_stores'),
    path('star_stores/', views.star_stores, name='star_stores'),

]

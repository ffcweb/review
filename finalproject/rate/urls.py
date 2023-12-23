
from django.urls import path
from .views import all_reviews, category_list,category_detail
from .views import search_store, toggle_follow_store,toggle_like
from .views import user_profile,update_user_image, delete_review
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),

    path('search_store/', search_store, name='search_store'),
    
    path('stores/', views.store_list, kwargs={'sort_by':'date'},name='store_list'),
    path('stores_sorted/<str:sort_by>/', views.store_list, name='store_sorted'),


    path('stores/<int:store_id>/', views.store_profile, name='store_profile'),
    path('all_reviews/', views.all_reviews, name='all_reviews'),
    path('create_review/', views.create_review, name='create_review'),

    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),


    path('update_user_image/', update_user_image, name='update_user_image'),

    
    path('toggle_follow/<int:store_id>/', toggle_follow_store, name='toggle_follow_store'),
    path('toggle_like/<int:review_id>/', toggle_like, name='toggle_like'),

    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),


]

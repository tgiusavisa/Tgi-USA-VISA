from django.urls import path
from .views import BlogListView, BlogDetailView, create_blog_post

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', create_blog_post, name='create_blog_post'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]
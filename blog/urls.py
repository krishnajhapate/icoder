from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    # API to post a comment
    path('postComment',views.postComment, name="postComment"),
    path('commentdelete',views.commentdelete, name="commentdelete"),
    path('', views.blogHome,name="blogHome" ),
    path('<str:slug>',views.blogPost, name="blogPost"),
]

from django.contrib import admin
from django.urls import path
from . import views

app_name='main'

urlpatterns = [
    path('', views.homeView.as_view(), name='home'),
    path('post/create/', views.CreatePost.as_view(), name='create_post'),
    path('review/', views.reviewView.as_view(), name='review_posts'),
    path('post_status', views.PostStatus.as_view(), name='post_status'),
    path('blog', views.BlogView.as_view(), name='blog'),
    path('rules', views.TemplateView.as_view(template_name='rules.html'), name='rules'),
    path('upvote/<int:id>', views.upvote, name='upvote'),
    path('prediction/<str:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('comment', views.Comment.as_view(), name='comment'),
]
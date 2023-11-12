from django.urls import path

from app import views

urlpatterns = [
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('',views.index,name='index'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search_posts, name='search'),
    path('about/', views.about, name='about'),
    path('accounts/register/', views.register_user, name='register'),
    path('bookmark_post/<slug:slug>', views.bookmark_post, name='bookmark_post'),
    path('like_post/<slug:slug>', views.like_post, name='like_post'),
    path('all_bookmark_post', views.all_bookmark_post, name='all_bookmark_post'),
    path('all_posts', views.all_posts, name='all_posts'),
]

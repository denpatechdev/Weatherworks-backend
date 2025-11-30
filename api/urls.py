from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('comments/<str:area>/post/', views.create_comment, name='create_comment'),
    path('comments/<str:area>/', views.get_comments, name='get_comments'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('login/', views.login_user, name='login_user')
]

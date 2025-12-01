from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/current/', views.get_weather, name='get_weather'),
    path('weather/forecast/', views.get_forecast, name='get_forecast'),
    path('weather/location/', views.get_location, name='get_location'),
    path('comments/<str:area>/post/', views.create_comment, name='create_comment'),
    path('comments/<str:area>/', views.get_comments, name='get_comments'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
]
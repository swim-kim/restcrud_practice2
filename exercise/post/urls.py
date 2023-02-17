from django.urls import path
from .views import *
from . import views

app_name="post"
urlpatterns = [
    path('profile', views.profile_list_create),
    path('profile/<int:profile_id>',views.profile_rud),
    path('post',views.post_list_create),
    path('post/<int:post_id>', views.post_rud),
]
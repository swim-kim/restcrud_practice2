from django.urls import path
from .views import *
from . import views

app_name="post"
urlpatterns = [
    path('profile/all', views.profile_all),
]
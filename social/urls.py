from django.urls import path

from .views import list_posts

urlpatterns = [
    path('home/', list_posts),
]

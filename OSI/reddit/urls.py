from django.urls import path
from . import views

urlpatterns = [
    path('reddit/', views.reddit, name='reddit'),
]
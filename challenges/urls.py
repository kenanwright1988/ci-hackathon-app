from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_challenges, name='view_challenges'),
    # Add more URL patterns here
]
from django.urls import path, include
from .views import HelloWorldView

urlpatterns = [
    path('hello', HelloWorldView.as_view(), name='hello_world'), 
]
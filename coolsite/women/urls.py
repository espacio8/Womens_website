from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  #http://coolsite.ru/
    path('cats/', views.categories),  #http://coolsite.ru/cats/
]
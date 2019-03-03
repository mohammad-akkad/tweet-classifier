from django.contrib import admin
from django.urls import path
from myapp.views import hello,classifiy
from myapp.add import add



urlpatterns = [
    path('hello/', hello, name = 'hello'),
    path('classifiy/', classifiy, name = 'classifiy'),
    path('add/', add, name = 'add'),
]
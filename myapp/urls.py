from django.contrib import admin
from django.urls import path
from myapp.views import hello,classifiy



urlpatterns = [
    path('hello/', hello, name = 'hello'),
    path('classifiy/', classifiy, name = 'classifiy'),
]
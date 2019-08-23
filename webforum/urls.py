from django.urls import path
from webforum import views

urlpatterns=[
    path('', views.home, name='home')
]
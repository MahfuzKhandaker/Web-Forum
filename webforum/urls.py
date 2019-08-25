from django.urls import path
from webforum import views

urlpatterns=[
    path('', views.home, name='home'),
    path('forums/<int:pk>/', views.forum_topics, name='forum_topics'),
]
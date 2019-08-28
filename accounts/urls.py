from django.urls import path
from accounts import views as accounts_view

urlpatterns=[
    path('signup/', accounts_view.signup, name='signup'),
]
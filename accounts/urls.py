from django.urls import path
from .views import signup, user_activate


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('<str:username>/account-activate', user_activate, name='account-activate'),
]
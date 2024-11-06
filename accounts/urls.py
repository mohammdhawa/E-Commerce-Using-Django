from django.urls import path
from .views import signup, user_activate, ProfileView, edit_profile, add_address, edit_address, delete_address


urlpatterns = [
    path('signup', signup, name='signup'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('add_address', add_address, name='add-address' ),
    path('edit_address', edit_address, name='edit-address'),
    path('delete_address/<int:pk>', delete_address, name='delete-address'),
    path('edit_profile', edit_profile, name='edit-profile'),
    path('<str:username>/account-activate', user_activate, name='account-activate'),
]
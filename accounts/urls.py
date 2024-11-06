from django.urls import path
from .views import (signup, user_activate, ProfileView, edit_profile,
                    add_address, edit_address, delete_address, add_contact_number, delete_contact_number)


urlpatterns = [
    path('signup', signup, name='signup'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('add_address', add_address, name='add-address' ),
    path('edit_address', edit_address, name='edit-address'),
    path('delete_address/<int:pk>', delete_address, name='delete-address'),
    path('add_contact_number', add_contact_number, name='add-contact-number'),
    path('delete_contact_number/<int:pk>', delete_contact_number, name='delete-contact-number'),
    path('edit_profile', edit_profile, name='edit-profile'),
    path('<str:username>/account-activate', user_activate, name='account-activate'),
]
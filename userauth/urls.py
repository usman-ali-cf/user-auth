from django.contrib import admin
from django.urls import path, include
from .views import Home
from .views import CreateUser, UserDetails, EditUser, DeleteUser


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create-user/', CreateUser.as_view(), name='create-user'),
    path('detail-user/<int:id>', UserDetails.as_view(), name='detail-user'),
    path('edit-user/<int:id>', EditUser.as_view(), name='edit-user'),
    path('delete-user/<int:id>', DeleteUser.as_view(), name='delete-user')
]

from django.contrib import admin
from django.urls import path, include
from .views import AdminHome, LoginView, LogoutView, UserHome
from .views import SignUpUser, UserDetails, EditUser, DeleteUser, CreateUserView


urlpatterns = [
    path('', UserHome.as_view(), name='user-home'),
    path('admin-home', AdminHome.as_view(), name='admin-home'),
    path('user-home', UserHome.as_view(), name='user-home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpUser.as_view(), name='signup'),
    path('detail-user/<int:id>', UserDetails.as_view(), name='detail-user'),
    path('edit-user/<int:id>', EditUser.as_view(), name='edit-user'),
    path('delete-user/<int:id>', DeleteUser.as_view(), name='delete-user'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
]

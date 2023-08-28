from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


def authenticate_user(username, password):
    try:
        user = CustomUser.objects.get(username=username)
        if user is not None and check_password(password, user.password):
            return authenticate(username=username, password=password)
        return None
    except ObjectDoesNotExist as e:
        print("User not found")
        return None


def check_user(username):
    try:
        user = CustomUser.objects.get(username=username)
        if user is not None:
            return user
        return None
    except ObjectDoesNotExist as e:
        print("User not found")
        return None

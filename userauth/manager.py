from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, password=password, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have superuser true')
        extra_fields['is_staff'] = True
        return self.create_user(email, username, password, **extra_fields)


class CustomUserQueryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def get_admins(self):
        return self.get_queryset().filter(is_superuser=True)

    def get_users(self):
        return self.get_queryset().filter(is_superuser=False)

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .email_sender import send_activation_email
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .manager import CustomUserQueryManager, UserManager

# Create your models here.


class CustomUser(AbstractUser,PermissionsMixin, models.Model):
    """
    a user custom model
    """
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Others')
    ]
    gender = models.CharField(
        choices=GENDER_CHOICES,
        null=True,
    )
    birth_date = models.DateField(null=True, blank=True)
    id_inc = models.IntegerField(null=True)

    objects = UserManager()
    users = CustomUserQueryManager()

    def __str__(self):
        if self.first_name == '' or self.last_name == '':
            return 'none' + " " + 'none' + " - " + self.username
        return self.first_name + " " + self.last_name + " - " + self.username

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)

        # send email to the user for setting the appointment
        print("send_activation_email(first_name=self.first_name,last_name=self.last_name,username=self.username,"
              "date_joined=self.date_joined,email=self.email)")


def get_incremented_number():
    count = CustomUser.objects.count()
    if count is None:
        return 1
    return int(count)+1


@receiver(pre_save, sender=CustomUser)
def increment_field_before_save(sender, instance, **kwargs):
    # Increment the field value here
    instance.id_inc = get_incremented_number()


pre_save.connect(increment_field_before_save, sender=CustomUser)

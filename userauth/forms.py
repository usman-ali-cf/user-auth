from django.forms import ModelForm
from django import forms
from .models import CustomUser


class UserForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password',  'gender', 'birth_date']
        birth_date = widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}
            )
        }


class EditUserForm(ModelForm):

    def __int__(self, data):
        pass

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']




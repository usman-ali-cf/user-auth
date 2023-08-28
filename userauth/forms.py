from django.forms import ModelForm
from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSignUpForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
        label='Birth Date'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender', 'birth_date']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'gender': 'Gender',
        }
        widgets = {
            'gender': forms.RadioSelect,
        }



class UserLoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Use password input widget

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
            'password': 'Password'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        #username = cleaned_data.get('username')
        #password = cleaned_data.get('password')

        return cleaned_data


class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender', 'birth_date', 'is_superuser']
        birth_date = widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}
            )
        }


class EditUserForm(ModelForm):

    def __int__(self, data):
        pass

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

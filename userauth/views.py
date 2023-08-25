from django.core.mail import send_mail
from django.shortcuts import render, loader, reverse, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm, EditUserForm
from .models import CustomUser
from django.views import View
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .email_sender import send_activation_email
from django.conf import settings
# Create your views here.


class Home(View):

    def get(self, request):
        all_users = CustomUser.objects.all()
        send_mail("User Registration", "Hello", 'osmanali6263@gmail.com', ['CodingOsm@gmail.com'], fail_silently=False)
        template = loader.get_template("home.html")
        context = {
            'users': all_users
        }
        return HttpResponse(template.render(context, request))


class UserDetails(View):

    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        except ObjectDoesNotExist as e:
            user = None
        template = loader.get_template("user_details.html")
        context = {
            'user': user
        }
        return HttpResponse(template.render(context, request))


class CreateUser(View):

    def get(self, request):
        form = UserForm()
        template = loader.get_template("create_form.html")
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                gender = form.cleaned_data['gender']
                birth_date = form.cleaned_data['birth_date']
                user = CustomUser(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email,
                    gender=gender,
                    birth_date=birth_date
                )
                user.save()
                return redirect('home')
            except ValueError as e:
                print(e)
                return redirect('home')


class EditUser(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        initial_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "id": user.id,
        }
        form = EditUserForm(initial=initial_data)
        template = loader.get_template('user_edit.html')
        context = {
            'form': form
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, id):
        form = EditUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.get(id=id)
            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            user.email = email
            user.save(update_fields=['first_name', 'last_name', 'email', 'password'])
            return redirect('home')
        else:
            return redirect("home")


class DeleteUser(View):

    def get(self, request, id):
        del_user = get_object_or_404(CustomUser, pk=id).delete()
        return redirect('home')

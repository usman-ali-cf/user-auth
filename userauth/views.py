from django.core.mail import send_mail
from django.shortcuts import render, loader, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserSignUpForm, EditUserForm, UserLoginForm, UserCreateForm
from .models import CustomUser
from django.views import View
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth import login, logout
from .email_sender import send_activation_email
from django.contrib.auth import get_user_model
from .authenticate import authenticate_user, check_user
from .mixins import CustomLoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
User = get_user_model()

# Create your views here.


class AdminHome(CustomLoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        users = CustomUser.objects.all()
        template = loader.get_template("home.html")
        context = {
            'users': users
        }
        return HttpResponse(template.render(context, request))
        # send_mail("User Registration", "Hello", 'osmanali6263@gmail.com', ['CodingOsm@gmail.com'], fail_silently=False)


class UserHome(CustomLoginRequiredMixin, View):
    def get(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        template = loader.get_template("user_home.html")
        context = {
            'user': user
        }
        return HttpResponse(template.render(context, request))


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')

    def get(self, request):
        logout(request)
        return redirect('login')


class LoginView(View):

    def get(self, request):
        template = loader.get_template("login_page.html")
        form = UserLoginForm()
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        form = UserLoginForm(request.POST)
        # if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate_user(username, password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('admin-home')
            return redirect('user-home')
        context = {
            'message': 'Invalid username or password.',
        }
        template = loader.get_template("login_page.html")
        form = UserLoginForm()
        context['form'] = form
        return HttpResponse(template.render(context, request))


class CreateUserView(CustomLoginRequiredMixin, View):

    def get(self, request):
        template = loader.get_template("create_user.html")
        form = UserCreateForm()
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        form = UserCreateForm(request.POST)
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            gender = request.POST['gender']
            birth_date = request.POST['birth_date']
            is_superuser = request.POST.get('is_superuser', False)
            if check_user(username) is not None:
                messages.error(request, 'Error! User Already Exist!')
                return redirect('create-user')
            if is_superuser == 'on':
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    birth_date=birth_date,
                    is_superuser=True
                )
                user.is_staff = True
                user.is_active = True
                user.set_password(password)
                user.save()
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    birth_date=birth_date,
                    is_superuser=False
                )
                user.set_password(password)
                user.save()
            return redirect('admin-home')
        except (ValueError, IntegrityError) as e:
            print(e)
            messages.error(request, "Integrity Error")
            return redirect('create-user')


class UserDetails(CustomLoginRequiredMixin, View):

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


class SignUpUser(View):

    def get(self, request):
        form = UserSignUpForm()
        template = loader.get_template("signup_form.html")
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        form = UserSignUpForm(request.POST)
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            gender = request.POST['gender']
            birth_date = request.POST['birth_date']
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email,
                gender=gender,
                birth_date=birth_date
            )
            if check_user(username) is None:
                user.set_password(password)
                user.save()
                return redirect('login')
            else:
                messages.error(request, 'Error! User Already Exist!')
                return redirect('signup')
        except (ValueError, IntegrityError) as e:
            print(e)
            return redirect('signup')


class EditUser(CustomLoginRequiredMixin, View):
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
            user.set_password(password)
            user.email = email
            user.save(update_fields=['first_name', 'last_name', 'email', 'password'])
            if request.user.is_superuser:
                return redirect('admin-home')
            return redirect('user-home')
        else:
            if request.user.is_superuser:
                return redirect('admin-home')
            return redirect('user-home')


class DeleteUser(CustomLoginRequiredMixin, View):

    def get(self, request, id):
        del_user = get_object_or_404(CustomUser, pk=id).delete()
        if request.user.is_superuser:
            return redirect('admin-home')
        return redirect('user-home')

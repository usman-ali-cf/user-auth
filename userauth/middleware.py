from django.shortcuts import loader, redirect
from django.http import HttpResponse
from .forms import UserLoginForm
from django.urls import reverse


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = [reverse('signup')]
        # Your custom authentication
        if self.is_authenticated(request) is None and request.path not in allowed_urls:
            template = loader.get_template('login_page.html')
            form = UserLoginForm()
            context = {
                'form': form
            }
            return HttpResponse(template.render(context, request))

        response = self.get_response(request)
        return response

    def is_authenticated(self, request):
        return request.user.is_authenticated

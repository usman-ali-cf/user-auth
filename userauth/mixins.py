from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'
    # Raise a 403 Forbidden error for unauthorized users
    raise_exception = False

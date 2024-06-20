from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.utils.http import url_has_allowed_host_and_scheme

class UserSignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'ksauth/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'ksauth/login.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Change 'home' to the name of your desired URL pattern
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        # Login the user
        login(self.request, form.get_user())

        if remember_me:
            # Set session expiry to 2 weeks
            self.request.session.set_expiry(1209600)  # 2 weeks in seconds
        else:
            # Use default session expiry (browser close)
            self.request.session.set_expiry(0)

        return redirect(self.get_success_url())

    def get_success_url(self):
        # Get the next URL
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import UserRegistrationForm, UserLoginForm

class UserSignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'account/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
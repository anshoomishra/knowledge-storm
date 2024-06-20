from django.urls import path
from .views import UserSignUpView, UserLoginView, UserLogoutView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', UserLoginView.as_view(), name='home'),  # Home page placeholder
]
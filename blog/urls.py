from blog.views import test
from django.urls import path

urlpatterns = [
    path('',test,name="home"),
]
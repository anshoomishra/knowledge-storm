from blog.views import test,HomePage
from django.urls import path

urlpatterns = [
    path('golu/',test,name="home"),
    path('',HomePage.as_view(),name="home-page"),
]
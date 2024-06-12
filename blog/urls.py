from blog.views import test, HomePage, ArticleCreateView, ArticleUpdateView, ArticleDetailView
from django.urls import path

urlpatterns = [
    path('golu/',test,name="home"),
    path('',HomePage.as_view(),name="home-page"),
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<pk>/', ArticleDetailView.as_view(), name='article_detail'),

]
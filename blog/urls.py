from blog.views import test, HomePage, ArticleCreateView, ArticleUpdateView, ArticleDetailView, ArticleListView, \
    ArticlePendingListView, publish_article
from django.urls import path

urlpatterns = [
    path('golu/',test,name="home"),
    path('',HomePage.as_view(),name="home-page"),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/pending/', ArticlePendingListView.as_view(), name='article_pending_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/publish/<int:pk>/', publish_article, name='publish_article'),
]
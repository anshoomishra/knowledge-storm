from blog.views import test, HomePage, ArticleCreateView, ArticleUpdateView, ArticleDetailView, ArticleListView, \
    ArticlePendingListView, publish_article
from ckeditor_uploader import views as ckeditor_views
from django.urls import path

urlpatterns = [
    path('golu/',test,name="home"),
    path('',ArticleListView.as_view(),name="home-page"),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('ckeditor/upload/', ckeditor_views.upload, name='ckeditor_upload'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/pending/', ArticlePendingListView.as_view(), name='article_pending_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/publish/<int:pk>/', publish_article, name='publish_article'),
]
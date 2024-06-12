from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.http import HttpResponse

from blog.forms import ArticleForm
from blog.models import Article
# Create your views here.

def test(request):
    return HttpResponse("Hello Golu Bitti")

class HomePage(TemplateView):
    template_name = "blog/home.html"

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('article_list')  # Replace with your article list view name

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Automatically set the user who created the article
        return super().form_valid(form)

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('article_list')  # Replace with your article list view name

    def form_valid(self, form):
        form.instance.updated_by = self.request.user  # Automatically set the user who updated the article
        return super().form_valid(form)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from django.http import HttpResponse

from blog.forms import ArticleForm
from blog.models import Article
from .permissions import ArticlePermissionMixin


# Create your views here.

def test(request):
    return HttpResponse("Hello Golu Bitti")


class HomePage(TemplateView):
    template_name = "blog/home.html"


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ArticleForm
from .models import Article
from django.views.generic import CreateView, UpdateView


class ArticleCreateView(LoginRequiredMixin, ArticlePermissionMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, ArticlePermissionMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.id
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='published')


class ArticlePendingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Article
    template_name = 'blog/article_pending_list.html'
    context_object_name = 'articles'
    permission_required = 'blog.can_publish_article'

    def get_queryset(self):
        return Article.objects.filter(status='draft')


@login_required
@permission_required('blog.can_publish_article', raise_exception=True)
def publish_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.status = 'published'
    article.published_by = request.user
    article.published_at = timezone.now()
    article.save()
    return redirect('article_list')

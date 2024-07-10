from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from django.http import HttpResponse

from blog.forms import ArticleForm
from blog.models import Article, SavedArticle
from .permissions import CreateViewPermissionMixin,UpdateViewPermissionMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ArticleForm
from .models import Article


# Create your views here.

def test(request):
    return HttpResponse("Hello Golu Bitti")


class HomePage(TemplateView):
    template_name = "blog/home.html"


class ArticleCreateView(LoginRequiredMixin, CreateViewPermissionMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('article_list')
    login_url = '/auth/login/'



    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateViewPermissionMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'



    def get(self, request, *args, **kwargs):
        # Get the article object
        self.object = self.get_object()

        # Increment the views count
        self.object.views += 1

        # Save the updated article
        self.object.save(update_fields=['views'])

        # Call the super class's get method to proceed with normal processing
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['related_articles'] = Article.objects.get_related_articles(article)
        return context



class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10  # Add pagination

    def get_queryset(self):
        queryset = Article.objects.published()

        # Filtering by author
        author = self.request.GET.get('author')
        queryset = queryset.filter_by_author(author)

        # Filtering by keywords
        keywords = self.request.GET.get('keywords')
        queryset = queryset.filter_by_keywords(keywords)

        # Sorting
        sort_order = self.request.GET.get('sort_order', 'latest')
        queryset = queryset.sort_by(sort_order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Article.objects.values_list('created_by__username', flat=True).distinct()
        context['keywords'] = Article.objects.values_list('keywords', flat=True).distinct()
        return context


class ArticlePendingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Article
    template_name = 'blog/article_pending_list.html'
    context_object_name = 'articles'
    permission_required = 'blog.can_publish_article'

    def get_queryset(self):
        return Article.objects.filter(status='draft')
class UserProfileView(LoginRequiredMixin,ListView):
    model = Article
    template_name = 'blog/user_profile.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saved_articles'] = SavedArticle.objects.filter(user=self.request.user)
        context['published_articles'] = Article.objects.filter(published_by=self.request.user)
        context['created_articles'] = Article.objects.filter(created_by=self.request.user)
        context['updated_articles'] = Article.objects.filter(updated_by=self.request.user)
        context['profile'] = self.request.user
        return context


@login_required
def save_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    user = request.user

    if SavedArticle.objects.filter(user=user, article=article).exists():
        messages.error(request, "You have already saved this article.")
    else:
        SavedArticle.objects.create(user=user, article=article)
        messages.success(request, "Article saved successfully.")

    return redirect('article_detail', pk=article.pk)


@login_required
@permission_required('blog.can_publish_article', raise_exception=True)
def publish_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.status = 'published'
    article.published_by = request.user
    article.published_at = timezone.now()
    article.save()
    return redirect('article_list')

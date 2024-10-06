import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from django.http import HttpResponse

from blog.forms import ArticleForm, CommentForm
from blog.models import Article, SavedArticle, ArticleProgress
from .permissions import CreateViewPermissionMixin,UpdateViewPermissionMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ArticleForm
from .models import Article
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache

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
        self.object = self.get_object()
        self.object.views += 1
        self.object.save(update_fields=['views'])
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.user = request.user
            comment.save()
            return redirect('article_detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['related_articles'] = Article.objects.get_related_articles(article)
        context['comments'] = article.articles_comment.filter(parent__isnull=True)
        context['form'] = CommentForm()
        return context

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10  # Add pagination

    def get_queryset(self):
        # Try to get the cached queryset
        cached_articles = cache.get('cached_articles')

        if cached_articles:
            return cached_articles

        # If not cached, query the database
        queryset = Article.objects.published()

        # Filtering by author
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter_by_author(author)

        # Filtering by keywords
        keywords = self.request.GET.get('keywords')
        if keywords:
            queryset = queryset.filter_by_keywords(keywords)

        # Sorting
        sort_order = self.request.GET.get('sort_order', 'latest')
        queryset = queryset.sort_by(sort_order)

        # Cache the queryset for future use (set a timeout of 5 minutes)
        cache.set('cached_articles', queryset, timeout=300)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Article.objects.values_list('created_by__username', flat=True).distinct()
        context['keywords'] = Article.objects.values_list('keywords', flat=True).distinct()
        if self.request.user.is_authenticated:
            progress_data = ArticleProgress.objects.filter(user=self.request.user)
            progress_dict = {p.article_id: p.progress * 100 for p in progress_data}  # Convert to percentage
            context['progress'] = progress_dict
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



@csrf_exempt
def update_progress(request, article_id):
    if request.method == 'POST':
        progress_data = json.loads(request.body)
        progress_value = progress_data.get('progress', 0)
        article = get_object_or_404(Article, id=article_id)

        article_progress, created = ArticleProgress.objects.get_or_create(
            user=request.user,
            article=article
        )
        article_progress.progress = progress_value
        article_progress.save()

        return JsonResponse({'status': 'success'})


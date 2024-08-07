from django.db import models
from ksauth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
import uuid
from django.db.models import Q

class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')

    def filter_by_author(self, author):
        if author:
            return self.filter(created_by__username=author)
        return self

    def filter_by_keywords(self, keywords):
        if keywords:
            return self.filter(Q(title__icontains=keywords) | Q(content__icontains=keywords))
        return self

    def filter_by_tags(self, tag_list):
        if tag_list:
            return self.filter(tags__text__in=tag_list).distinct()
        return self

    def sort_by(self, sort_order):
        if sort_order == 'oldest':
            return self.order_by('created_at')
        return self.order_by('-created_at')

    def get_related_articles(self,article):
        return self.filter(keywords__in=article.keywords.all()).exclude(id=article.id).distinct()[:5]


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def filter_by_author(self, author):
        return self.get_queryset().filter_by_author(author)

    def filter_by_keywords(self, keywords):
        return self.get_queryset().filter_by_keywords(keywords)

    def sort_by(self, sort_order):
        return self.get_queryset().sort_by(sort_order)

    def filter_by_tags(self, tag_list):
        return self.get_queryset().filter_by_tags(tag_list)

    def get_related_articles(self,article):
        return self.get_queryset().get_related_articles(article)

class Tags(models.Model):
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextField()
    created_by = models.ForeignKey(User, related_name='articles_created', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, related_name='articles_updated', on_delete=models.SET_NULL, null=True)
    published_by = models.ForeignKey(User, related_name='articles_published', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.IntegerField(default=0)
    keywords = models.ManyToManyField(Tags,null=True,blank=True)
    objects = ArticleManager()


    def __str__(self):
        return self.title

    def publish(self):
        self.published_at = timezone.now()

    class Meta:
        permissions = [
            ('can_create_article', 'Can create article'),
            ('can_update_article', 'Can update article'),
        ]


class Comment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,related_name="user_comments",null=True,blank=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)
    parent = models.ForeignKey("self",null=True,blank=True,related_name="comments_comment",on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, null=True, blank=True, related_name="articles_comment",
                                on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}"


class SavedArticle(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE,null=True,blank=True)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
    def __str__(self):
        return f"Saved article - {self.user} - {self.article}"





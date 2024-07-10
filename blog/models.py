from django.db import models
from ksauth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
import uuid
from django.db.models import Q
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
class Comment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,related_name="user_comments",null=True,blank=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)
    comment = models.ForeignKey("self",null=True,blank=True,related_name="comments_comment",on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id}"


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
    comment = models.ForeignKey(Comment,null=True,blank=True,related_name="articles_comment",on_delete=models.CASCADE)
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

    # def preprocess_text(self):
    #     # Combine title, description, and content for a comprehensive representation
    #     text = f"{self.title} {self.description} {self.content}"
    #     return text
    #
    # def get_article_embedding(self):
    #     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    #     model = BertModel.from_pretrained('bert-base-uncased')
    #
    #     text = self.preprocess_text()
    #     inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    #
    #     with torch.no_grad():
    #         outputs = model(**inputs)
    #
    #     embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
    #     return embeddings
    #
    # @staticmethod
    # def get_related_articles(article, top_k=5):
    #     all_articles = Article.objects.exclude(id=article.id)
    #     article_embedding = article.get_article_embedding()
    #
    #     similarities = []
    #     for other_article in all_articles:
    #         other_embedding = other_article.get_article_embedding()
    #         similarity = cosine_similarity(article_embedding, other_embedding)[0][0]
    #         similarities.append((other_article, similarity))
    #
    #     similarities.sort(key=lambda x: x[1], reverse=True)
    #     return [article for article, _ in similarities[:top_k]]

class SavedArticle(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE,null=True,blank=True)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
    def __str__(self):
        return f"Saved article - {self.user} - {self.article}"





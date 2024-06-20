from django.db import models
from ksauth.models import User
from django.utils import timezone
import uuid
from ckeditor.fields import RichTextField
# Create your models here.


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


    def __str__(self):
        return self.title

    def publish(self):
        self.published_at = timezone.now()

    class Meta:
        permissions = [
            ('can_create_article', 'Can create article'),
            ('can_update_article', 'Can update article'),
        ]
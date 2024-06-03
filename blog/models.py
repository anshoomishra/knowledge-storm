from django.db import models
from account.models import User
from django.utils import timezone
import uuid
# Create your models here.


class Article(models.Model):
    id = models.UUIDField(uuid.uuid4(),primary_key=True,editable=False)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True)
    content = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="article_creator")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="article_updator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField()
    publisher = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name="publisher")

    def __str__(self):
        return self.id

    def publish(self):
        self.published_at = timezone.now()
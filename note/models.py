from django.db import models
from ksauth.models import User
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,related_name='notes',on_delete=models.CASCADE)

    def __str__(self):
        return self.title

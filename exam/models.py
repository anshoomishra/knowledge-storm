from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from ksauth.models import User
import uuid
# Create your models here.

class TestType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    is_free_test = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="test_owner")
    updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="test_updator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_marks = models.IntegerField()
    published = models.BooleanField(default=False)
    test_type = models.ForeignKey(TestType,on_delete=models.SET_NULL,null=True,blank=True,related_name="test_type")

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = RichTextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions_updated')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions',null=True,blank=True)
    max_marks = models.PositiveIntegerField(default=1000)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negative_marks = models.IntegerField(default=-1)
    is_negative_marking_applicable = models.BooleanField(default=False)
    is_objective = models.BooleanField(default=True)

    def __str__(self):
        return self.text

# Answer model
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers',null=True,blank=True)
    text = models.CharField(max_length=1000,null=True,blank=True)
    is_correct = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.text

class TestSeries(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='test_series_created')
    no_of_tests = models.PositiveIntegerField()
    no_of_free_tests = models.PositiveIntegerField()
    language_mode = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    test_series = models.ForeignKey(TestSeries, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=self.test_series.duration_of_subscription)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.test_series.title} - Expires on {self.expires_at}"

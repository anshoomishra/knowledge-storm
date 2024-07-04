from datetime import timedelta

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


class TestSeries(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='test_series_created')
    no_of_tests = models.PositiveIntegerField()
    no_of_free_tests = models.PositiveIntegerField()
    language_mode = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="test_owner")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="test_updator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_marks = models.IntegerField()
    published = models.BooleanField(default=False)
    test_type = models.ForeignKey(TestType, on_delete=models.SET_NULL, null=True, blank=True, related_name="test_type")
    test_series = models.ForeignKey(TestSeries, on_delete=models.CASCADE, related_name="tests",null=True,blank=True)

    def __str__(self):
        return self.name


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


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = RichTextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions_updated')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    max_marks = models.PositiveIntegerField(default=1000)
    negative_marks = models.IntegerField(default=-1)
    is_negative_marking_applicable = models.BooleanField(default=False)
    is_objective = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
    text = models.CharField(max_length=1000, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.text


class TestAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    paused_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta())
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_attempts')
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    remained_time = models.DurationField(default=timedelta())

    @property
    def remaining_time(self):
        total_time = self.test.duration.total_seconds()
        time_spent = self.time_spent.total_seconds()
        if self.paused_at:
            time_spent += (timezone.now() - self.paused_at).total_seconds()
        return max(0, total_time - time_spent)

    def save(self, *args, **kwargs):
        # Ensure there is only one active attempt per user and test
        if self.is_active:
            TestAttempt.objects.filter(user=self.user, test=self.test, is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def pause(self):
        if self.is_active and not self.is_completed:
            self.paused_at = timezone.now()
            self.save()

    def resume(self):
        if self.paused_at:
            pause_duration = timezone.now() - self.paused_at
            self.time_spent += pause_duration
            self.paused_at = None
            self.save()

    def complete(self):
        if not self.is_completed:
            self.end_time = timezone.now()
            self.is_completed = True
            self.is_active = False
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"

class QuestionAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='question_attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_attempts')
    time_spent = models.DurationField(default=timezone.timedelta)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.SET_NULL)
    answered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.test_attempt.user.username} - {self.question.text[:20]}"